import tkinter as tk
from tkinter import ttk, messagebox
from ConnectionProvider import ConnectionProvider

class AdLogin(tk.Tk):
    def __init__(self,root):
        tk.Tk.__init__(self)
        self.root=root
        self.title("Admin Login")
        self.geometry("1030x610")
        self.resizable(False, False)

        self.label_title = ttk.Label(self, text="Admin Login", font=("Segoe UI", 30))
        self.label_title.pack(pady=20)

        self.label_username = ttk.Label(self, text="Username", font=("Segoe UI", 18))
        self.label_username.pack()
        self.txt_username = ttk.Entry(self, font=("Segoe UI", 18))
        self.txt_username.pack()

        self.label_password = ttk.Label(self, text="Password", font=("Segoe UI", 18))
        self.label_password.pack()
        self.txt_password = ttk.Entry(self, show="*", font=("Segoe UI", 18))
        self.txt_password.pack()

        self.ch_password = ttk.Checkbutton(self, text="Show Password", command=self.toggle_password, style='TCheckbutton')
        self.ch_password.pack()

        self.btn_login = ttk.Button(self, text="Login", command=self.login, style='TButton')
        self.btn_login.pack(pady=10)

        self.btn_back = ttk.Button(self, text="Back", command=self.go_back, style='TButton')
        self.btn_back.pack(pady=10)

        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TButton', font=("Segoe UI", 18))
        self.style.configure('TCheckbutton', font=("Segoe UI", 16))

    def toggle_password(self):
        if self.ch_password.instate(['selected']):
            self.txt_password.configure(show="")
        else:
            self.txt_password.configure(show="*")

    def login(self):
        username = self.txt_username.get()
        password = self.txt_password.get()
        temp = 0

        try:
            connection_provider = ConnectionProvider()
            con = connection_provider.get_con()
            cursor = con.cursor()
            cursor.execute(f"SELECT * FROM appuser WHERE username='{username}' AND password='{password}'")
            
            for row in cursor.fetchall():
                temp = 1
                if row[2] == "Admin":
                    self.withdraw()
                    AdDashboard(username).mainloop()
                    messagebox.showinfo("Success", "Admin Login Successful")
                elif row[2] == "Employee":
                    messagebox.showerror("Error", "Incorrect Username or Password!")

            if temp == 0:
                messagebox.showerror("Error", "Incorrect Username or Password!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            con.close()

    def go_back(self):
        self.destroy()

class AdDashboard(tk.Tk):
    def __init__(self, username):
        tk.Tk.__init__(self)
        self.title("Admin Dashboard")
        self.geometry("600x400")
        self.resizable(False, False)
        self.username = username

        # Add your admin dashboard UI elements here

if __name__ == "__main__":
    root=tk.Tk()
    ad_login = AdLogin(root)
    ad_login.mainloop()
