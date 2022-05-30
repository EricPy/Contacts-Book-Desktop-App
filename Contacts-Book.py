import tkinter as tk
import sqlite3 as sql
from tkinter import messagebox
from turtle import width

root = tk.Tk()
root.title("Contacts")
root.geometry("600x200")

# Connecting / Creating database
database = sql.connect("Phone-numbers.db")

# Create cursor to do stuff with
c = database.cursor()

# Creating the table (if does not already exist)
try:
    c.execute("""CREATE TABLE contacts (
        name text,
        number text,
        address text,
        birthday text
        )""")
except:
    pass


def proceed():
    # Connecting / Creating database
    database = sql.connect("Phone-numbers.db")

    # Create cursor to do stuff with
    c = database.cursor()

    # Insert data
    c.execute("""INSERT INTO contacts VALUES (
        :name,
        :number,
        :address,
        :birthday
        )""", 
        {
            'name':name_input.get(),
            'number':number_input.get(),
            'address':address_input.get(),
            'birthday':birthday_input.get()
        })

    # Committing the changes
    database.commit()

    # Close the connection
    database.close()

    # Clearing the input
    name_input.delete(0,tk.END)
    number_input.delete(0,tk.END)
    address_input.delete(0,tk.END)
    birthday_input.delete(0,tk.END)

def query():

    #Create a new window
    query_win = tk.Toplevel()
    query_win.title("Contact Book")

    tk.Label(query_win, text="Entry Number").grid(row=0,column=0,sticky="w")
    id_num = tk.Entry(query_win, width=50)
    id_num.grid(row=0, column=1)

    def refresh():
        query_win.destroy()
        query()

    def edit():
        
        if id_num.get() in oid_list:

            oid_num = id_num.get()

            edit_win = tk.Toplevel()
            edit_win.title(f"Edit Contact")
            edit_win.geometry("370x100")

            tk.Label(edit_win, text=f"(Entry {oid_num})").grid(row=0, column=0, pady=5, padx=3)
            
            # Dropdown menu
            choices = ["Name", "Phone Number", "Address", "Birthday"]
            chosen = tk.StringVar()
            chosen.set(choices[0])

            drop = tk.OptionMenu(edit_win, chosen, *choices)
            drop.config(width=26)
            drop.grid(row=0, column=1, pady=5, padx=2)

            tk.Label(edit_win, text="Updated :").grid(row=1, column=0, sticky="w", padx=3)
            new_data = tk.Entry(edit_win, width=30)
            new_data.grid(row=1, column=1, padx=2)

            def change():
                
                data_type = chosen.get()

                column_name_equivalents = {"Name" : "name",
                                           "Phone Number" : "number",
                                           "Address" : "address",
                                           "Birthday" : "birthday"}

                desired_column = column_name_equivalents[data_type]

                database = sql.connect("Phone-numbers.db")
                c = database.cursor()

                c.execute(f"""UPDATE contacts SET

                    {desired_column} = :updated_info
                
                    WHERE oid = :oid""", 
                    {
                    'updated_info' : new_data.get(),
                    'oid' : oid_num
                    })

                database.commit()
                database.close()

                new_data.delete(0,tk.END)

                refresh()
                edit_win.destroy()

            tk.Button(edit_win, text="Submit Change", width=20, command=change).grid(row=2, column=0, columnspan=2)
            
        else:
            pass

    def erase():
        if id_num.get() in oid_list:
            database = sql.connect("Phone-numbers.db")
            c = database.cursor()

            c.execute(f"DELETE FROM contacts WHERE oid = {id_num.get()}")

            database.commit()
            database.close()

            id_num.delete(0, tk.END)

            refresh()
        else:
            pass

    def erase_all():

        x = messagebox.askquestion("Warning","Doing this will delete all contacts, which cannot be reversed. \n\nAre you sure you want to proceed?")

        if x == "yes":
            database = sql.connect("Phone-numbers.db")
            c = database.cursor()

            c.execute(f"DELETE FROM contacts")

            database.commit()
            database.close()

            id_num.delete(0, tk.END)

            query_win.destroy()
        else:
            pass

    
    tk.Button(query_win, text="⟳", command=refresh).grid(row=0,column=2)
    tk.Button(query_win, text="Edit Entry", command=edit, width= 55).grid(row=1, column=0, columnspan=3)
    tk.Button(query_win, text="Delete Entry", command=erase, width= 55).grid(row=2, column=0, columnspan=3)
    tk.Button(query_win, text="Delete All", command=erase_all, width= 55).grid(row=3, column=0, columnspan=3)

    #Fetching and displaying Data
    database = sql.connect("Phone-numbers.db")
    c = database.cursor()

    c.execute("SELECT *,oid FROM contacts")
    records = c.fetchall()

    count = 1

    for record in records:
        if count%2 == 0: #If it's even put it on the right side
            Dataframe = tk.LabelFrame(query_win, text=f"Entry {record[-1]}")
            Dataframe.grid(row=count+2,column=1, pady=5)

            tk.Label(Dataframe, text=f"Name: {record[0]}").grid(row=0, column=0, sticky="w")
            tk.Label(Dataframe, text=f"Phone Number: {record[1]}").grid(row=1, column=0, sticky="w")
            tk.Label(Dataframe, text=f"Address: {record[2]}").grid(row=2, column=0, sticky="w")
            tk.Label(Dataframe, text=f"Birthday: {record[3]}").grid(row=3, column=0, sticky="w")
        else:
            Dataframe = tk.LabelFrame(query_win, text=f"Entry {record[-1]}")
            Dataframe.grid(row=count+3,column=0,columnspan=2,sticky="w", pady=5, padx=(15,0))

            tk.Label(Dataframe, text=f"Name: {record[0]}").grid(row=0, column=0, sticky="w")
            tk.Label(Dataframe, text=f"Phone Number: {record[1]}").grid(row=1, column=0, sticky="w")
            tk.Label(Dataframe, text=f"Address: {record[2]}").grid(row=2, column=0, sticky="w")
            tk.Label(Dataframe, text=f"Birthday: {record[3]}").grid(row=3, column=0, sticky="w")

        count+=1

    oid_list = [str(record[-1]) for record in records]

    #Closing everything
    database.commit()
    database.close()

# Entering data into the table
name_input = tk.Entry(root, width=50)
name_input.grid(row=0,column=1, pady=(10,2))

number_input = tk.Entry(root, width=50)
number_input.grid(row=1,column=1, pady=(0,2))

address_input = tk.Entry(root, width=50)
address_input.grid(row=2,column=1, pady=(0,2))

birthday_input = tk.Entry(root, width=50)
birthday_input.grid(row=3,column=1, pady=(0,2))

labels = ["Name", "Phone Number", "Address", "Birthday"]
count = 0

name_label = tk.Label(root, text = "Name")
name_label.grid(row=0,column=0, sticky="w", padx=10, pady=(10,2))

for i in range(1,4):
    label = tk.Label(root, text=labels[i])

    label.grid(row=i,column=0, sticky="w", padx=10, pady=3)

tk.Button(root, text = "Add", command=proceed, width=60).grid(row=4, column=0, columnspan=2, pady=(3,1), padx=5)
tk.Button(root, text = "Contact Book", command=query, width=60).grid(row=5, column=0, columnspan=2, padx=5)

# Committing the changes
database.commit()

# Close the connection
database.close()

root.mainloop()