import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ConnectionProvider import ConnectionProvider

class EmpLogin(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Employee Login")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        self.label_title = ttk.Label(self, text="Employee Login", font=("Segoe UI", 18))
        self.label_title.pack(pady=20)

        self.label_username = ttk.Label(self, text="Username", font=("Segoe UI", 14))
        self.label_username.pack()

        self.txt_username = ttk.Entry(self, font=("Segoe UI", 14))
        self.txt_username.pack()

        self.label_password = ttk.Label(self, text="Password", font=("Segoe UI", 14))
        self.label_password.pack()

        self.txt_password = ttk.Entry(self, show="*", font=("Segoe UI", 14))
        self.txt_password.pack()

        self.chpassword = ttk.Checkbutton(self, text="Show Password", command=self.toggle_password, style='TCheckbutton')
        self.chpassword.pack()

        self.btn_login = ttk.Button(self, text="Login", command=self.login, style='TButton')
        self.btn_login.pack(pady=10)

        self.btn_back = ttk.Button(self, text="Back", command=self.back, style='TButton')
        self.btn_back.pack(pady=10)

        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TButton', font=("Segoe UI", 14))
        self.style.configure('TCheckbutton', font=("Segoe UI", 12))

    def toggle_password(self):
        if self.chpassword.instate(['selected']):
            self.txt_password.config(show="")
        else:
            self.txt_password.config(show="*")

    def login(self):
        username = self.txt_username.get()
        password = self.txt_password.get()
        temp = 0

        try:
            connection_provider = ConnectionProvider()
            con = connection_provider.get_con()
            cursor = con.cursor()
            cursor.execute(f"SELECT * FROM appuser WHERE username='{username}' AND password='{password}'")
            rs = cursor.fetchall()

            for row in rs:
                temp = 1
                if row[2] == "Employee":
                    self.withdraw()
                    emp_dashboard = EmpDashboard(username)
                    emp_dashboard.mainloop()
                    messagebox.showinfo("Login Successful", "Employee Login Successful")
                elif row[2] == "Admin":
                    messagebox.showerror("Login Error", "Incorrect Username or Password!")

            if temp == 0:
                messagebox.showerror("Login Error", "Incorrect Username or Password!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def back(self):
        login = Login()
        login.mainloop()
        self.destroy()

class EmpDashboard(tk.Tk):
    def __init__(self, username):
        tk.Tk.__init__(self)
        self.title(f"Welcome, {username}!")
        self.geometry("400x300")
        # Add your dashboard components here

if __name__ == "__main__":
    emp_login = EmpLogin()
    emp_login.mainloop()
