import streamlit as st
import pandas as pd
import time
import json
from abc_sidebar import show_sidebar

from test_data import *
from quick_help import *
from common_utilities import *


###################################################################################
###                     Insert - session state and functions                    ###
###################################################################################
if 'manul_ins_sa_rec' not in st.session_state:
    st.session_state['manul_ins_sa_rec'] = []

def reset_manul_insert_sa_session_state():
    st.session_state['manul_ins_sa_rec'] = []

if 'disable_manul_ins_sbmt_btn' not in st.session_state:
    st.session_state['disable_manul_ins_sbmt_btn'] = False

def manual_insert_submit_clicked():
    st.session_state['disable_manul_ins_sbmt_btn'] = True

def manual_insert_add_clicked():
    st.session_state['disable_manul_ins_sbmt_btn'] = False

if 'ins_file_uploader_key' not in st.session_state:
    st.session_state['ins_file_uploader_key'] = 'sa_insert_file_'+str(time.time())

if 'ins_file_uploaded' not in st.session_state:
    st.session_state['ins_file_uploaded'] = False

def change_insert_file_uploader_key():
    st.session_state['ins_file_uploaded'] = False
    st.session_state['ins_file_uploader_key'] = 'sa_insert_file_'+str(time.time())


###################################################################################
###                   Update - session state and functions                      ###
###################################################################################

if 'manul_sa_upd_display' not in st.session_state:
    st.session_state['manul_sa_upd_display'] = []

if 'manul_sa_upd_payload' not in st.session_state:
    st.session_state['manul_sa_upd_payload'] = []

def reset_manul_update_sa_session_state():
    st.session_state['manul_sa_upd_display'] = []
    st.session_state['manul_sa_upd_payload'] = []
    st.session_state['disable_manul_upd_sbmt_btn'] = False


if 'manul_upd_toast_message' not in st.session_state:
    st.session_state['manul_upd_toast_message'] = ''

if 'disable_manul_upd_search_btn' not in st.session_state:
    st.session_state['disable_manul_upd_search_btn'] = False

if 'show_upd_add_cancel_buttons' not in st.session_state:
    st.session_state['show_upd_add_cancel_buttons'] = False

def manual_update_search_clicked():
    st.session_state['disable_manul_upd_search_btn'] = True

if 'disable_manul_upd_sbmt_btn' not in st.session_state:
    st.session_state['disable_manul_upd_sbmt_btn'] = False

def manual_update_submit_clicked():
    st.session_state['disable_manul_upd_sbmt_btn'] = True

if 'upd_file_uploader_key' not in st.session_state:
    st.session_state['upd_file_uploader_key'] = 'sa_update_file_'+str(time.time())

if 'upd_file_uploaded' not in st.session_state:
    st.session_state['upd_file_uploaded'] = False

def change_update_file_uploader_key():
    st.session_state['upd_file_uploaded'] = False
    st.session_state['upd_file_uploader_key'] = 'sa_update_file_'+str(time.time())


###################################################################################
###                 Delete - session state and functions                        ###
###################################################################################
if 'manul_del_sa_rec' not in st.session_state:
    st.session_state['manul_del_sa_rec'] = []

def reset_manul_delete_sa_session_state():
    st.session_state['manul_del_sa_rec'] = []

if 'disable_manul_del_sbmt_btn' not in st.session_state:
    st.session_state['disable_manul_del_sbmt_btn'] = False

def manual_delete_submit_clicked():
    st.session_state['disable_manul_del_sbmt_btn'] = True

def manual_delete_add_clicked():
    st.session_state['disable_manul_del_sbmt_btn'] = False

if 'del_file_uploader_key' not in st.session_state:
    st.session_state['del_file_uploader_key'] = 'sa_delete_file_'+str(time.time())

if 'del_file_uploaded' not in st.session_state:
    st.session_state['del_file_uploaded'] = False

def change_delete_file_uploader_key():
    st.session_state['del_file_uploaded'] = False
    st.session_state['del_file_uploader_key'] = 'sa_delete_file_'+str(time.time())



