import pandas as pd
import numpy as np
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from ipynb.fs.full.CollaborativeFiltering import movie_recommender_run

#Set page configuration
st.set_page_config(layout = "wide", page_title = "Collaborative Filtering Recommendation System App", page_icon = ":Cinema:")
# st.header("")


#Write code to call movie_recommender_run and display recommendations
columns=['User_ID', 'User_Name', 'Movie_ID', 'Ratings', 'Timestamp']
movie_data_df = pd.read_csv("Movie_data.csv", sep=",", names=columns)
unique_users = list(pd.unique(movie_data_df['User_Name']))

user_name = st.selectbox(
    'Select a user',
    (unique_users)
)

#Display movie rating charts here
st.write(f'{user_name} might be interested in the following movies:')
result = movie_recommender_run(user_name)
st.table(result.Movie_title)

# Display details of provided recommendations
movie_id = result['Movie_ID']
movie_name = result['Movie_title']
fig = make_subplots(
    rows=5, cols=2,
    subplot_titles=(movie_name),
    specs=[
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "bar"}, {"type": "bar"}] 
    ])

# x_row and y_col will determine the location of a plot in the plot-grid
x_row=1
y_col=1
for i in range (len(result)):
    temp=(movie_data_df.loc[movie_data_df['Movie_ID'] == movie_id[i]]).groupby('Ratings').User_ID.count().reset_index()
    
    Rating=temp.Ratings.to_numpy()
    User_ID= temp.User_ID.to_numpy()

    x_row= int( i/2 +1)
    y_col= i%2 + 1
    
    fig.add_trace(go.Bar(x=[1,2,3,4,5], y=User_ID), row=x_row, col=y_col)
    fig.update_xaxes(title_text="Ratings", row=x_row, col=y_col)
    fig.update_yaxes(title_text="Users", row=x_row, col=y_col)

fig.update_layout(height=900,width=800, showlegend=False, title= "Ratings of Suggested Movies")

st.plotly_chart(fig, use_container_width=True)