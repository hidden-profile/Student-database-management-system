from tkinter import *
from tkinter import ttk
import psycopg2
from tkinter import messagebox

def run_query(query,parameters=()):
    conn=psycopg2.connect(dbname="student",user="postgres",password="Sweety@2004",host="localhost",port="5432")
    cur=conn.cursor()
    res=None
    try:
        cur.execute(query,parameters)
        if query.lower().startswith("select"):
            res=cur.fetchall()
        conn.commit()
    except psycopg2.Error as e:
        messagebox.showerror("Database Error",str(e))
    
    finally:
        cur.close()
        conn.close()
    return res

def refresh_treeview():
    for i in tr.get_children():
        tr.delete(i)
    records=run_query("select * from students;")
    for i in records:
        tr.insert('',END,values=i)

def insert_data():
    q="INSERT INTO students(name,addr,age,phn) VALUES (%s,%s,%s,%s)"
    p=(e1.get(),e2.get(),e3.get(),e4.get())
    run_query(q,p)
    refresh_treeview()
    messagebox.showinfo("Information","Data Inserted Successfully")

def delete_data():
    s=tr.selection()[0]
    #we will get the id of view but no our id
    ss=tr.item(s)['values'][0]
    #will give the id
    q="delete from students where id=%s"
    p=(ss,)
    run_query(q,p)
    messagebox.showinfo("Information","Data Deleted Successfully")
    refresh_treeview()

def update_data():
    s=tr.selection()[0]
    #we will get the id of view but no our id
    ss=tr.item(s)['values'][0]
    #will give the id
    q="update students set name=%s,addr=%s,age=%s,phn=%s where id=%s"
    p=(e1.get(),e2.get(),e3.get(),e4.get(),ss)
    run_query(q,p)
    messagebox.showinfo("Information","Data Updated Successfully")
    refresh_treeview()

def create_table():
    q="create table if not exists students(id serial primary key,name text,addr text,age int, phn text);"
    run_query(q)
root=Tk()
root.title("Student Management System")
frame1=LabelFrame(root,text="Student Data")
frame1.grid(row=0,column=0,padx=10,pady=10,sticky="ew")
#ew-->east and west strech from left to right
l1=Label(frame1,text="Name")
l1.grid(row=0,column=0,padx=2,sticky="w")
e1=Entry(frame1)
e1.grid(row=0,column=1)

l2=Label(frame1,text="Address")
l2.grid(row=1,column=0,padx=2,sticky="w")
e2=Entry(frame1)
e2.grid(row=1,column=1)
l3=Label(frame1,text="Age")
l3.grid(row=2,column=0,padx=2,sticky="w")
e3=Entry(frame1)
e3.grid(row=2,column=1)
l4=Label(frame1,text="Phone Number")
l4.grid(row=3,column=0,padx=2,sticky="w")
e4=Entry(frame1)
e4.grid(row=3,column=1)

btnfr=Frame(root)
btnfr.grid(row=1,column=0,pady=5,sticky="ew")
b1=Button(btnfr,text="Create Table",command=create_table)
b1.grid(row=0,column=0,padx=5)
b2=Button(btnfr,text="Add Data",command=insert_data)
b2.grid(row=0,column=1,padx=5)
b3=Button(btnfr,text="Update Data",command=update_data)
b3.grid(row=0,column=2,padx=5)
b4=Button(btnfr,text="Delete Data",command=delete_data)
b4.grid(row=0,column=3,padx=5)

#tree view place database data in form of rows and columns
treefr=Frame(root)
treefr.grid(row=2,column=0,padx=10,sticky="nsew")
#tree in ttk module
scroll=Scrollbar(treefr)
scroll.pack(side=RIGHT,fill=Y)
#but scroolling wint work to work  use yscrollcommand
tr=ttk.Treeview(treefr,yscrollcommand=scroll.set,selectmode="browse")
#it we have multiple entries select only one 
scroll.config(command=tr.yview)
tr.pack()
tr['columns']=("student_id", "name", "address", "age", "number")
#configure columns
tr.column("#0", width=0, stretch=NO)
tr.column("student_id", anchor=CENTER, width=80)
tr.column("name", anchor=W, width=120)
tr.column("address", anchor=W, width=120)
tr.column("age", anchor=CENTER, width=50)
tr.column("number", anchor=W, width=120)
 
tr.heading("student_id", text="ID", anchor=CENTER)
tr.heading("name", text="Name", anchor=CENTER)
tr.heading("address", text="Address", anchor=CENTER)
tr.heading("age", text="Age", anchor=CENTER)
tr.heading("number", text="Phone Number", anchor=CENTER)
refresh_treeview()
root.mainloop()