### Main UI window ###
st.set_page_config(page_title='ABC-on-Web', layout="wide", page_icon='🔤')
show_sidebar()

st.title(":gray[Subject Area]")
tabs = st.tabs(["Insert", "Update", "Delete", "Table View"])

ins_option = tabs[0].selectbox("Choose insert data source", ('Manually', 'From File'), index=None, key = 'ins_sa_src_option')
upd_option = tabs[1].selectbox("Choose update data source", ('Manually', 'From File'), index=None, key = 'upd_sa_src_option')
del_option = tabs[2].selectbox("Choose delete data source", ('Manually', 'From File'), index=None, key = 'del_sa_src_option')


###################################################################################
###                         Insert From File                                    ###
###################################################################################
if ins_option == 'From File':

    tabs[0].divider()

    with tabs[0]:
        upld_col, info_col = st.columns([0.75,0.25], gap = 'medium')

        info_box = info_col.container(border=True)
        info_box.markdown(quick_help['file_subjarea_insert'])

        upld_box = upld_col.container(border=True)

        placeholder1 = upld_box.empty()
        cols = upld_box.columns([8,1,1], gap='small')
        placeholder2 = cols[1].empty()
        placeholder3 = cols[2].empty()

        sa_ins_file = placeholder1.file_uploader("Choose a file", key=st.session_state['ins_file_uploader_key'], accept_multiple_files=False)

        if bool(sa_ins_file):

            try:    
                if not st.session_state['ins_file_uploaded']:
                    st.toast("File Uploaded.")
                    st.session_state['ins_file_uploaded'] = True

                file_txt = sa_ins_file.read()
                json_dict = eval(file_txt)
                if json_dict['db_table'].upper() == 'ABC_SUBJECT_AREA_MST' and json_dict['operation'].upper() == 'INSERT':
                    ins_data = json_dict['payload']
                    df = pd.DataFrame(ins_data)
                else:
                    st.toast("Uploaded file format is incorrect.")
                    raise Exception('Uploaded file format is incorrect.')

            except:
                df = pd.DataFrame({})

            if df.empty:
                placeholder1.error(f"No records found in {sa_ins_file.name}")
                disable_submit = True
            else:

                if len(df['SubjectAreaName'].tolist()) != len(set(df['SubjectAreaName'].tolist())):
                    placeholder1.error(f"Uploaded file {sa_ins_file.name} has duplicate subject area.")
                    disable_submit = True
                else:    
                    placeholder1.dataframe(df, use_container_width = True)
                    disable_submit = False

            submit_btn_clked = placeholder2.button('Submit', key='ins_file_data_submt_btn', disabled=disable_submit)
            if submit_btn_clked:
                
                #Insert records in database
                df_json = df.to_json(orient='records')
                ins_payload_json = json.dumps(json.loads(df_json), indent=4)

                conn = st.connection('mysql', type='sql')
                df = conn.query(f"call insert_subjectarea_from_json('{ins_payload_json}','FILE')", ttl=0)
                sp_return_val = df['return_val'].tolist()[0]

                #if 'ERROR' in sp_return_val:
                if sp_return_val.startswith('ERROR'):
                    placeholder1.error(f"Record insert Failed. {sp_return_val}")
                else:                   
                    if sp_return_val == '0':
                        placeholder1.info('No records inserted into ABC_SUBJECT_AREA_MST table.')
                    else:
                     placeholder1.success(f"{sp_return_val} record(s) inserted into ABC_SUBJECT_AREA_MST table.")

                placeholder2.empty()

            back_btn_clked = placeholder3.button('Back', key='ins_file_data_back_btn')
            if back_btn_clked:
                change_insert_file_uploader_key()
                st.rerun()


