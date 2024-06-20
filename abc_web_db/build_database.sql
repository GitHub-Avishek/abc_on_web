CREATE DATABASE abc_frmwrk_db;

CREATE USER 'app_master' identified by '@dmin%P$wd'; 
CREATE USER 'app_devlpr' identified by 'D3v1p%P$wd'; 
CREATE USER 'app_reader' identified by 'R3adr%P$wd';

GRANT SELECT ON abc_frmwrk_db.* TO 'app_reader'@'%';
GRANT SELECT,INSERT,UPDATE,DELETE,EXECUTE,CREATE TEMPORARY TABLES ON abc_frmwrk_db.* TO 'app_devlpr'@'%';
GRANT ALL ON abc_frmwrk_db.* TO 'app_master'@'%';


USE abc_frmwrk_db;

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


delimiter //
create procedure insert_job_from_json(in json_txt blob, in src_typ varchar(10))
begin 
	declare insert_stmt blob;

	declare exit handler for sqlexception
    begin
		GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
		SET @full_error = CONCAT("ERROR ", @errno, " (", @sqlstate, "): ", @text);
		 SELECT @full_error as return_val;
    end;
    
	set @insert_stmt_txt = concat('insert into ABC_JOB_MST(JobName,JobTypeName,JobDescription,SubjectAreaID,JobScriptName,JobScriptLocation,isActive)
	select j.JobName,j.JobTypeName,j.JobDescription,z.SubjectAreaID,j.JobScriptName,j.JobScriptLocation,j.isActive
	from json_table(''', json_txt, ''', ''$[*]'' COLUMNS(
		  JobName VARCHAR(255) PATH "$.""JobName""" ERROR ON EMPTY, 
		  JobTypeName VARCHAR(255) PATH "$.""JobTypeName""" NULL ON EMPTY,
		  JobDescription VARCHAR(255) PATH "$.""JobDescription""" NULL ON EMPTY,
		  SubjectAreaName VARCHAR(255) PATH "$.""SubjectAreaName""" NULL ON EMPTY,
		  JobScriptName VARCHAR(255) PATH "$.""JobScriptName""" NULL ON EMPTY,
		  JobScriptLocation VARCHAR(255) PATH "$.""JobScriptLocation"""  NULL ON EMPTY,
		  isActive VARCHAR(255) PATH "$.""isActive""" NULL ON EMPTY
		)) as j
		left outer join ABC_SUBJECT_AREA_MST z
		on j.SubjectAreaName = z.SubjectAreaName');
		
	prepare insert_stmt from @insert_stmt_txt;
	execute insert_stmt;
    select cast(row_count() as char) as return_val;
	-- deallocate prepare insert_stmt;
	insert into ABC_METADATA_CHANGE_LOG values('ABC_JOB_MST','insert_job_from_json','INSERT',json_txt,src_typ,current_timestamp());
	commit;

end //

delimiter ;

-- MySQL UPDATE SP : ABC_JOB_MST --

delimiter //
create procedure update_job_from_json(in json_txt blob, in src_typ varchar(10))
begin 

	declare update_stmt blob;

	declare exit handler for sqlexception
    begin
		GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
		SET @full_error = CONCAT("ERROR ", @errno, " (", @sqlstate, "): ", @text);
		 SELECT @full_error as return_val;
    end;

	set @update_stmt_txt = concat('update ABC_JOB_MST s
	inner join
	(
	select j.JobName,j.JobNameNew,j.JobTypeName,j.JobDescription,z.SubjectAreaID,j.JobScriptName,j.JobScriptLocation,j.isActive,j.SubjectAreaName
	from json_table(''', json_txt, ''', ''$[*]'' COLUMNS(
      JobName VARCHAR(255) PATH "$.""upd_key"".""JobName""" ERROR ON EMPTY, 
	  JobNameNew VARCHAR(255) PATH "$.""upd_val"".""JobName""" NULL ON EMPTY, 
      JobTypeName VARCHAR(255) PATH "$.""upd_val"".""JobTypeName""" NULL ON EMPTY,
      JobDescription VARCHAR(255) PATH "$.""upd_val"".""JobDescription""" NULL ON EMPTY,
      SubjectAreaName VARCHAR(255) PATH "$.""upd_val"".""SubjectAreaName""" NULL ON EMPTY,
      JobScriptName VARCHAR(255) PATH "$.""upd_val"".""JobScriptName""" NULL ON EMPTY,
      JobScriptLocation VARCHAR(255) PATH "$.""upd_val"".""JobScriptLocation"""  NULL ON EMPTY,
      isActive VARCHAR(255) PATH "$.""upd_val"".""isActive""" NULL ON EMPTY
    )) as j
    left outer join ABC_SUBJECT_AREA_MST z
    on j.SubjectAreaName = z.SubjectAreaName
	) t
	on s.JobName = t.JobName
	set
		s.JobName = case when t.JobNameNew = ''NULL'' then NULL else coalesce(t.JobNameNew, s.JobName) end,
		s.JobTypeName = case when t.JobTypeName = ''NULL'' then NULL else coalesce(t.JobTypeName, s.JobTypeName) end,
		s.JobDescription = case when t.JobDescription = ''NULL'' then NULL else coalesce(t.JobDescription, s.JobDescription) end,
		s.SubjectAreaID = case when t.SubjectAreaName = ''NULL'' then NULL else coalesce(t.SubjectAreaID, s.SubjectAreaID) end,
		s.JobScriptName = case when t.JobScriptName = ''NULL'' then NULL else coalesce(t.JobScriptName, s.JobScriptName) end,
		s.JobScriptLocation = case when t.JobScriptLocation = ''NULL'' then NULL else coalesce(t.JobScriptLocation, s.JobScriptLocation) end,
		s.isActive = case when t.isActive = ''NULL'' then NULL else coalesce(t.isActive, s.isActive) end');
		
	prepare update_stmt from @update_stmt_txt;
	execute update_stmt;
    select cast(row_count() as char) as return_val;
	-- deallocate prepare update_stmt;
	insert into ABC_METADATA_CHANGE_LOG values('ABC_JOB_MST','update_job_from_json','UPDATE',json_txt,src_typ,current_timestamp());
	commit;

end //

delimiter ;

-- MySQL DELETE SP : ABC_JOB_MST --

delimiter //
create procedure delete_job_from_json(in json_txt blob, in src_typ varchar(10))
begin 

	declare delete_stmt blob;

	declare exit handler for sqlexception
    begin
		GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
		SET @full_error = CONCAT("ERROR ", @errno, " (", @sqlstate, "): ", @text);
		 SELECT @full_error as return_val;
    end;

	set @delete_stmt_txt = concat('delete from ABC_JOB_MST where JobName in 
	(select distinct JobName from json_table(''', json_txt, ''', ''$[*]'' COLUMNS(
      JobName VARCHAR(255) PATH "$.""JobName""" ERROR ON EMPTY
    )) j)');
		
	prepare delete_stmt from @delete_stmt_txt;
	execute delete_stmt;
    select cast(row_count() as char) as return_val;
	-- deallocate prepare delete_stmt;
	insert into ABC_METADATA_CHANGE_LOG values('ABC_JOB_MST','delete_job_from_json','DELETE',json_txt,src_typ,current_timestamp());
	commit;

end //

delimiter ;



-- MySQL INSERT SP : ABC_WORKFLOW_MST --

delimiter //
create procedure insert_workflow_from_json(in json_txt blob, in src_typ varchar(10))
begin 
	declare insert_stmt blob;

	declare exit handler for sqlexception
    begin
		GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
		SET @full_error = CONCAT("ERROR ", @errno, " (", @sqlstate, "): ", @text);
		 SELECT @full_error as return_val;
    end;
    
	set @insert_stmt_txt = concat('insert into ABC_WORKFLOW_MST(WorkflowName,WorkflowDescription,SubjectAreaID,WorkflowScriptName,WorkflowScriptLocation,isActive)
	select j.WorkflowName,j.WorkflowDescription,z.SubjectAreaID,j.WorkflowScriptName,j.WorkflowScriptLocation,j.isActive
	from json_table(''', json_txt, ''', ''$[*]'' COLUMNS(
		  WorkflowName VARCHAR(255) PATH "$.""WorkflowName""" ERROR ON EMPTY, 
		  WorkflowDescription VARCHAR(255) PATH "$.""WorkflowDescription""" NULL ON EMPTY,
		  SubjectAreaName VARCHAR(255) PATH "$.""SubjectAreaName""" NULL ON EMPTY,
		  WorkflowScriptName VARCHAR(255) PATH "$.""WorkflowScriptName""" NULL ON EMPTY,
		  WorkflowScriptLocation VARCHAR(255) PATH "$.""WorkflowScriptLocation"""  NULL ON EMPTY,
		  isActive VARCHAR(255) PATH "$.""isActive""" NULL ON EMPTY
		)) as j
		left outer join ABC_SUBJECT_AREA_MST z
		on j.SubjectAreaName = z.SubjectAreaName');
		
	prepare insert_stmt from @insert_stmt_txt;
	execute insert_stmt;
    select cast(row_count() as char) as return_val;
	-- deallocate prepare insert_stmt;
	insert into ABC_METADATA_CHANGE_LOG values('ABC_WORKFLOW_MST','insert_workflow_from_json','INSERT',json_txt,src_typ,current_timestamp());
	commit;

end //

delimiter ;

-- MySQL UPDATE SP : ABC_WORKFLOW_MST --

delimiter //
create procedure update_workflow_from_json(in json_txt blob, in src_typ varchar(10))
begin 

	declare update_stmt blob;

	declare exit handler for sqlexception
    begin
		GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
		SET @full_error = CONCAT("ERROR ", @errno, " (", @sqlstate, "): ", @text);
		 SELECT @full_error as return_val;
    end;

	set @update_stmt_txt = concat('update ABC_WORKFLOW_MST s
	inner join
	(
	select j.WorkflowName,j.newWorkflowName,j.WorkflowDescription,z.SubjectAreaID,j.WorkflowScriptName,j.WorkflowScriptLocation,j.isActive,j.SubjectAreaName
	from json_table(''', json_txt, ''', ''$[*]'' COLUMNS(
      WorkflowName VARCHAR(255) PATH "$.""upd_key"".""WorkflowName""" ERROR ON EMPTY, 
	  newWorkflowName VARCHAR(255) PATH "$.""upd_val"".""WorkflowName""" NULL ON EMPTY, 
      WorkflowDescription VARCHAR(255) PATH "$.""upd_val"".""WorkflowDescription""" NULL ON EMPTY,
      SubjectAreaName VARCHAR(255) PATH "$.""upd_val"".""SubjectAreaName""" NULL ON EMPTY,
      WorkflowScriptName VARCHAR(255) PATH "$.""upd_val"".""WorkflowScriptName""" NULL ON EMPTY,
      WorkflowScriptLocation VARCHAR(255) PATH "$.""upd_val"".""WorkflowScriptLocation"""  NULL ON EMPTY,
      isActive VARCHAR(255) PATH "$.""upd_val"".""isActive""" NULL ON EMPTY
    )) as j
    left outer join ABC_SUBJECT_AREA_MST z
    on j.SubjectAreaName = z.SubjectAreaName
	) t
	on s.WorkflowName = t.WorkflowName
	set
		s.WorkflowName = case when t.newWorkflowName = ''NULL'' then NULL else coalesce(t.newWorkflowName, s.WorkflowName) end,
		s.WorkflowDescription = case when t.WorkflowDescription = ''NULL'' then NULL else coalesce(t.WorkflowDescription, s.WorkflowDescription) end,
		s.SubjectAreaID = case when t.SubjectAreaName = ''NULL'' then NULL else coalesce(t.SubjectAreaID, s.SubjectAreaID) end,
		s.WorkflowScriptName = case when t.WorkflowScriptName = ''NULL'' then NULL else coalesce(t.WorkflowScriptName, s.WorkflowScriptName) end,
		s.WorkflowScriptLocation = case when t.WorkflowScriptLocation = ''NULL'' then NULL else coalesce(t.WorkflowScriptLocation, s.WorkflowScriptLocation) end,
		s.isActive = case when t.isActive = ''NULL'' then NULL else coalesce(t.isActive, s.isActive) end');
		
	prepare update_stmt from @update_stmt_txt;
	execute update_stmt;
    select cast(row_count() as char) as return_val;
	-- deallocate prepare update_stmt;
	insert into ABC_METADATA_CHANGE_LOG values('ABC_WORKFLOW_MST','update_workflow_from_json','UPDATE',json_txt,src_typ,current_timestamp());
	commit;

end //

delimiter ;

-- MySQL DELETE SP : ABC_WORKFLOW_MST --

delimiter //
create procedure delete_workflow_from_json(in json_txt blob, in src_typ varchar(10))
begin 

	declare delete_stmt blob;

	declare exit handler for sqlexception
    begin
		GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
		SET @full_error = CONCAT("ERROR ", @errno, " (", @sqlstate, "): ", @text);
		 SELECT @full_error as return_val;
    end;

	set @delete_stmt_txt = concat('delete from ABC_WORKFLOW_MST where WorkflowName in 
	(select distinct WorkflowName from json_table(''', json_txt, ''', ''$[*]'' COLUMNS(
      WorkflowName VARCHAR(255) PATH "$.""WorkflowName""" ERROR ON EMPTY
    )) j)');
		
	prepare delete_stmt from @delete_stmt_txt;
	execute delete_stmt;
    select cast(row_count() as char) as return_val;
	-- deallocate prepare delete_stmt;
	insert into ABC_METADATA_CHANGE_LOG values('ABC_WORKFLOW_MST','delete_workflow_from_json','DELETE',json_txt,src_typ,current_timestamp());
	commit;

end //

delimiter ;

-- MySQL INSERT SP : ABC_WORKFLOW_JOB_REL --

delimiter //
create procedure insert_workflow_job_relation_from_json(in json_txt blob, in src_typ varchar(10))
begin 
	declare insert_stmt blob;

	declare exit handler for sqlexception
    begin
		GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
		SET @full_error = CONCAT("ERROR ", @errno, " (", @sqlstate, "): ", @text);
		 SELECT @full_error as return_val;
    end;
    
	set @insert_stmt_txt = concat('insert into ABC_WORKFLOW_JOB_REL(WorkflowID,JobID,JobExecOrderSeq)
	select x.WorkflowID, y.JobID, j.JobExecOrderSeq
	from json_table(''', json_txt, ''', ''$[*]'' COLUMNS(
		  WorkflowName VARCHAR(255) PATH "$.""WorkflowName""" ERROR ON EMPTY, 
		  JobName VARCHAR(255) PATH "$.""JobName""" ERROR ON EMPTY, 
		  JobExecOrderSeq VARCHAR(255) PATH "$.""JobExecOrderSeq""" NULL ON EMPTY
		)) as j
		inner join ABC_WORKFLOW_MST x
		on j.WorkflowName = x.WorkflowName
		inner join ABC_JOB_MST y
		on j.JobName = y.JobName');
		
	prepare insert_stmt from @insert_stmt_txt;
	execute insert_stmt;
    select cast(row_count() as char) as return_val;
	-- deallocate prepare insert_stmt;
	insert into ABC_METADATA_CHANGE_LOG values('ABC_WORKFLOW_JOB_REL','insert_workflow_job_relation_from_json','INSERT',json_txt,src_typ,current_timestamp());
	commit;

end //

delimiter ;


-- MySQL UPDATE SP : ABC_WORKFLOW_JOB_REL --

delimiter //
create procedure update_workflow_job_relation_from_json(in json_txt blob, in src_typ varchar(10))
begin 

	declare update_stmt blob;

	declare exit handler for sqlexception
    begin
		GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
		SET @full_error = CONCAT("ERROR ", @errno, " (", @sqlstate, "): ", @text);
		 SELECT @full_error as return_val;
    end;

	set @update_stmt_txt = concat('update ABC_WORKFLOW_JOB_REL s
	inner join
	(
	select x.WorkflowID, y.JobID, j.JobExecOrderSeq
	from json_table(''', json_txt, ''', ''$[*]'' COLUMNS(
      WorkflowName VARCHAR(255) PATH "$.""upd_key"".""WorkflowName""" ERROR ON EMPTY, 
      JobName VARCHAR(255) PATH "$.""upd_key"".""JobName""" ERROR ON EMPTY,
      JobExecOrderSeq VARCHAR(255) PATH "$.""upd_val"".""JobExecOrderSeq""" NULL ON EMPTY
    )) as j
    inner join ABC_WORKFLOW_MST x
    on j.WorkflowName = x.WorkflowName
    inner join ABC_JOB_MST y
    on j.JobName = y.JobName
	) t
	on s.WorkflowID = t.WorkflowID and s.JobID = t.JobID
	set
		s.JobExecOrderSeq = case when t.JobExecOrderSeq = ''NULL'' then NULL else coalesce(t.JobExecOrderSeq, s.JobExecOrderSeq) end');
		
	prepare update_stmt from @update_stmt_txt;
	execute update_stmt;
    select cast(row_count() as char) as return_val;
	-- deallocate prepare update_stmt;
	insert into ABC_METADATA_CHANGE_LOG values('ABC_WORKFLOW_MST','update_workflow_from_json','UPDATE',json_txt,src_typ,current_timestamp());
	commit;

end //

delimiter ;


-- MySQL DELETE SP : ABC_WORKFLOW_JOB_REL --

delimiter //
create procedure delete_workflow_job_relation_from_json(in json_txt blob, in src_typ varchar(10))
begin 

	declare delete_stmt blob;

	declare exit handler for sqlexception
    begin
		GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
		SET @full_error = CONCAT("ERROR ", @errno, " (", @sqlstate, "): ", @text);
		 SELECT @full_error as return_val;
    end;

	set @delete_stmt_txt = concat('delete from ABC_WORKFLOW_JOB_REL where (WorkflowID,JobID) in 
	(
	select distinct x.WorkflowID, y.JobID
	from json_table(''', json_txt, ''', ''$[*]'' COLUMNS(
      WorkflowName VARCHAR(255) PATH "$.""WorkflowName""" ERROR ON EMPTY,
	  JobName VARCHAR(255) PATH "$.""JobName""" ERROR ON EMPTY
    )) as j
    inner join ABC_WORKFLOW_MST x
    on j.WorkflowName = x.WorkflowName
    inner join ABC_JOB_MST y
    on j.JobName = y.JobName
	)');
		
	prepare delete_stmt from @delete_stmt_txt;
	execute delete_stmt;
    select cast(row_count() as char) as return_val;
	-- deallocate prepare delete_stmt;
	insert into ABC_METADATA_CHANGE_LOG values('ABC_WORKFLOW_MST','delete_workflow_from_json','DELETE',json_txt,src_typ,current_timestamp());
	commit;

end //

delimiter ;


-- MySQL INSERT SP : ABC_SUBJECT_AREA_MST --

delimiter //
create procedure insert_subjectarea_from_json(in json_txt blob, in src_typ varchar(10))
begin 
	declare insert_stmt blob;

	declare exit handler for sqlexception
    begin
		GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
		SET @full_error = CONCAT("ERROR ", @errno, " (", @sqlstate, "): ", @text);
		 SELECT @full_error as return_val;
    end;
    
	set @insert_stmt_txt = concat('insert into ABC_SUBJECT_AREA_MST(SubjectAreaName,SubjectAreaDesc)
	select j.SubjectAreaName,j.SubjectAreaDesc
	from json_table(''', json_txt, ''', ''$[*]'' COLUMNS(
		  SubjectAreaName VARCHAR(255) PATH "$.""SubjectAreaName""" ERROR ON EMPTY, 
		  SubjectAreaDesc VARCHAR(255) PATH "$.""SubjectAreaDesc""" NULL ON EMPTY
		)) as j');
		
	prepare insert_stmt from @insert_stmt_txt;
	execute insert_stmt;
    select cast(row_count() as char) as return_val;
	-- deallocate prepare insert_stmt;
	insert into ABC_METADATA_CHANGE_LOG values('ABC_SUBJECT_AREA_MST','insert_subjectarea_from_json','INSERT',json_txt,src_typ,current_timestamp());
	commit;

end //

delimiter ;


-- MySQL UPDATE SP : ABC_SUBJECT_AREA_MST --

delimiter //
create procedure update_subjectarea_from_json(in json_txt blob, in src_typ varchar(10))
begin 

	declare update_stmt blob;

	declare exit handler for sqlexception
    begin
		GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
		SET @full_error = CONCAT("ERROR ", @errno, " (", @sqlstate, "): ", @text);
		 SELECT @full_error as return_val;
    end;

	set @update_stmt_txt = concat('update ABC_SUBJECT_AREA_MST s
	inner join
	(select j.SubjectAreaName, j.newSubjectAreaName, j.SubjectAreaDesc
		from json_table(''', json_txt, ''', ''$[*]'' COLUMNS(
		SubjectAreaName VARCHAR(255) PATH "$.""upd_key"".""SubjectAreaName""" ERROR ON EMPTY, 
		newSubjectAreaName VARCHAR(255) PATH "$.""upd_val"".""SubjectAreaName""" NULL ON EMPTY, 
		SubjectAreaDesc VARCHAR(255) PATH "$.""upd_val"".""SubjectAreaDesc""" NULL ON EMPTY
		)) as j
	) as t 
	on s.SubjectAreaName = t.SubjectAreaName
	set
		s.SubjectAreaName = case when t.newSubjectAreaName = ''NULL'' then NULL else coalesce(t.newSubjectAreaName, s.SubjectAreaName) end,
		s.SubjectAreaDesc = case when t.SubjectAreaDesc = ''NULL'' then NULL else coalesce(t.SubjectAreaDesc, s.SubjectAreaDesc) end');
		
	prepare update_stmt from @update_stmt_txt;
	execute update_stmt;
    select cast(row_count() as char) as return_val;
	-- deallocate prepare update_stmt;
	insert into ABC_METADATA_CHANGE_LOG values('ABC_SUBJECT_AREA_MST','update_subjectarea_from_json','UPDATE',json_txt,src_typ,current_timestamp());
	commit;

end //

delimiter ;


-- MySQL DELETE SP : ABC_SUBJECT_AREA_MST --

delimiter //
create procedure delete_subjectarea_from_json(in json_txt blob, in src_typ varchar(10))
begin 

	declare delete_stmt blob;

	declare exit handler for sqlexception
    begin
		GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @errno = MYSQL_ERRNO, @text = MESSAGE_TEXT;
		SET @full_error = CONCAT("ERROR ", @errno, " (", @sqlstate, "): ", @text);
		 SELECT @full_error as return_val;
    end;

	set @delete_stmt_txt = concat('delete from ABC_SUBJECT_AREA_MST where SubjectAreaName in 
	(select distinct SubjectAreaName from json_table(''', json_txt, ''', ''$[*]'' COLUMNS(
      SubjectAreaName VARCHAR(255) PATH "$.""SubjectAreaName""" ERROR ON EMPTY)) j)');
		
	prepare delete_stmt from @delete_stmt_txt;
	execute delete_stmt;
    select cast(row_count() as char) as return_val;
	-- deallocate prepare delete_stmt;
	insert into ABC_METADATA_CHANGE_LOG values('ABC_SUBJECT_AREA_MST','delete_subjectarea_from_json','DELETE',json_txt,src_typ,current_timestamp());
	commit;

end //

delimiter ;