import streamlit as st
import pandas as pd
import preprocessor
import helper
st.sidebar.title("WHATSAPP CHAT ANALYSIS")
upload_file=st.sidebar.file_uploader("upload the chat here",type="txt")
if upload_file is not None:
    bytes_data=upload_file.getvalue()
    data=bytes_data.decode("utf-8")#to get the data in the form of string 
    # st.write(data)#just to check that we had get the data as string 
    df=preprocessor.preprocessor(data)
    # st.dataframe(df)# to represent the data 
    #now we will create the dropdown for the user that we want to select so we have to see how many users are there 
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'overall')
    selected_user=st.sidebar.selectbox("SELECT THE USER ",user_list)

    if st.sidebar.button("SHOW ANALYSIS"):
        col1,col2,col3,col4=st.columns(4)
        num_messages,num_words,media_shared,link_shared=helper.help(selected_user,df)
        with col1:
            st.write("TOTAL NUMBER OF MESSGAES ")
            st.write(num_messages)
        with col2:
            st.write("WORDS")
            st.write(num_words)
        with col3:
            st.write("MEDIA SHARED")
            st.write(media_shared)
        with col4:
            st.write("LINKS SHARED")
            st.write(link_shared)
        st.title("most busiest user")
        col1,col2=st.columns(2)
        
        names,values,new_df=helper.help2(df)
        import matplotlib.pyplot as plt
        fig,ax=plt.subplots()

        with col1:
            # new_df=pd.DataFrame(names,values)#it will create a 2d array like structure and treat the numerical column as index
            # new_df=new_df.transpose
            # new_df.columns=['user','values']
            # new_df.rename(columns={'index':'values'},inplace=True)
            st.write("names")
            st.dataframe(new_df)
        with col2:
            st.write("graphical analysis")
            ax.bar(names,values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        st.title("the most important word cloud of your chat ")
        image=helper.create_word_cloud(df,selected_user)
        fig,ax=plt.subplots()
        ax.imshow(image)
        st.pyplot(fig)

        st.title("MOST COMMON 20 WORDS ARE")
        col1,col2=st.columns(2)
        common_words=helper.common_words(df,selected_user)
        with col1:
            st.dataframe(common_words)
        with col2:
            fig,ax=plt.subplots(figsize=(8,8))
            ax.barh(common_words[0],common_words[1])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("ANALYSISOF MESSAGES WRT TIME")
        timeline=helper.time_analysis(df,selected_user)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily analysis
        st.title("daily analysis")
        daily=helper.daily_analysis(df,selected_user)
        fig,ax=plt.subplots()
        ax.plot(daily['date'],daily['messages'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        col1,col2=st.columns(2)
        with col1:
            st.title("MOST BUSY DAY")
            busy_day=helper.weekely_activity(df,selected_user)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)
        with col2:
            st.title("MOST BUSY MONTH")
            busy_month=helper.monthly_activity(df,selected_user)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        #we can also make activity heat map here by making the pivot tabel