###################################################################################
###                               Manual Insert                                 ###
###################################################################################
if ins_option == 'Manually':

    tabs[0].divider()

    with tabs[0]:

        form_col, info_col = st.columns([0.75,0.25], gap = 'medium')
        form_box = form_col.form("manual_insert_subjectarea", clear_on_submit = True, border = False)
        info_box = info_col.container(border=True)
        form_box.markdown("### :gray[Add subject area details]")
        info_box.markdown(quick_help['manual_subjarea_insert'])

        sa_name       = form_box.text_input("Subject Area Name :red[*]")
        sa_desc       = form_box.text_input("Subject Area Description")
        
        add_btn_clkd = form_box.form_submit_button('Add')

        if add_btn_clkd:

            #Mandetory field check
            if bool(sa_name.strip()) and bool(sa_desc.strip()):
                if not is_subjectarea_exists(sa_name):
                    if sa_name not in  [x[1] for x in st.session_state['manul_ins_sa_rec']]:
                        ins_subjarea_rec = [False,sa_name,sa_desc]
                        st.session_state['manul_ins_sa_rec'].append(ins_subjarea_rec)
                        manual_insert_add_clicked()
                    else:
                        st.toast(f"Subject area {sa_name} already added.")
                else:
                    st.toast(f"Subject area {sa_name} already present in database table.")
            else:
                st.toast('Provide all the mandetory fields.')

        #Show added data
        if len(st.session_state['manul_ins_sa_rec']) > 0:

            placeholder = form_col.empty()
            
            with placeholder.container():
                st.divider()
                st.markdown('##### Added subject area details')
                
                ins_sa_rec_cols = ['Ignore','SubjectAreaName','SubjectAreaDesc']
                df = pd.DataFrame(st.session_state['manul_ins_sa_rec'], columns = ins_sa_rec_cols)
                edited_df = st.data_editor(df, use_container_width = True, hide_index = True)
                
                if not df.equals(edited_df):
                    st.session_state['manul_ins_sa_rec'] = edited_df.values.tolist()
                    st.rerun()


            cols = form_col.columns([8,1,1], gap='small')
            sbmt_btn_ckld = cols[1].button('Submit', key='ins_manual_data_submt_btn', on_click=manual_insert_submit_clicked, disabled=st.session_state['disable_manul_ins_sbmt_btn'])
            cncl_btn_ckld = cols[2].button("Cancel", key='ins_manual_data_back_btn')

            if sbmt_btn_ckld:
                #Insert records in database table

                edited_df = edited_df[edited_df['Ignore'] == False]
                edited_df_json = edited_df[ins_sa_rec_cols[1:]].to_json(orient='records')
                ins_payload_json = json.dumps(json.loads(edited_df_json), indent=4)

                conn = st.connection('mysql', type='sql')
                df = conn.query(f"call insert_subjectarea_from_json('{ins_payload_json}','MANUAL')", ttl=0)
                sp_return_val = df['return_val'].tolist()[0]

                #if 'ERROR' in sp_return_val:
                if sp_return_val.startswith('ERROR'):
                    placeholder.error(f"Record insert Failed. {sp_return_val}")
                else:                   
                    if sp_return_val == '0':
                        placeholder.info('No records inserted into ABC_SUBJECT_AREA_MST table.')
                    else:
                     placeholder.success(f"{sp_return_val} record(s) inserted into ABC_SUBJECT_AREA_MST table.")

                reset_manul_insert_sa_session_state()

            if cncl_btn_ckld:
                reset_manul_insert_sa_session_state()
                st.rerun()


