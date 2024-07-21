import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector



class Cart(tk.Tk):
    def __init__(self, tempUsername=None):
        super().__init__()
        self.username = tempUsername
        self.finalTotalPrice = 0
        self.bill_id = ""
        self.initialize_components()

    def initialize_components(self):
        self.title("Cart")
        self.geometry("1000x600")

        # Search
        self.lbl_search = tk.Label(self, text="Search")
        self.lbl_search.grid(row=0, column=0, padx=10, pady=10)
        self.search = tk.Entry(self)
        self.search.grid(row=0, column=1, padx=10, pady=10)
        self.search.bind("<KeyRelease>", self.search_key_release)

        # Medicine Table
        self.medtable = ttk.Treeview(self, columns=("Medicine ID", "Medicine Name", "Date of Expiry","Price Per Unit", "Quantity"))
        self.medtable.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.medtable.bind("<ButtonRelease-1>", self.medtable_clicked)
        self.initialize_med_table()

        # Medicine Details
        self.lbl_medname = tk.Label(self, text="Medicine Name")
        self.lbl_medname.grid(row=2, column=0, padx=10, pady=10)
        self.txtmedname = tk.Entry(self, state='readonly')
        self.txtmedname.grid(row=2, column=1, padx=10, pady=10)

        self.lbl_price = tk.Label(self, text="Price Per Unit")
        self.lbl_price.grid(row=3, column=0, padx=10, pady=10)
        self.txtprice = tk.Entry(self, state='readonly')
        self.txtprice.grid(row=3, column=1, padx=10, pady=10)

        self.lbl_quantity = tk.Label(self, text="Quantity")
        self.lbl_quantity.grid(row=4, column=0, padx=10, pady=10)
        self.txtquantity = tk.Entry(self)
        self.txtquantity.grid(row=4, column=1, padx=10, pady=10)
        self.txtquantity.bind("<KeyRelease>", self.txtquantity_key_release)

        self.lbl_total = tk.Label(self, text="Total Price")
        self.lbl_total.grid(row=5, column=0, padx=10, pady=10)
        self.txttotal = tk.Entry(self, state='readonly')
        self.txttotal.grid(row=5, column=1, padx=10, pady=10)

        # Add to Cart Button
        self.btn_add_to_cart = tk.Button(self, text="Add To Cart", command=self.add_to_cart)
        self.btn_add_to_cart.grid(row=6, column=0, padx=10, pady=10)

        # Back Button
        self.btn_back = tk.Button(self, text="Back", command=self.go_back)
        self.btn_back.grid(row=6, column=1, padx=10, pady=10)

        # Cart Table
        self.carttable = ttk.Treeview(self, columns=("Medicine Name", "Quantity", "Price Per Unit", "Total Price"))
        self.carttable.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.carttable.bind("<ButtonRelease-1>", self.carttable_clicked)

        # Grand Total Price
        self.lbl_grand_total_price = tk.Label(self, text="Grand Total Price")
        self.lbl_grand_total_price.grid(row=8, column=0, padx=10, pady=10)
        self.lbl_ftp = tk.Label(self, text="00")
        self.lbl_ftp.grid(row=8, column=1, padx=10, pady=10)

        # Generate Bill Button
        self.btn_generate_bill = tk.Button(self, text="Generate Bill", command=self.generate_bill)
        self.btn_generate_bill.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    def initialize_med_table(self):
        self.medtable.heading("#0", text="Index")
        self.medtable.heading("Medicine ID", text="Medicine ID")
        self.medtable.heading("Medicine Name", text="Medicine Name")
        self.medtable.heading("Date of Expiry", text="Date of Expiry")
        self.medtable.heading("Price Per Unit", text="Price Per Unit")
        self.medtable.heading("Quantity", text="Quantity")
        # Populate the medicine table from the database
        self.populate_med_table()

    def populate_med_table(self):
        try:
            connection = self.establish_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT Id, medicineName, doe,price , quantity FROM inventory")

                rows = cursor.fetchall()
                for index, row in enumerate(rows, start=1):
                    self.medtable.insert("", "end", text=index, values=row)
                cursor.close()
                connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching medicine details: {e}")

    def establish_connection(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='pharmacy',
                user='root',
                password='root'
            )
            return connection
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error connecting to database: {e}")
            return None

    def search_key_release(self, event):
        search_text = self.search.get()
        for row in self.medtable.get_children():
            self.medtable.delete(row)
        try:
            connection = self.establish_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM inventory WHERE `medicineName` LIKE %s", (f"%{search_text}%",))
                rows = cursor.fetchall()
                for index, row in enumerate(rows, start=1):
                    self.medtable.insert("", "end", text=index, values=row)
                cursor.close()
                connection.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error searching medicine: {e}")

    def medtable_clicked(self, event):
        selected_item = self.medtable.selection()[0]
        values = self.medtable.item(selected_item, "values")

        self.txtmedname.config(state='normal')
        self.txtprice.config(state='normal')

        self.txtmedname.delete(0, tk.END)
        self.txtprice.delete(0, tk.END)

        self.txtmedname.insert(0, values[1])
        self.txtprice.insert(0, values[3])

        self.txtmedname.config(state='readonly')
        self.txtprice.config(state='readonly')

    def txtquantity_key_release(self, event):
        quantity = self.txtquantity.get()
        if quantity:
            price = self.txtprice.get()
            total_price = int(quantity) * int(price)
            self.txttotal.config(state='normal')
            self.txttotal.delete(0, tk.END)
            self.txttotal.insert(0, str(total_price))
            self.txttotal.config(state='readonly')

    def add_to_cart(self):
        pass  # Implementation of add_to_cart functionality goes here

    def go_back(self):
        pass  # Implementation of go_back functionality goes here

    def carttable_clicked(self, event):
        pass  # Implementation of carttable_clicked functionality goes here

    def generate_bill(self):
        pass  # Implementation of generate_bill functionality goes here


if __name__ == "__main__":
    app = Cart()
    app.mainloop()
