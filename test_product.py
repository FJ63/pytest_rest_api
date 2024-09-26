import pytest
import requests
import globalConfig
import UrlParameters
import dbQuery
import json

def test_get_products():
# from globalconfig import Url
    if globalConfig.mock == True:
        response = requests.get(globalConfig.mockUrlAllProducts)
    else:
        response = requests.get(globalConfig.baseUrl+"/products")
# Verify status code
    assert response.status_code == 200 

# Verify content-type
    assert response.headers["Content-Type"] == "application/json; charset=UTF-8"

# Verify response structure (Assuming a product object with 'id', 'name', 'description' and 'price')
    data = response.json()  
    assert "id" in data[0]
    assert "name" in data[0]
    assert "description" in data[0]
    assert "price" in data[0]

# Verify number of products in database is the same as number of products returned
    SQLResult = dbQuery.queryExecutorSingleRow('SELECT COUNT(ID) as count from products')
    assert len(data) == SQLResult.count

# Verify response values against database for first element returned
    SQLResult = dbQuery.queryExecutor('SELECT TOP 1 id,name,description,price from products')
    for row in SQLResult:
        assert data[0]["id"] == row.id  
        assert data[0]["name"] == row.name 
        assert data[0]["description"] == row.description
        assert data[0]["price"] == row.price

####################################################################################
def test_get_productById():
# from globalconfig import Url 
# use productid as parameter in the construction of your url

    if globalConfig.mock == True:
        response = requests.get(globalConfig.mockUrlProductById)
    else:
        payload = UrlParameters.exisitingProductIdPayload
        response = requests.get(globalConfig.baseUrl+"/product/{id}", params= payload)
# Verify status code
    assert response.status_code == 200 

# Verify content-type
    assert response.headers["Content-Type"] == "application/json; charset=UTF-8"

# Verify response structure (Assuming a product object with 'id', 'name', 'description' and 'price')
    data = response.json()  
    assert "id" in data
    assert "name" in data
    assert "description" in data
    assert "price" in data

# Verify response values against database
    SQLResult = dbQuery.queryExecutor('SELECT id,name,description,price from products where id = ' +  str(UrlParameters.exisitingProductId))
    for row in SQLResult:
        assert data["id"] == row.id  
        assert data["name"] == row.name 
        assert data["description"] == row.description
        assert data["price"] == row.price


####################################################################################
def test_get_productByIdNotFound():
# from globalconfig import Url 
    if globalConfig.mock == True:
        response = requests.get(globalConfig.mockUrlProductByIdNotFound)
    else:
        payload = UrlParameters.unknownProductIdPayload
        response = requests.get(globalConfig.baseUrl+"/product/{id}", params= payload)
# Verify status code
    assert response.status_code == 404 

# Verify content-type
    assert response.headers["Content-Type"] == "application/json; charset=UTF-8"

# Verify response structure (message)
    data = response.json()  
    assert "message" in data

# Verify response message (Assuming an error with message "ID not found")
    data = response.json()  
    assert data["message"]  == 'ID not found'


####################################################################################
def test_post_product():
# from globalconfig import Url 
# use product info as parameter in the construction of your url
    
    json_object= json.dumps(UrlParameters.newProduct)
    if globalConfig.mock == True:
        response = requests.post(globalConfig.mockUrlCreateProduct)
    else:

        response = requests.post(globalConfig.baseUrl + "/product", data=json_object)

# Verify status code
    assert response.status_code == 201 

# Verify content-type
    assert response.headers["Content-Type"] == "application/json; charset=UTF-8"

# Verify response structure (Assuming a product object with 'id', 'name', 'description' and 'price')
    data = response.json()  
    assert "id" in data
    assert "name" in data
    assert "description" in data
    assert "price" in data

    productId = data["id"]

# Verify response values against the json passed
    assert data["name"] == UrlParameters.newProduct["name"]
    assert data["description"] == UrlParameters.newProduct["description"]
    assert data["price"] == UrlParameters.newProduct["price"]

# Verify response values against the database -> new product is inserted in database
    SQLResult = dbQuery.queryExecutor('SELECT id,name,description,price from products where id = ' +  str(data["id"]))
    for row in SQLResult:
        assert data["id"] == row.id  
        assert data["name"] == row.name 
        assert data["description"] == row.description
        assert data["price"] == row.price



