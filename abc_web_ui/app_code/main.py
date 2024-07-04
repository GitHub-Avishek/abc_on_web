import streamlit as st    
from abc_sidebar import show_sidebar
import numpy as np
import pandas as pd

from test_data import *

st.set_page_config(page_title='ABC-on-Web', layout="wide", page_icon='🔤')
show_sidebar()

st.title(":gray[At a glance ...]")
st.divider()

col_matrix = []
for i in range(3):
    col_matrix += st.columns(3, gap="small")


#Tile1: Job
tile = col_matrix[0].container(border = True)
tile.subheader("Jobs", divider = 'gray')

#tile.text(f"Total jobs: 1000\nCurrently running: 200")

total_jobs = 1000
runng_jobs = 100
tile.markdown(f'###### Total jobs: :blue[{total_jobs}]$~~~~~~~~~~~~~~~$Currently running: :blue[{runng_jobs}]')

tile.markdown('###### *Jobs per Subject Area*')
tile.bar_chart(test_chart_data_1, x = 'Subject Area', y = 'Job Count', use_container_width = True)


#Tile2: Workflow
tile = col_matrix[1].container(border = True)
tile.subheader("Workflows", divider = 'gray')

total_wf = 100
runng_wf = 10
tile.markdown(f'###### Total workflows: :blue[{total_wf}]$~~~~~~~~~~~~~~~$Currently running: :blue[{runng_wf}]')
tile.markdown('###### *Workflows per Subject Area*')
tile.bar_chart(test_chart_data_2, x = 'Subject Area', y = 'Workflow Count', use_container_width = True)


#Tile3: DataObject


#Tile4 : WorkFlow-Job Relationship

tile = col_matrix[2].container(border = True)
tile.subheader("Workflow-Job Relationship", divider = 'gray')
option = tile.selectbox("Choose Subject Area", ('MDT', 'FLS', 'CRO', 'EMD', 'CBI'), index=None)
if option:
    tile.bar_chart(test_chart_data_3[option], x = 'Workflow', y = 'Job Count', use_container_width = True)

