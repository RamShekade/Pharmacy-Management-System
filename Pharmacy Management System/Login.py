import tkinter as tk
from tkinter import ttk
from AdLogin import AdLogin
from EmpLogin import EmpLogin

class Login(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("HOMEPAGE")
        self.geometry("1030x610")
        # Labels and Buttons
        self.label_title = ttk.Label(self, text="HOMEPAGE", font=("Segoe UI", 30))
        self.label_title.pack(pady=20)

        self.label_login_as = ttk.Label(self, text="Login As", font=("Segoe UI", 16))
        self.label_login_as.pack()

        self.button_admin = ttk.Button(self, text="ADMIN", command=self.open_admin_login, style='TButton')
        self.button_admin.pack(pady=10)

        self.button_employee = ttk.Button(self, text="EMPLOYEE", command=self.open_employee_login, style='TButton')
        self.button_employee.pack(pady=10)

        # Configure button style
        self.style = ttk.Style()
        self.style.configure('TButton', font=("Segoe UI", 18))

    def open_admin_login(self):
        self.root.destroy()
        root=tk.Tk()
        ad=AdLogin.AdLogin(root)
        root.mainloop()

    def open_employee_login(self):
        self.withdraw()  # Hide the current window
        emp_login = EmpLogin(self)
        emp_login.mainloop()

if __name__ == "__main__":
    login_window = Login()
    login_window.mainloop()
