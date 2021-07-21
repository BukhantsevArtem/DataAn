import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing


#Import data
fandango = pd.read_csv("fandango_scrape.csv")
all_sites = pd.read_csv('all_sites_scores.csv')


plt.figure(figsize=(10,4), dpi = 200)
sns.scatterplot(data = fandango, x = 'RATING', y = 'VOTES')
fandango.corr()

# def year(film):
#     nfilm = film.split('(')[1][0:4]
#     return nfilm

# fandango['Year'] = np.vectorize(year)(fandango['FILM'])

fandango['YEAR'] = fandango['FILM'].apply(lambda title:title.split('(')[-1][0:4])
fandango['YEAR'].value_counts()

# sns.displot(data = fandango, x = 'YEAR', palette = 'plasma')
plt.figure(dpi = 200)
sns.countplot(data = fandango, x = 'YEAR')

fandango.sort_values('VOTES', ascending = False)[:10]
fandango[fandango['VOTES']==0].count()


fan_reviewed = fandango[fandango['VOTES']>0]
sns.kdeplot(data = fan_reviewed, x = 'RATING', clip = (0,5), shade = True, label='RATING')
sns.kdeplot(data = fan_reviewed, x = 'STARS', clip = (0,5), shade = True, label='STARS')
plt.legend(bbox_to_anchor=(1.3,0.5))

fan_reviewed['STARS_DIFF'] = np.round(fan_reviewed['STARS'] - fan_reviewed['RATING'],2)
plt.figure(figsize=(10,5))
sns.countplot(data = fan_reviewed, x = 'STARS_DIFF', palette = 'plasma')

fan_reviewed.nlargest(columns = 'STARS_DIFF',n = 1)

all_sites.describe()
all_sites.info()
all_sites.columns

plt.figure(dpi = 200)
sns.scatterplot(data = all_sites, x = 'RottenTomatoes', y = 'RottenTomatoes_User')

all_sites['DIFF_ROTT'] = all_sites['RottenTomatoes'] - all_sites['RottenTomatoes_User']

np.mean(np.absolute(all_sites['DIFF_ROTT']))

#Hist for RT 
plt.figure(figsize=(10,5), dpi = 200)
sns.histplot(data = all_sites, x = 'DIFF_ROTT', bins = 20, kde = True)
plt.title('RT critics score minus RT User score')

#Hist for RT 
plt.figure(figsize=(10,5), dpi = 200)
sns.histplot(x = np.absolute(all_sites['DIFF_ROTT']), bins = 20, kde = True)
plt.title('ABS difference between critics score and RT User score')

#The biggest difference between users and critics
all_sites.nsmallest(5, 'DIFF_ROTT')[['FILM', 'DIFF_ROTT']]
all_sites.nlargest(5, 'DIFF_ROTT')[['FILM', 'DIFF_ROTT']]

#Scatterplot for metac
plt.figure(figsize=(10,5), dpi = 200)
sns.scatterplot(data = all_sites, x = 'Metacritic', y='Metacritic_User')

#Scatter plot imdb vs metac
plt.figure(figsize=(10,5), dpi = 200)
sns.scatterplot(data = all_sites, x = 'Metacritic_user_vote_count', y = 'IMDB_user_vote_count')

all_sites.nlargest(1,'IMDB_user_vote_count')
all_sites.nlargest(1,'Metacritic_user_vote_count')

#Join data
all_data = pd.merge(fandango, all_sites, how = 'inner', on='FILM')
all_data.info()

#Norm scores
all_data['RT_Norm'] = np.round(all_data['RottenTomatoes']/20,1)
all_data['RTU_Norm'] =  np.round(all_data['RottenTomatoes_User']/20,1)
all_data['Meta_Norm'] =  np.round(all_data['Metacritic']/20,1)
all_data['Meta_U_Norm'] =  np.round(all_data['Metacritic_User']/2,1)
all_data['IMDB_Norm'] = np.round(all_data['IMDB']/2,1)

norm_scores = all_data[['STARS','RATING','RT_Norm','RTU_Norm','Meta_Norm','Meta_U_Norm','IMDB_Norm']]

#KDE plot ratings

def move_legend(ax, new_loc, **kws):
    old_legend = ax.legend_
    handles = old_legend.legendHandles
    labels = [t.get_text() for t in old_legend.get_texts()]
    title = old_legend.get_title().get_text()
    ax.legend(handles, labels, loc=new_loc, title=title, **kws)
    
    
fig, ax = plt.subplots(figsize=(15,6),dpi=150)
sns.kdeplot(data=norm_scores,clip=[0,5],shade=True,palette='Set1',ax=ax)
move_legend(ax, "upper left")

fig, ax = plt.subplots(figsize=(15,6),dpi=150)
sns.kdeplot(data=norm_scores[['RT_Norm', 'STARS']],clip=[0,5],shade=True,palette='Set1',ax=ax)
move_legend(ax, "upper left")

fig, ax = plt.subplots(figsize=(15,6),dpi=150)
sns.histplot(data = norm_scores, palette='Set1',ax=ax, bins = 50)
move_legend(ax, "upper left")

sns.clustermap(data = norm_scores, lw = 0.5, annot = True, cmap="plasma", col_cluster=False)

fig, ax = plt.subplots(figsize=(15,6),dpi=150)
sns.kdeplot(data=all_data.nsmallest(10, 'RT_Norm')[['STARS','RATING','RT_Norm','RTU_Norm','Meta_Norm','Meta_U_Norm','IMDB_Norm']],clip=[0,5],shade=True,palette='Set1',ax=ax)
plt.title("Ratings for RT Critic's 10 Worst Reviewed Films");

all_data[['STARS','RATING','RT_Norm','RTU_Norm','Meta_Norm','Meta_U_Norm','IMDB_Norm']].iloc[21]