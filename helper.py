import urllib.request

def over_time_analysis(df,col,name):

    over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('index')
    over_time.rename(columns={'index':'Editions', 'Year':name}, inplace=True)
    return over_time


def most_successful_athletes(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    temp_df = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index').reset_index().drop('level_0', axis=1)
    temp_df.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)

    return temp_df


# def medal_of_countries(df):
#
#     overall_countries = df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','Sport','Event','Medal'])
#     overall_countries = overall_countries.groupby('region')['Gold','Bronze','Silver'].sum().sort_values('Gold',ascending=False).reset_index()
#     overall_countries['Medals']=overall_countries['Gold']+overall_countries['Bronze']+overall_countries['Silver']
#     overall_countries = overall_countries[['region','Medals']]
#     overall_countries['Medals'] = overall_countries['Medals'].astype(int)
#     return overall_countries

def medal_of_country_all_year(df,country):

    countries = df.dropna(subset=['Medal'])
    countries.drop_duplicates(['Team','NOC','Year','City','Sport','Event','Medal'],inplace=True)
    countries = countries[countries['region']==country]['Year'].value_counts().reset_index().sort_values('index')
    countries.rename(columns={'index': 'Year', 'Year': 'Medals'}, inplace=True)
    return countries

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(['Team', 'NOC', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    temp_df = temp_df[temp_df['region']==country]
    pt = temp_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count')
    return pt

def most_successful_athletes_of_countries(df, region):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == region]
    temp_df = temp_df['Name'].value_counts().reset_index().head(11).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index').reset_index().drop('level_0', axis=1)
    temp_df.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)

    return temp_df

def weight_vs_height(df,sport):

    athletic_df = df.drop_duplicates(subset=['Name', 'region'])
    athletic_df['Medal'].fillna('NO Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athletic_df[athletic_df['Sport'] == sport]
        return temp_df
    else:
        return athletic_df

def men_vs_women(df):
    athletic_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athletic_df[athletic_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athletic_df[athletic_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final


