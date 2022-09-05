import database
import overall_details
import sql_query_details
import utility
import tkinter as tk  
from tkinter import ttk
from tkinter import *
import os

def delete3():
      screen4.destroy()
      
def delete4():
      screen5.destroy()


def password_not_recognised():
      global screen4
      screen4 = Toplevel(screen)
      screen4.title("Success")
      screen4.geometry("150x100")
      Label(screen4, text = "Password Error").pack()
      Button(screen4, text = "OK", command =delete3).pack()

def user_not_found():
      global screen5
      screen5 = Toplevel(screen)
      screen5.title("Success")
      screen5.geometry("150x100")
      Label(screen5, text = "User Not Found").pack()
      Button(screen5, text = "OK", command =delete4).pack()

def register_user():
      username_info = username.get()
      password_info = password.get()
      file=open(username_info, "w")
      file.write(username_info+"\n")
      file.write(password_info)
      file.close()
      username_entry.delete(0, END)
      password_entry.delete(0, END)
      Label(screen1, text = "Registration Sucess", fg = "green" ,font = ("calibri", 11)).pack()

def login_verify():  
      username1 = username_verify.get()
      password1 = password_verify.get()
      username_entry1.delete(0, END)
      password_entry1.delete(0, END)
      list_of_files = os.listdir()
      if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()
        else:
            password_not_recognised()

      else:
            user_not_found()

def register():
      global screen1
      screen1 = Toplevel(screen)
      screen1.title("Register")
      screen1.geometry("300x250")
    
      global username
      global password
      global username_entry
      global password_entry
      username = StringVar()
      password = StringVar()

      Label(screen1, text = "Please enter details below", ).pack()
      Label(screen1, text = "").pack()
      Label(screen1, text = "Username * ").pack()
      username_entry = Entry(screen1, textvariable = username)
      username_entry.pack()
      Label(screen1, text = "Password * ").pack()
      password_entry =  Entry(screen1, textvariable = password, show = "*")
      password_entry.pack()
      Label(screen1, text = "").pack()
      Button(screen1, text = "Register", width = 10, height = 1, command = register_user).pack()


def login():
      global screen2
      screen2 = Toplevel(screen)
      screen2.title("Login")
      screen2.geometry("300x250")
      Label(screen2, text = "Please enter details below to login", bg = "grey", width = "300", height = "2", font = ("Calibri", 13)).pack()
      Label(screen2, text = "").pack()

      global username_verify
      global password_verify
      
      username_verify = StringVar()
      password_verify = StringVar()

      global username_entry1
      global password_entry1
      
      Label(screen2, text = "Username * ").pack()
      username_entry1 = Entry(screen2, textvariable = username_verify)
      username_entry1.pack()
      Label(screen2, text = "").pack()
      Label(screen2, text = "Password * ").pack()
      password_entry1 = Entry(screen2, textvariable = password_verify, show = "*")
      password_entry1.pack()
      Label(screen2, text = "").pack()
      Button(screen2, text = "Login", width = 10, height = 1, command = login_verify).pack()
      

def login_sucess():
    screen.destroy()        



def main_screen():
      global screen
      screen = Tk()
      screen.geometry("300x250")
      screen.title("Natural Language to SQL ")
      Label(text = "Natural Language to SQL", bg = "grey", width = "300", height = "2", font = ("Calibri", 13)).pack()
      Label(text = "").pack()
      Button(text = "Login", height = "2", width = "30", command = login).pack()
      Label(text = "").pack()
      Button(text = "Register",height = "2", width = "30", command = register).pack()

      screen.mainloop()

main_screen()

def compare():
    base_op = open("base_output.txt", "r")
    op = open("output.txt", "r")
    log = open("log.txt", "w")  

    line1 = next(base_op)
    line2 = next(op)

    count = 1

    while line1 and line2:
        if line1 != line2:
            log.write("Query %d\n" % count)
            print("Query ", count)
        count += 1
        line1 = next(base_op)
        line2 = next(op)

    base_op.close()
    op.close()
    log.close()


op_file = open("output.txt", "w")

db = database.Database("localhost", "root", "root", "test")
db.connect()

overall_details = overall_details.OverallDetails(db)
overall_details.collect_details()

count = 1


win = tk.Tk()
win.title("NLP TO SQL")
lbl = ttk.Label(win, text = "Enter The Query:").grid(column = 0, row = 0)# Click event  
def click():   
        sql_query_details_obj = sql_query_details.SQLQueryDetails(db, overall_details)

        clauses = sql_query_details_obj.collect_query_details(name.get())

        [query, type_query] = clauses.create_query()
        [neg_query, neg_tyoe_query] = clauses.create_neg_query(clauses.where_clause, clauses.negation_constants, utility.Utility.inversion_array)
        
        print("\n-----------")
        print("Final query: ", query)
        print("-----------\n")
        print("Negated Query... ", neg_query)
        ttk.Label(win, text=query, width = 100).grid(column = 0, row = 3)  
name = tk.StringVar()  
nameEntered = ttk.Entry(win, width = 100, textvariable = name).grid(column = 0, row = 1)  
lbl1 = ttk.Label(win, text = "Result:").grid(column = 0, row = 2) 
button = ttk.Button(win, text = "Search", command = click).grid(column = 1, row = 1)  
win.mainloop()     