###################################################################################
###                             Update From File                                ###
###################################################################################
if upd_option == 'From File':

    tabs[1].divider()

    with tabs[1]:

        upld_col, info_col = st.columns([0.75,0.25], gap = 'medium')

        info_box = info_col.container(border=True)
        info_box.markdown(quick_help['file_subjarea_update'])

        upld_box = upld_col.container(border=True)

        placeholder1 = upld_box.empty()
        cols = upld_box.columns([8,1,1], gap='small')
        placeholder2 = cols[1].empty()
        placeholder3 = cols[2].empty()

        sa_upd_file = placeholder1.file_uploader("Choose a file", key=st.session_state['upd_file_uploader_key'], accept_multiple_files=False)

        if bool(sa_upd_file):

            try:    
                if not st.session_state['upd_file_uploaded']:
                    st.toast("File Uploaded.")
                    st.session_state['upd_file_uploaded'] = True

                file_txt = sa_upd_file.read()
                json_dict = eval(file_txt)
                if json_dict['db_table'].upper() == 'ABC_SUBJECT_AREA_MST' and json_dict['operation'].upper() == 'UPDATE':
                    upd_data = json_dict['payload']
                    df = pd.DataFrame(upd_data)

                else:
                    st.toast("Uploaded file format is incorrect.")
                    raise Exception('Uploaded file format is incorrect.')

            except:
                df = pd.DataFrame({})

            if df.empty:
                placeholder1.error(f"No records found in {sa_upd_file.name}")
                disable_submit = True
            else:
                upd_sa_list = [x['SubjectAreaName'] for x in df['upd_key']]
                if len(upd_sa_list) != len(set(upd_sa_list)):
                    placeholder1.error(f"Uploaded file {sa_upd_file.name} has duplicate subject area.")
                    disable_submit = True
                else:
                    display_dict = {}
                    payload_dict = df.to_dict(orient='records')

                    for d in payload_dict:                    
                        if bool(display_dict.get('SubjectAreaName')):
                            display_dict['SubjectAreaName'].append(d['upd_key']['SubjectAreaName'])
                        else:
                            display_dict['SubjectAreaName'] = [d['upd_key']['SubjectAreaName']]

                        if bool(display_dict.get('Column Update(s)')):
                            display_dict['Column Update(s)'].append(','.join([f"{k}='{v}'" for k,v in d['upd_val'].items()]).replace("'NULL'", 'NULL'))
                        else:
                            display_dict['Column Update(s)'] = [','.join([f"{k}='{v}'" for k,v in d['upd_val'].items()]).replace("'NULL'", 'NULL')]

                    placeholder1.dataframe(display_dict, use_container_width=True)
                    disable_submit = False


            submit_btn_clked = placeholder2.button('Submit', key='upd_file_data_submt_btn', disabled=disable_submit)
            if submit_btn_clked:

                #Update records in database
                df_json = df.to_json(orient='records')
                upd_payload_json = json.dumps(json.loads(df_json), indent=4)

                conn = st.connection('mysql', type='sql')
                df = conn.query(f"call update_subjectarea_from_json('{upd_payload_json}','FILE')", ttl=0)
                sp_return_val = df['return_val'].tolist()[0]

                #if 'ERROR' in sp_return_val:
                if sp_return_val.startswith('ERROR'):
                    placeholder1.error(f"Record update Failed. {sp_return_val}")
                else:                   
                    if sp_return_val == '0':
                        placeholder1.info('No records updated into ABC_SUBJECT_AREA_MST table.')
                    else:
                     placeholder1.success(f"{sp_return_val} record(s) updated into ABC_SUBJECT_AREA_MST table.")

                placeholder2.empty()

            back_btn_clked = placeholder3.button('Back', key='upd_file_data_back_btn')
            if back_btn_clked:
                change_update_file_uploader_key()
                st.rerun()


