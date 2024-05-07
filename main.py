import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3 



def add_details():
    name=name_ent.get()
    email=email_ent.get()
    product=product_ent.get()
    website=website_combobox.get()
    quantity=quantity_spinbox.get()
    amount=amount_ent.get()

    conn=sqlite3.connect('main.db')
    cursor=conn.cursor()
    table_create_query = '''CREATE TABLE IF NOT EXISTS Shopping_Catalog
            (Name TEXT ,Email TEXT PRIMARY KEY,Product TEXT,Website TEXT,Quantity INT,Amount INT) 
            '''
    conn.execute(table_create_query)
    emails=email_ent.get()
    cursor.execute('''SELECT * FROM Shopping_Catalog WHERE Email=?''',(emails,) )
    existing_record=cursor.fetchone()
    if existing_record:
        messagebox.showwarning(title="Error",message="Email already exists")
    else:


        data_insert_query='''INSERT INTO Shopping_Catalog(Name,Email,Product,Website,Quantity,Amount) VALUES(?,?,?,?,?,?) '''
        data_insert_tuple=(name,email,product,website,quantity,amount)
        cursor=conn.cursor()
        cursor.execute(data_insert_query,data_insert_tuple)
        conn.commit()
        conn.close() 

def  show_details():
    conn= sqlite3.connect('main.db')
    cursor= conn.cursor()

    results_window=Toplevel(master=window)
    treeview = ttk.Treeview(results_window)
    treeview.pack()
    treeview["columns"] = ("Name",  "Email", 'Product', "Website", "Quantity", "Amount")
    cursor.execute("SELECT * from Shopping_Catalog")
    data= cursor.fetchall()
    treeview.column("#0", width=0, stretch=NO)
    treeview.column("Name", anchor=E, width=70)
    treeview.column("Email", anchor=E, width=70)
    treeview.column("Product", anchor=E, width=70)
    treeview.column("Website", anchor=E, width=70)
    treeview.column("Quantity", anchor=E, width=70)
    treeview.column("Amount", anchor=E, width=70)
    
    
    treeview.heading("#0", text="", anchor=W)
    treeview.heading("Name", text="Name", anchor=W)
    treeview.heading("Email", text="Email", anchor=W)
    treeview.heading("Product", text="Product", anchor=W)
    treeview.heading("Website", text="Website", anchor=W)
    treeview.heading("Quantity", text="Quantity", anchor=W)
    treeview.heading("Amount", text="Amount", anchor=W)
    for row in data:
        treeview.insert("", END, values=row)

def delete_details():
    def deleterecord():
        Email_id = EmailId.get()

        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        
        cursor.execute('''DELETE FROM Shopping_Catalog WHERE Email=?''', (Email_id,))
        conn.commit()

        conn.close()
        
        popup=Toplevel(master=addroot)
        popup.grab_set()
        popup.geometry("100x100")
        popup.config()
        tk.Label(popup, text="Record successfully deleted", padx=20, pady=10).pack(anchor="center")
        
        addroot.destroy()
        
    addroot = Toplevel(master=window)
    addroot.grab_set()
    addroot.geometry("470x200")
    addroot.title("Delete record")
    addroot.config()

    tk.Label(addroot, text="Enter Email Id:", padx=20, pady=10).pack()
    EmailId = tk.Entry(addroot)
    EmailId.pack(padx=20, pady=10)

    btn = tk.Button(addroot, text="Delete", command=deleterecord)
    btn.pack(padx=20, pady=10)
def update_details():
    def fetch_record():
       
        search_id=UD_entry.get()
        conn= sqlite3.connect('main.db')
        cursor=conn.cursor()
        cursor.execute('''SELECT * FROM Shopping_Catalog WHERE Email=?''', (search_id,))
        search_result = cursor.fetchone()
        conn.close()
        if search_result:
            updated_name_entry.delete(0, tk.END)
            updated_name_entry.insert(0, search_result[0])
            
            updated_product_entry.delete(0, tk.END)
            updated_product_entry.insert(0, search_result[2])
            updated_website_entry.delete(0, tk.END)
            updated_website_entry.insert(0, search_result[3])
            updated_quantity_entry.delete(0, tk.END)
            updated_quantity_entry.insert(0, search_result[4])
            updated_amount_entry.delete(0, tk.END)
            updated_amount_entry.insert(0, search_result[5])
            
        else:
            tk.messagebox.showwarning(title="Error", message="No record found!")
    def updaterecord():
        Name= updated_name_entry.get()
        Email=UD_entry.get()
        
        Product = updated_product_entry.get()
        Website = updated_website_entry.get()
        Quantity = updated_quantity_entry.get()
        Amount = updated_amount_entry.get()
        
            
        conn= sqlite3.connect("main.db")
        cursor= conn.cursor()
            
        cursor.execute('''UPDATE Shopping_Catalog SET Name=?, Product=?, Website=?, Quantity=?, Amount=?
                       WHERE Email=?''',(Name,Product,Website,Quantity,Amount,Email))
        conn.commit()
        conn.close()
        addroot.destroy()
        tk.messagebox.showinfo(title="Success", message="Record Updated Successfully.")
    addroot = Toplevel(master=window)
    addroot.grab_set()
    addroot.geometry("380x480")
    addroot.title("Update record")

    UD_label= tk.Label(addroot, text="Enter Email ID:", padx=20, pady=10)
    UD_label.grid(row=0, column=2)
    UD_entry= Entry(addroot)
    UD_entry.grid(row=1, column=2)

    btn_fetch = Button(addroot, text="Fetch Record", command=fetch_record)
    btn_fetch.grid(row=3,column=2, padx=20, pady= 10)

    updated_name_label=tk.Label(addroot, text="Updated Name:")
    updated_name_label.grid(row=5,column=2, padx=20, pady=10)
    updated_name_entry = Entry(addroot)
    updated_name_entry.grid(row=5, column=3,padx=20, pady=10)
            
    updated_product_label=tk.Label(addroot, text="Updated  Product:")
    updated_product_label.grid(row=6,column=2,padx=20, pady=10)
    updated_product_entry =Entry(addroot)
    updated_product_entry.grid(row=6,column=3,padx=20, pady=10)
            
    updated_website_label=tk.Label(addroot, text="Updated Website:",)
    updated_website_label.grid(row=7,column=2,padx=20, pady=10)
    updated_website_entry = ttk.Combobox(addroot,values=["Amazon","Flipkart","Myntra","Tata Cliq"])
    updated_website_entry.grid(row=7,column=3,padx=20, pady=10)
            
    updated_quantity_label=tk.Label(addroot, text="Updated Quantity:")
    updated_quantity_label.grid(row=8,column=2,padx=20, pady=10)
    updated_quantity_entry = Spinbox(addroot,from_=1,to=20)
    updated_quantity_entry.grid(row=8,column=3,padx=20, pady=10)

    updated_amount_label=tk.Label(addroot, text="Updated Amount:")
    updated_amount_label.grid(row=9,column=2,padx=20, pady=10)
    updated_amount_entry = Entry(addroot)
    updated_amount_entry.grid(row=9,column=3,padx=20, pady=10)
            
    

    btn = tk.Button(addroot, text="Update", command=updaterecord)
    btn.grid(row=13,column=2,padx=21, pady=10)

