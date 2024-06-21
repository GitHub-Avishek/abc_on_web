#test data for abc web ui, will be fetched from database later on 

#https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

import pandas as pd

test_chart_data_1 = pd.DataFrame(data = {'Subject Area': ['MDT', 'FLS', 'CRO', 'EMD', 'CBI'], 'Job Count': [100, 120, 125, 75, 50]})

test_chart_data_2 = pd.DataFrame(data = {'Subject Area': ['MDT', 'FLS', 'CRO', 'EMD', 'CBI'], 'Workflow Count': [10, 12, 15, 8, 11]})

test_chart_data_3 = {'MDT' : pd.DataFrame(data = {'Workflow': ['MDT_WF_1', 'MDT_WF_2', 'MDT_WF_3', 'MDT_WF_4', 'MDT_WF_5'], 'Job Count': [20, 5, 2, 7, 11]}),
                     'FLS' : pd.DataFrame(data = {'Workflow': ['FLS_WF_1', 'FLS_WF_2', 'FLS_WF_3', 'FLS_WF_4', 'FLS_WF_5'], 'Job Count': [5, 10, 8, 8, 3]}),
                     'CRO' : pd.DataFrame(data = {'Workflow': ['CRO_WF_1', 'MDT_WF_2', 'CRO_WF_3', 'CRO_WF_4', 'CRO_WF_5'], 'Job Count': [11, 7, 8, 5, 2]}),
                     'EMD' : pd.DataFrame(data = {'Workflow': ['EMD_WF_1', 'EMD_WF_2', 'EMD_WF_3', 'EMD_WF_4', 'EMD_WF_5'], 'Job Count': [9, 3, 7, 2, 13]}),
                     'CBI' : pd.DataFrame(data = {'Workflow': ['CBI_WF_1', 'CBI_WF_2', 'CBI_WF_3', 'CBI_WF_4', 'CBI_WF_5'], 'Job Count': [10, 12, 6, 8, 17]}),
                    }

test_chart_data_4 = pd.DataFrame(data = {'JobID': ['100', '101', '103','104', '105'], 
                                         'JobName': ['DEMO_RAW_TO_STRUCT', 'DEMO_STRUCT_TO_WORK', 'DEMO_WORK_TO_PREP', 'DEMO_STRUCT_TO_WORK_WTD', 'DEMO_STRUCT_TO_PREP_TD'],
                                         'JobTypeName': ['ETL','ETL','ETL','ETL','ETL'],
                                         'JobDescription':['DEMO ETL Job','DEMO ETL Job','DEMO ETL Job','DEMO ETL Job','DEMO ETL Job'],
                                         'SubjectAreaID' : ['5','5','5','5','5'],
                                         'JobScriptName' : ['DEMO_RAW_TO_STRUCT.py', 'DEMO_STRUCT_TO_WORK.py', 'DEMO_WORK_TO_PREP.py', 'DEMO_STRUCT_TO_WORK_WTD.py', 'DEMO_STRUCT_TO_PREP_TD.py'],
                                         'JobScriptLocation' : ['/xxx/{env}/etl/','/xxx/{env}/etl/','/xxx/{env}/etl/','/xxx/{env}/etl/','/xxx/{env}/etl/'],
                                         'isActive' : ['Y','Y','Y','Y','Y']
                                         })

test_chart_data_5 = pd.DataFrame(data = {'WorkflowID': ['10', '11', '12'], 
                                         'WorkflowName': ['XXX_Daily_Load', 'YYY_Daily_Load', 'ZZZ_Daily_Load'],
                                         'WorkflowDescription':['Daily load for XXX','Daily load for YYY','Daily load for ZZZ'],
                                         'SubjectAreaID' : ['5','5','5'],
                                         'WorkFlowScriptName' : ['XXX_Airflow_D.py', 'YYY_Airflow_D.py', 'ZZZ_Airflow_D.py'],
                                         'WorkflowLocation' : ['/af_pipelines/xxx/{env}/','/af_pipelines/yyy/{env}/','/af_pipelines/zzz/{env}/'],
                                         'isActive' : ['Y','Y','Y']
                                         })

test_chart_data_6 = pd.DataFrame(data = {'WorkflowName': ['XXX_Daily_Load', 'XXX_Daily_Load', 'YYY_Daily_Load', 'YYY_Daily_Load', 'ZZZ_Daily_Load', 'ZZZ_Daily_Load'],
                                         'JobName' : ['XXX_SRC_TO_STG','XXX_STG_TO_TGT','YYY_SRC_TO_STG','YYY_STG_TO_TGT','ZZZ_SRC_TO_STG','ZZZ_STG_TO_TGT'],
                                         'JobExeOrderSeq' : [1,2,1,2,1,2]
                                         })