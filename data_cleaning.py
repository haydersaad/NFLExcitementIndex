import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import altair as alt
from PIL import Image as PImage

df=pd.read_csv(r'C:\Users\hyder\Desktop\file2.csv')
teams={'Baltimore Ravens':"BAL",'Chicago Bears':'CHI','Tampa Bay Buccaneers':'TB','Arizona Cardinals':'ARI',
    'Atlanta Falcons':'ATL','Carolina Panthers':'CAR','Dallas Cowboys':'DAL','Detroit Lions':'DET','Green Bay Packers':'GB',
    'Los Angeles Rams':'LA','Minnesota Vikings':'MIN','Buffalo Bills':'BUF','Cincinnati Bengals':'CIN','Cleveland Browns':'CLE',
    'Denver Broncos':'DEN','Houston Texans':'HOU','Indianapolis Colts':'IND','Jacksonville Jaguars':'JAX','Kansas City Chiefs':'KC',
    'Las Vegas Raiders':'LV','Los Angeles Chargers':'LAC','Miami Dolphins':'MIA','New England Patriots':'NE','New Orleans Saints':'NO',
    'New York Giants':'NYG','New York Jets':'NYJ','Philadelphia Eagles':'PHI','Pittsburgh Steelers':'PIT','San Francisco 49ers':'SF',
    'Seattle Seahawks':'SEA','Tennessee Titans':'TEN','Washington Commanders':'WAS'}
teams_reversed=dict([(value, key) for key, value in teams.items()])
week_dict={1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'11',12:'12',13:'13',14:'14',15:'15',16:'16',
    17:'17',18:'18',19:'Wildcard',20:'Conference Semis',21:'Conference Finals',22:'Super Bowl'}

st.sidebar.title("NFL 2021/22 Season Entertainment Index")
menu_option=st.sidebar.selectbox('Main Menu',('By Team','By Matchup',
                'Most Entertaining Games','Least Entertaining Games','Regular Season Games','Playoff Games'))

if menu_option=='By Team':

    team_option = st.sidebar.selectbox(
        'Select Team',
        ('Arizona Cardinals','Atlanta Falcons','Baltimore Ravens','Buffalo Bills','Carolina Panthers','Chicago Bears',
        'Cincinnati Bengals','Cleveland Browns','Dallas Cowboys','Denver Broncos','Detroit Lions','Green Bay Packers',
        'Houston Texans','Indianapolis Colts','Jacksonville Jaguars','Kansas City Chiefs','Las Vegas Raiders','Los Angeles Chargers',
        'Los Angeles Rams','Miami Dolphins','Minnesota Vikings','New England Patriots','New Orleans Saints','New York Giants',
        'New York Jets','Philadelphia Eagles','Pittsburgh Steelers','San Francisco 49ers','Seattle Seahawks','Tampa Bay Buccaneers',
        'Tennessee Titans','Washington Commanders'))
    team=teams[team_option]
    df=df[(df['away_team']==team) | (df['home_team']==team)]

    table_form = st.sidebar.checkbox('Table Form')
    chart_form = st.sidebar.checkbox('Chart Form')
    Sort = st.sidebar.radio(
     "Sort",
     ('By Week', 'By Entertainment Value: Ascending', 'By Entertainment Value: Descending'))

    if table_form:
        if Sort=='By Entertainment Value: Ascending':
            df=df.sort_values(by=['normalised_result'])
        elif Sort=='By Entertainment Value: Descending':
            df=df.sort_values(by=['normalised_result'],ascending=False)
        df = df.reset_index(drop=True)
        df1 = df[['normalised_result','home_team','away_team','Score','week']]
        df1=df1.replace({'home_team':teams_reversed,'away_team':teams_reversed,'week':week_dict})
        df1=df1.rename({'normalised_result':'Entertainment Value','home_team':'Home Team','away_team':'Away Team','week':'Week'},axis=1)
        df1.index = df1.index + 1
        st.dataframe(df1)

    if chart_form:
        if Sort=='By Week':
            sorting=None
        elif Sort=='By Entertainment Value: Ascending':
            sorting='x'
        else:
            sorting='-x'
        c=alt.Chart(df).mark_bar().encode(
            x=alt.X('normalised_result',title='Entertainment Value'),
            y=alt.Y('game',title='Game',sort=sorting),
            color=alt.condition(
                alt.datum.home_team == team,  
                alt.value('orange'),     # which sets the bar orange.
                alt.value('steelblue')  # And if it's not true it sets the bar steelblue.
            ),
            tooltip=['Score','image']
        )
        st.write(team_option, 'home games in orange, away games in blue.')
        text = c.mark_text(
            align='left',
            baseline='middle',
            dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
            text=alt.Text('normalised_result',format=",.2f")
        )
        rule = alt.Chart(df).mark_rule(color='red').encode(
            x='mean(normalised_result)'
        )
        st.altair_chart((c+text+rule),use_container_width=True)

