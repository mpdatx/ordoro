"""Unit test for inventory.py"""

import inventory
import unittest

class MagentoInventoryTests(unittest.TestCase):

    def testInventoryUpdate(self):
        test_product_id = 16

        inventory_record = inventory.get_inventory('demo', [test_product_id])
        expected_quantity = float(inventory_record[0].qty) - 1
        inventory.update_inventory('demo', [{'cart_prod_id':test_product_id, 'qty':expected_quantity}])
        inventory_record = inventory.get_inventory('demo', [test_product_id])
        actual_quantity = float(inventory_record[0].qty)
        self.failUnless(expected_quantity==actual_quantity)

def main():
    unittest.main()

if __name__ == '__main__':
    main()

