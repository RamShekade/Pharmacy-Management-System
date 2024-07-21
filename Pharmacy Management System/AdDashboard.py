import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

class AdDashboard(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Admin Dashboard")
        self.geometry("800x600")

        self.label_title = ttk.Label(self, text="Admin Dashboard", font=("Segoe UI", 30))
        self.label_title.pack(pady=20)

        self.btn_admin_employee = ttk.Button(self, text="Admin & Employee", command=self.show_admin_employee, style='TButton')
        self.btn_admin_employee.pack(pady=10)

        self.btn_supplier = ttk.Button(self, text="Supplier Details", command=self.show_supplier, style='TButton')
        self.btn_supplier.pack(pady=10)

        self.btn_stock_purchased = ttk.Button(self, text="Stock Purchased", command=self.show_stock_purchased, style='TButton')
        self.btn_stock_purchased.pack(pady=10)

        self.btn_inventory = ttk.Button(self, text="Inventory", command=self.show_inventory, style='TButton')
        self.btn_inventory.pack(pady=10)

        self.btn_view_bills = ttk.Button(self, text="View Bills", command=self.show_view_bills, style='TButton')
        self.btn_view_bills.pack(pady=10)

        self.btn_logout = ttk.Button(self, text="Log Out", command=self.log_out, style='TButton')
        self.btn_logout.pack(pady=10)

        self.treeview = ttk.Treeview(self, columns=('Medicine ID', 'Medicine Name', 'Date of Expiry', 'Quantity'), show='headings', height=15)
        self.treeview.heading('Medicine ID', text='Medicine ID')
        self.treeview.heading('Medicine Name', text='Medicine Name')
        self.treeview.heading('Date of Expiry', text='Date of Expiry')
        self.treeview.heading('Quantity', text='Quantity')
        self.treeview.pack(pady=20)

        self.label_expiration_alerts = ttk.Label(self, text="Expiration Alerts", font=("Segoe UI", 18))
        self.label_expiration_alerts.pack(pady=10)

        self.load_data()

    def load_data(self):
        # Replace this with your data retrieval logic
        data = [
            (1, 'Medicine1', '2022-05-01', 20),
            (2, 'Medicine2', '2022-06-15', 15),
            # Add more rows as needed
        ]

        for row in data:
            self.treeview.insert('', tk.END, values=row)

    def show_admin_employee(self):
        # Implement your logic to show the Admin & Employee page
        print("Showing Admin & Employee")

    def show_supplier(self):
        # Implement your logic to show the Supplier Details page
        print("Showing Supplier Details")

    def show_stock_purchased(self):
        # Implement your logic to show the Stock Purchased page
        print("Showing Stock Purchased")

    def show_inventory(self):
        # Implement your logic to show the Inventory page
        print("Showing Inventory")

    def show_view_bills(self):
        # Implement your logic to show the View Bills page
        print("Showing View Bills")

    def log_out(self):
        # Implement your logic for logging out
        print("Logging Out")

if __name__ == "__main__":
    ad_dashboard = AdDashboard()
    ad_dashboard.mainloop()
