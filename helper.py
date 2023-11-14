import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
def fetchStats(selected_user,df):
    #fetching total messages

    if(selected_user!='All'):
        df=df[df['Users']==selected_user]
    num_of_messages=df.shape[0]
    #fetching words count
    words=[]
    for message in df['Messages']:
        words.extend(message.split())
    #fetching media count
    
    media_df=df[df['Messages']=='<Media omitted>']
    media_count=media_df.shape[0]
    
    #fetching url
    extractor=URLExtract()
    link=[]
    for message in df['Messages']:
        link.extend(extractor.find_urls(message))
    #fetching count of emojis used
    emoji_count=df[df['Emoji']!='Not Used'].shape[0]
    return num_of_messages,len(words),media_count,len(link),emoji_count
def most_busiest_user(df):
    new_df=round(df['Users'].value_counts()/df['Users'].shape[0]*100,2).reset_index()
    new_df.columns=['Name','Percent']
    return new_df
def create_word_cloud(selected_user,df):
    fd=open('stop_hinglish.txt','r')
    content=fd.read()
    if(selected_user!='All'):
        df=df[df['Users']==selected_user]
    temp=df[df['Messages']!='<Media omitted>']
    temp=temp[temp['Messages']!='Group notifications']
    temp=temp[temp['Messages']!='urdu']
    def remove_words(message):
        k=[]
        for word in message.lower().split():
            if word not in content:
                k.append(word)
        return " ".join(k)
    temp['Messages']=temp['Messages'].apply(remove_words)

    wc= WordCloud(width=300,height=300,min_font_size=10,background_color='white')
    df_wc=wc.generate(temp['Messages'].str.cat(sep=' '))
    return df_wc
def monthly_timeline(selected_user,df):
    if(selected_user!='All'):
        df=df[df['Users']==selected_user]
    timeline=df.groupby(['year','month_name'])['Messages'].count().reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i]+"-"+str(timeline['year'][i]))
    timeline['Time']=time
    return timeline
def daily_timeline(selected_user,df):
    if(selected_user!='All'):
        df=df[df['Users']==selected_user]
    
    timeline=df.groupby('date_only')['Messages'].count().reset_index()
    return timeline
def most_busy_by_month(selected_user,df):
    if(selected_user!='All'):
        df=df[df['Users']==selected_user]
    x=df.groupby('month_name')['Messages'].count().index
    y=df.groupby('month_name')['Messages'].count().values
    return x,y
def most_busy_by_day(selected_user,df):
    if(selected_user!='All'):
        df=df[df['Users']==selected_user]
    x=df.groupby('day_name')['Messages'].count().index
    y=df.groupby('day_name')['Messages'].count().values
    return x,y
def daily_activity_map(selected_user,df):
    if(selected_user!='All'):
        df=df[df['Users']==selected_user]
    new_df=df.pivot_table(index='day_name',columns='period',values='Messages',aggfunc='count').fillna(0)
    return new_df
def most_frequent_emojis(selected_user,df):
    if(selected_user!='All'):
        df=df[df['Users']==selected_user]
    new_df=df['Emoji'].value_counts().reset_index().head(6)
    new_df=new_df[new_df['Emoji']!='Not Used']
    return new_df
    
def most_frequent_words(selected_user,df):
    file=open('stop_hinglish.txt','r')
    content=file.read()
    if(selected_user!='All'):
        df=df[df['Users']==selected_user]
    words=[]
    df=df[df['Messages']!='<Media omitted>']
    for message in df['Messages']:
        for word in message.split(' '):
            if(word not in content):
                words.append(word)
    new_df=pd.DataFrame(Counter(words).most_common(20),columns=['words','frequency'])
    
    return new_df

    


   

 
