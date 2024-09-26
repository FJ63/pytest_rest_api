import pytest
import requests
import globalConfig
import UrlParameters
import dbQuery
import json
from datetime import datetime

def test_get_orders():
# from globalconfig import Url
    if globalConfig.mock == True:
        response = requests.get(globalConfig.mockUrlGetOrders)
    else:
        response = requests.get(globalConfig.baseUrl+"/orders")
# Verify status code
    assert response.status_code == 200 

# Verify content-type
    assert response.headers["Content-Type"] == "application/json; charset=UTF-8"

# Verify response structure (Assuming a product object with 'id', 'time', 'name', 'items', 'name' and 'quantity' in items and 'subtotal')
    data = response.json()  
    assert "id" in data[0]
    assert "time" in data[0]
    assert "name" in data[0]
    assert "items" in data[0]
    assert "name" in data[0]["items"][0]
    assert "quantity" in data[0]["items"][0]
    assert "subtotal" in data[0]

# Verify number of orders in database is the same as number of orders returned
    SQLResult = dbQuery.queryExecutorSingleRow('SELECT COUNT(ID) as count from orders')
    assert len(data) == SQLResult.count

    
###################################################################
def test_get_orderById():
# from globalconfig import Url 
# use orderid as parameter in the construction of your url

    if globalConfig.mock == True:
        response = requests.get(globalConfig.mockUrlGetOrdersById)
    else:
        payload = UrlParameters.exisitingOrderIdPayload
        response = requests.get(globalConfig.baseUrl+"/order/{id}", params= payload)
# Verify status code
    assert response.status_code == 200 

# Verify content-type
    assert response.headers["Content-Type"] == "application/json; charset=UTF-8"

# Verify response structure (Assuming an order object with 'id', 'name', 'time', 'subtotal')
    data = response.json()  
    assert "id" in data
    assert "name" in data
    assert "time" in data
    assert "items" in data
    items = data["items"]
    #check that each item as the correct structure (name and quantity)
    for item in items:
            assert "name" in item
            assert "quantity" in item
    assert "subtotal" in data


# Verify response values against database table order
    SQLResult = dbQuery.queryExecutor('SELECT id,name,created_at from orders where id = ' +  str(data["id"]))
    for row in SQLResult:
        assert data["id"] == row.id  
        assert data["name"] == row.name 

        #dates have different formats in DB and returned by the API, you need to use the same format to do the assertion
        dateFromAPI = str(datetime.fromisoformat(str(data["time"]).replace('Z', '')))
        assert dateFromAPI == str(row.created_at) 

# Verify response values against database table order_products and products
    SQLResult = dbQuery.queryExecutor('SELECT P.name as name,OP.quantity as quantity FROM order_products OP JOIN products P ON OP.product_id = p.id WHERE order_id = '
                                             +  str(data["id"]) + 'ORDER BY P.id')
    i = 0
    for row in SQLResult:
        assert data["items"][i]["name"] == row.name
        assert data["items"][i]["quantity"] == row.quantity
        i = i + 1

###################################################################
def test_get_orderByIdNotFound():
# from globalconfig import Url 
    if globalConfig.mock == True:
        response = requests.get(globalConfig.mockUrlOrderByIdNotFound)
    else:
        payload = UrlParameters.unknownOrderIdPayload
        response = requests.get(globalConfig.baseUrl+"/order/{id}", params= payload)
# Verify status code
    assert response.status_code == 404 

# Verify content-type
    assert response.headers["Content-Type"] == "application/json; charset=UTF-8"

# Verify response structure (message)
    data = response.json()  
    print (data)
    assert "message" in data

# Verify response message (Assuming an error with message "ID not found")
    assert data["message"]  == 'ID not found'


###################################################################
def test_post_order():
# from globalconfig import Url 
# use product info as parameter in the construction of your url
    
    json_object= json.dumps(UrlParameters.newOrder)
    if globalConfig.mock == True:
        response = requests.post(globalConfig.mockUrlCreateOrder)
    else:

        response = requests.post(globalConfig.baseUrl+ "/order", data=json_object)

# Verify status code
    assert response.status_code == 201 

# Verify content-type
    assert response.headers["Content-Type"] == "application/json; charset=UTF-8"

# Verify response structure (Assuming an order object with 'id', 'name', 'time', 'subtotal')
    data = response.json()  
    assert "id" in data
    assert "name" in data
    assert "time" in data
    items = data["items"]
    #check that each item as the correct structure (name and quantity)
    for item in items:
            assert "name" in item
            assert "quantity" in item
    assert "subtotal" in data

# Verify items passed are correctly returned 
    # here you need to create a function that will get the product name with product id passed  for each tuple in items,  
    # create a test json and assert this json against data["items"]
    ##
    assert data["items"] == UrlParameters.expectedNewOrderCReatedItem["items"]
    ############################################################################


# Verify response values against database table order
    SQLResult = dbQuery.queryExecutor('SELECT id,name,created_at from orders where id = ' +  str(data["id"]))
    for row in SQLResult:
        assert data["id"] == row.id  
        assert data["name"] == row.name 

        #dates have different formats in DB and returned by the API, you need to use the same format to do the assertion
        dateFromAPI = str(datetime.fromisoformat(str(data["time"]).replace('Z', '')))
        assert dateFromAPI == str(row.created_at) 

# Verify response values against database table order_products and products
    SQLResult = dbQuery.queryExecutor('SELECT P.name as name,OP.quantity as quantity FROM order_products OP JOIN products P ON OP.product_id = p.id WHERE order_id = '
                                             +  str(data["id"]) + 'ORDER BY P.id')
    i = 0
    for row in SQLResult:
        assert data["items"][i]["name"] == row.name
        assert data["items"][i]["quantity"] == row.quantity
        i = i + 1


###################################################################
# The test will run with each of the parameters for the value json_data        
@pytest.mark.parametrize("json_data", [UrlParameters.order_error_list1, UrlParameters.order_error_list2, UrlParameters.order_error_list3])
def test_post_order_with_errors(json_data):
# from globalconfig import Url 
# use product info as parameter in the construction of your url
    
    json_object= json.dumps(UrlParameters.newOrder)
    if globalConfig.mock == True:
        response = requests.post(globalConfig.mockUrlCreateOrderWithError)
    else:

        response = requests.post(globalConfig.baseUrl+ "/order", data=json_object)

# Verify status code
    assert response.status_code == 422 

# Verify content-type
    assert response.headers["Content-Type"] == "application/json; charset=UTF-8"

# Verify response structure (message)
    data = response.json()  
    print (data)
    assert "message" in data
    
# Verify response message (Assuming an error with message "Invalid input")
    assert data["message"]  == 'Invalid input'