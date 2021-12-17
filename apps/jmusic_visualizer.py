import streamlit as st
import pandas as pd

"""App that will manipulate and display nautiljon's data in various way
"""

jmusic_collection = pd.read_csv("zmusic.csv", sep=",")
data_filtered = st.container()

artist_list = jmusic_collection['artists'].str.split(',').explode()
artist_list = list(dict.fromkeys(artist_list)).sort()

with data_filtered:
    artist_list