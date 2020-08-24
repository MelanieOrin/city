import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast

#Import relevant columns
colnames=['_id','createdAt','itemSubType','categoryGroup','category','dataSourceCategory','dataSourceOfficial','threadSummary']
df=pd.read_csv("raw.csv", usecols=colnames)[colnames]
#Filter for social media posts and relevant data
df = df[(df['itemSubType']=='post') & (df['categoryGroup']!='irrelevant')]
#Edit datetime column and filter for relevent months
df['createdAt'] = pd.to_datetime(df.createdAt).dt.strftime('%B %Y')
df = df[df['createdAt']!='September 2018']
#Extract data from 'threadSummary' column
df2=df['threadSummary'].apply(lambda x: ast.literal_eval(x)).apply(pd.Series)
df3=pd.concat([df, df2], axis = 1).drop('threadSummary', axis = 1)
#Sum sentiment values
df3['Discourse']=df3['negativeSentiment']+df3['neutralSentiment']+df3['positiveSentiment']

#Question 1
#Calculate monthly discourse
junDisc=df3.loc[df3['createdAt'] == 'June 2018', 'Discourse'].sum()
julDisc=df3.loc[df3['createdAt'] == 'July 2018', 'Discourse'].sum()
augDisc=df3.loc[df3['createdAt'] == 'August 2018', 'Discourse'].sum()
print ('junDisc:', junDisc, 'julDisc:', julDisc, 'augDisc:', augDisc)

#Question 2
#Calculate social media discourse from official and unofficial data
offDataDisc=df3.loc[df3['dataSourceOfficial'] == True, 'Discourse'].sum()
unoffDataDisc=df3.loc[df3['dataSourceOfficial'] == False, 'Discourse'].sum()
print ('offDataDisc:', offDataDisc, 'unoffDataDisc:', unoffDataDisc)
#Investigate by category group
df3[df3['dataSourceOfficial']==True].groupby(['categoryGroup'])['Discourse'].sum().sort_values(ascending=False)
df3[df3['dataSourceOfficial']==False].groupby(['categoryGroup'])['Discourse'].sum().sort_values(ascending=False)
#Investigate by category
df3[df3['dataSourceOfficial']==True].groupby(['category'])['Discourse'].sum().sort_values(ascending=False)
df3[df3['dataSourceOfficial']==False].groupby(['category'])['Discourse'].sum().sort_values(ascending=False)
#Investigate by data sources
df3[df3['dataSourceOfficial']==True].groupby(['dataSourceCategory'])['Discourse'].sum().sort_values(ascending=False)
df3[df3['dataSourceOfficial']==False].groupby(['dataSourceCategory'])['Discourse'].sum().sort_values(ascending=False)

#Question 3
#Group by category Group and sum discourse
df3.groupby(['categoryGroup'])['Discourse'].sum().sort_values(ascending=False).head()
#Group by category and sum discourse
df3.groupby(['category'])['Discourse'].sum().sort_values(ascending=False).head()

#Question 4
#Sum of discouse for each category group each month
junGro=df3[df3['createdAt']=='June 2018'].groupby(['categoryGroup'])['Discourse'].sum()
julGro=df3[df3['createdAt']=='July 2018'].groupby(['categoryGroup'])['Discourse'].sum()
augGro=df3[df3['createdAt']=='August 2018'].groupby(['categoryGroup'])['Discourse'].sum()
#Calculate the discourse difference by month for category groups
jjDiscDiffCg=(julGro-junGro).sort_values(ascending=False).head()
ayDiscDiffCg=(augGro-julGro).sort_values(ascending=False)
aeDiscDiffCg=(augGro-junGro).sort_values(ascending=False)
print('jjDiscDiffCg', jjDiscDiffCg)
#Sum of discouse for each category each month
junCat=df3[df3['createdAt']=='June 2018'].groupby(['category'])['Discourse'].sum().sort_values(ascending=False)
julCat=df3[df3['createdAt']=='July 2018'].groupby(['category'])['Discourse'].sum().sort_values(ascending=False)
augCat=df3[df3['createdAt']=='August 2018'].groupby(['category'])['Discourse'].sum().sort_values(ascending=False)
#Calculate the discourse difference by month for specific topics
jjDiscDiffCat=(julCat-junCat).sort_values(ascending=False).head()
ayDiscDiffCat=(augCat-julCat).sort_values(ascending=False)
aeDiscDiffCat=(augCat-junCat).sort_values(ascending=False)
print('jjDiscDiffCat', jjDiscDiffCat)

#Question 5
#Investigate overall negative sentiment for categories/topics
df3.groupby(['categoryGroup'])['negativeSentiment'].sum().sort_values(ascending=False).head()
df3.groupby(['category'])['negativeSentiment'].sum().sort_values(ascending=False).head()
#Calculate % negative sentiment
dfq51=df3.groupby(['categoryGroup'])['Discourse','negativeSentiment'].sum()
dfq51['%negSen'] = dfq51['negativeSentiment']/dfq51['Discourse']
dfq51['%negSen'].sort_values(ascending=False)
dfq52=df3.groupby(['category'])['Discourse','negativeSentiment'].sum()
dfq52['%negSen'] = dfq52['negativeSentiment'] / dfq52['Discourse']
dfq52['%negSen'].sort_values(ascending=False).head(10)
#Investigate water-pollution
df3[df3['category']=='water-pollution']

#Question 6
dfq6=df3[(df3['category']=='catering') | (df3['category']=='violence-crime')]
dfq6.groupby(['category'])['negativeSentiment','neutralSentiment','positiveSentiment'].sum().plot(kind='bar', stacked=True)
plt.ylabel('Discourse')
plt.xlabel('Category')
plt.title('Discourse breakdown of catering and violence-crime social media posts during summer 2018')
plt.legend(bbox_to_anchor=(1.05, 1))
plt.show()