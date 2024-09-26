

baseUrl = "https://tv.test.io/api/v1"

mock=True

mockUrlAllProducts = "https://run.mocky.io/v3/8fd435f9-df96-4b37-994b-1ee686d0e850"
mockUrlProductById = "https://run.mocky.io/v3/0bcc0f2d-e5e7-43a4-a815-fcb48da041cf"
mockUrlProductByIdNotFound = "https://run.mocky.io/v3/67df6260-c96b-4299-bab0-e3493d930dd1"
mockUrlCreateProduct = "https://run.mocky.io/v3/9e14a025-891e-45e1-94da-089bfc79993a"
mockUrlCreateProductWithError = "https://run.mocky.io/v3/a12dedcd-572a-4059-a3cb-d8d038221ab1"
mockUrlPutProduct = "https://run.mocky.io/v3/d21e9211-2778-4317-873d-dab89336d769"
mockUrlGetOrders = "https://run.mocky.io/v3/c773d9f1-35e6-4685-a8cb-673e3a0fde58"
mockUrlGetOrdersById = "https://run.mocky.io/v3/27acedd1-ced6-448b-9384-d86a67902e03" 
mockUrlOrderByIdNotFound = "https://run.mocky.io/v3/67df6260-c96b-4299-bab0-e3493d930dd1"
mockUrlCreateOrder = "https://run.mocky.io/v3/99ee7fb8-7197-4922-9d05-e2728df04a66"
mockUrlCreateOrderWithError = "https://run.mocky.io/v3/a12dedcd-572a-4059-a3cb-d8d038221ab1"

#DB connection
server = 'DESKTOP-E0L486P'
database = 'master'

connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_connection=yes;Encrypt=no'
