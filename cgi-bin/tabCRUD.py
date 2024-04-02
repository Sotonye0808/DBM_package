#!C:\Users\Sotonye.Dagogo\AppData\Local\Programs\Python\Python311\python.exe
import sys
sys.stderr = open('error.log', 'w')

import cgi
import mysql.connector
import html
import re

# Retrieve form data
form = cgi.FieldStorage()

# Get action and form data
actiont = form.getvalue("actiont")
host = form.getvalue("host")
user = form.getvalue("username")
password = form.getvalue("password")
database = form.getvalue("database")
table = form.getvalue("table")
pk = form.getvalue("pk")
handledExceptionMessage = f"<p>An error has occurred. This may be due to one of the following:</p> <p>- An incorrect or invalid entry.</p> <p>- More or fewer entries than required.</p> <p>- An element (database, primary key, or table) does not exist.</p>"
confirmation_status_tab = form.getvalue("isConfirmedTab")
confirmation_status_col = form.getvalue("isConfirmedCol")

class DBM:
    def __init__(self, host, user, password, database):
        
        self.host = host
        self.user = user
        self.password = password
        self.database = database
            

#to create a table
    def createTable(self):
        try:
            if not host :
                return "Please enter host!"
            
            elif not user:
                return "Please enter user!"
            
            elif not password:
                return "Please enter password!"
            
            elif not database:
                return "Please enter database!"
            
            elif not table:
                return "Please enter table name!"
            
            db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password)
            cursor = db.cursor()

            # Check if the database exists
            cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{self.database}'")
            db_exists = cursor.fetchone()

            if db_exists:
                db.cmd_init_db(self.database)
                # Check if the table exists
                cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.database}' AND table_name = '{table}'")
                table_exists = cursor.fetchone()

                if table_exists:
                    return "Table already exists!"
                
                else:
                    if pk:
                        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table} ({pk} INT AUTO_INCREMENT PRIMARY KEY)')
                        return f'Table "{table}" created with primary key "{pk}".'
                    else:
                        return "Primary key name is required to create a table."
            else:
                return f"Database \"{self.database}\" does not exist."

        except Exception as e:
            return handledExceptionMessage


#for reading table from database
    def readTable(self):
        try:
            if not host :
                return "Please enter host!"
            
            elif not user:
                return "Please enter user!"
            
            elif not password:
                return "Please enter password!"
            
            elif not database:
                return "Please enter database!"
            
            elif not table:
                return "Please enter table name!"
            
            db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password)
            cursor = db.cursor()
            # Check if the database exists 
            cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{database}'")
            db_exists = cursor.fetchone()

            if db_exists:
                db.cmd_init_db(self.database)
                # Check if the table exists
                cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.database}' AND table_name = '{table}'")
                table_exists = cursor.fetchone()

                if table_exists:
                    cursor.execute(f"SELECT * FROM {table}")
                    table_data = cursor.fetchall()

                    if not table_data:
                        return f'No data found in the table "{table}".'
                    else:
                        # Generate an HTML table
                        html_table = "<table style='text-align: center;' class='response-table'>"
                        html_table += "<tr>"
                        for column_name in [description[0] for description in cursor.description]:
                            html_table += f"<th class='response-column-header'>{html.escape(column_name)}</th>"
                        html_table += "</tr>"

                        for row in table_data:
                            html_table += "<tr>"
                            for cell in row:
                                cell_value = html.escape(str(cell)) if cell is not None else "-"  # Replace None with empty string
                                html_table += f"<td class='response-column-data'>{cell_value}</td>"
                            html_table += "</tr>"

                        html_table += "</table>"

                        return html_table
                    
                else:
                    return f"Table '{table}' does not exist in the database '{self.database}'."
            else:
                    return f"Database \"{database}\" does not exist."
                
        except Exception as e:
            return handledExceptionMessage

