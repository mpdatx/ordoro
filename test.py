"""Unit test for inventory.py"""

import inventory
import unittest
import random

class MagentoInventoryTests(unittest.TestCase):

    def testInventoryUpdate(self):
        """update_inventory should update magento inventory properly"""
        test_product_id = 16
        inventory_record = inventory.get_inventory('demo', [test_product_id])
        expected_quantity = float(inventory_record[0].qty) + 1
        inventory.update_inventory('demo', [{'cart_prod_id':test_product_id, 'qty':expected_quantity}])
        inventory_record = inventory.get_inventory('demo', [test_product_id])
        actual_quantity = float(inventory_record[0].qty)
        self.assertEqual(expected_quantity, actual_quantity)

    def testInventoryUpdateAsync(self):
        """update_inventory should update magento inventory with an async call"""
        test_product_id = 16
        inventory_record = inventory.get_inventory('demo', [test_product_id])
        expected_quantity = float(inventory_record[0].qty) + 1
        inventory.update_inventory('demo', [{'cart_prod_id':test_product_id, 'qty':expected_quantity}], async=True)
        inventory_record = inventory.get_inventory('demo', [test_product_id])
        actual_quantity = float(inventory_record[0].qty)
        self.assertEqual(expected_quantity, actual_quantity)

    def testInventoryMassUpdateAsync(self):
        """update_inventory should properly mass-update magento inventory async"""
        # these products always fail the inventory update no matter what
        failing_product_ids = [54,83,98,103,119,120,123,126,158,163,164,165]

        test_product_ids = [16, 17, 18, 19, 20, 25, 26, 27, 28, 29, 31, 32, 34, 
            35, 36, 37, 38, 39, 41, 42, 44, 45, 46, 47, 48, 51, 52, 53, 
            84, 85, 86, 87, 88, 89, 90, 91, 92, 99, 100, 101, 102, 104, 
            105, 106, 107, 109, 110, 111, 117, 118, 121, 122, 124, 125, 
            127, 128, 129, 130, 131, 132, 133, 134, 137, 138, 139, 
            140, 141, 144, 145, 148, 149, 151, 152, 153, 154, 157, 
            159, 161, 162, 166, 167]
        inventory_updates = []
        inventory_expected_values = {}
            
        for product_id in test_product_ids:
            inventory_expected_values[product_id] = random.randint(1,1000)
            inventory_updates.append({'qty': inventory_expected_values[product_id], 'cart_prod_id': product_id})
        inventory.update_inventory('demo', inventory_updates, async=True)

        inventory_list = inventory.get_inventory('demo', test_product_ids)
        for inventory_record in inventory_list:
            expected_quantity = float(inventory_expected_values[ int(inventory_record.product_id) ])
            actual_quantity = float(inventory_record.qty)
            self.assertEqual(expected_quantity, actual_quantity, 
                'Got %s for product_id %s, expected %s' % 
                (actual_quantity, inventory_record.product_id, expected_quantity))

def main():
    unittest.main()

if __name__ == '__main__':
    main()

