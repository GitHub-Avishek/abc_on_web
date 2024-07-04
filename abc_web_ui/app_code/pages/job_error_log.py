import streamlit as st
import pandas as pd
import time
import json
from abc_sidebar import show_sidebar

from test_data import *
from quick_help import *
from common_utilities import *

st.set_page_config(page_title='ABC-on-Web', layout="wide", page_icon='🔤')
show_sidebar()

st.title(":gray[Job Error Log]")

try:
    conn = st.connection('mysql', type='sql')
    df = conn.query('SELECT count(1) cnt from ABC_JOB_RUN_ERROR_LOG;', ttl=0)
    if df['cnt'].tolist()[0] > 0:
        df = conn.query('select trim(JobRunID) JobRunID, trim(JobID) JobID, ErrorText, cast(ErrorDetails as char) ErrorDetails, ErrorLogTmst from ABC_JOB_RUN_ERROR_LOG;', ttl=0)
        st.dataframe(df, use_container_width=True,hide_index=True)
    else:
        st.error("No records found in ABC_JOB_RUN_ERROR_LOG")
except Exception as e:
    st.error(str(e))

refsh_btn_ckld = st.button("Refresh")
if refsh_btn_ckld:
    st.rerun()
