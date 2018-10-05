# CSE310 Programming Homework #1

## Description

Linux-Server.py is a python script which starts a simple server that is 
designed for use on Linux. You can pass in a preferred port via command 
line arguments, or just run the program without arguments and the program
will use the hard-coded default port of 8000. If the server is unable to
bind neither the custom port nor the default, it prompts the user for a 
new port. The server supports the following commands:

* GET [key] - Retrieve a value by using a key
* PUT [key] [value] - Set a key-value pair
* DELETE [key] - Delete a key-value pair
* CLEAR - Delete all key-value pairs
* QUIT - Close the connection to the server
* OFF - Close the connection and shut down the server

## Testing

Testing can be done as shown at the bottom of the homework PDF.

## Author

Name: Kuba Gasiorowski

ID: 109776237
