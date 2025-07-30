import streamlit as st
import pickle as pickle
import pandas as pd

teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Gujarat Lions',
 'Rising Pune Supergiant',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Delhi Daredevils',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Deccan Chargers'
]

cities = ['Hyderabad', 'Pune', 'Rajkot', 'Indore', 'Mumbai', 'Kolkata',
       'Bangalore', 'Chandigarh', 'Kanpur', 'Jaipur', 'Chennai',
       'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion',
       'East London', 'Johannesburg', 'Kimberley', 'Cuttack', 'Ahmedabad',
       'Nagpur', 'Dharamsala', 'Visakhapatnam', 'Ranchi', 'Delhi',
       'Abu Dhabi', 'Sharjah', 'Bengaluru', 'Mohali']

pipe = pickle.load(open('pipe.pkl', 'rb'))
st.title('IPL WIN Predictor')

col1, col2 = st.columns(2)

with col1:
    teams = sorted(teams)
batting_team = st.selectbox('Select the batting team', teams)

with col2:
    teams = sorted(teams)
bowling_team = st.selectbox('Select the bowling team', teams)

selected_city = st.selectbox('Select the city', sorted(cities))

target = st.number_input('Target')

col3, col4, col5 = st.columns(3)

with col3:
   score = st.number_input('Score')
with col4:
   overs = st.number_input('Overs completed')
with col5:
   wickets =  st.number_input('Wickets out')

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - overs * 6
    wickets = 10 - wickets
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

    input_df = pd.DataFrame({'batting_team': [batting_team],'bowling_team': [bowling_team],'city': [selected_city],'runs_left': [runs_left], 'balls_left': [balls_left], 'wickets': [wickets], 'crr': [crr], 'rrr': [rrr],'total_runs_x': [target]})

    st.table(input_df)

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + ' win probability: ' + str(round(result[0][1] * 100)) + '%')
    st.header(bowling_team + ' win probability: ' + str(round(result[0][0] * 100)) + '%')