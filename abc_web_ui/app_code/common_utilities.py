### Common Functions ###

import streamlit as st


def get_subj_areas_list():
    conn = st.connection('mysql', type='sql')
    df = conn.query(f"select SubjectAreaName from ABC_SUBJECT_AREA_MST", ttl=0)
    return df['SubjectAreaName'].tolist()


def is_subjectarea_exists(sa_name):
    conn = st.connection('mysql', type='sql')
    df = conn.query(f"select count(1) as cnt from ABC_SUBJECT_AREA_MST where subjectareaname = '{sa_name.strip()}'", ttl=0)
    if df['cnt'].tolist()[0] > 0:
        return True
    else:
        return False
    

def is_job_exists(job_name):
    conn = st.connection('mysql', type='sql')
    df = conn.query(f"select count(1) as cnt from ABC_JOB_MST where jobname = '{job_name.strip()}'", ttl=0)
    if df['cnt'].tolist()[0] > 0:
        return True
    else:
        return False


def is_workflow_exists(wf_name):
    conn = st.connection('mysql', type='sql')
    df = conn.query(f"select count(1) as cnt from ABC_WORKFLOW_MST where workflowname = '{wf_name.strip()}'", ttl=0)
    if df['cnt'].tolist()[0] > 0:
        return True
    else:
        return False


def get_workflow_id(wf_name):
    conn = st.connection('mysql', type='sql')
    df = conn.query(f"select workflowid from ABC_WORKFLOW_MST where workflowname = '{wf_name.strip()}'", ttl=0)
    return df['workflowid'].tolist()[0]


def get_job_id(job_name):
    conn = st.connection('mysql', type='sql')
    df = conn.query(f"select jobid from ABC_JOB_MST where jobname = '{job_name.strip()}'", ttl=0)
    return df['jobid'].tolist()[0]


def is_wfjob_relation_exists(wf_name, job_name):
    wf_id = get_workflow_id(wf_name)
    job_id = get_job_id(job_name)
    conn = st.connection('mysql', type='sql')
    df = conn.query(f"select count(1) as cnt from ABC_WORKFLOW_JOB_REL where workflowid = {wf_id} and jobid = {job_id}", ttl=0)
    if df['cnt'].tolist()[0] > 0:
        return True
    else:
        return False

