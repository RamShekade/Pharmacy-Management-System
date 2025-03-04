from tkinter import *
import mysql
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import time
import os
from ConnectionProvider import ConnectionProvider


class Cartapp:
    cursor = None
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Pharmacy Management System ")
        self.root.config(bg="white")
        self.root.resizable(False, False)

        try:
            connection_provider = ConnectionProvider()
            con = connection_provider.get_con()
            self.cursor = con.cursor()

        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")
            self.root.destroy()
            return

        self.cart_list = []
        title = Label(self.root, text="Pharmacy Management System", compound=LEFT,font=("times new roman", 40, "bold"), bg="#add8e6", fg="black", padx=20).place(x=0,y=0,relwidth=1,height=70)
        self.var_cname = StringVar()
        self.var_contact = StringVar()
        self.net_pay = 0
        self.var_search = StringVar()
        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(x=6, y=103, width=410, height=550)

        pTitle = Label(ProductFrame1, text="All Products", font=("goudy old style", 17, "bold"), bg="#add8e6",fg="#333333").pack(side=TOP, fill=X)

        # Search Frame
        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=398, height=90)

        lbl_search = Label(ProductFrame2, text="Search Medicine | By Name ", font=("times new roman", 15, "bold"),bg="white", fg="green").place(x=2, y=5)
        lbl_search = Label(ProductFrame2, text="Medicine Name", font=("times new roman", 13, "bold"), bg="white").place(x=2, y=45)
        txt_search = Entry(ProductFrame2, textvariable=self.var_search, font=("times new roman", 15),bg="#ebf3fb").place(x=128, y=47, width=150, height=22)
        btn_search = Button(ProductFrame2, text="Search", command=self.search, font=("goudy old style", 15), bg="#000080",fg="white", cursor="hand2").place(x=285, y=45, width=100, height=25)
        btn_show_all = Button(ProductFrame2, text="Show All", command=self.show, font=("goudy old style", 15),bg="#1e90ff", fg="white", cursor="hand2").place(x=285, y=10, width=100, height=25)
        # Inventory Details Frame
        ProductFrame3 = Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, width=398, height=375)

        scrolly = Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        self.product_Table = ttk.Treeview(ProductFrame3, columns=("id", "name", "price", "qty", "expiry"),yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("id", text="ID")
        self.product_Table.heading("name", text="Name")
        self.product_Table.heading("price", text="Price")
        self.product_Table.heading("qty", text="QTY")
        self.product_Table.heading("expiry", text="Expiry")
        self.product_Table["show"] = "headings"
        self.product_Table.column("id", width=40)
        self.product_Table.column("name", width=100)
        self.product_Table.column("price", width=100)
        self.product_Table.column("qty", width=40)
        self.product_Table.column("expiry", width=90)
        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)
        self.show()

        # Customer Frame
        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place(x=420, y=103, width=530, height=70)

        cTitle = Label(CustomerFrame, text="Customer Details", font=("goudy old style", 17,"bold"), bg="#add8e6").pack(side=TOP, fill=X)
        lbl_name = Label(CustomerFrame, text="Name", font=("times new roman", 15), bg="white").place(x=5, y=35)
        txt_name = Entry(CustomerFrame, textvariable=self.var_cname, font=("times new roman", 13),bg="#ebf3fb").place(x=60, y=35, width=180)
        lbl_contact = Label(CustomerFrame, text="Contact No.", font=("times new roman", 15), bg="white").place(x=250,y=35)
        txt_contact = Entry(CustomerFrame, textvariable=self.var_contact, font=("times new roman", 13),bg="#ebf3fb").place(x=355, y=35, width=160)

        # Cart Frame
        Cal_Cart_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Cal_Cart_Frame.place(x=420, y=177, width=530, height=360)
        cart_Frame = Frame(Cal_Cart_Frame, bd=3, relief=RIDGE)
        cart_Frame.place(x=8, y=8, width=500, height=342)
        self.cartTitle = Label(cart_Frame, text="Cart \t Total Product: [0]", font=("goudy old style", 15),bg="lightgray")
        self.cartTitle.pack(side=TOP, fill=X)

        scrolly = Scrollbar(cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_Frame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(cart_Frame, columns=("id", "name", "price", "qty"), yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("id", text="ID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="QTY")
        self.CartTable["show"] = "headings"
        self.CartTable.column("id", width=40)
        self.CartTable.column("name", width=90)
        self.CartTable.column("price", width=90)
        self.CartTable.column("qty", width=40)
        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        # ADD Cart Widgets Frame
        self.var_id = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        Add_CartWidgetsFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Add_CartWidgetsFrame.place(x=420, y=543, width=530, height=110)

        lbl_p_name = Label(Add_CartWidgetsFrame, text="Medicine Name", font=("times new roman", 15), bg="white").place(x=5, y=5)
        txt_p_name = Entry(Add_CartWidgetsFrame, textvariable=self.var_pname, font=("times new roman", 15),bg="#ebf3fb", state='readonly').place(x=5, y=35, width=190, height=22)
        lbl_p_price = Label(Add_CartWidgetsFrame, text="Price per Qty", font=("times new roman", 15), bg="white").place(x=230, y=5)
        txt_p_price = Entry(Add_CartWidgetsFrame, textvariable=self.var_price, font=("times new roman", 15),bg="#ebf3fb", state='readonly').place(x=230, y=35, width=150, height=22)
        lbl_p_qty = Label(Add_CartWidgetsFrame, text="Quantity", font=("times new roman", 15), bg="white").place(x=390,y=5)
        txt_p_qty = Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("times new roman", 15),bg="#ebf3fb").place(x=390, y=35, width=120, height=22)

        self.lbl_inStock = Label(Add_CartWidgetsFrame, text="In Stock", font=("times new roman", 15), bg="white")
        self.lbl_inStock.place(x=5, y=70)

        btn_clear_cart = Button(Add_CartWidgetsFrame, text="Clear", command=self.clear_cart,font=("times new roman", 15, "bold"), bg="lightgray", cursor="hand2").place(x=180, y=70,width=150,height=30)
        btn_add_cart = Button(Add_CartWidgetsFrame, text="Add  |  Update Cart", command=self.add_update_cart,font=("times new roman", 15, "bold"), bg="orange", cursor="hand2").place(x=340, y=70,width=180,height=30)

        # Billing area
        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billFrame.place(x=950, y=103, width=398, height=410)

        BTitle = Label(billFrame, text="Customer Bill Area", font=("goudy old style", 17, "bold"), bg="#add8e6",fg="#333333").pack(side=TOP, fill=X)
        scroll = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)
        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        # Billing buttons
        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        billMenuFrame.place(x=950, y=513, width=498, height=140)

        self.lbl_amnt = Label(billMenuFrame, text='Bill Amount\n[0]', font=("goudy old style", 15, "bold"),bg="#3f51b5", fg="white")
        self.lbl_amnt.place(x=2, y=5, width=120, height=70)
        self.lbl_discount = Label(billMenuFrame, text='Discount\n[5%]', font=("goudy old style", 15, "bold"),bg="#8bc34a",fg="white")
        self.lbl_discount.place(x=124, y=5, width=120, height=70)
        self.lbl_net_pay = Label(billMenuFrame, text='Net Pay\n[0]', font=("goudy old style", 15, "bold"), bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=246, y=5, width=150, height=70)

        btn_back = Button(self.root, text="Back", command=self.back, font=("times new roman", 15, "bold"),bg="#90ee90",fg="black").place(x=1200, y=71, width="130", height="32")
        btn_print = Button(billMenuFrame, text='Print', cursor='hand2', font=("goudy old style", 15, "bold"),bg="lightgreen", fg="white")
        btn_print.place(x=2, y=80, width=120, height=50)
        btn_clear_all = Button(billMenuFrame, text='Clear All', command=self.clear_all, cursor='hand2',font=("goudy old style", 15, "bold"),bg="gray", fg="white")
        btn_clear_all.place(x=124, y=80, width=120, height=50)
        btn_generate = Button(billMenuFrame, text='Generate Bill', command=self.generate_bill, cursor='hand2',font=("goudy old style", 15, "bold"), bg="#009688",fg="white")
        btn_generate.place(x=246, y=80, width=150, height=50)

    # All Functions

    def show(self):
        try:
            self.cursor.execute("SELECT Id, medicineName, price, quantity, doe FROM inventory")
            rows = self.cursor.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert("", END, values=row)
        except mysql.connector.Error as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def search(self):
        try:
            connection_provider = ConnectionProvider()
            con = connection_provider.get_con()
            self.cursor = con.cursor()
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                self.cursor.execute("SELECT Id, medicineName, price, quantity, doe FROM inventory WHERE medicineName LIKE '%" + self.var_search.get() + "%'")
                rows = self.cursor.fetchall()

                if len(rows) != 0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No Record Found!!!", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.product_Table.focus()
        content = (self.product_Table.item(f))
        row = content['values']

        self.var_id.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock[{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        content = (self.CartTable.item(f))
        row = content['values']
        # pid,name,price,qty,stock

        self.var_id.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock[{str(row[4])}]")
        self.var_stock.set(row[4])

    def add_update_cart(self):
        if self.var_id.get() == '':
            messagebox.showerror("Error", "Please select product from the list", parent=self.root)

        elif self.var_qty.get() == '':
            messagebox.showerror("Error", "Quantity is required", parent=self.root)
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror("Error", "Invalid Quantity", parent=self.root)
        else:
            price_cal = self.var_price.get()
            cart_data = [self.var_id.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()]

            # ====================================Update Cart===============================
            present = 'no'
            index_ = 0
            for row in self.cart_list:
                if self.var_id.get() == row[0]:
                    present = 'yes'
                    break
                index_ += 1
            if present == 'yes':
                op = messagebox.askyesno('Confirm',
                                          "Product already present\nDo you want to update | Remove from the Cart List",
                                          parent=self.root)
                if op == True:
                    if self.var_qty.get() == "0":
                        self.cart_list.pop(index_)
                    else:
                        self.cart_list[index_][3] = self.var_qty.get()
            else:
                self.cart_list.append(cart_data)

            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amnt = 0
        self.discount = 0
        for row in self.cart_list:
            # pid,name,price,qty,stock
            self.bill_amnt = self.bill_amnt + (float(row[2]) * int(row[3]))

        self.discount = (self.bill_amnt * 5) / 100
        self.net_pay = self.bill_amnt - self.discount
        self.lbl_amnt.config(text=f'Bill Amnt.\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Net Pay\n{str(self.net_pay)}')
        self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to :{str(ex)}", parent=self.root)

    def generate_bill(self):
        if self.var_cname.get() == '':
            messagebox.showerror("Error", f"Customer Details are required", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", f"Please Add product to the cart", parent=self.root)
        else:
            self.bill_top_temp()
            self.bill_middle()
            self.bill_bottom()
            try:
                connection_provider = ConnectionProvider()
                con = connection_provider.get_con()
                self.cursor = con.cursor()
                customer_query = "INSERT INTO customer(billid, bill_date, cname, mobile) VALUES (%s, %s, %s, %s)"
                customer_data = (
                str(self.invoice), time.strftime("%Y-%m-%d"), self.var_cname.get(), self.var_contact.get())
                self.cursor.execute(customer_query, customer_data)

                # Insert bill details into the 'bill' table
                bill_query = "INSERT INTO bill(bill_id, billdate, totalamount) VALUES (%s, %s, %s)"
                bill_data = (str(self.invoice), time.strftime("%Y-%m-%d"), str(self.net_pay))
                self.cursor.execute(bill_query, bill_data)

                messagebox.showinfo("Success", "Details Added Successfully", parent=self.root)
                con.commit()  # Commit the transaction
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

            fp = open(f'bill/{str(self.invoice)}.txt', 'w')
            fp.write(self.txt_bill_area.get('1.0', END))
            fp.close()
            messagebox.showinfo('Saved', 'Bill has been generated/saved in Backend', parent=self.root)


    def bill_top_temp(self):
            self.invoice = int(time.strftime("%H%M%S"))
            bill_top_temp = f'''
    \t\tPharmacy-Store(xyz) 
    \t Phone No. 93215***** ,Mumbai-400606
{str("=" * 47)}
Customer Name: {self.var_cname.get()}
Ph no. :{self.var_contact.get()}
Bill No. :{str(self.invoice)}\t\t\tDate: {str(time.strftime("%Y-%m-%d"))}
{str("=" * 47)}
Product Name\t\t\tQTY\txt_p_price
{str("=" * 47)}
            '''  # Bill No. :{str(self.invoice)}\t\t\tDate: {str(time("%d/%m/%Y"))}
            self.txt_bill_area.delete("1.0", END)
            self.txt_bill_area.insert('1.0', bill_top_temp)
    def bill_bottom(self):
        bill_bottom_temp = f'''
{str("=" * 47)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("=" * 47)}\n
        '''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def bill_middle(self):
        try:
            connection_provider = ConnectionProvider()
            con = connection_provider.get_con()
            self.cursor = con.cursor()
            for row in self.cart_list:
                id = row[0]
                name = row[1]
                qty = int(row[4]) - int(row[3])
                price = float(row[2]) * int(row[3])
                price = str(price)
                self.txt_bill_area.insert(END, "\n " + name + "\t\t\t" + row[3] + "\tRs." + price)
                # Update quantity in product table
                self.cursor.execute('UPDATE inventory SET quantity = %s WHERE Id = %s', (qty, id))
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            if con:
                con.commit()  # Commit changes
                self.cursor.close()  # Close cursor
                con.close()  # Close connection

    def clear_cart(self):
        self.var_id.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.bill_updates()
        self.clear_cart()
        self.show()
        self.show_cart()
        self.lester()

    def lester(self):
        self.bill_photo = Image.open("images/man.png")
        self.bill_photo = self.bill_photo.resize((183,183), Image.LANCZOS)
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)
        lbl_image = Label(self.root, image=self.bill_photo, bd=0)
        lbl_image.place(x=721, y=197)


    def back(self):
        self.root.destroy()
        os.system("python login.py")

if __name__ == "__main__":
    root = Tk()
    obj = Cartapp(root)
    root.mainloop()