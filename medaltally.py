import pandas as pd

def medal_tally(df):

    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region')['Gold', 'Bronze', 'Silver'].sum().sort_values('Gold',
                                                                                              ascending=False).reset_index()

    medal_tally['Gold'] = medal_tally['Gold'].astype(int)
    medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Bronze'] + medal_tally['Silver']

    return medal_tally

def year(df):

    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')
    return year

def country(df):

    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')
    return country


def medal_tally_fetch(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year')['Gold', 'Bronze', 'Silver'].sum().sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region')['Gold', 'Bronze', 'Silver'].sum().sort_values('Gold',
                                                                                    ascending=False).reset_index()
    x['Gold'] = x['Gold'].astype(int)
    x['Bronze'] = x['Bronze'].astype(int)
    x['Silver'] = x['Silver'].astype(int)

    x['Total'] = x['Gold'] + x['Bronze'] + x['Silver']

    return x