####################################################################################
# The test will run with each of the parameters for the value json_data        
@pytest.mark.parametrize("json_data", [UrlParameters.product_error_list1, UrlParameters.product_error_list2, UrlParameters.product_error_list3,
                                       UrlParameters.product_error_list4, UrlParameters.product_error_list5])
def test_post_product_with_error(json_data):
# from globalconfig import Url 
# use product info as parameter in the construction of your url

    productData=json.loads(json_data)
    productInfo = {'json_payload': productData}
    if globalConfig.mock == True:
        response = requests.post(globalConfig.mockUrlCreateProductWithError)
    else:
        response = requests.post(globalConfig.baseUrl+"/product", data=productInfo)
# Verify status code
    assert response.status_code == 422 

# Verify content-type
    assert response.headers["Content-Type"] == "application/json; charset=UTF-8"

# Verify response structure (message)
    data = response.json()  
    assert "message" in data

# Verify response message (Assuming an error with message "Invalid input")
    assert data["message"]  == 'Invalid input'


####################################################################################
def test_put_product():
# from globalconfig import Url 
# use product info as parameter in the construction of your url
    
    json_object= json.dumps(UrlParameters.updated_product)
    payload = UrlParameters.updated_product_id
    if globalConfig.mock == True:
        response = requests.put(globalConfig.mockUrlPutProduct)
    else:
        response = requests.put(globalConfig.baseUrl+"/product/{id}", params=payload, data=json_object)

# Verify status code
    assert response.status_code == 200 

# Verify content-type
    assert response.headers["Content-Type"] == "application/json; charset=UTF-8"

# Verify response structure (Assuming a product object with 'id', 'name', 'description' and 'price')
    data = response.json()  
    assert "id" in data
    assert "name" in data
    assert "description" in data
    assert "price" in data

    productId = data["id"]

# Verify response values against the json passed
    assert data["id"] == UrlParameters.updated_product_id
    assert data["name"] == UrlParameters.updated_product_name
    assert data["description"] == UrlParameters.updated_product_description
    assert data["price"] == UrlParameters.updated_product_price

# Verify response values against the database -> product is updated in database
    SQLResult = dbQuery.queryExecutor('SELECT id,name,description,price from products where id = ' +  str(data["id"]))
    for row in SQLResult:
        assert data["id"] == row.id  
        assert data["name"] == row.name 
        assert data["description"] == row.description
        assert data["price"] == row.price


####################################################################################
def test_put_productByIdNotFound():
# from globalconfig import Url 
    if globalConfig.mock == True:
        response = requests.put(globalConfig.mockUrlProductByIdNotFound)
    else:
        json_object= json.dumps(UrlParameters.updated_product)
        payload = UrlParameters.unknownProductIdPayload
        response = requests.put(globalConfig.baseUrl+"/product/{id}", params= payload, data = json_object)
# Verify status code
    assert response.status_code == 404 

# Verify content-type
    assert response.headers["Content-Type"] == "application/json; charset=UTF-8"

# Verify response structure (message)
    data = response.json()  
    assert "message" in data

# Verify response message (Assuming an error with message "ID not found")
    data = response.json()  
    assert data["message"]  == 'ID not found'



####################################################################################
# The test will run with each of the parameters for the value json_data        
@pytest.mark.parametrize("json_data", [UrlParameters.product_error_list1, UrlParameters.product_error_list2, UrlParameters.product_error_list3,
                                       UrlParameters.product_error_list4, UrlParameters.product_error_list5])
def test_put_product_with_error(json_data):
# from globalconfig import Url 
# use product info as parameter in the construction of your url

    productData=json.loads(json_data)
    productInfo = {'json_payload': productData}
    payload = UrlParameters.exisitingProductIdPayload
    if globalConfig.mock == True:
        response = requests.post(globalConfig.mockUrlCreateProductWithError)
    else:
        response = requests.post(globalConfig.baseUr+"/product/{id}", params=payload, data=productInfo)
# Verify status code
    assert response.status_code == 422 

# Verify content-type
    assert response.headers["Content-Type"] == "application/json; charset=UTF-8"

# Verify response structure (message)
    data = response.json()  
    assert "message" in data

# Verify response message (Assuming an error with message "Invalid input")
    assert data["message"]  == 'Invalid input'


