# an App with a GUI that let's you manage a database of employees.
# Author Pascal Marcel Küng, University of Zürich.
# This is a project simply to practice my first steps with Tkinter.
# For my next project I will work using classes.
from tkinter import *
from tkinter import messagebox
import sqlite3
# To show the random picture from the API:
from urllib.request import urlopen
from PIL import ImageTk, Image
import io

# This clear function is used to empty all fields of the GUI


def clear():
    enter_id.delete(0, 'end')
    enter_name.delete(0, 'end')
    enter_dep.delete(0, 'end')
    show_data.delete(0, 'end')


# Calling the 2nd GUI Window (mask to enter deatils etc.)
def mask(id):
    # Set colors according to theme
    global window
    global bg
    window = Toplevel()
    window.title('Employee Details')
    window.resizable(False, False)

    font = ('Sans Serif', 12)
    if theme_switch['text'] == 'Dark Theme':
        bg = bg_l
        fg = 'BLACK'
        ac = ac_l
        ac2 = ac2_l
    if theme_switch['text'] == 'Light Theme':
        bg = bg_d
        fg = 'WHITE'
        ac = ac_d
        ac2 = ac2_d

    window.configure(bg=bg)

    # Add padding from the top to the content
    pad = Label(window,
                font=('Serif', 5),
                bg=bg,
                fg=bg)
    pad.grid(row=0, column=1)

    # All labels
    lbl_id = Label(window, text='ID: ')
    lbl_name = Label(window, text='Name: ')
    lbl_dep = Label(window, text='Department: ')
    lbl_tel = Label(window, text='Tel. Nr.: ')
    lbl_email = Label(window, text='Email: ')
    lbl_adress = Label(window, text='Adress: ')
    lbl_salary = Label(window, text='Salary: ')

    for idx, val in enumerate([lbl_id, lbl_name, lbl_dep, lbl_tel, lbl_email, lbl_adress, lbl_salary]):
        val.configure(font=font,
                      bg=bg,
                      fg=fg)
        val.grid(column=1,
                 row=idx+1,
                 columnspan=2,
                 sticky='W',
                 padx=10,
                 pady=8)

    # All Entry Fields
    global ent_id
    global ent_name
    global ent_dep
    global ent_tel
    global ent_email
    global ent_adress
    global ent_salary

    ent_id = Entry(window)
    ent_name = Entry(window)
    ent_dep = Entry(window)
    ent_tel = Entry(window)
    ent_email = Entry(window)
    ent_adress = Entry(window)
    ent_salary = Entry(window)

    for idx, val in enumerate([ent_id, ent_name, ent_dep, ent_tel, ent_email, ent_adress, ent_salary]):
        val.configure(bg=ac2,
                      width=50)
        val.grid(column=3,
                 row=idx+1,
                 columnspan=2,
                 sticky='E',
                 padx=20)
    # All buttons
    global close
    close = Button(window,
                   text='Close',
                   font=('Sans Serif', 15),
                   bg=ac,
                   fg=fg,
                   command=lambda: window.destroy())
    close.bind('<Return>', lambda x: window.destroy())
    close.grid(row=10,
               column=1,
               columnspan=20,
               sticky="WE",
               padx=10,
               pady=10)


#  Functions to manage actual database.


def insertData(id, name, dep):
    mask(id)  # call window
    ent_id.insert(0, 'Generated automatically')  # insert all the info already typed.
    ent_id.configure(state='readonly', readonlybackground=bg, fg='Grey')

    ent_name.insert(0, name)
    ent_dep.insert(0, dep)

    # makes the button insert the data, when pressed next
    close.configure(text='INSERT', command=insertDataOK)
    close.bind('<Return>', lambda x: insertDataOK())


def insertDataOK():
    id, name, dep, tel, email, adress, salary = [
        ent_id.get(), ent_name.get(), ent_dep.get(), ent_tel.get(), ent_email.get(), ent_adress.get(), ent_salary.get()]
    if name == '' or dep == '':
        messagebox.showerror(
            'Cannot Insert',
            'Name and Department required to add employee!\nEmployee ID will be generated automatically'
        )
        return

    # Check if record already esists.
    cur.execute('''SELECT id FROM Employee WHERE
                name = (?)''', (name,))
    if cur.fetchone() != None:
        messagebox.showerror(
            'Cannot Insert',
            'This Employee already esits!'
        )
        return

    # Insert into Department table (if department new)
    # Or grab the id of the department.
    cur.execute('''INSERT OR IGNORE INTO Department (name)
                VALUES (?)''', (dep,))
    cur.execute('''SELECT id FROM Department WHERE
                name = (?)''', (dep,))
    department_id = cur.fetchone()[0]

    # Insert Into Employee Table

    cur.execute('''INSERT INTO Employee (name, department, tel, email, adress, salary)
                VALUES (?, ?, ?, ?, ?, ?)''', (name, department_id, tel, email, adress, salary))

    conn.commit()
    clear()
    window.destroy()  # supposed to close the window (entry)
    messagebox.showinfo('Success', 'Employee addes to Database')


