# product ID for URL 
exisitingProductId = 11
exisitingProductIdPayload = '{id": 11}'
unknownProductId = 100000000000000000000
unknownProductIdPayload = '{id": 100000000000000000000}'

#product creation
newProduct = {"name": "TSHIRT","description": "Product description","price": 10}
product_name = "TSHIRT"
product_description = "Product description"
product_price = 10

#product update
updated_product = {"name": "TSHIRTS","description": "New description","price": 15}
updated_product_id = 10
updated_product_name = "TSHIRTS"
updated_product_description = "New description"
updated_product_price = 15


#product creation list with different errors
product_error_list1 = '{"name":  1,"description": "product name integer","price":  1}' 
product_error_list2 = '{"name":  "ERRORDESC" , "description": 1, "price":  1}'
product_error_list3 = '{"name":  "ERRORPRICE", "description": "price char", "price":  "PRICE"}'
product_error_list4 = '{"name":  "aaaa", "description": "product name not uppecase", "price":  1}'
product_error_list5 = '{"name":  "1111", "description": "product name contains number", "price":  1}'

# order ID for URL 
exisitingOrderId = 10000
exisitingPOrderIdPayload = '{id": 10000}'
unknownOrderId = 100000000000000000000
unknownOrderIdPayload = '{id": 100000000000000000000}'

#order creation
newOrder = {"name": "John Doe","items": [{"productId": 111,"quantity": 1}]}
expectedNewOrderCReatedItem = {"items": [{"name": "TSHIRT","quantity": 1}]}
order_name = "John Doe"
item_productId = 11
item_quantity = 1

#order creation list with different errors
order_error_list1 = '{"name": "John Doe","items": [{"productId": 100000000,"quantity": 1}]}'  # product not in database
order_error_list2 = '{"name": "John Doe","items": [{"productId": ABC,"quantity": 1}]}' # product id not an integer
order_error_list3 = '{"name": "John Doe","items": [{"productId": 111,"quantity": A}]}' # quantity not an integer
