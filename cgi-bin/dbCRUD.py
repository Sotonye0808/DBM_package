#!C:\Users\Sotonye.Dagogo\AppData\Local\Programs\Python\Python311\python.exe
import sys
sys.stderr = open('error.log', 'w')

import cgi
import mysql.connector

# Retrieve form data
form = cgi.FieldStorage()

# Get action and form data
action = form.getvalue("action")
host = form.getvalue("host")
user = form.getvalue("username")
password = form.getvalue("password")
database = form.getvalue("database")
handledExceptionMessage = f"<p>An error has occurred. This may be due to one of the following:</p> <p>- An incorrect or invalid entry.</p> <p>- More or fewer entries than required.</p> <p>- An element (database, primary key, or table) does not exist.</p>"
confirmation_status = form.getvalue("isConfirmed")

# Initialize the database manager
class DBM:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def createDB(self, database):
        try:
            if not host :
                return "Please enter host!"
            
            elif not user:
                return "Please enter user!"
            
            elif not password:
                return "Please enter password!"
            
            elif not database:
                return "Please enter database!"
            
            db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password)
            cursor = db.cursor()
            # Check if the database exists 
            cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{database}'")
            db_exists = cursor.fetchone()

            if db_exists:
                return "Database already exists!"
            else:
                cursor.execute(f'CREATE DATABASE IF NOT EXISTS {database}')
                return f'database "{database}" created'
        except Exception as e:
            return f"An error has occurred. This may be due to incorrect or invalid entry. Please try again and ensure you enter the right details."

    def showTables(self, database):
        try:
            if not host :
                return "Please enter host!"
            
            elif not user:
                return "Please enter user!"
            
            elif not password:
                return "Please enter password!"
            
            elif not database:
                return "Please enter database!"

            db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password)
            cursor = db.cursor()
            # Check if the database exists 
            cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{database}'")
            db_exists = cursor.fetchone()

            if db_exists:
                db.cmd_init_db(database)

                cursor.execute(f"SHOW TABLES IN {database}")
                tables = [table[0] for table in cursor.fetchall()]

                if not tables:
                    return f'No tables found in the database "{database}".'
                else:
                # Format tables as an HTML table
                    table_html = "<table style='text-align: center;' class='response-table'>"
                    table_html += f"<tr><th class='response-column-header'>Tables in Database \"{database}\"</th></tr>"
                    for table_name in tables:
                        table_html += f"<tr><td class='response-column-data'>{table_name}</td></tr>"
                    table_html += "</table>"
                    return table_html
            else:
                return f"Database \"{database}\" does not exist."
                
        except Exception as e:
            return handledExceptionMessage

    def deleteDatabase(self, database):
        if confirmation_status == 'y':
            try:
                if not host :
                    return "Please enter host!"
            
                elif not user:
                    return "Please enter user!"
                
                elif not password:
                    return "Please enter password!"
                
                elif not database:
                    return "Please enter database!"
        
                db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password)
                cursor = db.cursor()

                # Check if the database exists 
                cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{database}'")
                db_exists = cursor.fetchone()

                if db_exists:
                    # Database exists, proceed with deletion
                    db.cmd_init_db(database)
                    cursor.execute(f"DROP DATABASE {database}")
                    return f"Database \"{database}\" has been deleted."
                else:
                    return f"Database \"{database}\" does not exist."

            except Exception as e:
                return handledExceptionMessage
        else:
            return "Database deletion canceled."
        
    def testConnection(self, database):
        try:
                if not host :
                    return "Please enter host!"
            
                elif not user:
                    return "Please enter user!"
                
                elif not password:
                    return "Please enter password!"
                
                elif not database:
                    return "Please enter database!"
        
                connection = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password, database = database)
                cursor = connection.cursor()

                # Check if the database exists 
                cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{database}'")
                db_exists = cursor.fetchone()

                if db_exists:
                    # Database exists, proceed with deletion
                    if connection.is_connected():
                        connection.close()
                        return "Connected successfully!"
                        
                    else:
                        connection.close()
                        return "Connection unsuccessful!"
                        
                else:
                    return f"Database \"{database}\" does not exist."

        except mysql.connector.Error as error:
            return f"Error: {error}"


        
# Perform the requested action and generate a response
response = ""
oracle = DBM(host, user, password)

if action == "createDB":
    response = oracle.createDB(database)
elif action == "showTables":
    response = oracle.showTables(database)
elif action == "deleteDatabase":
    response = oracle.deleteDatabase(database)
elif action == "testConnection":
    response = oracle.testConnection(database)

# Print the message directly
print(f"Content-type: text/html\n\n{response}")
