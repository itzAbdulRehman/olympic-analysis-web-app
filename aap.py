import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import helper
import preprocessor
import medaltally
import medaltally
import plotly.express as px
import plotly.figure_factory as ff




# @st.experimental_memo
# def get_img_as_base64(file):
#     with open(file, "rb") as f:
#         data = f.read()
#     return base64.b64encode(data).decode()
#
#
# urllib.request.urlretrieve("https://unsplash.com/s/photos/human", "image.jpg")
# img = get_img_as_base64("image.jpg")
#
# page_bg_img = f"""
# <style>
# [data-testid="stAppViewContainer"]{{
# background-image: url("https://images.unsplash.com/photo-1542446633-362158ea0052?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1033&q=80");
# background-size: cover;
# }}
#
# [data-testid="stSidebar"] > div:first-child {{
# background-image: url("data:image/png;base64,{img}");
# background-position: center;
# }}
#
# [data-testid="stHeader"] {{
# background: rgba(0,0,0,0);
# }}
#
# </style>
# """
#
# st.markdown(page_bg_img, unsafe_allow_html=True)

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

st.sidebar.header('Olympics Analysis')
st.sidebar.image(
    'https://c4.wallpaperflare.com/wallpaper/631/310/523/2014-winter-paralympics-sochi-2014-olympics-wallpaper-preview.jpg')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Over-all Analysis', 'Country-wise Analysis', 'Athelete-wise Analysis')
)

df = preprocessor.preprocess(df, region_df)
# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    year = medaltally.year(df)
    country = medaltally.country(df)

    select_year = st.sidebar.selectbox('Select Year', year)
    select_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = medaltally.medal_tally_fetch(df, select_year, select_country)

    if select_year == 'Overall' and select_country == 'Overall':
        st.title('Overall Tally')
    if select_year == 'Overall' and select_country != 'Overall':
        st.title('Overall Performance of ' + select_country)
    if select_year != 'Overall' and select_country == 'Overall':
        st.title('All Countries Performance in ' + str(select_year))
    if select_year != 'Overall' and select_country != 'Overall':
        st.title('Performance of ' + select_country + ' in ' + str(select_year))

    st.table(medal_tally)

if user_menu == 'Over-all Analysis':
    st.title('Top Statistics')

    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Cities')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    nations_over_time = helper.over_time_analysis(df, 'region', 'No of Countries')
    fig = px.line(nations_over_time, x='Editions', y='No of Countries', markers=True)
    st.title('Participating nations over time')
    st.plotly_chart(fig)

    events_over_time = helper.over_time_analysis(df, 'Event', 'No of Events')
    fig = px.line(events_over_time, x='Editions', y='No of Events', markers=True)
    st.title('Events over the years')
    st.plotly_chart(fig)

    athletes_over_time = helper.over_time_analysis(df, 'Name', 'No of Athletes')
    fig = px.line(athletes_over_time, x='Editions', y='No of Athletes', markers=True)
    st.title('Participating Athletes over time')
    st.plotly_chart(fig)

    plt.title('Every Sport Events over time')
    events_for_every_sport = df.drop_duplicates(['Year', 'Sport', 'Event'])
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(
        events_for_every_sport.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(
            0).astype(int), annot=True, cmap="YlGnBu", ax=ax)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    select_sport = df['Sport'].unique().tolist()
    select_sport.sort()
    select_sport.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', select_sport)
    most_successful_athletes = helper.most_successful_athletes(df, selected_sport)
    st.table(most_successful_athletes)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country wise Analysis')

    country = df['region'].dropna().unique().tolist()
    country.sort()
    selected_country = st.sidebar.selectbox('Select Country', country)

    # if selected_country=='Overall':
    #     st.title(str(selected_country) + ' Medal Tally over the years')
    #     all_countries = helper.medal_of_countries(df)
    #     fig = px.line(all_countries, x='region', y='Medals')
    #     st.plotly_chart(fig)
    # if selected_country!='Overall':

    st.title(str(selected_country) + ' Medal Tally over the years')
    all_countries_over_year = helper.medal_of_country_all_year(df, selected_country)
    fig = px.line(all_countries_over_year, x='Year', y='Medals', markers=True)
    st.plotly_chart(fig)

    try:
        st.title(str(selected_country) + ' excels in following sports')
        pt = helper.country_event_heatmap(df, selected_country)
        fig, ax = plt.subplots(figsize=(15, 15))
        sns.heatmap(pt.fillna(0).astype(int), annot=True, cmap="YlGnBu", ax=ax)
        st.pyplot(fig)
    except:
        st.header(str(selected_country) + ' not good in any sport')

    st.title('Top 10 Athletes of ' + str(selected_country))
    top10 = helper.most_successful_athletes_of_countries(df, selected_country)
    st.table(top10)

if user_menu == 'Athelete-wise Analysis':
    athletic_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athletic_df['Age'].dropna()
    x2 = athletic_df[athletic_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athletic_df[athletic_df['Medal'] == 'Bronze']['Age'].dropna()
    x4 = athletic_df[athletic_df['Medal'] == 'Silver']['Age'].dropna()

    st.title('Distribution of Age')

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Madelist', 'Bronze Madelist', 'Silver Madelist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athletic_df[athletic_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    st.title('Weight vs Height')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_vs_height(df, selected_sport)

    fig, ax = plt.subplots()
    sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=100, ax=ax)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"], markers=True)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
