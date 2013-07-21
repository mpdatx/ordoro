from suds.client import Client
from eventlet import GreenPool, monkey_patch

def get_api_products():
    """Return a sample list of products."""
    return [
        {'sku': 'n2610', 'cart_prod_id': 16, 'name': 'Nokia 2610 Phone', 'qty': 996.0000}, 
        {'sku': 'bb8100', 'cart_prod_id': 17, 'name': 'BlackBerry 8100 Pearl', 'qty': 797.0000}, 
        {'sku': 'sw810i', 'cart_prod_id': 18, 'name': 'Sony Ericsson W810i', 'qty': 989.0000}
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

def update_inventory(store_id, products, async=False, max_connections=15, retry=True):
    """Update inventory for a list of products for the given magento store.

    Keyword arguments:
    store_id -- The store_id passed to connect_magento_store
    products -- A list of product dicts, each of whic must contain an entry for cart_prod_id and qty
    async -- If True, make the API calls concurrently with eventlet
    max_connections -- If calling asynchronously, the max number of concurrent connections
    retry -- Should we retry failed async calls?  These often fail due to SQL deadlocks caused by calling
        the Magento api concurrently.  Retrying the failed calls lets us make every update properly and
        still gain the massive speedup from doing it concurrently.  Code that makes use of this functionality
        should keep an eye on the retry_count (3rd return) as some stores may be too slow to handle even 2
        concurrent connections. 
    """
    client, session = connect_magento_store(store_id)
    products_updated = []
    products_errored = []

    def api_call(product_id, qty):
        try:
            return client.service.catalogInventoryStockItemUpdate(session, product_id, {'qty':qty})
        except:
            return 0

    def callback(thread, id):
        result = thread.wait()
        if result:
            products_updated.append(id)
        else:
            products_errored.append(id)

    if async:
        pool = GreenPool(max_connections)
        monkey_patch()

    for p in products:
        if async:
            pool.spawn(api_call, p['cart_prod_id'], p['qty']).link(callback, p['cart_prod_id'])
        else:
            if api_call(p['cart_prod_id'], p['qty']) == 1:
                products_updated.append(p['cart_prod_id'])
            else:
                products_errored.append(p['cart_prod_id'])

    if async:
        pool.waitall()

    retry_count = 0
    if async and retry and len(products_errored) > 0:
        while (len(products_errored) > 0) and (retry_count < len(products)*2): # @todo tweak the retry count
            for p in products:
                if p['cart_prod_id'] in products_errored:
                    products_errored.pop( products_errored.index(p['cart_prod_id']))
                    retry_count += 1
                    pool.spawn(api_call, p['cart_prod_id'], p['qty']).link(callback, p['cart_prod_id'])
            pool.waitall()

    return products_updated, products_errored, retry_count

if __name__ == '__main__':
    to_update = get_api_products()
    print 'Updating %d products' % (len(to_update))
    updated, errored, retries = update_inventory('demo', to_update)
    print '%s products updated, %s errors, %s retries.' % (len(updated), len(errored), retries)
