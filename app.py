import streamlit as st
import preprocess,helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title('Whatsapp chat analyizer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # st.write("Filename:", uploaded_file.name)
    bytes_data=uploaded_file.getvalue()
    data= bytes_data.decode('utf-8')
    # st.text(data)

    df=preprocess.preprocess(data)
    # st.dataframe(df)

    user_list= df['user'].unique().tolist()

    user_list.remove('system')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user =st.sidebar.selectbox('Show analysis wrt',user_list)

    if st.sidebar.button('show analysis'):
        # st.dataframe(df)

        num_message,num_word,media_message,link=helper.fatch_stats(selected_user,df)
        st.title('Top Statistics')
        col1,col2,col3,col4 =st.columns(4)

        with col1:
            st.header('Total message')
            st.title(num_message)
        with col2:       
            st.header('Total word')
            st.title(num_word)   
        with col3:       
            st.header('media shared')
            st.title(media_message)
        with col4:       
            st.header('media link')
            st.title(link)

            # time line
        st.title('Timeline')    
        timeline=helper.month_timeline(selected_user,df) 
        fig,ax= plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color= 'green') 
        plt.xticks(rotation= 'vertical')
        st.pyplot(fig) 


        # most busy day/activity Map
        st.title('Most Active Week/Month')
        col9,col10= st.columns(2)
        
        with col9:
            day= helper.week_activity_map(selected_user,df)
            fig,ax= plt.subplots()
            ax.bar(day.index,day.values)
            plt.xticks(rotation= 'vertical')
            st.pyplot(fig)

        with col10:
            month= helper.month_activity_map(selected_user,df)
            fig,ax= plt.subplots()
            ax.bar(month.index,month.values,color='red')
            plt.xticks(rotation= 'vertical')
            st.pyplot(fig)


            #  which time user activity action 
        st.title('Weekly Activity Map')    
        activity_time= helper.activity_heatmap(selected_user,df)
        fig,ax= plt.subplots()
        ax= sns.heatmap(activity_time)
        plt.xticks(rotation= 'vertical')
        st.pyplot(fig)            


# bar most busy user
        if selected_user=="Overall":
            st.title('most busy users')
            x,user_persent= helper.most_busy_user(df)
            fig,ax =plt.subplots()
#  bar 
            col5,col6= st.columns(2)
            with col5:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation= 'vertical')
                st.pyplot(fig)
# persent
            with col6:
                st.dataframe(user_persent) 
# wordcloud
        df_wc = helper.create_wordcloud(selected_user,df)
        st.title('WordCloud')
        fig,ax =plt.subplots()
        
        ax.imshow(df_wc)
        st.pyplot(fig)        

# most common word
        mcw_df =helper.most_common_words(selected_user,df)
        # st.dataframe(mcw_df)
        st.title('most common words')
        fig,ax= plt.subplots()
        ax.barh(mcw_df['most_common_words'],mcw_df['count'])
        # plt.yticks(rotation= 'vertical')
        st.pyplot(fig)

# emoji

        df_e = helper.emoji_extract(selected_user,df)
        if df_e.shape[0]>0:

            st.title('Emoji Analysis')
            col7,col8 = st.columns(2)
            with col7:
                st.dataframe(df_e)
            with col8:
                fig,ax= plt.subplots()
                # Try to use an emoji-supporting font
                plt.rcParams['font.family'] = 'Segoe UI Emoji'  # or 'Noto Color Emoji', 'Apple Color Emoji
                ax.pie(df_e[1].head(),labels=df_e[0].head(),autopct='%1.1f%%', startangle=90)
                st.pyplot(fig)    