elif menu_option=='By Matchup':
    team_option1 = st.sidebar.selectbox(
        'Select Team 1',
        ('Arizona Cardinals','Atlanta Falcons','Baltimore Ravens','Buffalo Bills','Carolina Panthers','Chicago Bears',
        'Cincinnati Bengals','Cleveland Browns','Dallas Cowboys','Denver Broncos','Detroit Lions','Green Bay Packers',
        'Houston Texans','Indianapolis Colts','Jacksonville Jaguars','Kansas City Chiefs','Las Vegas Raiders','Los Angeles Chargers',
        'Los Angeles Rams','Miami Dolphins','Minnesota Vikings','New England Patriots','New Orleans Saints','New York Giants',
        'New York Jets','Philadelphia Eagles','Pittsburgh Steelers','San Francisco 49ers','Seattle Seahawks','Tampa Bay Buccaneers',
        'Tennessee Titans','Washington Commanders'))
    team_option2 = st.sidebar.selectbox(
        'Select Team 2',
        ('Arizona Cardinals','Atlanta Falcons','Baltimore Ravens','Buffalo Bills','Carolina Panthers','Chicago Bears',
        'Cincinnati Bengals','Cleveland Browns','Dallas Cowboys','Denver Broncos','Detroit Lions','Green Bay Packers',
        'Houston Texans','Indianapolis Colts','Jacksonville Jaguars','Kansas City Chiefs','Las Vegas Raiders','Los Angeles Chargers',
        'Los Angeles Rams','Miami Dolphins','Minnesota Vikings','New England Patriots','New Orleans Saints','New York Giants',
        'New York Jets','Philadelphia Eagles','Pittsburgh Steelers','San Francisco 49ers','Seattle Seahawks','Tampa Bay Buccaneers',
        'Tennessee Titans','Washington Commanders'),key=1)

    team1=teams[team_option1]
    team2=teams[team_option2]
    season_mean=df['normalised_result'].mean()
    mean_df={'normalised_result':season_mean,'home_team':'Season Average','away_team':'Season Average','Score':"0",'week':"0"}
    df=df[(df['away_team']==team1) & (df['home_team']==team2)|(df['away_team']==team2) & (df['home_team']==team1)]
    df = df.reset_index(drop=True)
    
    df1 = df[['normalised_result','home_team','away_team','Score','week']]
    df1=df1.replace({'home_team':teams_reversed,'away_team':teams_reversed,'week':week_dict})
    df1=df1.append(mean_df,ignore_index=True)
    df1=df1.rename({'normalised_result':'Entertainment Value','home_team':'Home Team','away_team':'Away Team','week':'Week'},axis=1)
    df1.index = df1.index + 1
    st.dataframe(df1)

elif menu_option=='Most Entertaining Games':

    df=df.sort_values(by=['normalised_result'],ascending=False)
    games_option = st.sidebar.slider('Select Number of Games', 0, 285, 20,5)
    df=df.head(games_option)
    df = df.reset_index(drop=True)
    df.index = df.index + 1

    table_form = st.sidebar.checkbox('Table Form')
    chart_form = st.sidebar.checkbox('Chart Form')
    st.write('Best ',games_option, 'Games')

    if table_form:
        week_dict={1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'11',12:'12',13:'13',14:'14',15:'15',16:'16',
        17:'17',18:'18',19:'Wildcard',20:'Conference Semis',21:'Conference Finals',22:'Super Bowl'}

        df1 = df[['normalised_result','home_team','away_team','Score','week']]
        df1=df1.replace({'home_team':teams_reversed,'away_team':teams_reversed,'week':week_dict})
        df1=df1.rename({'normalised_result':'Entertainment Value','home_team':'Home Team','away_team':'Away Team','week':'Week'},axis=1)
        st.dataframe(df1)

    if chart_form:
        c=alt.Chart(df).mark_bar().encode(
            x=alt.X('normalised_result',title='Entertainment Value'),
            y=alt.Y('game',title='Game',sort=None),
            tooltip=['Score','image'],
        )
        text = c.mark_text(
            align='left',
            baseline='middle',
            dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
            text=alt.Text('normalised_result',format=",.2f")
        )
        rule = alt.Chart(df).mark_rule(color='red').encode(
            x='mean(normalised_result)'
        )
        st.altair_chart((c+text+rule),use_container_width=True)

elif menu_option=='Least Entertaining Games':

    df=df.sort_values(by=['normalised_result'])
    games_option = st.sidebar.slider('Select Number of Games', 0, 285, 20,5)
    df=df.head(games_option)
    df = df.reset_index(drop=True)
    df.index = df.index + 1

    table_form = st.sidebar.checkbox('Table Form')
    chart_form = st.sidebar.checkbox('Chart Form')
    st.write('Worst ',games_option, 'Games')

    if table_form:
        df1 = df[['normalised_result','home_team','away_team','Score','week']]
        df1=df1.replace({'home_team':teams_reversed,'away_team':teams_reversed,'week':week_dict})
        df1=df1.rename({'normalised_result':'Entertainment Value','home_team':'Home Team','away_team':'Away Team','week':'Week'},axis=1)
        st.dataframe(df1)

    if chart_form:
        c=alt.Chart(df).mark_bar().encode(
            x=alt.X('normalised_result',title='Entertainment Value'),
            y=alt.Y('game',title='Game',sort=None),
            tooltip=['Score','image']
        )
        text = c.mark_text(
            align='left',
            baseline='middle',
            dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
            text=alt.Text('normalised_result',format=",.2f")
        )
        rule = alt.Chart(df).mark_rule(color='red').encode(
            x='mean(normalised_result)'
        )
        st.altair_chart((c+text+rule),use_container_width=True)

