
from datetime import datetime
from math import isfinite

# Staff Requisition System

class Requisition:
    next_id = 10001
    all_requests = []
 
    def __init__(self, date, staff_id, staff_name):
        self.date = date
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.requisition_id = Requisition.next_id
        Requisition.next_id += 1

        self.items = []
        self.total = 0
        self.status = "Pending"
        self.approval_reference = "Not available"

        Requisition.all_requests.append(self)

    # Add items and calculate the total
    def add_requisition(self, items):
        self.items = items
        self.total = 0

        for item, price in items:
            self.total += float(price)

        self.total = round(self.total, 2)
        self.approve_requisition()
        return self.total

    # Return the total amount
    def requisitions_details(self):
        return self.total

    # Automatically approve requests below $500
    def approve_requisition(self):
        if self.requisitions_details() < 500:
            self.status = "Approved"
            self.approval_reference = (
                self.staff_id + str(self.requisition_id)[-3:]
            )
        else:
            self.status = "Pending"
            self.approval_reference = "Not available"

    # Manager responds to pending requests
    def respond_requisition(self, decision):
        if self.status != "Pending":
            print("This request is already processed.")
            return

        if decision == "yes":
            self.status = "Approved"
            self.approval_reference = (
                self.staff_id + str(self.requisition_id)[-3:]
            )

        elif decision == "no":
            self.status = "Not approved"
            self.approval_reference = "Not available"

        elif decision == "pending":
            self.status = "Pending"
            self.approval_reference = "Not available"

        else:
            print("Invalid decision.")

    # Display one requisition
    def display_requisition(self):
        print("\n-----------------------------")
        print("Date:", self.date)
        print("Requisition ID:", self.requisition_id)
        print("Staff IDD:", self.staff_id)
        print("Staff Name:", self.staff_name)
        print(f"Total: ${self.total:.2f}")
        print("Status:", self.status)
        print("Approval Reference Number:", self.approval_reference)

    # Display all requisitions
    @classmethod
    def display_requisitions(cls):
        if not cls.all_requests:
            print("No requisitions have been submitted.")
            return

        for request in cls.all_requests:
            request.display_requisition()

    # Display and return statistics
    @classmethod
    def requisition_statistics(cls):
        approved = 0
        pending = 0
        rejected = 0

        for request in cls.all_requests:
            if request.status == "Approved":
                approved += 1

            elif request.status == "Pending":
                pending += 1

            elif request.status == "Not approved":
                rejected += 1

        print("\n--- Requisition Statistics ---")
        print("Submitted:", len(cls.all_requests))
        print("Approved:", approved)
        print("Pending:", pending)
        print("Not approved:", rejected)

        return {
            "submitted": len(cls.all_requests),
            "approved": approved,
            "pending": pending,
            "not_approved": rejected
        }


# Enter staff details and requested items
def submit_request():
    date = input("Enter date (DD/MM/YYYY): ").strip()

    try:
        datetime.strptime(date, "%d/%m/%Y")

    except ValueError:
        print("Please enter a valid date.")
        return

    staff_id = input("Enter staff ID: ").strip()
    staff_name = input("Enter staff name: ").strip()

    if not staff_id or not staff_name:
        print("Staff ID and name cannot be empty.")
        return

    items = []

    while True:
        item_name = input("Enter item name: ").strip()

        if not item_name:
            print("Item name cannot be empty.")
            continue

        try:
            price = float(input("Enter item price: $"))

        except ValueError:
            print("Please enter a valid price.")
            continue

        if not isfinite(price) or price <= 0:
            print("Price must be a valid number greater than zero.")
            continue

        items.append((item_name, price))

        while True:
            answer = input(
                "Add another item? (yes/no): "
            ).strip().lower()

            if answer in ["yes", "no"]:
                break

            print("Please enter yes or no.")

        if answer == "no":
            break

    request = Requisition(date, staff_id, staff_name)
    request.add_requisition(items)

    print("\nRequisition submitted successfully!")
    request.display_requisition()


# Manager responds to pending requests
def manager_decision():
    pending_requests = []

    for request in Requisition.all_requests:
        if request.status == "Pending":
            pending_requests.append(request)

    if not pending_requests:
        print("There are no pending requests.")
        return

    for request in pending_requests:
        request.display_requisition()

        while True:
            answer = input(
                "Approve this request? (yes/no/pending): "
            ).strip().lower()

            if answer in ["yes", "no", "pending"]:
                request.respond_requisition(answer)
                break

            print("Please enter yes, no or pending.")

        print("Updated Status:", request.status)


# Test the program using five staff requisitions
def test_five_requisitions():

    # Save existing requests before testing
    original_requests = Requisition.all_requests
    original_next_id = Requisition.next_id

    # Create separate data for testing
    Requisition.all_requests = []
    Requisition.next_id = 10001

    try:
        examples = [
            ("03/04/2024", "FN19", "John Paul",
             [("Mouse", 50), ("Keyboard", 80)]),

            ("05/04/2024", "FN20", "Tracy Brown",
             [("Monitor", 350), ("Office chair", 250)]),

            ("07/05/2024", "FN15", "Emma Wellington",
             [("Laptop", 1200)]),

            ("03/05/2024", "FN02", "Catlin White",
             [("Printer", 490)]),

            ("10/05/2024", "FN25", "David Smith",
             [("Desk", 500)])
        ]

        requests = []

        # Create all five requisitions
        for date, staff_id, staff_name, items in examples:
            request = Requisition(date, staff_id, staff_name)
            request.add_requisition(items)
            requests.append(request)

        # Display details before manager decisions
        print("\n===== BEFORE MANAGER RESPONSE =====")
        Requisition.display_requisitions()
        Requisition.requisition_statistics()

        # Manager approves Tracy and rejects Emma
        # David's request remains pending
        requests[1].respond_requisition("yes")
        requests[2].respond_requisition("no")
        requests[4].respond_requisition("pending")

        # Display details after manager decisions
        print("\n===== AFTER MANAGER RESPONSE =====")
        Requisition.display_requisitions()
        Requisition.requisition_statistics()

    finally:
        # Restore existing requests after testing
        Requisition.all_requests = original_requests
        Requisition.next_id = original_next_id


# Main menu
def main():
    while True:
        print("\n===== STAFF REQUISITION SYSTEM =====")
        print("1. Submit Requisition")
        print("2. Manager Response")
        print("3. Display All Requisitions")
        print("4. Display Statistics")
        print("5. Run Five Example Requisitions")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            submit_request()

        elif choice == "2":
            manager_decision()

        elif choice == "3":
            Requisition.display_requisitions()

        elif choice == "4":
            Requisition.requisition_statistics()

        elif choice == "5":
            test_five_requisitions()

        elif choice == "6":
            print("Thank you for using the system.")
            break

        else:
            print("Please choose a valid option.")


if __name__ == "__main__":
    main()
