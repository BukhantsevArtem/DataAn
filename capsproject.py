import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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

plt.figure(figsize=(10,5), dpi = 200)
sns.histplot(data = all_sites, x = 'DIFF_ROTT', bins = 20, kde = True)
plt.title('RT critics score minus RT User score')

plt.figure(figsize=(10,5), dpi = 200)
sns.histplot(x = np.absolute(all_sites['DIFF_ROTT']), bins = 20, kde = True)
plt.title('ABS difference between critics score and RT User score')

all_sites.nsmallest(5, 'DIFF_ROTT')
