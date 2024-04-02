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
actiond = form.getvalue("actiond")
host = form.getvalue("host")
user = form.getvalue("username")
password = form.getvalue("password")
database = form.getvalue("database")
table = form.getvalue("table")
pk = form.getvalue("pk")
handledExceptionMessage = f"<p>An error has occurred. This may be due to one of the following:</p> <p>- An incorrect or invalid entry.</p> <p>- More or fewer entries than required.</p> <p>- An element (database, primary key, or table) does not exist.</p>"

class DBM:
    def __init__(self, host, user, password, database):
        
        self.host = host
        self.user = user
        self.password = password
        self.database = database
            
    def addRecords(self):
        try:
            sql = ""
            value_list = ""
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
                    # Get column headers and entries from the HTML form
                    headers_input = form.getvalue("dataColumnNames")
                    headers = [col.strip() for col in headers_input.split(',')]

                    entries_input = form.getvalue("dataColumnValues").splitlines()
                    
                    if len(headers) == 0:
                        return "No column headers provided."
                    
                    if len(entries_input) == 0:
                        return "No entries provided."
                    
                    # Check if columns exist
                    existing_columns = set()
                    cursor.execute(f"DESCRIBE {table}")
                    column_info = {row[0]: row[1] for row in cursor.fetchall()}
                    for column in column_info.keys():
                        existing_columns.add(column)
                    
                    values_list = []
                    placeholders = ", ".join(["%s" for _ in headers])
                    sql = f"INSERT INTO {table} ({', '.join(headers)}) VALUES ({placeholders})"
                    
                    for entry_line in entries_input:
                        values = [value.strip() for value in entry_line.split(',')]

                        # Pad the values with None to match the number of headers
                        while len(values) < len(headers):
                            values.append(None)
                        
                        # Filter out extra values to match the number of headers
                        values = values[:len(headers)]
                        
                        for value in values:
                            if headers[values.index(value)] not in existing_columns:
                                return f"Column '{headers[values.index(value)]}' does not exist in the table '{table}'."
                        
                        values_list.append(tuple(values))
                    
                    cursor.executemany(sql, values_list)
                    db.commit()

                    if cursor.rowcount > 0:
                        return f"{cursor.rowcount} record(s) successfully inserted."
                    else:
                        return "No records were inserted."
                    
                else:
                    return f"Table '{table}' does not exist in the database '{self.database}'."
            else:
                return f"Database \"{database}\" does not exist."
        except Exception as e:
            return handledExceptionMessage

    def displayKeys(self):
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
                    # Get primary keys for the table
                    cursor.execute(f"SHOW KEYS FROM {table} WHERE Key_name = 'PRIMARY'")
                    primary_keys = [row[4] for row in cursor.fetchall()]

                    # Get foreign keys for the table and their associated tables
                    cursor.execute(f"SELECT column_name, referenced_table_name FROM information_schema.key_column_usage WHERE referenced_table_name IS NOT NULL AND table_name = '{table}'")
                    foreign_keys_info = cursor.fetchall()

                    # Start building the HTML response
                    response_html = ""

                    # Display primary keys
                    if primary_keys:
                        response_html += f"<h2>Primary Keys in the table '{table}':</h2>"
                        response_html += "<br><p>"
                        for key in primary_keys:
                            response_html += f"{key}"
                        response_html += "</p><br>"

                    # Display foreign keys and associated tables
                    if foreign_keys_info:
                        response_html += f"<h2>Foreign Keys in the table '{table}':</h2>"
                        response_html += "<br>"
                        for column_name, referenced_table_name in foreign_keys_info:
                            response_html += f"<p>{column_name} (References {referenced_table_name})<p><br>"
                        response_html += ""

                    if not primary_keys:
                        response_html += f"<p>No primary keys found for the table '{table}'.</p>"

                    if not foreign_keys_info:
                        response_html += f"<p>No foreign keys found for the table '{table}'.</p>"

                    if not primary_keys and not foreign_keys_info:
                        response_html += f"<p>No primary keys or foreign keys found for the table '{table}'.</p>"

                    # Close the HTML response
                    response_html += ""
                    return response_html
                else:
                    return f"Table '{table}' does not exist in the database '{self.database}'."
            else:
                return f"Database \"{self.database}\" does not exist."
        except Exception as e:
            return handledExceptionMessage
        
    def displayRecords(self):
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
                    ids = form.getvalue("primaryKeys")
                    columnNames = form.getvalue("dataColumnNames")
                    columnValues = form.getvalue("dataColumnValues")

                    if not ids and not pk and not columnNames and not columnValues:
                        return f"Enter Criteria to Display!"
                    
                    if ids and pk:
                        ids = ids.splitlines()
                        ids = ", ".join([f"'{value.strip()}'" for value in ids])
                        primary_query = f'SELECT * FROM {table} WHERE {pk} IN ({ids})'
                            
                    else:
                        primary_query = ""
                        
                    if columnNames and columnValues:
                        columnNames = [col.strip() for col in columnNames.split(',')]
                        columnValues = columnValues.split(',')

                        if not ids and pk and len(columnNames) != len(columnValues):
                            return "Number of column names does not match the number of lines of column values."
                        # Check if columns exist
                        existing_columns = set()
                        cursor.execute(f"DESCRIBE {table}")
                        column_info = {row[0]: row[1] for row in cursor.fetchall()}
                        for column in column_info.keys():
                            existing_columns.add(column)

                        for columnName in columnNames:
                            if columnName not in existing_columns:
                                return f"Column '{columnName}' does not exist in the table '{table}'."

                        conditions = []
                        for column, values in zip(columnNames, columnValues):
                            values = ", ".join([f"'{value.strip()}'" for value in values.split(",")])
                            conditions.append(f"{column} IN ({values})")
                        column_query = f'SELECT * FROM {table} WHERE {" AND ".join(conditions)}'
                    else:
                        column_query = ""

                    if primary_query and column_query:
                        query = f"{primary_query} UNION {column_query}"
                    else:
                        query = primary_query if primary_query else column_query

                    cursor.execute(query)
                    allrows = cursor.fetchall()

                    if not allrows:
                        # Return an error message if no records match the criteria
                        return "No record exists with the specified criteria. Please check entries and try again."
                    else:
                        # Generate HTML response with the table
                        response_html = "<html><head><title>Records</title></head><body><table style='text-align: center;' class='response-table'><tr>"

                        # Add table headers
                        for description in cursor.description:
                            response_html += f"<th class='response-column-header'>{description[0]}</th>"
                        response_html += "</tr>"

                        # Add table rows
                        for row in allrows:
                            response_html += "<tr>"
                            for cell in row:
                                cell = html.escape(str(cell)) if cell is not None else "-"  # Replace None with empty string
                                response_html += f"<td class='response-column-data'>{cell}</td>"
                            response_html += "</tr>"

                        response_html += "</table></body></html>"
                        return response_html
                else:
                    return f"Table '{table}' does not exist in the database '{self.database}'."
            else:
                return f"Database \"{database}\" does not exist."
        except Exception as e:
            return handledExceptionMessage

    def searchRecords(self):
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
                    searchColumnName = form.getvalue("searchColumnName")
                    searchOptions = form.getvalue("searchOptions")
                    searchChar = form.getvalue("searchChar")

                    if not searchChar:
                        return "Please enter a character!"

                    if searchOptions == 'starts':
                        operator = 'LIKE'
                        search_term = f"'{searchChar}%'"
                    elif searchOptions == 'ends':
                        operator = 'LIKE'
                        search_term = f"'%{searchChar}'"
                    elif searchOptions == 'contains':
                        operator = 'LIKE'
                        search_term = f"'%{searchChar}%'"
                    elif searchOptions == 'notContains':
                        operator = 'NOT LIKE'
                        search_term = f"'%{searchChar}%'"

                    if not searchColumnName:
                        # Search across all columns
                        cursor.execute(f"SHOW COLUMNS FROM {table}")
                        columns = [column[0] for column in cursor.fetchall()]
                        conditions = []
                        for col in columns:
                            conditions.append(f'{col} {operator} {search_term}')
                        query = f'SELECT * FROM {table} WHERE ' + ' OR '.join(conditions)

                    else:
                        #check if column exists
                        existing_columns = set()
                        cursor.execute(f"DESCRIBE {table}")
                        column_info = {row[0]: row[1] for row in cursor.fetchall()}
                        for column in column_info.keys():
                            existing_columns.add(column)

                        if searchColumnName not in existing_columns:
                            return f"Column '{searchColumnName}' does not exist in the table '{table}'."
                        # Search in a specific column
                        query = f'SELECT * FROM {table} WHERE {searchColumnName} {operator} {search_term}'

                    cursor.execute(query)
                    allrows = cursor.fetchall()

                    if not allrows:
                        return f"No records found matching the criteria using the selected option."
                    else:
                        # Generate HTML response with the table
                        response_html = "<html><head><title>Records</title></head><body><table style='text-align: center;' class='response-table'><tr>"

                        # Add table headers
                        for description in cursor.description:
                            response_html += f"<th class='response-column-header'>{description[0]}</th>"
                        response_html += "</tr>"

                        # Add table rows
                        for row in allrows:
                            response_html += "<tr>"
                            for cell in row:
                                cell = html.escape(str(cell)) if cell is not None else "-"  # Replace None with empty string
                                response_html += f"<td class='response-column-data'>{cell}</td>"
                            response_html += "</tr>"

                        response_html += "</table></body></html>"
                        return response_html
                else:
                    return f"Table '{table}' does not exist in the database '{self.database}'."
            else:
                return f"Database \"{database}\" does not exist."
        except Exception as e:
            return handledExceptionMessage
        
    def executeQuery(self):
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
                    queryOptions = form.getvalue("queryOptions")
                    if queryOptions == 'concat':
                        # Concatenate specific columns
                        columnsToConcat = form.getvalue("columnsToConcat")
                        concatColumnName = form.getvalue("concatColumnName")
                        displayColumns = form.getvalue("displayColumns")
                        separatorChar = form.getvalue("separatorChar")

                        separatorChar = separatorChar.replace('\\', '\\\\').replace('"', '""').replace("'", "\'")
                        concatColumnName = concatColumnName.replace('\\', '\\\\').replace('"', '""').replace("'", "\'")

                        if columnsToConcat:
                            columns_to_concat = [col.strip() for col in columnsToConcat.split(',') if col.strip()]
                            display_columns = [col.strip() for col in displayColumns.split(',') if col.strip()]

                            # Get the list of columns in the table
                            cursor.execute(f"DESCRIBE {table}")
                            columns = [column[0] for column in cursor.fetchall()]

                            # Validate column names
                            invalid_columns = [col for col in columns_to_concat if col not in columns]
                            if invalid_columns:
                                return f"Invalid column name(s): {', '.join(invalid_columns)}"
                            
                            if concatColumnName:
                                if displayColumns:
                                    # Validate column names
                                    invalid_columns = [col for col in display_columns if col not in columns]
                                    if invalid_columns:
                                        return f"Invalid column name(s): {', '.join(invalid_columns)}"
                                    
                                    display_columns = ", ".join(display_columns)
                                    columns_to_concat = ", ".join(columns_to_concat)
                                    if separatorChar:
                                        query = f'SELECT {display_columns}, CONCAT_WS("{separatorChar}", {columns_to_concat})  AS "{concatColumnName}" FROM {table}'
                                    else:
                                        separatorChar = " "
                                        query = f'SELECT {display_columns}, CONCAT_WS("{separatorChar}", {columns_to_concat}) AS "{concatColumnName}" FROM {table}'
                                else:
                                    columns_to_concat = ", ".join(columns_to_concat)
                                    if separatorChar:
                                        query = f"SELECT CONCAT_WS('{separatorChar}', {columns_to_concat}) AS '{concatColumnName}' FROM {table}"

                                    else:
                                        query = f"SELECT CONCAT_WS(' ', {columns_to_concat}) AS '{concatColumnName}' FROM {table}"

                            else:
                                concatColumnName = "Concatenated Column"
                                if displayColumns:
                                    # Validate column names
                                    invalid_columns = [col for col in display_columns if col not in columns]
                                    if invalid_columns:
                                        return f"Invalid column name(s): {', '.join(invalid_columns)}"
                                    
                                    display_columns = ", ".join(display_columns)
                                    columns_to_concat = ", ".join(columns_to_concat)
                                    if separatorChar:
                                        query = f'SELECT {display_columns}, CONCAT_WS("{separatorChar}", {columns_to_concat}) AS "{concatColumnName}" FROM {table}'
                                    else:
                                        separatorChar = " "
                                        query = f'SELECT {display_columns}, CONCAT_WS("{separatorChar}", {columns_to_concat}) AS "{concatColumnName}" FROM {table}'
                                else:
                                    columns_to_concat = ", ".join(columns_to_concat)
                                    if separatorChar:
                                        query = f"SELECT CONCAT_WS('{separatorChar}', {columns_to_concat}) AS '{concatColumnName}' FROM {table}"

                                    else:
                                        query = f"SELECT CONCAT_WS(' ', {columns_to_concat}) AS '{concatColumnName}' FROM {table}"

                        else:
                            return "Enter column(s) to concatenate!"

                    elif queryOptions == 'distinct':
                        # Get distinct results
                        columnsToDistinct = form.getvalue("columnsToDistinct")
                        if columnsToDistinct:
                            column_to_distinct = [col.strip() for col in columnsToDistinct.split(',') if col.strip()]
                            
                            # Get the list of columns in the table
                            cursor.execute(f"DESCRIBE {table}")
                            columns = [column[0] for column in cursor.fetchall()]

                            # Validate column names
                            invalid_columns = [col for col in column_to_distinct if col not in columns]
                            if invalid_columns:
                                return f"Invalid column name(s): {', '.join(invalid_columns)}"
                        
                            distinct_cols = ", ".join(column_to_distinct)
                            query = f"SELECT DISTINCT {distinct_cols} FROM {table}"
                        
                        else:
                            return "Enter column(s) to distinct!"

                    elif queryOptions == 'range':
                        # Get results within a specific range
                        columnToRange = form.getvalue("columnToRange")
                        lowerBound = form.getvalue("lowerBound")
                        upperBound = form.getvalue("upperBound")
                        
                        if not lowerBound:
                            return "Enter lower bound!"
                        
                        if not upperBound:
                            return "Enter upper bound!"
                        
                        if columnToRange:
                            column_to_range = columnToRange
                            # Check if columns already exist
                            existing_columns = set()
                            cursor.execute(f"DESCRIBE {table}")
                            column_info = {row[0]: row[1] for row in cursor.fetchall()}
                            for column in column_info.keys():
                                existing_columns.add(column)
                            
                            if column_to_range not in existing_columns:
                                return f"Column '{column_to_range}' does not exist in the table '{table}'."
                            
                            query = f'SELECT * FROM {table} WHERE {column_to_range} BETWEEN {lowerBound} AND {upperBound}'
                        else: 
                            return "Enter a column to get range!"

                    cursor.execute(query)
                    allrows = cursor.fetchall()

                    if not allrows:
                        return f"No records found matching the criteria using the selected option."
                    else:
                        # Generate HTML response with the table
                        response_html = "<html><head><title>Records</title></head><body><table style='text-align: center;' class='response-table'><tr>"

                        # Add table headers
                        for description in cursor.description:
                            response_html += f"<th class='response-column-header'>{description[0]}</th>"
                        response_html += "</tr>"

                        # Add table rows
                        for row in allrows:
                            response_html += "<tr>"
                            for cell in row:
                                cell = html.escape(str(cell)) if cell is not None else "-"  # Replace None with empty string
                                response_html += f"<td class='response-column-data'>{cell}</td>"
                            response_html += "</tr>"

                        response_html += "</table></body></html>"
                        return response_html
                else:
                    return f"Table '{table}' does not exist in the database '{self.database}'."
            else:
                return f"Database \"{database}\" does not exist."
        except Exception as e:
            return e
        
    def performJoin(self):
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
                db.cmd_init_db(self.database)

                
                numTablesToJoin = int(form.getvalue("numTablesToJoin"))
                tablesToJoin = form.getvalue("tablesToJoin")
                joinTypes = form.getvalue("joinType")
                primaryKeyColumns = form.getvalue("primaryKeyColumns")
                foreignKeyColumns = form.getvalue("foreignKeyColumns")
                joinColumnQ = form.getvalue("joinColumnQ")  # Boolean value from the form
                joinColumns = form.getvalue("joinColumns")

                # Split input values into lists using space, comma, or newline as separators
                tablesToJoin = re.split(r'[\s,]+', tablesToJoin)
                joinTypes = re.split(r'[\s,]+', joinTypes)
                primaryKeyColumns = re.split(r'[\s,]+', primaryKeyColumns)
                foreignKeyColumns = re.split(r'[\s,]+', foreignKeyColumns)
                joinColumns = re.split(r'[\s,]+', joinColumns)

                # Verify that the number of tables, primary key columns, and foreign key columns match
                if len(tablesToJoin) != numTablesToJoin:
                    return "Mismatch in the number of tables and table names."

                if len(joinTypes) != numTablesToJoin - 1:
                    return "Mismatch in the number of join types."
                

                join_conditions = []

                # Construct the SQL query based on user input
                sql_query = f"SELECT * FROM {tablesToJoin[0]}"

                for i in range(1, numTablesToJoin):
                    join_condition = joinTypes[i - 1].lower()
                    if join_condition not in ['inner', 'left', 'right', 'full-outer']:
                        return "Invalid join type specified."

                    else:
                        if joinColumnQ == "true":
                            if len(joinColumns) != numTablesToJoin:
                                return "Mismatch in the number of join columns."
                            
                            if join_condition == 'full-outer':
                                
                                join_condition = joinColumns[i - 1]
                                # Simulate FULL OUTER JOIN using LEFT JOIN and RIGHT JOIN
                                left_join_query = f" LEFT JOIN {tablesToJoin[i]} ON {tablesToJoin[i - 1]}.{join_condition} = {tablesToJoin[i]}.{join_condition}"
                                right_join_query = f" SELECT * FROM {tablesToJoin[i - 1]} RIGHT JOIN {tablesToJoin[i]} ON {tablesToJoin[i - 1]}.{join_condition} = {tablesToJoin[i]}.{join_condition};\n"
                                sql_query += left_join_query + f" UNION ALL " + right_join_query

                            else:
                                join_condition = joinColumns[i - 1]
                                sql_query += f" {joinTypes[i - 1].upper()} JOIN {tablesToJoin[i]}"   
                                sql_query += f" ON {tablesToJoin[i - 1]}.{join_condition} = {tablesToJoin[i]}.{join_condition}"

                                
                        else:
                            if len(primaryKeyColumns) != numTablesToJoin and len(foreignKeyColumns) != numTablesToJoin:
                                return "Mismatch in the number of primary key and foreign key columns."
                            
                            if join_condition == 'full-outer':
                                # Simulate FULL OUTER JOIN using LEFT JOIN and RIGHT JOIN
                                left_join_query = f" LEFT JOIN {tablesToJoin[i]} ON {tablesToJoin[i - 1]}.{primaryKeyColumns[i - 1]} = {tablesToJoin[i]}.{foreignKeyColumns[i - 1]}"
                                right_join_query = f" SELECT * FROM {tablesToJoin[i - 1]} RIGHT JOIN {tablesToJoin[i]} ON {tablesToJoin[i - 1]}.{primaryKeyColumns[i - 1]} = {tablesToJoin[i]}.{foreignKeyColumns[i - 1]} WHERE {tablesToJoin[i - 1]}.{primaryKeyColumns[i - 1]} IS NULL;\n"
                                sql_query += left_join_query + f" UNION ALL" + right_join_query

                            else:    
                                join_condition = (primaryKeyColumns[i - 1], foreignKeyColumns[i - 1])

                                join_conditions.append(join_condition)

                                sql_query += f" {joinTypes[i - 1].upper()} JOIN {tablesToJoin[i]}"

                                if isinstance(join_condition, tuple):
                                    primary_key, foreign_key = join_condition
                                    sql_query += f" ON {tablesToJoin[i - 1]}.{primary_key} = {tablesToJoin[i]}.{foreign_key}"
                                else:
                                    sql_query += f" ON {tablesToJoin[i - 1]}.{join_condition} = {tablesToJoin[i]}.{join_condition}"

                cursor.execute(sql_query)

                
                allrows = cursor.fetchall()

                if not allrows:
                    return f"No records found matching the criteria using the selected option."
                else:
                        # Generate HTML response with the table
                    response_html = "<html><head><title>Records</title></head><body><table style='text-align: center;' class='response-table'><tr>"

                        # Add table headers
                    for description in cursor.description:
                        response_html += f"<th class='response-column-header'>{description[0]}</th>"
                    response_html += "</tr>"

                        # Add table rows
                    for row in allrows:
                        response_html += "<tr>"
                        for cell in row:
                            cell = html.escape(str(cell)) if cell is not None else "-"  # Replace None with empty string
                            response_html += f"<td class='response-column-data'>{cell}</td>"
                        response_html += "</tr>"

                    response_html += "</table></body></html>"
                    return response_html
            else:
                return f"Database \"{database}\" does not exist."
        except Exception as e:
            return e
        
    def deleteRows(self):
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

                    if not pk: 
                        return f"Enter Primary Key Column Name!"
                    
                    ids = form.getvalue("primaryKeys")
                    
                    if not ids:
                        return f"Enter Primary Key Values!"
                    
                    if ids and pk:
                        ids = ids.splitlines()
                        ids = ", ".join([f"'{value.strip()}'" for value in ids])
                        command = f"DELETE FROM {table} WHERE ({pk}) IN ({ids})"
                        cursor.execute(command)
                        db.commit()
                        db.close()
                        return f"Record(s) of id {ids} has/have been deleted"
                    
                    else: 
                        return f"No criteria specified!"
                    
                else:
                    return f"Table '{table}' does not exist in the database '{self.database}'."
            else:
                return f"Database \"{database}\" does not exist."
        except Exception as e:
            return handledExceptionMessage
        
    def deleteRecords(self):
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
                    pkRange = form.getvalue("pkRange")
                    specificColumnByPKRange = form.getvalue("specificColumnByPKRange")
                    allInSpecificColumn = form.getvalue("allInSpecificColumn")
                    allInTable = form.getvalue("allInTable")
                    startingPK = form.getvalue("startingPK")
                    endingPK = form.getvalue("endingPK")
                    specificColumn = form.getvalue("specificColumn")


                    if pkRange != "true" and specificColumnByPKRange != "true" and allInSpecificColumn != "true" and allInTable != "true":
                        return "You have to Check a box first!"
                    
                    elif pkRange == "true" and specificColumnByPKRange != "true" and allInSpecificColumn != "true" and allInTable != "true":
                        if not startingPK:
                            return "Enter starting primary key value!"
                        if not endingPK:
                            return "Enter starting primary key value!"
                        if not pk:
                            return "Enter primary key column name!"
                        
                        cursor.execute(f"DELETE FROM {table} WHERE {pk} BETWEEN {startingPK} AND {endingPK}")

                    elif specificColumnByPKRange == "true" and pkRange != "true" and allInSpecificColumn != "true" and allInTable != "true":
                        if not startingPK:
                            return "Enter starting primary key value!"
                        if not endingPK:
                            return "Enter starting primary key value!"
                        if not pk:
                            return "Enter primary key column name!"
                        if not specificColumn:
                            return "Enter specific column(s)!"
                        
                        cursor.execute(f"UPDATE {table} SET {specificColumn} = NULL WHERE {pk} BETWEEN {startingPK} AND {endingPK}")
                    
                    elif allInTable == "true" and pkRange != "true" and allInSpecificColumn != "true" and specificColumnByPKRange != "true":
                        cursor.execute(f"DELETE FROM {table}")

                    elif allInSpecificColumn == "true" and pkRange != "true" and specificColumnByPKRange != "true" and allInTable != "true":
                        if not specificColumn:
                            return "Enter specific column(s)!"
                        
                        cursor.execute(f"UPDATE {table} SET {specificColumn} = NULL")

                    else:
                        return "Ensure you only check one box!"

                    db.commit()
                    return "Records deleted successfully."
                    
                else:
                    return f"Table '{table}' does not exist in the database '{self.database}'."
            else:
                return f"Database \"{database}\" does not exist."
        except Exception as e:
            return handledExceptionMessage
        
    def updateRecords(self):
        try:
            sql = ""
            value_list = ""
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
                    # Get primary key column name and entries from the HTML form
                    ids = form.getvalue("primaryKeys")
                    ids = ids.strip()
                    headers_input = form.getvalue("dataColumnNames")
                    entries_input = form.getvalue("dataColumnValues").splitlines()
                    
                    if not pk:
                        return "Enter primary key column name!"
                    
                    if not ids:
                        return "Enter primary key column values!"
                    
                    if not headers_input or not entries_input:
                        return "Enter column headers and entries."
                    
                    headers = [col.strip() for col in headers_input.split(',')]
                    pk_values = [value.strip() for value in ids.splitlines()]
                    
                    if len(headers) == 0:
                        return "No column headers provided."
                    
                    if len(pk_values) == 0:
                        return "No primary key values provided."
                    
                    # Check if columns exist
                    existing_columns = set()
                    cursor.execute(f"DESCRIBE {table}")
                    column_info = {row[0]: row[1] for row in cursor.fetchall()}
                    for column in column_info.keys():
                        existing_columns.add(column)

                    for header in headers:
                            if header not in existing_columns:
                                return f"Column '{header}' does not exist in the table '{table}'."
                            
                    #values_list = []
                    #sql = f"UPDATE {table} SET {', '.join([f'{header} = %s' for header in headers if header in existing_columns])} WHERE {pk} = %s"
                    
                    for pk_value, entry_line in zip(pk_values, entries_input):
                        values = [value.strip() for value in entry_line.split(',')]
                        
                        # Get the original values from the database
                        original_values = {}
                        for header in headers:
                            cursor.execute(f"SELECT {header} from {table} WHERE {pk} = '{pk_value}'")
                            original = cursor.fetchone()
                            original_values[header] = original[0]
                        
                        # Ensure that values and headers match in length
                        if len(values) < len(headers):
                            values.extend([None] * (len(headers) - len(values)))
                        elif len(values) > len(headers):
                            values = values[:len(headers)]
                        
                        # Iterate through the values and replace blank ones with original values
                        for i, value in enumerate(values):
                            if value is None or not value.strip():
                                values[i] = original_values[headers[i]]
                        
                        # Create a list of update values for each header
                        update_values = [value if header in existing_columns else original_values[header] for header, value in zip(headers, values)]
                        
                        # Pad the list with None for headers not provided for in the form
                        update_values.extend([original_values[header] if header in existing_columns else None for header in headers[len(update_values):]])
                        
                        # Construct the SQL statement for updating the record
                        update_sql = f"UPDATE {table} SET " + ", ".join([f"{header} = %s" for header in headers]) + f" WHERE {pk} = '{pk_value}'"
                        
                        # Execute the update SQL statement
                        cursor.execute(update_sql, update_values)
                        db.commit()

                    if cursor.rowcount > 0:
                        return f"Record(s) successfully updated."
                    else:
                        return "No records were updated."
                    
                    
                else:
                    return f"Table '{table}' does not exist in the database '{self.database}'."
            else:
                return f"Database \"{database}\" does not exist."
        except Exception as e:
            return handledExceptionMessage

# Perform the requested action and generate a response
response = ""
oracle = DBM(host, user, password, database)


if actiond == "addRecords":
    response = oracle.addRecords()
elif actiond == "displayKeys":
    response = oracle.displayKeys()
elif actiond == "displayRecords":
    response = oracle.displayRecords()
elif actiond == "searchRecords":
    response = oracle.searchRecords()
elif actiond == "executeQuery":
    response = oracle.executeQuery()
elif actiond == "performJoin":
    response = oracle.performJoin()
elif actiond == "deleteRows":
    response = oracle.deleteRows()
elif actiond == "deleteRecords":
    response = oracle.deleteRecords()
elif actiond == "updateRecords":
    response = oracle.updateRecords()

# Print the message directly
print(f"Content-type: text/html\n\n{response}")