###################################################################################
###                             Manual Update                                   ###
###################################################################################
if upd_option == 'Manually':

    tabs[1].divider()

    with tabs[1]:

        if bool(st.session_state['manul_upd_toast_message']):
            st.toast(st.session_state['manul_upd_toast_message'])
            st.session_state['manul_upd_toast_message'] = ''

        show_upd_add_cancel_buttons = False

        form_col, info_col = st.columns([0.75,0.25], gap = 'medium')
        form_box = form_col.form("manual_update_subjarea", clear_on_submit=True, border=False)
        info_box = info_col.container(border=True)
        form_box.markdown("### :gray[Add subject area details]")
        info_box.markdown(quick_help['manual_subjarea_update'])

        sa_name = form_box.text_input("Subject Area Name :red[*]").strip()
        sa_present = is_subjectarea_exists(sa_name)
        srch_btn_clkd = form_box.form_submit_button('Search', on_click=manual_update_search_clicked, disabled=st.session_state['disable_manul_upd_search_btn'])

        if srch_btn_clkd:

            #Mandetory field check
            if bool(sa_name):
                if sa_present:
                    st.session_state['show_upd_add_cancel_buttons'] = True
                else:
                    st.session_state['disable_manul_upd_search_btn'] = False
                    st.session_state['manul_upd_toast_message'] = "Subject Area not found in database table."
                    st.rerun()
            else:
                st.session_state['disable_manul_upd_search_btn'] = False
                st.session_state['manul_upd_toast_message'] = 'Please provide Subject Area Name.'
                st.rerun()

        if st.session_state['show_upd_add_cancel_buttons']:

            placeholder = form_col.empty()
            with placeholder.container():
                st.divider()
                st.markdown('##### Added subject area details')

                conn = st.connection('mysql', type='sql')
                df = conn.query(f"""select SubjectAreaName,SubjectAreaDesc from ABC_SUBJECT_AREA_MST where SubjectAreaName = '{sa_name}'""", ttl=60)

                edited_df = st.data_editor(df, use_container_width = True, hide_index = True) #, disabled=['SubjectAreaName'])

            cols = form_col.columns([8,1,1], gap='small')
            add_btn_ckld = cols[1].button("Add", key='upd_manual_data_add_btn')
            cncl_btn1_ckld = cols[2].button("Cancel", key='upd_manual_data_cancel_btn_1')

            if add_btn_ckld:

                befr_upd_row = df.iloc[0].to_dict()
                aftr_upd_row = edited_df.iloc[0].to_dict()

                col_upd_vals = []
                for col in befr_upd_row.keys():
                    if befr_upd_row[col] != aftr_upd_row[col]:
                        new_val = aftr_upd_row[col]
                        col_upd_vals.append([col,new_val])

                if bool(col_upd_vals):

                    upd_vals_txt = ','.join([x + '=' + (f"'{y}'" if y!='NULL' else 'NULL') for x,y in col_upd_vals])
                    upd_payload = {"upd_key" : {"SubjectAreaName" : sa_name}, "upd_val" : dict(col_upd_vals)}

                    subjarea_for_upd = [x[1] for x in st.session_state['manul_sa_upd_display']]
                    if sa_name in subjarea_for_upd:
                        sa_idx = subjarea_for_upd.index(sa_name)
                        st.session_state['manul_sa_upd_display'][sa_idx][2] = upd_vals_txt
                        st.session_state['manul_sa_upd_payload'][sa_idx] = upd_payload
                    else:
                        st.session_state['manul_sa_upd_display'].append([False,sa_name,upd_vals_txt])
                        st.session_state['manul_sa_upd_payload'].append(upd_payload)

                else:
                    st.session_state['manul_upd_toast_message'] = "No update made in subject area details."

                st.session_state['show_upd_add_cancel_buttons'] = False
                st.session_state['disable_manul_upd_search_btn'] = False
                st.rerun()

            if cncl_btn1_ckld:
                st.session_state['show_upd_add_cancel_buttons'] = False
                st.session_state['disable_manul_upd_search_btn'] = False
                st.rerun()

        if len(st.session_state['manul_sa_upd_display']):
            upd_val_df = pd.DataFrame(st.session_state['manul_sa_upd_display'], columns = ['Ignore','Subject Area Name', 'Column(s) Updated'])
            form_col.divider()
            placeholder = form_col.empty()
            edited_df = placeholder.data_editor(upd_val_df, hide_index=True, disabled=['Subject Area Name', 'Column(s) Updated'])

            ignr_upd_checked_list = edited_df["Ignore"].tolist()
            for i in range(len(ignr_upd_checked_list)):
                st.session_state['manul_sa_upd_display'][i][0] = ignr_upd_checked_list[i]


            cols = form_col.columns([1,1,8], gap='small')
            sbmt_btn_ckld = cols[0].button('Submit', key='upd_manual_data_submt_btn', on_click=manual_update_submit_clicked, disabled=st.session_state['disable_manul_upd_sbmt_btn'])
            cncl_btn2_ckld = cols[1].button('Cancel', key='upd_manual_data_cancel_btn_2')

            if sbmt_btn_ckld:
                #Process data in st.session_state['manul_sa_upd_payload'] using ignr_upd_checked_list
                final_sa_upd_payload = []

                for i in range(len(st.session_state['manul_sa_upd_payload'])):
                    if not ignr_upd_checked_list[i]:
                       final_sa_upd_payload.append(st.session_state['manul_sa_upd_payload'][i]) 

                #Update records in database
                sa_upd_payload_json = json.dumps(final_sa_upd_payload, indent=4)

                conn = st.connection('mysql', type='sql')
                df = conn.query(f"call update_subjectarea_from_json('{sa_upd_payload_json}','MANUAL')", ttl=0)
                sp_return_val = df['return_val'].tolist()[0]

                #if 'ERROR' in sp_return_val:
                if sp_return_val.startswith('ERROR'):
                    placeholder.error(f"Record insert Failed. {sp_return_val}")
                else:                   
                    if sp_return_val == '0':
                        placeholder.info('No records updated in ABC_SUBJECT_AREA_MST table.')
                    else:
                     placeholder.success(f"{sp_return_val} record(s) update in ABC_SUBJECT_AREA_MST table.")

                reset_manul_update_sa_session_state()

            if cncl_btn2_ckld:
                reset_manul_update_sa_session_state()


