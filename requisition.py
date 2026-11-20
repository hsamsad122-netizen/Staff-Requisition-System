# Staff Requisition System
from datetime import datetime


# Store staff requisition details
class Requisition:
    next_id = 10001
    all_requisitions = []

    # Store staff information
    def __init__(self, date, staff_id, staff_name):
        datetime.strptime(date, "%d/%m/%Y")
        if not staff_id.strip() or not staff_name.strip():
            raise ValueError("Staff ID and staff name cannot be empty")

        self.date = date
        self.staff_id = staff_id.strip()
        self.staff_name = staff_name.strip()

        # Generate a unique requisition ID
        self.requisition_id = Requisition.next_id
        Requisition.next_id += 1
        self.items = []
        self.total = 0.0
        self.status = "Pending"
        self.approval_reference = "Not available"
        Requisition.all_requisitions.append(self)

    # Add items and calculate the total
    def add_requisition(self, items):
        if self.items:
            raise ValueError("Items have already been submitted")
        if not items:
            raise ValueError("Please add at least one item")

        validated_items = []
        for name, price in items:
            if not str(name).strip():
                raise ValueError("Item name cannot be empty")
            price = float(price)
            if price < 0:
                raise ValueError("Price cannot be negative")
            validated_items.append((str(name).strip(), price))

        self.items = validated_items
        self.total = round(sum(price for _, price in self.items), 2)
        self.approve_requisition()
        return self.total

    # Check if the requisition is approved
    def approve_requisition(self):
        if self.total < 500:
            self.status = "Approved"
            self.approval_reference = self.staff_id + str(self.requisition_id)[-3:]
        else:
            self.status = "Pending"
            self.approval_reference = "Not available"

    # Allow the manager to approve or reject
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

    # Display one requisition
    def display_requisition(self):
        print("Date:", self.date)
        print("Requisition ID:", self.requisition_id)
        print("Staff ID:", self.staff_id)
        print("Staff Name:", self.staff_name)
        print(f"Total: ${self.total:.2f}")
        print("Status:", self.status)
        print("Approval Reference Number:", self.approval_reference)
        print("-" * 35)

    # Display all requisitions
    @classmethod
    def display_requisitions(cls):
        for requisition in cls.all_requisitions:
            requisition.display_requisition()

    # Calculate requisition statistics
    @classmethod
    def requisition_statistics(cls):
        results = {
            "submitted": len(cls.all_requisitions),
            "approved": sum(r.status == "Approved" for r in cls.all_requisitions),
            "pending": sum(r.status == "Pending" for r in cls.all_requisitions),
            "not_approved": sum(r.status == "Not approved" for r in cls.all_requisitions),
        }
        print("Displaying the Requisition Statistics")
        print("The total number of requisitions submitted:", results["submitted"])
        print("The total number of approved requisitions:", results["approved"])
        print("The total number of pending requisitions:", results["pending"])
        print("The total number of not approved requisitions:", results["not_approved"])
        return results
