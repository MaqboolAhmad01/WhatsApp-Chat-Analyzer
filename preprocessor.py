import pandas as pd
import re
import emoji
def preprocess(content):
    pattern='\d{1,2}\/\d{1,2}\/\d{2,4}\,\s\d{1,2}\:\d{1,2}\s'
    messages=re.split(pattern,content)[1:]
    dates=re.findall(pattern,content)
    df=pd.DataFrame({'Dates':dates,'msg':messages})
    df['Dates']=pd.to_datetime(df['Dates'],format='%d/%m/%Y, %H:%M ')
    msg=[]
    user=[]
    pattern='\-\s([\w\W]+?)\:\s'
    for message  in df['msg']:
        result=re.split(pattern ,message)
        print(result)
        if(result[1:]):
            user.append(result[1])
            msg.append(result[2])
        else:
            
            user.append('Group notifications')
            msg.append(result[0])
    
    df['Messages']=msg
    df['Users']=user
    df['Users']=df['Users'].str.replace('☺️','Maqbool')
    df=df.drop(columns='msg')
    df['Messages']=df['Messages'].str.replace('-',"",1)
    df['Messages']=df['Messages'].str.replace('\n',"")
    x=[]
    for i in df['Messages']:
        x.extend(emoji.distinct_emoji_list(i))
    a=set(x)
    emojis=list(a)
    dict={}
    index=[]
    column=[]
    for message in df['Messages']:
        k=[]
    
        index.append(message)
        for emj in emojis:
            if emj in message:
                k.append(emj)
        # elif emj not in message:
            # k.append(' ')
        mystr="".join(k)
        column.append(mystr)
    mydict={'Emoji':column}
    dict.update(mydict)
        
                
    
    df1=pd.DataFrame(dict,index=index)
    df1.index=range(df1.shape[0])
    df=pd.concat([df,df1],axis=1)
    df['Emoji']=df['Emoji'].replace('','Not Used')
    df['date_only']=df['Dates'].dt.date
    df['month']=df['Dates'].dt.month
    df['year']=df['Dates'].dt.year
    df['month_name']=df['Dates'].dt.month_name()
    df['day_name']=df['Dates'].dt.day_name()
    df['hours']=df['Dates'].dt.hour
    df['minutes']=df['Dates'].dt.minute
    
    period=[]
    for i in df[['day_name','hours']]['hours']:
        if(i==23):
            period.append(str(i)+'-'+str('00'))
        elif(i==0):
            period.append(str('00')+'-'+str('01'))
        else:
            period.append(str(i)+'-'+str(i+1))
            
    df['period']=period      

    return df