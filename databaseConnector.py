import pyodbc


server = 'DESKTOP-E0L486P'
database = 'master'

connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_connection=yes;Encrypt=no'

with pyodbc.connect(connectionString) as conn:
    cursor = conn.cursor()
    cursor.execute()
    row = cursor.fetchone()
    print(row[0])