def updateData(id, name, dep):
    messagebox.showinfo('Instructions',
                        'The Employee ID cannot be changed. \nAll changes are applied to the employee with the specified ID.')

    if getData(id) == None:  # call the window filled with all data about employee (with specified ID)
        clear()
        return
    for i in [ent_name, ent_dep, ent_tel, ent_email, ent_adress, ent_salary]:
        i.configure(state=NORMAL)

    close.configure(text='UPDATE', command=updateDataOK)
    close.bind('<Return>', lambda x: updateDataOK())


def updateDataOK():
    # Insert Into Employee Table
    id, name, dep, tel, email, adress, salary = [
        ent_id.get(), ent_name.get(), ent_dep.get(), ent_tel.get(), ent_email.get(), ent_adress.get(), ent_salary.get()]
    if name == '' or dep == '':
        messagebox.showerror(
            'Cannot Update',
            'Name and Department required!'
        )
        return

    cur.execute('''INSERT OR IGNORE INTO Department (name)
                VALUES (?)''', (dep,))
    cur.execute('''SELECT id FROM Department WHERE
                name = (?)''', (dep,))
    department_id = cur.fetchone()[0]

    # Update
    cur.execute('''UPDATE Employee SET
                name = (?),
                department = (?),
                tel = (?),
                email = (?),
                adress = (?),
                salary = (?)
                WHERE id = (?)''', (name, department_id, tel, email, adress, salary, id))

    conn.commit()
    clear()
    window.destroy()  # supposed to close the window (entry)
    messagebox.showinfo('Success', 'Employee updated')


def getData(id):
    # Search DB. If empty, return messagebox. Else, start mask.
    cur.execute('''SELECT Employee.id, Employee.name, Department.name, Employee.tel, Employee.email, Employee.adress, Employee.salary
                FROM Employee JOIN Department
                ON Employee.department = Department.id
                WHERE Employee.id = (?)
                LIMIT 1''', (id,))
    global result
    result = cur.fetchone()
    if result == None:
        messagebox.showerror('Not found',
                             'This Employee does not exist.\nMake sure to enter an existing ID.')
        return None

    mask(id)  # Calling the Window
    for idx, val in enumerate([ent_id, ent_name, ent_dep, ent_tel, ent_email, ent_adress, ent_salary]):
        val.insert(0, result[idx])
        val.configure(state='readonly', readonlybackground='Light Grey')
    clear()
    return 5


def deleteData(id, name, dep):
    if id == '' or name == '' or dep == 0:
        messagebox.showerror('Specify Employee', 'Specify an employee to delete')
        return
    yn = messagebox.askquestion(
        'Delete Employee?', f'Are you sure you want to delete\nemployee {name} from {dep}?')
    if yn == 'no':
        return
    cur.execute('''DELETE FROM Employee
                WHERE id = (?) and name = (?)''', (id, name))
    conn.commit()
    clear()

# Functions that adaptively search the database every time a character is entered_d into one of the fields and provides suggestions


def fill_id(x):
    id = enter_id.get()  # Reading the value of the id field
    if id == '' or id == ' ':
        # deleting all the fields, to make sure the 'nothingness' donesn't get matched with the whole database.
        clear()
        return
    cur.execute('''SELECT Employee.name, Department.name
                FROM Employee JOIN Department
                ON Employee.department = Department.id
                WHERE Employee.id = (?)''', (id,))  # Join the dataset in order to display the info
    global result
    result = cur.fetchone()

    enter_dep.delete(0, 'end')
    enter_name.delete(0, 'end')
    enter_name.delete(0, 'end')
    if result == None:  # delete the text if no match.
        return
    enter_name.insert(0, result[0])  # write the name
    enter_dep.insert(0, result[1])  # write the department