#for displaying columns of table and their description
    def showColumns(self):
        try:
            if not host :
                return "Please enter host!"
            
            elif not user:
                return "Please enter user!"
            
            elif not password:
                return "Please enter password!"
            
            elif not database:
                return "Please enter database!"
            
            elif not table:
                return "Please enter table name!"
            
            db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password)
            cursor = db.cursor()
            # Check if the database exists 
            cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{database}'")
            db_exists = cursor.fetchone()

            if db_exists:
                db.cmd_init_db(self.database)
                # Check if the table exists
                cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.database}' AND table_name = '{table}'")
                table_exists = cursor.fetchone()

                if table_exists:

                    cursor.execute(f"DESCRIBE {table}")
                    columns_info = cursor.fetchall()

                    if not columns_info:
                        return f'No columns found in the table "{table}".'
                    else:
                        # Generate an HTML table with centered content
                        html_table = "<table style='text-align: center;' class='response-table'>"
                        html_table += "<tr>"
                        html_table += """<th class='response-column-header'>Column Name</th>
                        <th class='response-column-header'>Data Type</th>
                        <th class='response-column-header'>Nullable</th>
                        <th class='response-column-header'>Key</th>
                        <th class='response-column-header'>Default</th>
                        <th class='response-column-header'>Extra</th>"""
                        html_table += "</tr>"

                        for column_info in columns_info:
                            html_table += "<tr>"
                            for cell in column_info:
                                cell_value = html.escape(str(cell)) if cell is not None else "-"  # Replace None with empty string
                                html_table += f"<td class='response-column-data'>{cell_value}</td>"
                            html_table += "</tr>"

                        html_table += "</table>"

                        return html_table
                else:
                    return f"Table '{table}' does not exist in the database '{self.database}'."
            else:
                    return f"Database \"{database}\" does not exist."
                
        except Exception as e:
            return handledExceptionMessage

