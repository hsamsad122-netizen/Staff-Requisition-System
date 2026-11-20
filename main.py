# Run five example requisitions in the terminal
from requisition import Requisition


def main():
    # Keep the original example staff details and prices
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

    # Show results before the manager responds
    print("\nBEFORE MANAGER RESPONSE")
    Requisition.display_requisitions()
    Requisition.requisition_statistics()

    # Manager decisions for pending requisitions
    requests[1].respond_requisition("Approved")
    requests[2].respond_requisition("Not approved")
    requests[4].respond_requisition("Pending")

    # Show results after the manager responds
    print("\nAFTER MANAGER RESPONSE")
    Requisition.display_requisitions()
    Requisition.requisition_statistics()


if __name__ == "__main__":
    main()
