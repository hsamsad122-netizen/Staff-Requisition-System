"""A simple system for staff to submit requisitions."""
from datetime import datetime


# This class keeps the details for each staff request.
class Requisition:
    # Start the requisition numbers from 10001.
    next_id = 10001
    all_requisitions = []

    # Save the staff details when a new request is created.
    def __init__(self, date, staff_id, staff_name):
        # Check that the date is written in the correct format.
        datetime.strptime(date, "%d/%m/%Y")
        if not staff_id.strip() or not staff_name.strip():
            raise ValueError("Staff ID and staff name cannot be empty")
        self.date = date
        self.staff_id = staff_id.strip()
        self.staff_name = staff_name.strip()
        # Give each request its own ID number.
        self.requisition_id = Requisition.next_id
        Requisition.next_id += 1
        self.items = []
        self.total = 0.0
        self.status = "Pending"
        self.approval_reference = "Not available"
        Requisition.all_requisitions.append(self)

    # Add the requested items and work out the total cost.
    def add_requisition(self, items):
        if self.items:
            raise ValueError("Items have already been submitted")
        if not items:
            raise ValueError("Please add at least one item")
        for name, price in items:
            if not str(name).strip():
                raise ValueError("Item name cannot be empty")
            price = float(price)
            if price < 0:
                raise ValueError("Price cannot be negative")
            self.items.append((name, price))
            self.total += price
        self.total = round(self.total, 2)
        # Check the total to see if the request can be approved.
        self.approve_requisition()
        return self.total

    # Requests below $500 are approved automatically.
    def approve_requisition(self):
        if self.total < 500:
            self.status = "Approved"
            self.approval_reference = self.staff_id + str(self.requisition_id)[-3:]
        else:
            self.status = "Pending"
            self.approval_reference = "Not available"

    # The manager can decide what to do with a pending request.
    def respond_requisition(self, decision):
        if self.status != "Pending" or not self.items:
            return False
        if decision == "Approved":
            self.status = "Approved"
            self.approval_reference = self.staff_id + str(self.requisition_id)[-3:]
        elif decision == "Not approved":
            self.status = "Not approved"
            self.approval_reference = "Not available"
        elif decision == "Pending":
            return True
        else:
            raise ValueError("Decision must be Approved, Not approved, or Pending")
        return True

    # Show the details of one requisition.
    def display_requisition(self):
        print("Date:", self.date)
        print("Requisition ID:", self.requisition_id)
        print("Staff ID:", self.staff_id)
        print("Staff Name:", self.staff_name)
        print(f"Total: ${self.total:.2f}")
        print("Status:", self.status)
        print("Approval Reference Number:", self.approval_reference)
        print("-" * 35)

    @classmethod
    # Show all the requisitions that have been submitted.
    def display_requisitions(cls):
        for requisition in cls.all_requisitions:
            requisition.display_requisition()

    @classmethod
    # Count how many requests are approved, pending or not approved.
    def requisition_statistics(cls):
        approved = sum(r.status == "Approved" for r in cls.all_requisitions)
        pending = sum(r.status == "Pending" for r in cls.all_requisitions)
        not_approved = sum(r.status == "Not approved" for r in cls.all_requisitions)
        results = {"submitted": len(cls.all_requisitions), "approved": approved,
                   "pending": pending, "not_approved": not_approved}
        print("Displaying the Requisition Statistics")
        print("The total number of requisitions submitted:", results["submitted"])
        print("The total number of approved requisitions:", results["approved"])
        print("The total number of pending requisitions:", results["pending"])
        print("The total number of not approved requisitions:", results["not_approved"])
        return results


# Try the program using five different staff requests.
def main():
    examples = [
        ("03/04/2024", "FN19", "John Paul", [("Mouse", 50), ("Keyboard", 80)]),
        ("05/04/2024", "FN20", "Tracy Brown", [("Monitor", 350), ("Office chair", 250)]),
        ("07/05/2024", "FN15", "Emma Wellington", [("Laptop", 1200)]),
        ("03/05/2024", "FN02", "Catlin White", [("Printer", 490)]),
        ("10/05/2024", "FN25", "David Smith", [("Desk", 500)]),
    ]
    requests = []
    for date, staff_id, staff_name, items in examples:
        request = Requisition(date, staff_id, staff_name)
        request.add_requisition(items)
        requests.append(request)
    print("\nBEFORE MANAGER RESPONSE")
    Requisition.display_requisitions()
    Requisition.requisition_statistics()
    # The manager approves one, rejects one and leaves one pending.
    requests[1].respond_requisition("Approved")
    requests[2].respond_requisition("Not approved")
    requests[4].respond_requisition("Pending")
    print("\nAFTER MANAGER RESPONSE")
    Requisition.display_requisitions()
    Requisition.requisition_statistics()


# Run the examples when this file is opened directly.
if __name__ == "__main__":
    main()
