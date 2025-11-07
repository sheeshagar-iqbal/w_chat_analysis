from wordcloud import WordCloud
from nltk.corpus import stopwords 
from collections import Counter
import pandas as pd
from urlextract import URLExtract
import emoji
urlextracter =URLExtract()


def fatch_stats(selected_user,df):

    if selected_user !='Overall':
        df =df[df['user']==selected_user]
# num message
    num_massage =df.shape[0]

# num word
    counter=[]
    for message in df['message']:
        counter.extend(message.split())

# medai msg,shared
    medai_message=df[df['message']=='<Media omitted>\n'].shape[0]
# link
    link= []
    for message in df['message']:
        link.extend(urlextracter.find_urls(message))

    return num_massage,len(counter),medai_message,len(link)   


# show bar for most busy user and persent
def most_busy_user(df):
    x= df['user'].value_counts().head()
    persent =round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user':'name','count':'percent'})
    return x,persent

# word cloud


def create_wordcloud(selected_user,df):

    if selected_user !='Overall':
        df =df[df['user']==selected_user]

    f= open(r"C:\Users\sheeshragar\Downloads\stop_hinglish.txt",'r')
    stop_word= f.read()    
    temp=df[df['message']!='<Media omitted>\n']
    temp= temp[temp['user']!= 'system']
    
    def remove_stop_words(message):
        ms =[]
        for i in message.lower().split():
            
                if i not in stop_word or i not in stopwords.words('english'):
                    ms.append(i)
        return " ".join(ms)


    df= df[df['message']!='<Media omitted>\n']
    wc = WordCloud(height=500,width=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=' ')) 
    return df_wc  


# most common word
def most_common_words(selected_user,df):

    if selected_user !='Overall':
        df =df[df['user']==selected_user]

    f= open(r"C:\Users\sheeshragar\Downloads\stop_hinglish.txt",'r')
    stop_word= f.read()    
    temp=df[df['message']!='<Media omitted>\n']
    temp= temp[temp['user']!= 'system']
    ms =[]
    for i in temp['message']:
        for j in i.lower().split():
            if j not in stop_word or j not in stopwords.words('english'):
                ms.append(j)

    mcw_df= pd.DataFrame(Counter(ms).most_common(20),columns=['most_common_words','count'])  
    return mcw_df     


# emoji

def emoji_extract(selected_user,df):
    if selected_user !='Overall':
        df =df[df['user']==selected_user]

    ew=[]
    for message in df['message']:
        for word in message:
            if emoji.is_emoji(word):
                ew.append(word)
    
    df_e=pd.DataFrame(Counter(ew).most_common(len(Counter(ew))))
    return df_e
        
#month time line
def month_timeline(selected_user,df):
    if selected_user !='Overall':
        df =df[df['user']==selected_user] 
    timeline=df.groupby(['year','month'])['message'].count().reset_index()
    timeline['time']=timeline['month']+'-'+(timeline['year'].astype(str))

    return timeline    
            
def week_activity_map(selected_user,df):
    if selected_user !='Overall':
        df =df[df['user']==selected_user]  

    return df['day_name'].value_counts()        


def month_activity_map(selected_user,df):
    if selected_user !='Overall':
        df =df[df['user']==selected_user]  

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user !='Overall':
        df =df[df['user']==selected_user] 

    heatmapdata=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return heatmapdata      