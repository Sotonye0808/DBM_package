# NOTE: 
## Working on a version that will be functional and independent of installation or server dependencies!
### MySQL Database Manager
This project is a web-application that serves as an alternative to using the MySQL workbench (although one still needs to create a connection first). It has a much more pleasant UI and easy-to-use structure, with simple buttons to carry out database queries such as basic CRUD operations and other tasks like Joins, search, etc.

Project built with a Python CGI script, which renders some functionality null unless properly configured.
Anyone keen on using this project will need to pull it, get the Apache server (other similar services like Azure may suffice) up and running, store it there and perform the necessary configurations to handle the CGI script.
Perhaps modifications will be made to enable it work without any of that.
