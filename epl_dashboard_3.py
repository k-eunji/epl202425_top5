import pandas as pd

df = pd.read_csv("team_stats_2.csv")
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True).dt.strftime('%d-%m-%Y')

df['TotalGoals'] = df['FTHG']+df['FTAG']
df['TotalShots'] = df['HS'] + df['AS']

df['BothTeamsScored'] = ((df['FTHG'] > 0) & (df['FTAG'] >0)).astype(int)

df['ExcitementScore'] = df['TotalGoals']*2+df['TotalShots']*0.5+df['BothTeamsScored']*3

top5_matches = df.sort_values(by='ExcitementScore', ascending=False).head(5)

top5_matches[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'TotalGoals', 'TotalShots', 'ExcitementScore']].reset_index(drop=True)


import streamlit as st

st.markdown(
    """
    <style>
    table td:nth-child(1), table th:nth-child(1) {
        white-space: nowrap;
    }
    </style>
    """,
    unsafe_allow_html=True
)

columns_to_show = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG',
                   'BothTeamsScored', 'TotalGoals', 'TotalShots', 'ExcitementScore']
st.markdown(top5_matches[columns_to_show].to_html(index=False), unsafe_allow_html=True)

def generate_match_summary(row):
    summary = f"""
    <div style='border:1px solid #ccc; padding:16px; border-radius:12px; margin-bottom:20px; background-color:#f9f9f9;'>
    <h4 style='color:#1f77b4;'>⚽ {row['HomeTeam']} {row['FTHG']} - {row['FTAG']} {row['AwayTeam']}</h4>
   
    <p style='color:#000;'><b style='color:#2ca02c;'>· Date:</b> {row['Date']}</p>
    <p style='color:#000;'><b style='color:#d62728;'>· Total Goals:</b> {row['TotalGoals']}</p>
    <p style='color:#000;'><b style='color:#9467bd;'>· Total Shots:</b>{row['TotalShots']}</p>
    <p style='color:#000;'><b style='color:#ff7f0e;'>· Both Teams Scored:</b> {'Yes' if row['BothTeamsScored'] else 'No'}</p>
    <p style='color:#000;'><b style='color:#8c564b;'>· Excitement Score:</b> {row['ExcitementScore']:.1f}</p>

    <hr style='margin:10px 0;'>

    <p style='color:#000;'><b style='color:#333;'> Summary:</b><br>
    On <b>{row['Date']}</b>, <b>{row['HomeTeam']}</b> and <b>{row['AwayTeam']}</b> played a thrilling match.<br>
    The game featured <b>{row['TotalGoals']} goals</b> and <b>{row['TotalShots']} shots</b>.<br>
    {'Both teams found the net,' if row['BothTeamsScored'] else 'Only one team scored,'}
    resulting in an <b>excitement score</b> of <span style='color:#d62728;'>{row['ExcitementScore']:.1f}</span>.
    </p>
    </div>
    """
    return summary

st.title("Top 5 Most Exciting Matches - EPL 2024/25")
st.subheader("What is the Excitement Score?")

st.markdown("""
The Excitement Score is a numeric measure designed to capture how thrilling a match was.  
It is calculated based on three key factors:

- **Total Goals**: The sum of goals scored by both teams  
- **Total Shots**: The combined number of shots taken by both teams  
- **Both Teams Scored**: Whether both teams scored at least one goal (Yes or No)

The formula is:  
**Excitement Score = (Total Goals × 2) + (Total Shots × 0.5) + (Both Teams Scored × 3)**

This means matches with more goals, more shots, and goals from both teams score higher.  
Using this score, we ranked the top 5 most exciting matches in the EPL 2024/25 season!
""")

st.markdown("""
### Column Explanation
- **FTHG**: Full Time Home Goals
- **FTAG**: Full Time Away Goals
""")

st.write("These rankings are based on total goals, total shots, and whether both teams scored.")

for idx, row in top5_matches.iterrows():
    st.markdown(generate_match_summary(row), unsafe_allow_html=True)

st.caption("Created with using Streamlit ｜ Data: https://www.football-data.co.uk")