###################################################################################
###                             Delete From File                                ###
###################################################################################
if del_option == 'From File':

    tabs[2].divider()

    with tabs[2]:

        upld_col, info_col = st.columns([0.75,0.25], gap = 'medium')

        info_box = info_col.container(border=True)
        info_box.markdown(quick_help['file_subjarea_delete'])

        upld_box = upld_col.container(border=True)

        placeholder1 = upld_box.empty()
        cols = upld_box.columns([8,1,1], gap='small')
        placeholder2 = cols[1].empty()
        placeholder3 = cols[2].empty()

        sa_del_file = placeholder1.file_uploader("Choose a file", key=st.session_state['del_file_uploader_key'], accept_multiple_files=False)

        if bool(sa_del_file):
            try:    
                if not st.session_state['del_file_uploaded']:
                    st.toast("File Uploaded.")
                    st.session_state['del_file_uploaded'] = True

                file_txt = sa_del_file.read()
                df = pd.DataFrame(eval(file_txt)['payload'])

            except:
                df = pd.DataFrame({})

            if df.empty:
                placeholder1.error(f"No records found in {sa_del_file.name}")
                disable_submit = True
            else:    
                if len(df['SubjectAreaName'].tolist()) != len(set(df['SubjectAreaName'].tolist())):
                    placeholder1.error(f"Uploaded file {sa_del_file.name} has duplicate subject area.")
                    disable_submit = True
                else:    
                    placeholder1.dataframe(df, hide_index=True, use_container_width=True)
                    disable_submit = False

            submit_btn_clked = placeholder2.button('Submit', key='del_file_data_submt_btn', disabled=disable_submit)
            if submit_btn_clked:

                df_json = df.to_json(orient='records')
                del_payload_json = json.dumps(json.loads(df_json), indent=4)

                conn = st.connection('mysql', type='sql')
                df = conn.query(f"call delete_subjectarea_from_json('{del_payload_json}','FILE')", ttl=0)
                sp_return_val = df['return_val'].tolist()[0]

                #if 'ERROR' in sp_return_val:
                if sp_return_val.startswith('ERROR'):
                    placeholder1.error(f"Record delete Failed. {sp_return_val}")
                else:                   
                    if sp_return_val == '0':
                        placeholder1.info('No records deleted from ABC_SUBJECT_AREA_MST table.')
                    else:
                     placeholder1.success(f"{sp_return_val} record(s) deleted from ABC_SUBJECT_AREA_MST table.")

                placeholder2.empty()

            back_btn_clked = placeholder3.button('Back', key='del_file_data_back_btn')
            if back_btn_clked:
                change_delete_file_uploader_key()
                st.rerun()


###################################################################################
###                             Manual Delete                                   ###
###################################################################################

