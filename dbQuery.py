import globalConfig
import pyodbc

def queryExecutor(query):
    with pyodbc.connect(globalConfig.connectionString) as conn:
        cursor = conn.cursor()
        rows = cursor.execute(query).fetchall()
        return rows


def queryExecutorSingleRow(query):    #used for counts
    with pyodbc.connect(globalConfig.connectionString) as conn:
        cursor = conn.cursor()
        row = cursor.execute(query).fetchone()
        return row    


