from suds.client import Client

def get_api_products():
    return [
        {'sku': n2610, 'cart_prod_id': 16, 'name': 'Nokia 2610 Phone', 'qty': 996.0000}, 
        {'sku': bb8100, 'cart_prod_id': 17, 'name': 'BlackBerry 8100 Pearl', 'qty': 797.0000}, 
        {'sku': sw810i, 'cart_prod_id': 18, 'name': 'Sony Ericsson W810i', 'qty': 989.0000}
    ]

def update_inventory(products, session, client):
    for p in products:
        client.service.catalogInventoryStockItemUpdate(session, p['product_id'], {'qty': p['qty']})

if __name__ == '__main__':
    store_url = 'https://ordorodemo.gostorego.com/api/v2_soap?wsdl=1'
    username = 'api_user'
    api_key = '111111'
    client = Client(store_url)
    session = client.service.login(username, api_key)
    update_inventory([{'product_id':16, 'qty':995}], session, client)
