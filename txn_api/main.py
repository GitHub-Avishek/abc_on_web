from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

def get_mysql_conn():
    conn = mysql.connector.connect(
        #host     = "127.0.0.1",
        #port     = 3360,
        host     = "db_host",
        port     = "3306",
        user     = "app_devlpr",
        passwd   = "D3v1p%P$wd",
        database = "abc_frmwrk_db",
    )
    return conn


app = FastAPI()


class AddJobRunLog(BaseModel):
    JobName: str

class ModJobRunLog(BaseModel):
    JobRunID: str
    JobStatus: str

class AddJobRunErrorLog(BaseModel):
    JobRunID: str
    ErrorText: str
    ErrorDetails: str


@app.get("/test")
def test_function():
    return{"Hello":"World"}


# x = requests.post(url='http://127.0.0.1:8000/jobs/runlog/add', json={"JobName":"ETLJOB1"})
@app.post("/jobs/runlog/add")
def add_job_run(req: AddJobRunLog):
    cnx = get_mysql_conn()
    cur = cnx.cursor()
    cur.execute("""call insert_job_run_log('{"JobName":"P1"}')""".replace('P1',req.JobName))
    result = cur.fetchall()
    cnx.close()
    return {"result":None if result[0][0].lower().startswith('error') else result[0][0]}


# x = requests.put(url='http://127.0.0.1:8000/jobs/runlog/update', json={"JobRunID":"16422528700111","JobStatus":"S"})
@app.put("/jobs/runlog/update")
def upd_job_run(req: ModJobRunLog):
    cnx = get_mysql_conn()
    cur = cnx.cursor()
    cur.execute("""call update_job_run_log('{"JobRunID":"P1","JobStatus":"P2"}')""".replace('P1',req.JobRunID).replace('P2',req.JobStatus))
    cnx.close()

# x = requests.post(url='http://127.0.0.1:8000/jobs/errorlog/add', json={"JobRunID":"16422528700111","ErrorText":"error","ErrorDetails":"Test Error Message"})
@app.post("/jobs/errorlog/add")
def add_job_error(req: AddJobRunErrorLog):
    cnx = get_mysql_conn()
    cur = cnx.cursor()
    cur.execute("""call insert_job_run_error_log('{"JobRunID":"P1","ErrorText":"P2","ErrorDetails":"P3"}')""".replace('P1',req.JobRunID).replace('P2',req.ErrorText).replace('P3',req.ErrorDetails))
    cnx.close()
