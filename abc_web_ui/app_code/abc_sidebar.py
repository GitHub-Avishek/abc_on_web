import streamlit as st

#displays sidebar
def show_sidebar():
    with st.sidebar:

        #Sidebar Font CSS
        st.markdown("""
        <style>
        .big-font {
            font-size:30px;
            font-weight: bold;
            color: silver;
        }
        .small-font {
            font-size:15px;
            font-weight: small;
            color: gray;
        }
        </style>
        """, unsafe_allow_html=True)

        #Sidebar header
        st.sidebar.markdown('<p class="big-font">ABC Framework UI</p><p class="small-font">(v1.0)</p>', unsafe_allow_html=True)
        st.sidebar.divider()

        #Home
        st.sidebar.page_link("main.py", label="🏛️ :gray[__Home__]")

        st.sidebar.markdown(':gray[__Master Tables__]',unsafe_allow_html=True)
        #SubjectArea
        st.sidebar.page_link("pages/subjectarea.py", label=":gray[▶ __SubjectArea__]")
        #Job
        st.sidebar.page_link("pages/job.py", label=":gray[▶ __Job__]")
        #Workflow
        st.sidebar.page_link("pages/workflow.py", label=":gray[▶ __Workflow__]")        

        st.sidebar.markdown(':gray[__Relationship Tables__]',unsafe_allow_html=True)
        #Workflow & Job
        st.sidebar.page_link("pages/workflow_job.py", label=":gray[▶ __Workflow-Job__]")

        st.sidebar.markdown(':gray[__Transaction Tables__]',unsafe_allow_html=True)
        #job run log
        st.sidebar.page_link("pages/job_run_log.py", label=":gray[▶ __Job-Run-Log__]")
        #job error log
        st.sidebar.page_link("pages/job_error_log.py", label=":gray[▶ __Job-Error-Log__]")