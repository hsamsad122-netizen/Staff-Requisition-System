import unittest
from requisition_system import Requisition
# These tests help me check that the requisition system works.
class RequisitionTests(unittest.TestCase):
    # Start fresh before each test so the results do not mix.
    def setUp(self):
        Requisition.next_id = 10001
        Requisition.all_requisitions = []

    # A request below $500 should be approved straight away.
    def test_below_500_auto_approved(self):
        r = Requisition('03/04/2024', 'FN19', 'John Paul')
        self.assertEqual(r.add_requisition([('Mouse', 100), ('Keyboard', 50)]), 150)
        self.assertEqual(r.status, 'Approved')
        self.assertEqual(r.approval_reference, 'FN19001')

    # A request of exactly $500 should wait for the manager.
    def test_500_is_pending(self):
        r = Requisition('03/04/2024', 'FN20', 'Tracy Brown')
        r.add_requisition([('Desk', 500)])
        self.assertEqual(r.status, 'Pending')

    # Check the manager decisions and the final numbers.
    def test_manager_response_and_statistics(self):
        a = Requisition('03/04/2024', 'FN19', 'John Paul')
        a.add_requisition([('Laptop', 900)])
        b = Requisition('03/04/2024', 'FN20', 'Tracy Brown')
        b.add_requisition([('Desk', 600)])
        a.respond_requisition('Approved')
        b.respond_requisition('Not approved')
        stats = Requisition.requisition_statistics()
        self.assertEqual(stats, {'submitted': 2, 'approved': 1, 'pending': 0, 'not_approved': 1})

    # The program should not accept a negative item price.
    def test_negative_price_rejected(self):
        r = Requisition('03/04/2024', 'FN19', 'John Paul')
        with self.assertRaises(ValueError):
            r.add_requisition([('Bad item', -5)])

    # An approved request should not be changed by the manager.
    def test_cannot_change_approved(self):
        r = Requisition('03/04/2024', 'FN19', 'John Paul')
        r.add_requisition([('Mouse', 50)])
        self.assertFalse(r.respond_requisition('Not approved'))
        self.assertEqual(r.status, 'Approved')

if __name__ == '__main__':
    unittest.main()
