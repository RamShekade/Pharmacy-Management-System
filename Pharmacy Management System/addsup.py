import tkinter as tk
from tkinter import messagebox
import mysql.connector

class AddSupp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Add Supplier")
        self.geometry("1030x610")
        
        self.MobileNumberPattern = "^[0-9]*$"
        self.checkSupplier_ID = 0
        
        self.create_widgets()

    def create_widgets(self):
        self.lbl_title = tk.Label(self, text="ADD SUPPLIER", font=("Serif", 32, "bold"))
        self.lbl_title.place(x=340, y=20)

        self.lbl_supplier_id = tk.Label(self, text="Supplier ID", font=("Tahoma", 18))
        self.lbl_supplier_id.place(x=83, y=129)

        self.lbl_supplier_name = tk.Label(self, text="Supplier Name", font=("Tahoma", 18))
        self.lbl_supplier_name.place(x=520, y=130)

        self.lbl_mobile = tk.Label(self, text="Mobile Number", font=("Tahoma", 18))
        self.lbl_mobile.place(x=90, y=240)

        self.lbl_address = tk.Label(self, text="Address", font=("Tahoma", 18))
        self.lbl_address.place(x=530, y=240)

        self.txtsuppid = tk.Entry(self, font=("Segoe UI", 18))
        self.txtsuppid.place(x=83, y=166)
        self.txtsuppid.bind("<KeyRelease>", self.txtsuppid_keyreleased)

        self.txtsuppname = tk.Entry(self, font=("Segoe UI", 18))
        self.txtsuppname.place(x=520, y=170)

        self.txtmobile = tk.Entry(self, font=("Segoe UI", 18))
        self.txtmobile.place(x=83, y=276)

        self.txtaddress = tk.Entry(self, font=("Segoe UI", 18))
        self.txtaddress.place(x=520, y=280)

        self.btn_save = tk.Button(self, text="Save", font=("Tahoma", 18, "bold"), command=self.save_supplier)
        self.btn_save.place(x=310, y=390)

        self.btn_back = tk.Button(self, text="Back", font=("Tahoma", 18, "bold"), command=self.go_back)
        self.btn_back.place(x=480, y=390)

    def save_supplier(self):
        Id = self.txtsuppid.get()
        supplierName = self.txtsuppname.get()
        mobileNumber = self.txtmobile.get()
        address = self.txtaddress.get()

        if Id == "":
            messagebox.showerror("Error", "Supplier ID field is required.")
        elif self.checkSupplier_ID == 1:
            messagebox.showerror("Error", "This supplier ID already exists.")
        elif supplierName == "":
            messagebox.showerror("Error", "Supplier Name field is required.")
        elif mobileNumber == "":
            messagebox.showerror("Error", "Mobile number field is required.")
        elif not mobileNumber.isdigit() or len(mobileNumber) != 10:
            messagebox.showerror("Error", "Mobile Number field is invalid.")
        elif address == "":
            messagebox.showerror("Error", "Address field is required.")
        else:
            try:
                conn = mysql.connector.connect(host="root", user="root", password="Ram@1818", database="medical")
                cursor = conn.cursor()
                query = "INSERT INTO supplier(Id, supplierName, mobileNumber, address) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (Id, supplierName, mobileNumber, address))
                conn.commit()
                messagebox.showinfo("Success", "Supplier Added Successfully.")
                self.txtsuppid.delete(0, tk.END)
                self.txtsuppname.delete(0, tk.END)
                self.txtmobile.delete(0, tk.END)
                self.txtaddress.delete(0, tk.END)
                self.checkSupplier_ID = 0
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    def go_back(self):
        self.destroy()

    def txtsuppid_keyreleased(self, event):
        Id = self.txtsuppid.get()
        if Id != "":
            self.checkSupplier_ID = 0
            try:
                conn = mysql.connector.connect(host="your_host", user="your_username", password="your_password", database="your_database")
                cursor = conn.cursor()
                query = "SELECT * FROM supplier WHERE Id = %s"
                cursor.execute(query, (Id,))
                result = cursor.fetchone()
                if result:
                    self.checkSupplier_ID = 1
                    messagebox.showerror("Error", "This supplier ID already exists.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

if __name__ == "__main__":
    app = AddSupp()
    app.mainloop()
