from GoogleNews import GoogleNews
from newspaper import Article
import pandas as pd

#get new for a given date range
#googlenews=GoogleNews(start='05/01/2020',end='05/31/2020')

#get new for previous days
googlenews=GoogleNews(period='7d')

#get new for previous hourses
#googlenews=GoogleNews(period='1h')

#get new for previous minutes
#googlenews=GoogleNews(period='30min')

#Search for news about specific topic
googlenews.search('erdogan')

#get Result
result=googlenews.result()

#print results
df=pd.DataFrame(result)
print(df.all)
print(type(result))