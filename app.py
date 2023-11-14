import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import helper,preprocessor
st.sidebar.title('Whatsapp Chat Analysis')



chat_file=st.sidebar.file_uploader('Choose a File')
if chat_file is not None:
    Bytes_data=chat_file.getvalue()
    data= Bytes_data.decode("utf-8") 
    df=preprocessor.preprocess(data)
    user_list=df['Users'].unique().tolist()
    user_list.remove('Group notifications')
    user_list.sort()
    user_list.insert(0,'All')
    selected_user=st.sidebar.selectbox('Select a user',user_list)
    if st.sidebar.button('Show Analysis'):
        if selected_user!='All':
            st.dataframe(df[df['Users']==selected_user])
        else:
            st.dataframe(df)
        num_of_messages,words_count,media_count,links_count,emoji_count=helper.fetchStats(selected_user,df)

        st.markdown('<h2 style="text-align: center; margin-bottom: 60px;font-weight: bold;">Top Statistics</h2>', unsafe_allow_html=True)


        C1,C2,C3,C4,C5=st.columns(5)
        with C1:
            st.markdown('<h2 style="margin-bottom: 20px;">Total Message</h2>', unsafe_allow_html=True)

            st.header(num_of_messages)
        with C2:
            st.markdown('<h2 style="margin-bottom: 20px;">Total words</h2>', unsafe_allow_html=True)

            st.header(words_count)
        with C3:
            st.markdown('<h2 style="margin-bottom: 20px;">Total Media</h2>', unsafe_allow_html=True)

            st.header(media_count)
        with C4:
            st.markdown('<h2 style="margin-bottom: 20px;">Total Links</h2>', unsafe_allow_html=True)

            st.header(links_count)
        with C5:
            st.markdown('<h2 style="margin-bottom: 20px;">Total Emojis</h2>', unsafe_allow_html=True)

            st.header(emoji_count)
        if(selected_user)=='All':
            col1,col2=st.columns(2)
            new_df=helper.most_busiest_user(df)
            fig,ax=plt.subplots()
            with col1:
                ax.bar(new_df['Name'],new_df['Percent'],color='g',edgecolor='black')

                plt.xticks(rotation='vertical')
                plt.xlabel("User's Name")
                plt.ylabel("Perecentage")
                plt.title('Most busiest Users')

                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        df_wc=helper.create_word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.markdown('<h2 style="text-align: center;font-size: 60px;font-weight: bold;margin-bottom: 20px;">Word Cloud</h2>', unsafe_allow_html=True)
        
        st.pyplot(fig)
        c1,c2=st.columns(2)
        with c1:
            st.title('Monthly Timeline')
            monthly_timeline=helper.monthly_timeline(selected_user,df)
            fig,ax=plt.subplots()
            ax.plot(monthly_timeline['Time'],monthly_timeline['Messages'],color='r')
            plt.xticks(rotation='vertical')
            plt.ylabel('Total Messages')
            plt.xlabel('Months')
            ax.set_xticklabels(monthly_timeline['Time'])
            plt.title('Monthly Timeline')
            st.pyplot(fig)
        with c2:
            st.title('Daily Timeline')
            daily_timeline=helper.daily_timeline(selected_user,df)
            fig,ax=plt.subplots()
            ax.plot(daily_timeline['date_only'],daily_timeline['Messages'],color='r')
            plt.xticks(rotation='vertical')
            plt.ylabel('Total Messages')
            plt.xlabel('Days')
            plt.title('Daily Timeline')
            ax.set_xticklabels(daily_timeline['date_only'])
            st.pyplot(fig)
        cols1,cols2=st.columns(2)
        with cols1:
            x,y=helper.most_busy_by_month(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(x,y,color='orange',edgecolor='yellow')
            plt.xlabel('Months')
            plt.xticks(rotation='vertical')
            plt.ylabel('Messages')
            st.pyplot(fig)
        with cols2:
            x,y=helper.most_busy_by_day(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(x,y,color='yellow',edgecolor='orange')
            plt.xlabel('Days')
            plt.xticks(rotation='vertical')
            plt.ylabel('Messages')
            st.pyplot(fig)
        daily_activity_map=helper.daily_activity_map(selected_user,df)
        fig,ax=plt.subplots()
        st.title('Activity Map')
        sns.heatmap(data=daily_activity_map,ax=ax)
        st.pyplot(fig)
        st.title('Emojis Analysis')
        emojis=helper.most_frequent_emojis(selected_user,df)
        x1,x2,x3=st.columns(3)
        fig,ax=plt.subplots()
        with x1:
            ax.pie(emojis['count'],labels=emojis['Emoji'],autopct="%0.2f") 
            st.pyplot(fig)
        with x3:
            st.dataframe(emojis)
        new_df=helper.most_frequent_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(new_df['words'],width=new_df['frequency'],color='g')
        plt.xlabel('Frequency')
        plt.ylabel('Common Words')
        st.title('Most commmon words')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)