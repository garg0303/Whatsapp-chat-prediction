import pandas as pd
import numpy as np
import re
def preprocessor(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages=re.split(pattern,data)
    messages=messages[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'user_message':messages,'dates':dates})
    df['date'] = pd.to_datetime(df['dates'], format='%d/%m/%y, %H:%M - ')
    df.drop(columns=['dates'],inplace=True)
    users=[]
    messages=[]
    for message in df['user_message']:
        entry=message.split(':',1)
        if len(entry)==2:
            users.append(entry[0])
            messages.append(entry[1])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user']=users
    df['messages']=messages
    df.drop(columns=['user_message'],inplace=True)
    #df['year']=df['date'].dt.year will show date as 2,023 because of our vs code representaion settings so to avoid that we will apply the following code 
    
    df['year'] = df['date'].dt.year.map(lambda x: '{:04d}'.format(x))  # Format year to 4 digits without comma
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['month_num']=df['date'].dt.month
    df['hour']=df['date'].dt.hour   
    df['minute']=df['date'].dt.minute
    df['day_name']=df['date'].dt.day_name()
    df['only_date']=df['date'].dt.date
    return df

    