if del_option == 'Manually':

    tabs[2].divider()

    with tabs[2]:

        form_col, info_col = st.columns([0.75,0.25], gap = 'medium')
        form_box = form_col.form("manual_delete_subjarea", clear_on_submit = True, border = False)
        info_box = info_col.container(border=True)
        form_box.markdown("### :gray[Add subject area delete details]")
        info_box.markdown(quick_help['manual_subjarea_delete'])

        sa_name = form_box.text_input("Subject Area Name :red[*]").strip()

        add_btn_clkd = form_box.form_submit_button('Add')

        if add_btn_clkd:

            #mandetory field check
            if bool(sa_name):
                sa_present = is_subjectarea_exists(sa_name)
                if not sa_present:
                    st.toast('Aubject Area not found in database table.')   
                else:
                    if sa_name not in  [x[1] for x in st.session_state['manul_del_sa_rec']]:
                        st.session_state['manul_del_sa_rec'].append([False, sa_name])
                        manual_delete_add_clicked()
                    else:
                        st.toast(f"Wo {sa_name} already added.")
            else:
                st.toast('Provide all the mandetory fields.')

        #Show added data
        if len(st.session_state['manul_del_sa_rec']) > 0:
            placeholder = form_col.empty()
            
            with placeholder.container():
                st.divider()
                st.markdown('##### Added subject area details')
                df = pd.DataFrame(st.session_state['manul_del_sa_rec'], columns = ['Ignore','SubjectAreaName'])
                edited_df = st.data_editor(df, hide_index=True, 
                                           column_config={"Ignore": st.column_config.Column(width="small"),
                                                          "SubjectAreaName": st.column_config.Column(width="medium")}, disabled=["SubjectAreaName"])
                
                if not df.equals(edited_df):
                    st.session_state['manul_del_sa_rec'] = edited_df.values.tolist()
                    st.rerun()

            cols = form_col.columns([1,1,8], gap='small')
            sbmt_btn_ckld = cols[0].button('Submit', key='del_manual_data_submt_btn', on_click=manual_delete_submit_clicked, disabled=st.session_state['disable_manul_del_sbmt_btn'])
            cncl_btn_ckld = cols[1].button("Cancel", key='del_manual_data_back_btn')

            if sbmt_btn_ckld:

                #Delete records in database
                del_sa_list = edited_df[edited_df['Ignore'] == False]['SubjectAreaName'].tolist()

                del_sa_payload = []
                for sa_nm in del_sa_list:
                    del_sa_payload.append({"SubjectAreaName" : sa_nm})
 
                del_payload_json = json.dumps(del_sa_payload, indent=4)

                conn = st.connection('mysql', type='sql')
                df = conn.query(f"call delete_subjectarea_from_json('{del_payload_json}','MANUAL')", ttl=0)
                sp_return_val = df['return_val'].tolist()[0]

                #if 'ERROR' in sp_return_val:
                if sp_return_val.startswith('ERROR'):
                    placeholder.error(f"Record delete Failed. {sp_return_val}")
                else:                   
                    if sp_return_val == '0':
                        placeholder.info('No records deleted from ABC_SUBJECT_AREA_MST table.')
                    else:
                     placeholder.success(f"{sp_return_val} record(s) delete from ABC_SUBJECT_AREA_MST table.")

                reset_manul_delete_sa_session_state()

            if cncl_btn_ckld:
                reset_manul_delete_sa_session_state()
                st.rerun()


###################################################################################
###                              Table View                                     ###
###################################################################################

try:
    conn = st.connection('mysql', type='sql')
    df = conn.query('SELECT count(1) cnt from ABC_SUBJECT_AREA_MST;', ttl=0)
    if df['cnt'].tolist()[0] > 0:
        df = conn.query('select * from ABC_SUBJECT_AREA_MST;', ttl=0)
        tabs[3].dataframe(df, use_container_width=True,hide_index=True)
    else:
        tabs[3].error("No records found in ABC_SUBJECT_AREA_MST")

except Exception as e:
    tabs[3].error(str(e))

refsh_btn_ckld = tabs[3].button("Refresh")
if refsh_btn_ckld:
    st.rerun()