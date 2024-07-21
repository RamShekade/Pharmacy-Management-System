import mysql.connector

class ConnectionProvider:
    def get_con(self):
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="pharmacy",
                port=3306,
                ssl_disabled=True  # UseSSL=false
            )
            print ("connection successful.")
            return con
        except mysql.connector.Error as e:
            print(e)
            return None
