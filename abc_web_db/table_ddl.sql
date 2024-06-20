
use abc_frmwrk_db;

-- ----------------------------------------------------------------- # LOG TABLE and VIEW # -------------------------------------------------------------------
CREATE TABLE ABC_METADATA_CHANGE_LOG
(
	TABLE_NAME	VARCHAR(100),
	PROC_NAME	VARCHAR(100),
	OPERATION	VARCHAR(10),
	PAYLOAD		BLOB,
	DATA_SOURCE	VARCHAR(10),
	CHANGE_TMST	TIMESTAMP(0)
);

create view ABC_METADATA_CHANGE_LOG_VW as
select TABLE_NAME,PROC_NAME,OPERATION,cast(PAYLOAD as CHAR) as PAYLOAD,DATA_SOURCE,CHANGE_TMST from ABC_METADATA_CHANGE_LOG;


-- ----------------------------------------------------------------- # Tables DDL # -------------------------------------------------------------------

-- drop table ABC_WORKFLOW_JOB_REL;
-- drop table ABC_JOB_MST;
-- drop table ABC_WORKFLOW_MST;
-- drop table ABC_SUBJECT_AREA_MST;


CREATE TABLE ABC_SUBJECT_AREA_MST
(
    SubjectAreaID   	integer not null auto_increment,
    SubjectAreaName 	varchar(100) not null,
    SubjectAreaDesc 	varchar(1024) null,
    constraint PK_ABC_SUBJECT_AREA_MST primary key (SubjectAreaID)
);


CREATE TABLE ABC_JOB_MST
(
    JobID                    integer not null auto_increment,
    JobName                  varchar(100) not null,
    JobTypeName              varchar(20) not null,
    JobDescription           varchar(1024) null,
    SubjectAreaID            integer not null,
    JobScriptName            varchar(100) not null,
    JobScriptLocation        varchar(512) not null,
    isActive                 char(1) not null,
    constraint PK_ABC_JOB_MST primary key (JobID),
    constraint FK_ABC_JOB_MST_SUBJAREA foreign key (SubjectAreaID) references ABC_SUBJECT_AREA_MST(SubjectAreaID) on delete cascade
);


CREATE TABLE ABC_WORKFLOW_MST
(
    WorkflowID                integer not null auto_increment,
    WorkflowName              varchar(100) not null,
    WorkflowDescription       varchar(1024) null,
    SubjectAreaID             integer not null,
    WorkflowScriptName        varchar(256) not null,
    WorkflowScriptLocation    varchar(512) not null,
    isActive                  char(1) not null,
    constraint PK_ABC_WORKFLOW_MST primary key (WorkflowID),
    constraint FK_ABC_WORKFLOW_MST_SUBJAREA foreign key (SubjectAreaID) references ABC_SUBJECT_AREA_MST(SubjectAreaID) on delete cascade
);


CREATE TABLE ABC_WORKFLOW_JOB_REL
(
    WorkflowID               integer not null,
    JobID                    integer not null,
    JobExecOrderSeq          integer not null,
    constraint PK_ABC_WORKFLOW_JOB_REL primary key (WorkflowID, JobID),
    constraint FK_ABC_WORKFLOW_JOB_REL_WORKFLOW foreign key (WorkflowID) references ABC_WORKFLOW_MST(WorkflowID) on delete cascade,
    constraint FK_ABC_WORKFLOW_JOB_REL_JOB foreign key (JobID) references ABC_JOB_MST(JobID) on delete cascade
);