def fill_name(x):
    name = enter_name.get()  # Reading the content of the field with every keypress
    if name == '' or name == ' ':  # Making sure that not all entries are found as matching, due to the space or the 'nothing'
        show_data.delete(0, 'end')
        return
    cur.execute('''SELECT Employee.id, Employee.name, Department.name
                FROM Employee JOIN Department
                ON Employee.department = Department.id
                WHERE Employee.name LIKE (?)
                LIMIT 10''', (f'%{name}%',))  # return the first 10 that have a partially matching string
    global result
    result = cur.fetchall()
    show_data.delete(0, 'end')
    if result == []:  # If no result, stop
        return
    for i in result:  # Filling the output box with the Suggestions fo employees
        show_data.insert('end', f'{i[0]}     {i[1]}      {i[2]}')


def fill_dep(x):
    name = enter_dep.get()
    if name == '' or name == ' ':
        show_data.delete(0, 'end')
        return
    cur.execute('''SELECT Employee.id, Employee.name, Department.name
                FROM Employee JOIN Department
                ON Employee.department = Department.id
                WHERE Department.name LIKE (?)
                LIMIT 10''', (f'%{name}%',))
    global result
    result = cur.fetchall()
    show_data.delete(0, 'end')
    if result == []:
        return
    for i in result:
        show_data.insert('end', f'{i[0]}     {i[1]}      {i[2]}')


def listbox_choose(x):
    index = show_data.curselection()[0]  # Getting the index of the double clicked listing
    emp = result[index]  # Getting the actual listing

    enter_id.delete(0, 'end')  # Deleting, then filling the ID-Field
    enter_id.insert(0, emp[0])

    enter_name.delete(0, 'end')  # Deleting, then filling the name-field
    enter_name.insert(0, emp[1])

    enter_dep.delete(0, 'end')  # Same with the department field
    enter_dep.insert(0, emp[2])


def picture(url, backup):
    try:
        bytes = urlopen(url).read()
        stream = io.BytesIO(bytes)
        img = Image.open(stream)
        image = ImageTk.PhotoImage(img)
    except:
        with Image.open(backup) as img:
            image = ImageTk.PhotoImage(img)
    finally:
        return image


def theme():
    if theme_switch['text'] == 'Light Theme':
        theme_switch.configure(text='Dark Theme')
        root.configure(bg=bg_l)
        for i in [employee_id, employee_name, department_id, pad]:
            i.configure(bg=bg_l,
                        fg=color_font_l)
        for i in [enter_id, enter_dep, enter_name, insert_btn, update_btn]:
            i.configure(bg=ac2_l)
        for i in [theme_switch, show_data]:
            i.configure(bg=ac_l,
                        fg=color_font_l)
        reset_btn.configure(bg=ac_l)
        image = picture('https://picsum.photos/610/100?.jpg', 'light.jpg')
        pici.configure(image=image)
        pici.image = image
        return

    if theme_switch['text'] == 'Dark Theme':
        theme_switch.configure(text='Light Theme')
        root.configure(bg=bg_d)
        for i in [employee_id, employee_name, department_id, pad]:
            i.configure(bg=bg_d,
                        fg=color_font_d)
        for i in [enter_id, enter_dep, enter_name, insert_btn, update_btn]:
            i.configure(bg=ac2_d)
        for i in [theme_switch, show_data]:
            i.configure(bg=ac_d,
                        fg=color_font_d)
        reset_btn.configure(bg=ac_d)
        image = picture('https://picsum.photos/610/100?grayscale.jpg', 'dark.jpg')
        pici.configure(image=image)
        pici.image = image
        return


