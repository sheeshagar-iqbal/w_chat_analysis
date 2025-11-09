import re
import pandas as pd

def preprocess(data):
    # WhatsApp exports (e.g. 12/03/2023, 7:45 - User:)
    # pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    # This pattern covers:
    # 12/03/2023, 7:45 -
    # 12/03/23, 07:45 pm -
    # 12/03/23, 07:45 AM -
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[ap]m)?\s?-\s'
    dates = re.findall(pattern, data)
    messages = re.split(pattern, data)[1:]

    df = pd.DataFrame({'user_message':messages,'message_date':dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')
    df.rename(columns={ 'message_date' : 'date' },inplace=True)


    # users=[]
    # messages=[]
    # for item in df['user_message']:
    #     if ': ' in item:   # only split if ':' is present
    #         user,msg = item.split(': ', 1)
    #         users.append(user)
    #         messages.append(msg)
    #     else:
    #         users.append('system')   # for system messages like encryption info
    #         messages.append(item)
    users=[]
    messages=[]
    for item in df['user_message']:
        # r'^(.*?)[=:]\s*' text number
        # r'^(.*?):\s' only text
        entry= re.split(r'^(.*?)[=:]\s*', item, maxsplit=1)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('system')
            messages.append(entry[0])

    df['user']= users
    df['message']= messages


    df['year']=df['date'].dt.year
    df['month']= df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['hours']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute
    df['day_name']= df['date'].dt.day_name()

    df.drop(columns=['user_message'],inplace=True)

    period=[]
    for hour in df['hours']: 
        if hour==23:
            period.append(str(hour)+"-"+str(00))
        elif hour==0:
            period.append(str(00)+"-"+str(hour+1) )
        else:
            period.append(str(hour)+"-"+str(hour+1))

    df['period']= period        

    return df