elif menu_option=='Regular Season Games':

    week_option=st.sidebar.selectbox('Select Week:',('All','Week 1','Week 2','Week 3','Week 4','Week 5','Week 6','Week 7','Week 8',
    'Week 9','Week 10','Week 11','Week 12','Week 13','Week 14','Week 15','Week 16','Week 17','Week 18'))
    if week_option=='All':
        df=df.loc[df.week<19]
    else:
        df=df.loc[df.week==int(week_option[5:])]
    df = df.sort_index().reset_index(drop=True)

    table_form = st.sidebar.checkbox('Table Form')
    chart_form = st.sidebar.checkbox('Chart Form')
    Sort = st.sidebar.radio(
     "Sort",
     ('None', 'By Entertainment Value: Ascending', 'By Entertainment Value: Descending'))

    if table_form:
        if Sort=='By Entertainment Value: Ascending':
            df=df.sort_values(by=['normalised_result'])
        elif Sort=='By Entertainment Value: Descending':
            df=df.sort_values(by=['normalised_result'],ascending=False)
        df = df.reset_index(drop=True)
        df1 = df[['normalised_result','home_team','away_team','Score','week']]
        df1=df1.replace({'home_team':teams_reversed,'away_team':teams_reversed,'week':week_dict})
        df1=df1.rename({'normalised_result':'Entertainment Value','home_team':'Home Team','away_team':'Away Team','week':'Week'},axis=1)
        df1.index = df1.index + 1
        st.dataframe(df1)
    
    if chart_form:
        if Sort=='None':
            sorting=None
        elif Sort=='By Entertainment Value: Ascending':
            sorting='-x'
        else:
            sorting='x'

        c=alt.Chart(df).mark_bar().encode(
            x=alt.X('normalised_result',title='Entertainment Value'),
            y=alt.Y('game',title='Game',sort=sorting),
            tooltip=['Score','image']
        )
        text = c.mark_text(
            align='left',
            baseline='middle',
            dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
            text=alt.Text('normalised_result',format=",.2f")
        )
        rule = alt.Chart(df).mark_rule(color='red').encode(
            x='mean(normalised_result)'
        )
        st.altair_chart((c+text+rule),use_container_width=True)

elif menu_option=='Playoff Games':

    week_option=st.sidebar.selectbox('Select Round:',('All','Wildcard','Conference Semifinal','Conference Final','Super Bowl'))
    if week_option=='All':
        df=df.loc[df.week>18]
    elif week_option=='Wildcard':
        df=df.loc[df.week==19]
    elif week_option=='Conference Semifinal':
        df=df.loc[df.week==20]
    elif week_option=='Conference Final':
        df=df.loc[df.week==21]
    elif week_option=='Super Bowl':
        df=df.loc[df.week==22]
    df = df.sort_index().reset_index(drop=True)

    table_form = st.sidebar.checkbox('Table Form')
    chart_form = st.sidebar.checkbox('Chart Form')
    Sort = st.sidebar.radio(
     "Sort",
     ('None', 'By Entertainment Value: Ascending', 'By Entertainment Value: Descending'))

    if table_form:
        if Sort=='By Entertainment Value: Ascending':
            df=df.sort_values(by=['normalised_result'])
        elif Sort=='By Entertainment Value: Descending':
            df=df.sort_values(by=['normalised_result'],ascending=False)
        df = df.reset_index(drop=True)
        df1 = df[['normalised_result','home_team','away_team','Score','week']]
        df1=df1.replace({'home_team':teams_reversed,'away_team':teams_reversed,'week':week_dict})
        df1=df1.rename({'normalised_result':'Entertainment Value','home_team':'Home Team','away_team':'Away Team','week':'Round'},axis=1)
        df1.index = df1.index + 1
        st.dataframe(df1)
    
    if chart_form:
        if Sort=='None':
            sorting=None
        elif Sort=='By Entertainment Value: Ascending':
            sorting='-x'
        else:
            sorting='x'
            
        c=alt.Chart(df).mark_bar().encode(
            x=alt.X('normalised_result',title='Entertainment Value'),
            y=alt.Y('game',title='Game',sort=sorting),
            tooltip=['Score','image']
        )
        text = c.mark_text(
            align='left',
            baseline='middle',
            dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
            text=alt.Text('normalised_result',format=",.2f")
        )
        rule = alt.Chart(df).mark_rule(color='red').encode(
            x='mean(normalised_result)'
        )
        st.altair_chart((c+text+rule),use_container_width=True)

