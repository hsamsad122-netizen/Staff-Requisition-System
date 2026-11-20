# Staff Requisition System GUI
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from requisition import Requisition


# Create the GUI window
class RequisitionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Staff Requisition System")
        self.root.geometry("1050x700")
        self.root.minsize(850, 600)
        self.current_items = []

        # Display the main heading
        title = tk.Label(root, text="STAFF REQUISITION SYSTEM",
                         font=("Arial", 20, "bold"), bg="#234a68",
                         fg="white", pady=15)
        title.pack(fill="x")

        # Enter staff information
        form = ttk.LabelFrame(root, text="Staff Details", padding=12)
        form.pack(fill="x", padx=15, pady=10)
        ttk.Label(form, text="Date (DD/MM/YYYY):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(form, width=18)
        self.date_entry.grid(row=0, column=1, padx=5)
        self.date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        ttk.Label(form, text="Staff ID:").grid(row=0, column=2, padx=5)
        self.staff_id_entry = ttk.Entry(form, width=18)
        self.staff_id_entry.grid(row=0, column=3, padx=5)
        ttk.Label(form, text="Staff Name:").grid(row=0, column=4, padx=5)
        self.staff_name_entry = ttk.Entry(form, width=20)
        self.staff_name_entry.grid(row=0, column=5, padx=5)

        # Add items to the requisition
        item_frame = ttk.LabelFrame(root, text="Requisition Items", padding=12)
        item_frame.pack(fill="x", padx=15, pady=5)
        ttk.Label(item_frame, text="Item Name:").grid(row=0, column=0, padx=5)
        self.item_entry = ttk.Entry(item_frame, width=25)
        self.item_entry.grid(row=0, column=1, padx=5)
        ttk.Label(item_frame, text="Price ($):").grid(row=0, column=2, padx=5)
        self.price_entry = ttk.Entry(item_frame, width=15)
        self.price_entry.grid(row=0, column=3, padx=5)
        ttk.Button(item_frame, text="Add Item", command=self.add_item).grid(
            row=0, column=4, padx=10)
        self.item_list = tk.Listbox(item_frame, height=4)
        self.item_list.grid(row=1, column=0, columnspan=5,
                            sticky="ew", padx=5, pady=10)

        # Submit the requisition
        ttk.Button(item_frame, text="Submit Requisition",
                   command=self.submit_requisition).grid(
                       row=2, column=0, columnspan=5, pady=5)

        # Display requisitions in the table
        table_frame = ttk.LabelFrame(root, text="Submitted Requisitions", padding=10)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)
        columns = ("id", "date", "staff_id", "name", "total", "status", "reference")
        self.table = ttk.Treeview(table_frame, columns=columns,
                                  show="headings", height=8)
        headings = {
            "id": "Requisition ID", "date": "Date", "staff_id": "Staff ID",
            "name": "Staff Name", "total": "Total", "status": "Status",
            "reference": "Approval Reference",
        }
        for column in columns:
            self.table.heading(column, text=headings[column])
            self.table.column(column, width=125, anchor="center")
        self.table.pack(fill="both", expand=True)

        # Manager approval and rejection buttons
        manager_frame = ttk.Frame(root, padding=10)
        manager_frame.pack()
        ttk.Button(manager_frame, text="Approve Selected",
                   command=lambda: self.manager_response("Approved")).grid(
                       row=0, column=0, padx=10)
        ttk.Button(manager_frame, text="Reject Selected",
                   command=lambda: self.manager_response("Not approved")).grid(
                       row=0, column=1, padx=10)
        ttk.Button(manager_frame, text="Show Statistics",
                   command=self.show_statistics).grid(row=0, column=2, padx=10)

        # Show the statistics at the bottom
        self.stats_label = ttk.Label(
            root,
            text="Submitted: 0    Approved: 0    Pending: 0    Not Approved: 0",
            font=("Arial", 11, "bold"),
        )
        self.stats_label.pack(pady=10)

    # Add an item to the list
    def add_item(self):
        name = self.item_entry.get().strip()
        try:
            price = float(self.price_entry.get())
            if not name:
                raise ValueError("Please enter an item name")
            if price < 0:
                raise ValueError("Price cannot be negative")
            self.current_items.append((name, price))
            self.item_list.insert(tk.END, f"{name} - ${price:.2f}")
            self.item_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
        except ValueError as error:
            messagebox.showerror("Input Error", str(error))

    # Submit a new requisition
    def submit_requisition(self):
        if not self.current_items:
            messagebox.showwarning("Missing Items", "Please add at least one item")
            return
        try:
            requisition = Requisition(
                self.date_entry.get(),
                self.staff_id_entry.get(),
                self.staff_name_entry.get(),
            )
            requisition.add_requisition(self.current_items)
            self.current_items = []
            self.item_list.delete(0, tk.END)
            self.staff_id_entry.delete(0, tk.END)
            self.staff_name_entry.delete(0, tk.END)
            self.refresh_table()
            messagebox.showinfo(
                "Success", f"Requisition {requisition.requisition_id} submitted successfully!"
            )
        except ValueError as error:
            messagebox.showerror("Input Error", str(error))

    # Update the requisition table and statistics
    def refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)
        for requisition in Requisition.all_requisitions:
            self.table.insert(
                "", tk.END, iid=str(requisition.requisition_id),
                values=(
                    requisition.requisition_id, requisition.date,
                    requisition.staff_id, requisition.staff_name,
                    f"${requisition.total:.2f}", requisition.status,
                    requisition.approval_reference,
                ),
            )
        stats = self.get_statistics()
        self.stats_label.config(
            text=(f"Submitted: {stats['submitted']}    "
                  f"Approved: {stats['approved']}    "
                  f"Pending: {stats['pending']}    "
                  f"Not Approved: {stats['not_approved']}")
        )

    # Count the current statuses
    def get_statistics(self):
        requests = Requisition.all_requisitions
        return {
            "submitted": len(requests),
            "approved": sum(r.status == "Approved" for r in requests),
            "pending": sum(r.status == "Pending" for r in requests),
            "not_approved": sum(r.status == "Not approved" for r in requests),
        }

    # Update the approval status
    def manager_response(self, decision):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning(
                "Select Requisition", "Please select a requisition from the table"
            )
            return
        selected_id = int(selected[0])
        for requisition in Requisition.all_requisitions:
            if requisition.requisition_id == selected_id:
                if requisition.respond_requisition(decision):
                    self.refresh_table()
                    messagebox.showinfo("Updated", f"Requisition {selected_id}: {decision}")
                else:
                    messagebox.showwarning(
                        "Not Allowed", "Only pending requisitions can be changed"
                    )
                return

    # Show the requisition statistics
    def show_statistics(self):
        stats = self.get_statistics()
        messagebox.showinfo(
            "Requisition Statistics",
            f"Total Submitted: {stats['submitted']}\n"
            f"Approved: {stats['approved']}\n"
            f"Pending: {stats['pending']}\n"
            f"Not Approved: {stats['not_approved']}",
        )


# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = RequisitionGUI(root)
    root.mainloop()
