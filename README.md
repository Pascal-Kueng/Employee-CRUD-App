# Employee-CRUD-App

This was one of my first projects after learning the basics of Python. 
Here I used Tkinter and SQL to create a GUI to manage a database of people one can enter. 

## Setup
When opening the App for the first time, simply click on "Insert" (optionally already fill out the fields for "Employee Name" and "Department" beforehand.
An SQL Database in the folder of the scipts will be created. 

## Search Employees
Typing the EmployeeID into the first field, will autofill the fields below. 
To search by name or department, simply start typing the information into the appropriate fields. On the right, suggestions will update on the fly. Double clicking on a suggestion inserts the information into the fields. 

## Other functionality
**You must first select an employee by using one of the methods mentioned above.** Then, you may use "Fetch" for more Infos, "Update" to change infos, or "Delete". 
You may switch between light and dark theme. Every time the App loads or switches themes, a new random image from the Lorem Pixum API (https://picsum.photos/) will be loaded. 
If internet is not available, it will use the two backup images in the folder ("dark.jpg", "light.jpg"). 
