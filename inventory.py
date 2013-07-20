from suds.client import Client

def get_api_products():
    """Return a sample list of products."""
    return [
        {'sku': n2610, 'cart_prod_id': 16, 'name': 'Nokia 2610 Phone', 'qty': 996.0000}, 
        {'sku': bb8100, 'cart_prod_id': 17, 'name': 'BlackBerry 8100 Pearl', 'qty': 797.0000}, 
        {'sku': sw810i, 'cart_prod_id': 18, 'name': 'Sony Ericsson W810i', 'qty': 989.0000}
    ]

def connect_magento_store(store_id):
    """Connects and logs in to a magento store via SOAP."""
    stores = {
        'demo': {
            'url': 'https://ordorodemo.gostorego.com/api/v2_soap?wsdl=1',
            'username': 'api_user',
            'api_key': '111111'
        }
    }

    if not stores.has_key(store_id):
        raise Exception('Invalid store_id', store_id)

    store = stores[store_id]
    client = Client(store['url'])
    session = client.service.login(store['username'], store['api_key'])
    return client, session

def update_inventory(store_id, products):
    """Update inventory for a list of products for the given magento store."""
    client, session = connect_magento_store(store_id)
    products_updated = []
    products_errored = []
    for p in products:
        try:
            if client.service.catalogInventoryStockItemUpdate(session, p['product_id'], {'qty': p['qty']}) == 1:
                products_updated.append(p['product_id'])
            else:
                products_errored.append(p['product_id'])
        except:
            products_errored.append(p['product_id'])

    return products_updated, products_errored

if __name__ == '__main__':
    updated, errored = update_inventory('demo', [{'product_id':161, 'qty':995}, {'product_id':1611111, 'qty':995}])
    print '%s products updated, %s errors.' % (len(updated), len(errored))
