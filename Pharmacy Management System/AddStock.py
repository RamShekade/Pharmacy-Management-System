from tkinter import *
from tkinter import messagebox
from datetime import datetime
import tkinter as tk
from ConnectionProvider import ConnectionProvider

class AddStock:
    def __init__(self, root):
        self.root = root
        self.root.title("Add Stock")
        self.root.geometry("800x600")

        # UI Elements
        self.lbl_title = Label(root, text="Add Stock", font=("Tahoma", 24, "bold"))
        self.lbl_title.pack(pady=20)

        self.lbl_med_id = Label(root, text="Medicine ID")
        self.lbl_med_id.pack()
        self.txt_med_id = Entry(root)
        self.txt_med_id.pack()

        self.lbl_med_name = Label(root, text="Medicine Name")
        self.lbl_med_name.pack()
        self.txt_med_name = Entry(root)
        self.txt_med_name.pack()

        self.lbl_sup_name = Label(root, text="Supplier Name")
        self.lbl_sup_name.pack()
        self.txt_sup_name = Entry(root)
        self.txt_sup_name.pack()

        self.lbl_quantity = Label(root, text="Quantity")
        self.lbl_quantity.pack()
        self.txt_quantity = Entry(root)
        self.txt_quantity.pack()

        self.lbl_dom = Label(root, text="Date of Manufacture (yyyy/MM/dd)")
        self.lbl_dom.pack()
        self.txt_dom = Entry(root)
        self.txt_dom.pack()

        self.lbl_doe = Label(root, text="Date of Expiry (yyyy/MM/dd)")
        self.lbl_doe.pack()
        self.txt_doe = Entry(root)
        self.txt_doe.pack()

        self.lbl_pur_date = Label(root, text="Purchase Date (yyyy/MM/dd)")
        self.lbl_pur_date.pack()
        self.txt_pur_date = Entry(root)
        self.txt_pur_date.pack()

        self.lbl_price = Label(root, text="Price Per Unit")
        self.lbl_price.pack()
        self.txt_price = Entry(root)
        self.txt_price.pack()

        self.btn_add = Button(root, text="Add", command=self.add_stock)
        self.btn_add.pack(pady=20)
        

    def add_stock(self):
        med_id = self.txt_med_id.get()
        med_name = self.txt_med_name.get()
        sup_name = self.txt_sup_name.get()
        quantity = self.txt_quantity.get()
        dom = self.txt_dom.get()
        doe = self.txt_doe.get()
        pur_date = self.txt_pur_date.get()
        price = self.txt_price.get()

        try:
            quantity = int(quantity)
            price = float(price)

            # Database interaction (replace with your database connection details)
            connection_provider = ConnectionProvider()
            con = connection_provider.get_con()
            cursor = con.cursor()

            # Insert into the stock table
            cursor.execute("INSERT INTO stock (Id, medicineName, supplierName, dom, doe, purchasedate, quantity, price) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (med_id, med_name, sup_name, dom, doe, pur_date, quantity, price))
            con.commit()

            # Insert into the inventory table
            cursor.execute("INSERT INTO inventory (stock_id, Id, medicineName, dom, doe, quantity, price, totalPrice) "
                           "VALUES (LAST_INSERT_ID(), %s, %s, %s, %s, %s, %s, %s)",
                           (med_id, med_name, dom, doe, quantity, 2*price, quantity * (2 * price)))
            con.commit()

            con.close()

            messagebox.showinfo("Success", "Stock Added Successfully.")
            # Clear the entry fields
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Invalid input for Quantity or Price.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_entries(self):
        self.txt_med_id.delete(0, END)
        self.txt_med_name.delete(0, END)
        self.txt_sup_name.delete(0, END)
        self.txt_quantity.delete(0, END)
        self.txt_dom.delete(0, END)
        self.txt_doe.delete(0, END)
        self.txt_pur_date.delete(0, END)
        self.txt_price.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    app = AddStock(root)
    root.mainloop()
