from mysql.connector import Error
from tkinter import messagebox
from ConnectionProvider import ConnectionProvider

class Tables:
    def __init__(self):
        self.create_tables()

    def create_tables(self):
        try:
            connection_provider = ConnectionProvider()
            con = connection_provider.get_con()
            cursor = con.cursor()

            # Uncomment the statements below as needed
            #cursor.execute("drop table if exists inventory")
            cursor.execute("create table appuser(appuser_pk int AUTO_INCREMENT primary key, userRole varchar(200), name varchar(200), doj date, mobileNumber varchar(50), username varchar(200), password varchar(50), address varchar(200), salary varchar(50))")
            # cursor.execute("insert into appuser(userRole, name, doj, mobileNumber, username, password, address, salary) values('Admin', 'Piyush', '06/06/2015', '9321508792', 'piyush', '123456', 'Thane', '15000')")
            # cursor.execute("create table supplier(Id int, supplierName varchar(100), mobileNumber varchar(15), address varchar(100))")
            cursor.execute("create table stock(stock_id int AUTO_INCREMENT primary key, Id int, medicineName varchar(50), supplierName varchar(50), dom date, doe date, purchasedate date, quantity int, price float, totalPrice float GENERATED ALWAYS AS (quantity * price) STORED)")
            cursor.execute("create table inventory(stock_id int, Id int, medicineName varchar(100), dom date, doe date, quantity int, price float, totalPrice float, FOREIGN KEY (stock_id) REFERENCES stock(stock_id))")
            cursor.execute("create table bill(bill int AUTO_INCREMENT primary key, bill_id varchar(200), billdate date, totalamount float)")
            #cursor.execute("create table customer(billid varchar(200), bill_date date, cname varchar(100),mobile varchar(50))")

            messagebox.showinfo("Success", "Table Created Successfully")
        except Error as e:
            messagebox.showerror("Error", e)
        finally:
            if con.is_connected():
                cursor.close()
                con.close()
if __name__ == "__main__":
    Tables()