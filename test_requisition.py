# Test the requisition rules
import unittest
from requisition import Requisition


class RequisitionTests(unittest.TestCase):
    def setUp(self):
        Requisition.next_id = 10001
        Requisition.all_requisitions = []

    def test_below_500_auto_approved(self):
        r = Requisition("03/04/2024", "FN19", "John Paul")
        self.assertEqual(r.add_requisition([("Mouse", 100), ("Keyboard", 50)]), 150)
        self.assertEqual(r.status, "Approved")
        self.assertEqual(r.approval_reference, "FN19001")

    def test_500_is_pending(self):
        r = Requisition("03/04/2024", "FN20", "Tracy Brown")
        r.add_requisition([("Desk", 500)])
        self.assertEqual(r.status, "Pending")

    def test_manager_response_and_statistics(self):
        a = Requisition("03/04/2024", "FN19", "John Paul")
        a.add_requisition([("Laptop", 900)])
        b = Requisition("03/04/2024", "FN20", "Tracy Brown")
        b.add_requisition([("Desk", 600)])
        a.respond_requisition("Approved")
        b.respond_requisition("Not approved")
        stats = Requisition.requisition_statistics()
        self.assertEqual(stats, {
            "submitted": 2, "approved": 1, "pending": 0, "not_approved": 1
        })

    def test_negative_price_rejected(self):
        r = Requisition("03/04/2024", "FN19", "John Paul")
        with self.assertRaises(ValueError):
            r.add_requisition([("Bad item", -5)])

    def test_cannot_change_approved(self):
        r = Requisition("03/04/2024", "FN19", "John Paul")
        r.add_requisition([("Mouse", 50)])
        self.assertFalse(r.respond_requisition("Not approved"))
        self.assertEqual(r.status, "Approved")


if __name__ == "__main__":
    unittest.main()
