from urlextract import URLExtract
import pandas as pd
from wordcloud import WordCloud
import emoji
extraxt=URLExtract()
def help(selected_user,df):
    # if selected_user=='overall':
    #     word=[]
    #     for message in df['messages']:
    #         word.extend(message.split())
    #     return (df.shape[0],len(word))
    # else:
    #     word=[]
    #     new_df=df[df['user']==selected_user]
    #     for message in new_df['messages']:
    #         word.extend(message.split())
    #     return (new_df.shape[0],len(word))
    word=[]
    link=[]
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    num_messages=df.shape[0]
    for message in df['messages']:
        word.extend(message.split())
        link.extend(extraxt.find_urls(message))
    num_word=len(word)
    media_shared=df[df['messages']==" <Media omitted>\n"].shape[0]# /n is not visible in vscode but in jupyter notebopok it is visible
    link_shared=len(link)
    return num_messages,num_word,media_shared,link_shared

def help2(df):
    x=df['user'].value_counts().head()
    return x.index,x.values,x

def create_word_cloud(df,selected_user):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    image=wc.generate(df['messages'].str.cat(sep=" "))
    return image
def common_words(df,selected_user):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    #we will do some changes that is we will remove the media ommiteed, group notification,stop words for getting better most common 20 words
    temp=df[df['messages']!=" <Media omitted>\n"]
    temp=temp[temp['messages']!=" This message was deleted\n"]
    temp=temp[temp['user']!="group_notification"]
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    words=[]
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
            
    # word=[]
    # for message in df['messages']:
    #     word.extend(message.split())
    from collections import Counter 
    new_df=pd.DataFrame(Counter(words).most_common(20))
    return new_df

#emojis is not working now
# def common_emoji(df,selected_user):
#      emojis=[]
#      if selected_user!='overall':
#         df=df[df['user']==selected_user]
#     for message in df['messages']:
#         emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
#     return emojis

def time_analysis(df,selected_user):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    timeline=df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(str(timeline['year'][i]) + '-' + timeline['month'][i])
    timeline['time']=time
    return timeline

def daily_analysis(df,selected_user):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    daily=df.groupby(['date']).count()['messages'].reset_index()
    return daily
def weekely_activity(df,selected_user):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()

def monthly_activity(df,selected_user):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    return df['month'].value_counts()






    
    