window = Tk()
window.geometry("1280x720+0+0")
window.title("Online Shopping Catalog")

title_label=tk.Label(window,text="Online Shopping Catalog",font=("Algerian Regular",35,"bold"),border=12,relief=tk.RAISED,bg="red",foreground="white") 
title_label.pack(side=tk.TOP,fill=tk.X)

detail_frame=tk.LabelFrame(window,text="Enter Details : ",font=("Arial",30),bd=10,bg="lightgrey",fg="black",relief="raised")
detail_frame.place(x=20,y=120,width=1200,height=300)

name_lbl=tk.Label(detail_frame,text="Name",font=("Arial",20),bg="lightgrey",fg="black")
name_lbl.grid(row=0,column=0,padx=2,pady=2)

name_ent=tk.Entry(detail_frame,bd=7,font=('Arial', 20 ))
name_ent.grid(row=1,column=0,padx=2,pady=2)

email_lbl=tk.Label(detail_frame,text="E-Mail",font=("Arial",20),bg="lightgrey",fg="black")
email_lbl.grid(row=0,column=1,padx=2,pady=2)

email_ent=tk.Entry(detail_frame,bd=7,font=('Arial', 20 ))
email_ent.grid(row=1,column=1,padx=2,pady=2)

product_lbl=tk.Label(detail_frame,text="Product",font=("Arial",20),bg="lightgrey",fg="black")
product_lbl.grid(row=0,column=2,padx=2,pady=2)

product_ent=tk.Entry(detail_frame,bd=7,font=('Arial', 20 ))
product_ent.grid(row=1,column=2,padx=2,pady=2)

website_lbl=tk.Label(detail_frame,text="Website",font=("Arial",20),bg="lightgrey",fg="black")
website_lbl.grid(row=3,column=0,padx=2,pady=2)

website_combobox=ttk.Combobox(detail_frame,values=["Amazon","Flipkart","Myntra","Tata Cliq"],width=45,state="readonly")
website_combobox.grid(row=4,column=0,padx=2,pady=2)

quantity_lbl=tk.Label(detail_frame,text="Quantity",font=("Arial",20),bg="lightgrey",fg="black")
quantity_lbl.grid(row=3,column=1,padx=2,pady=2)

quantity_spinbox=tk.Spinbox(detail_frame,from_=1,to=20,width=45,state="readonly")
quantity_spinbox.grid(row=4,column=1,padx=2,pady=2)

amount_lbl=tk.Label(detail_frame,text="Amount",font=("Arial",20),bg="lightgrey",fg="black")
amount_lbl.grid(row=3,column=2,padx=2,pady=2)

amount_ent=tk.Entry(detail_frame,bd=7,font=('Arial', 20 ))
amount_ent.grid(row=4,column=2,padx=2,pady=2)


btn_frame=tk.Frame(window,bg="lightgrey",bd=10,relief=tk.RAISED)
btn_frame.place(x=20,y=450,width=1200,height=200)
 
add_btn=tk.Button(btn_frame,bg="lightgrey",text="ADD",bd=7,font=(("Arial"),15),width=50,command=add_details)
add_btn.grid(row=0,column=0,padx=2,pady=2)

update_btn=tk.Button(btn_frame,bg="lightgrey",text="UPDATE",bd=7,font=(("Arial"),15),width=50,command=update_details)
update_btn.grid(row=0,column=1,padx=2,pady=2)

delete_btn=tk.Button(btn_frame,bg="lightgrey",text="DELETE",bd=7,font=(("Arial"),15),width=50,command=delete_details)
delete_btn.grid(row=1,column=0,padx=2,pady=2)

show_btn=tk.Button(btn_frame,bg="lightgrey",text="SHOW",bd=7,font=(("Arial"),15),width=50,command=show_details)
show_btn.grid(row=1,column=1,padx=2,pady=2)










window.mainloop()