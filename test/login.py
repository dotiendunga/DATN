from tkinter import *
from tkinter import messagebox 
import mysql.connector 
from register import*

root1 =Tk()
root1.title('Railway Station')
root1.geometry('1000x550+300+200')
root1.configure(bg ="#fff")
root1.resizable(False,False)

def add_user():
    import register
    root1.destroy()
    print(2)

# mydb = mysql.connector.connect(host='localhost',user='root',password='012301230123',database='trainsystem')
## Sign in admin 

def signin():
    username=user.get()
    password=code.get()
    if (username =="" or username =="UserName" )and( password=="" or password =="Password") :
        messagebox.showerror("Entry Error","Type UserName or Password !!!")
    else:
        try:
            mydb = mysql.connector.connect(host='localhost',user='root',password='012301230123',database="trainsystem")
            mycursor=mydb.cursor()
            print("connected to database !!")
        except:
            messagebox.showerror("Connection","Database connection not stablish!!")
    command = "use trainsystem"
    mycursor.execute(command)
    command ="select * from login where Username=%s and Password=%s"
    mycursor.execute(command,(username,password))
    myresult=mycursor.fetchone()
    print(myresult)

    if myresult ==None:
        messagebox.showinfo("invalid","Invalid userid and password")
    else:
        messagebox.showinfo("login","Sucessfully Login!!")
        root1.destroy()
        import register
#frame login 

frame = Frame(root1,width=350,height=350,bg="white")
frame.place(relx = 0.5, rely = 0.5, anchor = E,x=480)
heading= Label(frame,text="Sign in",fg="#FFC271",bg='white',font=('Arial',23,'bold'))
heading.place(x=100,y=5)
######______________________
# e: event
def user_enter(e):
    user.delete(0,'end')
def user_leave(e):
    name=user.get()
    if name =='':
        user.insert(0,'UserName')
user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Arial',11))
user.place(x=30,y=80)
user.insert(0,'UserName')
user.bind('<FocusIn>',user_enter)
user.bind('<FocusOut>',user_leave)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)
###________________________
##show pass
##pass 
def code_enter(e):
    code.delete(0,'end')
    code.config(show="*")
def code_leave(e):
    name=code.get()
    if name =='':
        code.config(show="")
        code.insert(0,'Password')
code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Arial',11))
code.place(x=30,y=150)
code.insert(0,'Password')
code.bind('<FocusIn>',code_enter)
code.bind('<FocusOut>',code_leave)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)
# hide pass
button_mode =False
def hide():
    global button_mode 
    if button_mode:
        code.config(show="*")
        button_mode=False
    else:
        code.config(show="")
        button_mode=True
openeye=PhotoImage(file='image/key.png')
eyebutton= Button(frame,image=openeye,bg='#fff',bd=0,command=hide)
eyebutton.place(x=295,y=160)
#Button sign in 
Button(frame,width=34,pady=2, text='Sign in',bg='#FFC271',fg='white',border=0,command=signin,font=('Arial',11,'bold')).place(x=15,y=204)
label=Label(frame,text="Don't have an account?",fg='black',bg='white',font=('Arial',9))
label.place(x=75,y=270)
##sign up
sign_up =Button(frame,width=10,text='Add new user',border=0,bg='white',cursor='hand2',fg='#FFC271',comman=add_user)
sign_up.place(x=215,y=270)
root1.mainloop()

