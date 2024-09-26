python 3.12.6 (installed with pip optional feature)

packaged install with pip install

pyodbc==5.1.0				 pip install pyodbc
pytest==8.3.3				 pip install pytest
pytest-pretty==1.2.0			 pip install pytest-pretty


before running pytest, in globalConfig
- baseUrl shouldbe changed to the correct URL 
- mock should be changed to False

extract pytest_rest_api.zip in a folder
in the extracted folder run the command  
..>pytest   


23 tests should run 
