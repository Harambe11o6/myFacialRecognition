from tkinter import *
from tkinter import messagebox
import mysql.connector
import shutil
import os
from tkinter import filedialog


def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      "*.*")))
def copy_file(source_file, destination_folder):
    # Check if the source file exists
    if not os.path.exists(source_file):
        print(f"Error: The file '{source_file}' does not exist.")
        return

    # Create destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Get the filename from the source file path
    filename = os.path.basename(source_file)

    # Construct the full path where the file will be copied to
    destination_file = os.path.join(destination_folder, filename)

    try:
        # Copy the file to the destination folder
        shutil.copy2(source_file, destination_file)
        print(f"File '{filename}' copied successfully to '{destination_folder}'.")
    except Exception as e:
        print(f"Error: Failed to copy file '{filename}' to '{destination_folder}'.")
        print(e)

"""
def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      "*.*")))
"""



def login():
    global uname
    uname = username.get()
    global pword
    pword = password.get()
    window.destroy()

def regwrite():
    if(new_password.get()!=confirm_password.get()):
        messagebox.showinfo("Login Status", "new password doesnt match with the confirmed password ")
    reg_window.destroy()
    global newuname
    global newpword
    global newemail
    global newfile
    newuname=new_username.get()
    newpword=new_password.get()
    newemail=new_email.get()
    newfile=new_file.get()
    newfile=newfile.replace(os.sep, '/')
    newfile=newfile.strip('"\'')
    seccon = mysql.connector.connect(host="localhost ", user="root", passwd="SPINteg@123", database="sample")
    if seccon.is_connected() == True:
        print("Successfully connected mysql and python for register")
    else:
        print("connection failed")
    cursor1=seccon.cursor()
    cursor1.execute("insert into details values('{}','{}','{}','{}')".format(newuname,newpword,newemail,newfile))
    seccon.commit()
    seccon.close()
def Register():

    global reg_window
    reg_window=Tk()
    reg_window.title('REGISTER WINDOW')
    reg_window.geometry('400x250')
    lb1=Label(reg_window,text='Username:',font=(14))
    lb2=Label(reg_window,text='DATE OF BIRTH:',font=(14))
    lb3=Label(reg_window,text='confirm DATE OF BIRTH:',font=(14))
    lb4=Label(reg_window,text="Email:",font=(14))
    lb5=Label(reg_window,text="Image:",font=(14))
    #button_explore = Button(reg_window,text="Browse Files",command=browseFiles)
    lb1.grid(row=0,column=0,padx=5,pady=5)
    lb2.grid(row=1, column=0, padx=5, pady=5)
    lb3.grid(row=2, column=0, padx=5, pady=5)
    lb4.grid(row=3, column=0, padx=5, pady=5)
    lb5.grid(row=4, column=0, padx=5, pady=5)
    global new_username
    global new_password
    global confirm_password
    global new_email
    global new_file
    new_username=StringVar()
    new_password=StringVar()
    confirm_password=StringVar()
    new_email=StringVar()
    new_file=StringVar()
    tb1=Entry(reg_window,textvariable=new_username,font=(14))
    tb2= Entry(reg_window,textvariable=new_password, font=(14))
    tb3 = Entry(reg_window, textvariable=confirm_password, font=(14))
    tb4 = Entry(reg_window, textvariable=new_email, font=(14))
    tb5=Entry(reg_window,textvariable=new_file,font=(14))
    tb1.grid(row=0,column=1,padx=5,pady=5)
    tb2.grid(row=1, column=1, padx=5, pady=5)
    tb3.grid(row=2, column=1, padx=5, pady=5)
    tb4.grid(row=3, column=1, padx=5, pady=5)
    tb5.grid(row=4, column=1, padx=5, pady=5)
    b1 = Button(reg_window, command=regwrite, text='register_database', font=(14))
    b1.grid(row=5, column=1)
    reg_window.mainloop()
res=messagebox.askquestion('CREDENTIALS','EXISTING USER OR NOT?')
if res=='no':
    messagebox.showinfo('DIRECTING TO REGISTER PAGE', 'DIRECTING TO REGISTER PAGE')
    Register()

else:
    messagebox.showinfo('DIRECTING TO LOGIN PAGE','directing to login page')
window = Tk()
window.title('login Screen')
window.geometry('400x150')
l1 = Label(window, text='USERNAME:', font=(14))
l2 = Label(window, text='DATEOFBIRTH:', font=(14))
l1.grid(row=0, column=0, padx=5, pady=5)
l2.grid(row=1, column=0, padx=5, pady=5)
username = StringVar()
password = StringVar()
t1 = Entry(window, textvariable=username, font=(14))
t2 = Entry(window, textvariable=password, font=(14), show='*')
t1.grid(row=0, column=1)
t2.grid(row=1, column=1)
b1 = Button(window, command=login, text='Login', font=(14))
b1.grid(row=2, column=1)
window.mainloop()
mycon = mysql.connector.connect(host="localhost ", user="root", passwd="SPINteg@123", database="sample")#db connection
if (mycon.is_connected() == True):
    print("successfully connected mysql and python")
else:
    print("connection failed")
cursor = mycon.cursor()
cursor.execute("select name from details where name='{}'".format(uname))
checkdata=cursor.fetchall()
if(len(checkdata)==0):
    messagebox.showinfo("Login Status", "Login failed,PLEASE CHECK CREDENTIALS \n ")
    exit()
else:
    messagebox.showinfo("Login Status", "OPPENING FACE RECOGNITION ")
    cursor.execute(" SELECT IMAGE FROM details WHERE DOB='{}'".format(pword))
    data = cursor.fetchall()
    for r in data:
        global imgadd
        imgadd = ""
        for j in r:
            imgadd += j#saving the address of the image as a string

    source_file = imgadd
    destination_folder = "C:/Users/HP/PycharmProjects/myFacialRecognition/known_people"
    copy_file(source_file, destination_folder)
mycon.close()





