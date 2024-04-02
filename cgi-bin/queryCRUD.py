#!C:\Users\Sotonye.Dagogo\AppData\Local\Programs\Python\Python311\python.exe
import sys
sys.stderr = open('error.log', 'w')

import cgi
import html
import mysql.connector

# Retrieve form data
form = cgi.FieldStorage()

# Get action and form data
actionq = form.getvalue("actionq")
host = form.getvalue("host")
user = form.getvalue("username")
password = form.getvalue("password")
database = form.getvalue("database")
query = form.getvalue("dynamicQueryBox")

# Initialize the database manager
class DBM:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def queryDynamic(self, database):
        try:
            db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database=database)
            cursor = db.cursor()
            cursor.execute(f"{query}")
            results = cursor.fetchall()
            
            if results == []:   
                return "Execution Succesful!"
                
            if hasattr(cursor.fetchall(), '__iter__'):
                html_table = "<table style='text-align: center;' class='response-table'>"
                html_table += "<tr>"
                for column_name in [description[0] for description in cursor.description]:
                    html_table += f"<th class='response-column-header'>{html.escape(column_name)}</th>"
                html_table += "</tr>"

                for row in results:
                    html_table += "<tr>"
                    for cell in row:
                        cell_value = html.escape(str(cell)) if cell is not None else "-"  # Replace None with empty string
                        html_table += f"<td class='response-column-data'>{cell_value}</td>"
                    html_table += "</tr>"

                html_table += "</table>"
                db.commit()
                return html_table

        except mysql.connector.Error as error:
            if error.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                return"Error: Access denied, check your username and password."
            elif error.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                return "Error: The specified database does not exist."
            else:
                return f"Error: {error}"
        except Exception as e:
            return e

    
# Perform the requested action and generate a response
response = ""
oracle = DBM(host, user, password)

if actionq == "queryDynamic":
    response = oracle.queryDynamic(database)

# Print the message directly
print(f"Content-type: text/html\n\n{response}")