#original addColumns function split into changeColumns and addNewColumn
    def changeColumns(self):
        try:
            if not host:
                return "Please enter host!"
            
            elif not user:
                return "Please enter user!"
            
            elif not password:
                return "Please enter password!"
            
            elif not database:
                return "Please enter database!"
            
            elif not table:
                return "Please enter table name!"
            
            db = mysql.connector.connect(
                host=self.host, 
                user=self.user, 
                passwd=self.password)
            cursor = db.cursor()
            # Check if the database exists 
            cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{database}'")
            db_exists = cursor.fetchone()

            if db_exists:
                db.cmd_init_db(self.database)
                # Check if the table exists
                cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.database}' AND table_name = '{table}'")
                table_exists = cursor.fetchone()

                if table_exists:
                    columnName = form.getvalue("columnName")
                    description = form.getvalue("description")
                    useDefaultDesc = form.getvalue("useDefaultDesc")
                    makeForeignKey = form.getvalue("makeForeignKey")
                    position = form.getvalue("position")
                    afterColumn = form.getvalue("afterColumn")
                    renameColumn = form.getvalue("renameColumn")

                    # Check if columns already exist
                    existing_columns = set()
                    cursor.execute(f"DESCRIBE {table}")
                    column_info = {row[0]: row[1] for row in cursor.fetchall()}
                    for column in column_info.keys():
                        existing_columns.add(column)
                    
                    if columnName not in existing_columns:
                        return f"Column '{columnName}' does not exist in the table '{table}'."

                    # Modify the existing column based on user inputs
                    sql = f"ALTER TABLE {table} MODIFY COLUMN {columnName}"

                    if useDefaultDesc == "true":
                        # Maintain the original description
                        original_description = column_info[columnName]
                        description = original_description.decode('utf-8').strip("b''")
                        sql += f" {description}"
                    elif description == "":
                        return f"Must have description!"
                    
                    else:
                        sql += f" {description}"

                    if position == "FIRST":
                        sql += " FIRST"
                    elif position == "AFTER":
                        if afterColumn == "":
                            return "Please enter a column to place it after!"
                        else:
                            sql += f" AFTER {afterColumn}"

                    cursor.execute(sql)
                    db.commit()
                    result = f"Column '{columnName}' has been updated successfully."
                    
                    # Check if the user wants to create a foreign key
                    if makeForeignKey == "true":
                        referenced_table = form.getvalue("referencedTable")
                        referenced_column = form.getvalue("referencedColumn")
                        sql_fk = f"ALTER TABLE {table} ADD FOREIGN KEY ({columnName}) REFERENCES {referenced_table}({referenced_column})"
                        cursor.execute(sql_fk)
                        db.commit()
                        result += f"\nForeign key added successfully."

                    # Check if the user wants to rename the column
                    if renameColumn == "true":
                        #check if name is already in use
                        existing_columns = set()
                        cursor.execute(f"DESCRIBE {table}")
                        column_info = {row[0]: row[1] for row in cursor.fetchall()}
                        for column in column_info.keys():
                            existing_columns.add(column)

                        changedName = form.getvalue("changedName")

                        if changedName == "":
                            return "Please enter a new name for the renaming the column!"
                        
                        else:
                            if changedName not in existing_columns:
                                sql_rename = f"ALTER TABLE {table} RENAME COLUMN {columnName} TO {changedName}"
                                cursor.execute(sql_rename)
                                db.commit()
                                result += f"\nColumn '{columnName}' has been renamed to '{changedName}' successfully"

                            else:
                                return "Column name already in use!"

                    return result
                
                else:
                    return f"Table '{table}' does not exist in the database '{self.database}'."
            else:
                    return f"Database \"{database}\" does not exist."

        except Exception as e:
            return e
            
            
    def addNewColumn(self):
        try:
            if not host :
                return "Please enter host!"
            
            elif not user:
                return "Please enter user!"
            
            elif not password:
                return "Please enter password!"
            
            elif not database:
                return "Please enter database!"
            
            elif not table:
                return "Please enter table name!"
            
            db = mysql.connector.connect(
                host=self.host, 
                user=self.user, 
                passwd=self.password)
            cursor = db.cursor()
        # Check if the database exists 
            cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{database}'")
            db_exists = cursor.fetchone()

            if db_exists:
                db.cmd_init_db(self.database)
                # Check if the table exists
                cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.database}' AND table_name = '{table}'")
                table_exists = cursor.fetchone()

                if table_exists:
                    newColumnName = form.getvalue("newColumnName")
                    newColumnDescription = form.getvalue("newColumnDescription")
                    useDefaultNewDesc = form.getvalue("useDefaultNewDesc")
                    makeNewColumnForeignKey = form.getvalue("makeNewColumnForeignKey")
                    newColumnPosition = form.getvalue("newColumnPosition")
                    newColumnAfter = form.getvalue("newColumnAfter")

                    # Check if columns already exist
                    existing_columns = set()
                    cursor.execute(f"DESCRIBE {table}")
                    column_info = {row[0]: row[1] for row in cursor.fetchall()}
                    for column in column_info.keys():
                        existing_columns.add(column)
                    
                    if newColumnName in existing_columns:
                        return f"Column '{newColumnName}' already exists in the table '{table}'."

                    # Add a new column based on user inputs
                    sql = f"ALTER TABLE {table} ADD COLUMN {newColumnName}"

                    if useDefaultNewDesc == "true":
                        # Use the default newColumnDescription
                        sql += " VARCHAR(255) NULL"
                    elif newColumnDescription == "":
                        return f"Must have description!"
                    else:
                        sql += f" {newColumnDescription}"

                    if newColumnPosition == "FIRST":
                        sql += " FIRST"
                    
                    elif newColumnPosition == "AFTER":
                        if newColumnAfter == "":
                            return "Please enter a column to place it after!"
                        else:
                            sql += f" AFTER {newColumnAfter}"

                    cursor.execute(sql)
                    db.commit()
                    result = f"Column '{newColumnName}' has been added successfully."
                    
                    # Check if the user wants to create a foreign key
                    if makeNewColumnForeignKey == "true":
                        referenced_table = form.getvalue("referencedTableAdd")
                        referenced_column = form.getvalue("referencedColumnAdd")
                        sql_fk = f"ALTER TABLE {table} ADD FOREIGN KEY ({newColumnName}) REFERENCES {referenced_table}({referenced_column})"
                        cursor.execute(sql_fk)
                        db.commit()
                        result += f"\nForeign key added successfully."

                    return result
                
                else:
                    return f"Table '{table}' does not exist in the database '{self.database}'."
            else:
                    return f"Database \"{database}\" does not exist."
                
        except Exception as e:
            return handledExceptionMessage
            

        # To delete a table from a database
    def deleteTable(self):
        if confirmation_status_tab == 'y':
            try:
                if not host :
                    return "Please enter host!"
            
                elif not user:
                    return "Please enter user!"
                
                elif not password:
                    return "Please enter password!"
                
                elif not database:
                    return "Please enter database!"
                
                elif not table:
                    return "Please enter table name!"
        
                db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password)
                cursor = db.cursor()                
                # Check if the database exists 
                cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{database}'")
                db_exists = cursor.fetchone()

                if db_exists:
                    db.cmd_init_db(self.database)
                    # Check if the table exists
                    cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.database}' AND table_name = '{table}'")
                    table_exists = cursor.fetchone()

                    if table_exists:
                        # if Table exists, proceed with deletion
                        cursor.execute(f'DROP TABLE {table}')
                        return f"Table '{table}' has been deleted."
                    else:
                        return f"Table '{table}' does not exist in the database '{self.database}'."
                else:
                    return f"Database \"{database}\" does not exist."
                
            except Exception as e:
                return handledExceptionMessage

        else:
            return "Table deletion canceled."

    # For deleting columns
    def deleteColumns(self):
        if confirmation_status_col == 'y':
            try:
                if not host :
                    return "Please enter host!"
            
                elif not user:
                    return "Please enter user!"
                
                elif not password:
                    return "Please enter password!"
                
                elif not database:
                    return "Please enter database!"
                
                elif not table:
                    return "Please enter table name!"
        
                # Retrieve the column names from the form
                column_names_input = form.getvalue("columnNames")
                # Split the input by newlines, spaces, or commas and remove empty strings
                column_names = [col.strip() for col in re.split(r'[\n, ]+', column_names_input) if col.strip()]

                db = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password)
                cursor = db.cursor()
                # Check if the database exists 
                cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{database}'")
                db_exists = cursor.fetchone()

                if db_exists:
                    db.cmd_init_db(self.database)
                    # Check if the table exists
                    cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.database}' AND table_name = '{table}'")
                    table_exists = cursor.fetchone()

                    if table_exists:  
                        # Get the list of columns in the table
                        cursor.execute(f"DESCRIBE {table}")
                        columns = [column[0] for column in cursor.fetchall()]

                        # Validate column names
                        invalid_columns = [col for col in column_names if col not in columns]
                        if invalid_columns:
                            return f"Invalid column name(s): {', '.join(invalid_columns)}"

                        # Generate the ALTER TABLE query to drop the columns
                        alter_query = f"ALTER TABLE {table} "
                        alter_query += ", ".join([f"DROP COLUMN {col}" for col in column_names])

                        # Execute the ALTER TABLE query
                        cursor.execute(alter_query)
                        db.commit()
                        db.close()

                        if len(column_names) < 1:
                            return "Please enter column names."
                        
                        else:
                            formatted_column_names = [f'"{col}"' for col in column_names]
                            return f"Columns {', '.join(formatted_column_names)} deleted successfully."



                    else:
                            return f"Table '{table}' does not exist in the database '{self.database}'."
                else:
                    return f"Database \"{database}\" does not exist."
                    
            except Exception as e:
                    return handledExceptionMessage

        else:
            return "Column deletion canceled."  

   #decomposition of initial deleteForeignKeys method
    def getForeignKeys(self):
        try:
            if not host :
                return "Please enter host!"
            
            elif not user:
                return "Please enter user!"
            
            elif not password:
                return "Please enter password!"
            
            elif not database:
                return "Please enter database!"
            
            elif not table:
                return "Please enter table name!"
            
            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.password)
            cursor = db.cursor()
            
            # Check if the database exists 
            cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{self.database}'")
            db_exists = cursor.fetchone()

            if db_exists:
                db.cmd_init_db(self.database)
                # Check if the table exists
                cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.database}' AND table_name = '{table}'")
                table_exists = cursor.fetchone()

                if table_exists:
                    # Get foreign key constraints for the specified table
                    cursor.execute(f"SELECT COLUMN_NAME, CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = '{table}' AND CONSTRAINT_NAME IS NOT NULL")
                    foreign_keys = cursor.fetchall()

                    if not foreign_keys:
                        return "No foreign key columns found in the table."

                    # Generate a simple bullet-like list
                    form_html = ""
                    for i, (col, constraint) in enumerate(foreign_keys, start=1):
                        form_html += f"<p>{i}. {col} (Constraint: {constraint})</p>"
                    form_html += ""

                    db.close()

                    return form_html
                    
                else:
                    return f"Table '{table}' does not exist in the database '{self.database}'."
            else:
                return f"Database \"{self.database}\" does not exist."
                        
        except Exception as e:
            return handledExceptionMessage


    def deleteForeignKeyConstraints(self):
        try:
            if not host :
                return "Please enter host!"
            
            elif not user:
                return "Please enter user!"
            
            elif not password:
                return "Please enter password!"
            
            elif not database:
                return "Please enter database!"
            
            elif not table:
                return "Please enter table name!"
            
            selected_columns_input = form.getvalue("foreignKeyConstraints")

            # Retrieve the selected columns and their constraint names
            selected_columns = [int(col.strip()) for col in re.split(r'[\n, ]+', selected_columns_input) if col.strip()]

            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.password)
            cursor = db.cursor()
            # Check if the database exists 
            cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{database}'")
            db_exists = cursor.fetchone()

            if db_exists:
                db.cmd_init_db(self.database)
                    # Check if the table exists
                cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.database}' AND table_name = '{table}'")
                table_exists = cursor.fetchone()

                if table_exists:
                    cursor.execute(f"SELECT COLUMN_NAME, CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = '{table}' AND CONSTRAINT_NAME IS NOT NULL")
                    foreign_keys = cursor.fetchall()
                    # Drop the foreign key constraints associated with the selected columns

                     # Validate user choices
                    invalid_choices = [c for c in selected_columns if c < 1 or c > len(foreign_keys)]
                    if invalid_choices:
                        return "Invalid choice(s). Please enter valid numbers."
                    
                    columns_to_delete = [(col, constraint) for c, (col, constraint) in enumerate(foreign_keys, start=1) if c in selected_columns]

                    for column, constraint in columns_to_delete:
                        cursor.execute(f"ALTER TABLE {table} DROP FOREIGN KEY {constraint}")


                    db.commit()
                    db.close()
                    if len(columns_to_delete) < 1:
                        return "Please enter the indexes (number)."
                    else:
                        return "Foreign key constraints have been dropped."
                
                else:
                    return f"Table '{table}' does not exist in the database '{self.database}'."
            else:
                return f"Database \"{database}\" does not exist."
                    
        except Exception as e:
            return handledExceptionMessage  
        
    def deleteForeignKeys(self):
        try:
            if not host :
                return "Please enter host!"
            
            elif not user:
                return "Please enter user!"
            
            elif not password:
                return "Please enter password!"
            
            elif not database:
                return "Please enter database!"
            
            elif not table:
                return "Please enter table name!"
            
            selected_columns_input = form.getvalue("foreignKeyConstraints")

            # Retrieve the selected columns and their constraint names
            selected_columns = [int(col.strip()) for col in re.split(r'[\n, ]+', selected_columns_input) if col.strip()]

            db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.password)
            cursor = db.cursor()
            # Check if the database exists 
            cursor.execute(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{database}'")
            db_exists = cursor.fetchone()

            if db_exists:
                db.cmd_init_db(self.database)
                    # Check if the table exists
                cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.database}' AND table_name = '{table}'")
                table_exists = cursor.fetchone()

                if table_exists:
                    cursor.execute(f"SELECT COLUMN_NAME, CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = '{table}' AND CONSTRAINT_NAME IS NOT NULL")
                    foreign_keys = cursor.fetchall()
                    

                     # Validate user choices
                    invalid_choices = [c for c in selected_columns if c < 1 or c > len(foreign_keys)]
                    if invalid_choices:
                        return "Invalid choice(s). Please enter valid numbers."
                    
                    columns_to_delete = [(col, constraint) for c, (col, constraint) in enumerate(foreign_keys, start=1) if c in selected_columns]
                    
                    # Drop the foreign key constraints associated with the selected columns
                    for column, constraint in columns_to_delete:
                        cursor.execute(f"ALTER TABLE {table} DROP FOREIGN KEY {constraint}")
                            # Generate the ALTER TABLE query to delete the columns
                        alter_query = f"ALTER TABLE {table} DROP COLUMN {column}"
                        cursor.execute(alter_query)
                    db.commit()
                    db.close()
                    if len(columns_to_delete) < 1:
                        return "Please enter the indexes (number)."
                    else:
                        return "Foreign key columns have been deleted."
                
                else:
                    return f"Table '{table}' does not exist in the database '{self.database}'."
            else:
                return f"Database \"{database}\" does not exist."
                    
        except Exception as e:
            return handledExceptionMessage


# Perform the requested action and generate a response
response = ""
oracle = DBM(host, user, password, database)


if actiont == "createTable":
    response = oracle.createTable() 
elif actiont == "readTable":
    response = oracle.readTable()
elif actiont == "showColumns":
    response = oracle.showColumns() 
elif actiont == "changeColumns":
    response = oracle.changeColumns()
elif actiont == "addNewColumn":
    response = oracle.addNewColumn()    
elif actiont == "deleteTable":
    response = oracle.deleteTable()
elif actiont == "deleteColumns":
    response = oracle.deleteColumns()
elif actiont == "getForeignKeys":
    response = oracle.getForeignKeys()
elif actiont == "deleteForeignKeyConstraints":
    response = oracle.deleteForeignKeyConstraints()
elif actiont == "deleteForeignKeys":
    response = oracle.deleteForeignKeys()
# Print the message directly
print(f"Content-type: text/html\n\n{response}")