###############################################################################
###############################################################################
if __name__ == '__main__':
    # Open or create database
    conn = sqlite3.connect('crud.sqlite')
    cur = conn.cursor()

    # Do some setup of the database
    # Create Tables if there are none yet. (main indicates if it is their main departmentor not (1 or 0))

    cur.executescript('''
    CREATE TABLE IF NOT EXISTS Department (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS Employee (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE,
        tel INTEGER,
        email TEXT,
        adress TEXT,
        salary INTEGER,
        department INTEGER NOT NULL
    )
    ''')

    conn.commit()

    # Dark color theme for GUI
    bg_d = '#282828'
    ac_d = '#404040'
    ac2_d = '#B3B3B3'
    color_font_d = 'WHITE'

    # Light color theme
    bg_l = '#FBF8F1'
    ac_l = '#F7ECDE'
    ac2_l = '#E9DAC1'
    color_font_l = 'BLACK'

    # Settings that stay the same
    red_d = '#FF4C29'
    green_d = '#347C2C'
    font = ('Serif', 12)
    font_inp = ('Serif', 10)

    # Set up tkinter for GUI construction
    root = Tk()
    root.title('Employee Management')
    root.resizable(False, False)
    root.configure(bg=bg_d)

    # Add padding from the top to the content
    pad = Label(root,
                font=('Serif', 2),
                bg=bg_d,
                fg=bg_d)
    pad.grid(row=0, column=1)

    # Adding Labels (for entry fields)
    employee_id = Label(root, text='Employee ID: ')
    employee_name = Label(root, text='Employee Name: ')
    department_id = Label(root, text='Department: ')

    for idx, val in enumerate([employee_id, employee_name, department_id]):
        val.configure(font=font,
                      bg=bg_d,
                      fg=color_font_d)
        val.grid(column=1,
                 row=idx+1,
                 columnspan=2,
                 sticky='W',
                 padx=5)

    # Adding entry fields

    enter_id = Entry(root)
    enter_id.bind('<KeyRelease>', fill_id)

    enter_name = Entry(root)
    enter_name.bind('<KeyRelease>', fill_name)

    enter_dep = Entry(root)
    enter_dep.bind('<KeyRelease>', fill_dep)

    # Draw in grid
    for idx, val in enumerate([enter_id, enter_name, enter_dep]):
        val.configure(bg=ac2_d)
        val.grid(column=3,
                 row=idx+1,
                 columnspan=2,
                 sticky='E',
                 padx=10)

    # Create buttons (first row)
    insert_btn = Button(root,
                        text='Insert',
                        font=font,
                        bg=ac2_d,
                        command=lambda: insertData(enter_id.get(),
                                                   enter_name.get(),
                                                   enter_dep.get())
                        )
    insert_btn.bind('<Return>', lambda x: insertData(enter_id.get(),  # This makes sure the enter key also does the function
                                                     enter_name.get(),
                                                     enter_dep.get()))

    update_btn = Button(root,
                        text='Update',
                        font=font,
                        bg=ac2_d,
                        command=lambda: updateData(enter_id.get(),
                                                   enter_name.get(),
                                                   enter_dep.get())
                        )
    update_btn.bind('<Return>', lambda x: updateData(enter_id.get(),  # This makes sure the enter key also does the function
                                                     enter_name.get(),
                                                     enter_dep.get()))
    get_btn = Button(root,
                     text='Fetch',
                     font=font,
                     bg=green_d,
                     command=lambda: getData(enter_id.get())
                     )
    get_btn.bind('<Return>', lambda x: getData(enter_id.get()))
    delete_btn = Button(root,
                        text='Delete',
                        font=font,
                        bg=red_d,
                        command=lambda: deleteData(enter_id.get(),
                                                   enter_name.get(),
                                                   enter_dep.get())
                        )
    delete_btn.bind('<Return>', lambda x: deleteData(enter_id.get(),  # This makes sure the enter key also does the function
                                                     enter_name.get(),
                                                     enter_dep.get()))
    # Place buttons
    for idx, val in enumerate([insert_btn, update_btn, get_btn, delete_btn]):
        val.grid(column=idx+1,
                 row=4,
                 padx=10,
                 pady=10,
                 sticky='EW')

    # Reset button
    reset_btn = Button(root,
                       text='Clear Fields',
                       font=font,
                       command=clear,
                       bg=ac_d,
                       fg=red_d)
    reset_btn.bind('<Return>', lambda x: clear())
    reset_btn.grid(column=1,
                   row=5,
                   columnspan=4,
                   padx=10,
                   pady=10,
                   sticky='EW')
    # Insert Random picture (greyscale)
    image = picture('https://picsum.photos/610/100?grayscale', 'dark.jpg')
    pici = Label(root, image=image)
    pici.grid(column=1,
              row=6,
              columnspan=10,
              pady=10)
    pici.bind('<Button-1>', lambda x: print('Nice Picture, right?'))
    # Add Listbox (to show output)

    show_data = Listbox(root,
                        bg=ac_d,
                        fg=color_font_d,
                        width=50,
                        )
    show_data.grid(column=5,
                   row=1,
                   rowspan=4,
                   columnspan=5,
                   padx=10,
                   pady=10)
    show_data.bind('<Double-Button-1>', listbox_choose)
    # Add button to switch theme

    theme_switch = Button(root,
                          font=font,
                          text='Light Theme',
                          bg=ac_d,
                          fg=color_font_d,
                          command=theme
                          )
    theme_switch.bind('<Return>', lambda x: theme())
    theme_switch.grid(column=9,
                      row=5)

    root.mainloop()
