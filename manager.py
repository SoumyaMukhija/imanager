#MADE IN PYTHON-3
from tkinter import *
from sqlite3 import *
from tkinter import messagebox as mb
from tkinter import ttk
from datetime import *
from PIL import Image, ImageTk as it
import os
import sys



#Main
login_frame=Tk()
login_frame.geometry("650x450+100+10")
login_frame.resizable(0,0)
login_frame.title('iManager')


#Databases
conn=Connection("Sample Data")
cur=conn.cursor()
cur.execute("CREATE TABLE if not exists U_Data (_UID INTEGER PRIMARY KEY AUTOINCREMENT, Fname varchar2 (15) NOT NULL, Sname varchar2 (15) NOT NULL, Uname varchar2 (15) UNIQUE, Password varchar2(15) NOT NULL);")
conn.commit()
cur.execute("CREATE TABLE IF NOT EXISTS F_Data (_FID INTEGER PRIMARY KEY AUTOINCREMENT, UID INTEGER(1000000), FileName varchar2 (15), Date_ varchar2 (15))")
conn.commit()

cur.execute("SELECT * FROM U_Data")
a=cur.fetchall()
print(a)

cur.execute("SELECT * FROM F_Data")
a=cur.fetchall()
print(a)




def openexistingfile(file):
	print(file)
	os.system("notepad "+file+".txt")



def openfile(uid, filename):
	global getinfo
	getinfo.destroy() 

	if filename=='':
		mb.showerror('Missing Input', 'Please specify a file name.')
	else:
		try:
			check=os.system("notepad " +filename+".txt")
			now=datetime.now()
			today= str(now.day) + '/' + str(now.month) +'/' + str(now.year)
			cur.execute("SELECT * FROM F_Data")
			f=cur.fetchall()
			print(f)
			cur.execute("insert into F_Data (UID, FileName, Date_) values (?, ?, ?)", ( uid, filename, today))
			conn.commit()
		except:
			raise
			mb.showerror('Error','Looks like something is wrong. Please try again.')
			sys.exit(0)





def write(uid):
	global getinfo
	getinfo=Toplevel(bg='white')
	getinfo.title('New File')
	getinfo.geometry('250x90')
	getinfo.resizable(0,0)
	Label(getinfo, text='File Name', font='Cambria 12 bold', bg='white').place(x=5, y=5)
	filename=Entry(getinfo, bd=3)
	filename.place(x=90, y=7)
	Button(getinfo, text='Done', width=15, bg='#013554', fg='white', command=lambda: openfile(uid, filename.get())).place(x=50, y=40)



def mainscreen(uname):
	global frame, subframe, subframe3, subframe2, dateframe, fileframe, testframe
	login_frame.withdraw()
	ms=Toplevel(master=None)
	ms.configure(background='white')
	ms.geometry('650x450+100+10')
	ms.resizable(0,0)
	ms.title('Main Screen')
	frame=Frame(ms, height=100, width=700, bg='#013554')
	frame.place(x=0, y=0)
	subframe=Frame(ms, height=40, width=700, bg='#CD342E')
	subframe.place(x=0, y=115)
	subframe2=Frame(ms, height=5, width=700, bg='#4A4C4C')
	subframe2.place(x=0, y=105)
	subframe3=Frame(ms, height=500, width=3, bg='black')
	subframe3.place(x=70, y=0)
	cur.execute("SELECT _UID FROM U_Data WHERE UNAME=?",(uname,))
	U=cur.fetchone()
	uid=U[0]
	print(uid)
	Label(frame, text='iManager', font='Cambria 40 bold', cursor='heart',bg='#013554', fg='white').place(x=240, y=25)
	tx=uname+"'s files"
	Label(subframe, text=tx, font='Georgia 15 italic', bg='#CD342E', fg='white').place(x=80, y=8)
	cur.execute("SELECT exists(SELECT 1 FROM F_Data, U_Data WHERE F_Data.UID=(?))", (uid, ))
	checknull=cur.fetchone()
	print(checknull[0])
	if checknull[0]!=0:
		cur.execute("SELECT FileName FROM F_Data where F_Data.UID=(?)", [uid])
		viewdata=cur.fetchall()
		print(viewdata)
		mainframe=Frame(ms, height=270, width=400, bg='white')
		mainframe.place(x=80, y=170)
		cnt=7
		top=225
		c=0
		docimg=PhotoImage ( file= "download.gif")
		for i in viewdata:
			doc=Button( mainframe, image=docimg, bd=0,cursor='hand1',  command=lambda: openexistingfile(str(i[0])))
			doc.place(x=cnt, y=70)
			doc.image=docimg
			Label(mainframe, text=str(i[0]), font='Times 12 italic', bg='white').place(x=cnt, y=130)
			cnt+=120

			#Label(dateframe, text=i[3], bg='white', fg='black', font='Courier 13').place(x=70, y=cnt)
			#abel(fileframe, text= str(i[2])+".txt", bg='white', fg='black', font='Courier 13').place(x=30, y=cnt)
			#Button(ms, text='Open', bg='#0070F7', fg='white', font='Arial 10 bold', bd=3, command=lambda: openexistingfile(str(i[2]))).place(x=500, y=c*2+top)
		testframe=Frame(ms, height=1, width=700, bg='#0070F7')
		testframe.place(x=0, y=220)
	else:
		Label(ms, text='No files yet! Start writing.', font='Cambria 15 italic', bg='white').place(x=240, y=190)
		img = PhotoImage(file="write.gif")
		img1lbl = Label(ms, image=img, height=160 , width=160, bd=0)
		img1lbl.image = img
		img1lbl.place(x=275, y=240)
	btimg=PhotoImage(file="images.gif")
	b=Button(ms, image=btimg, bd=0,  command=lambda: write(uid))
	b.image=btimg
	b.place(x=540, y=360)
	#b.place(x=265, y=395)
	



def sign_up_check(fname, lname, uname, password):
	global spp, subframe2, subframe3, frame
	pre_existing=cur.execute("SELECT Uname FROM U_Data WHERE Uname=?", (uname,));
	a=pre_existing.fetchall()
	try:
		if len(a)>0:
			raise
		if fname=='' or lname=='' or uname=='' or password=='':
			raise
		cur.execute("insert into U_Data (Fname, Sname, Uname, Password) values (?, ?, ?, ?);", (fname, lname, uname, password))
		conn.commit()
		x=cur.fetchone()
		mb.showinfo('Success', 'Sign-up successful!')
		login_frame.deiconify()
		subframe2.destroy()
		subframe3.destroy()
		frame.destroy()
		spp.destroy()
		login_page() 
	except:
		if fname=='':
			mb.showerror('Missing input','Please enter your first name.')
		elif lname=='':
			mb.showerror('Missing input', 'Please enter your surname.')
		elif uname=='':
			mb.showerror('Missing input', 'Please enter a unique username.')
		elif password=='':
			mb.showerror('Missing input', 'Please specify a password.')
		elif len(a)>0:
			mb.showerror('Username exists', 'This username already exists. Please try another.')
		else:
			raise
			mb.showerror('Error','Looks like there is something wrong. Please try again later.')
		



def sign_up_page():
	global subframe, subframe3, subframe2, frame, spp
	subframe.destroy()
	subframe2.destroy()
	subframe3.destroy()
	login_frame.withdraw()
	spp=Toplevel()
	spp.resizable(0,0)
	spp.title('Sign Up')
	spp.config(bg='white')
	spp.geometry('650x450+100+10')
	frame=Frame(spp, height=100, width=700, bg='#CD342E')
	frame.place(x=0,y=0)
	subframe3=Frame(spp, height=5, width=700, bg='#4A4C4C')
	subframe3.place(x=0, y=105)
	subframe2=Frame(spp, height=40, width=700, bg='black')
	subframe2.place(x=0, y=115)
	Label(subframe2, text='Welcome aboard! Tell us a bit about yourself.', bg='black', fg='white',font='Times 15').place(x=10, y=8)
	Label(spp, text='Sign Up', font='Times 30 bold', fg='white', bg='#CD342E').place(x=250, y=40)
	Label(spp, text='First Name', bg='white', font='Cambria 13 bold').place(x=201, y=170)
	fname=Entry(spp, bd=3)
	fname.place(x=305, y=175)
	Label(spp, text='Last Name',bg='white', font='Cambria 13 bold').place(x=201, y=210) 
	lname=Entry(spp, bd=3)
	lname.place(x=305, y=215)
	Label(spp, text='Username',bg='white', font='Cambria 13 bold').place(x=202, y=250)
	uname=Entry(spp, bd=3)
	uname.place(x=305, y=255)
	Label(spp, text='Password',bg='white', font='Cambria 13 bold').place(x=205, y=290)
	password=Entry(spp, bd=3, show='*')
	password.place(x=305, y=295)
	Button(spp, text='Sign Up',  height=1, width=25, bg='black', bd=0, fg='white', font='Cambria 13 bold', command= lambda: sign_up_check(fname.get(), lname.get(), uname.get(), password.get())).place(x=190, y=350)




def login_check(uname, password):
	global subframe, subframe2, subframe3
	if uname=='' or password=='':
		mb.showerror('Login Failed', 'Please enter your username.')
	else:
		try:
			cur.execute("SELECT Password from U_Data WHERE Uname = (?)",(uname,)) 
			checkpass=cur.fetchone()
			if checkpass[0]==password :
				subframe2.destroy()
				subframe.destroy()
				subframe3.destroy()
				mainscreen(uname)
			else:
				mb.showerror('Login Failed','Username or Password incorrect.')
				return
		except:
			raise
			mb.showerror('Login Failed', 'Username does not exist. Sign up for free instead!')



def login_page():
	global uname, password, subframe, subframe3, subframe2
	subframe=Frame( height=170, width=700, bg='#013554')
	subframe.place(x=0, y=0)
	Label(subframe, text='Login', font='Times 50 bold', fg='white', bg='#013554').place(x=250, y=50)
	subframe2=Frame( height=5, width=700, bg='#00496A')
	subframe2.place(x=0, y=180)
	subframe3=Frame( height=50, width=700, bg='#CD342E')
	subframe3.place(x=0, y=190)
	Label(subframe3, text="Glad to have you back! Let's get started.", font='Times 15', bg='#CD342E', fg='white').place(x=10, y=10)
	Label(login_frame, text='Username', bg='white', font='Cambria 15 bold').place(x=200, y=250)
	uname=Entry(login_frame, bd=3, cursor='pencil')
	uname.place(x=305, y=255)
	Label(login_frame, text='Password', bg='white', font='Cambria 15 bold').place(x=200, y=290)
	password=Entry(login_frame, show='*', bd=3, cursor='pencil')
	password.place(x=305, y=295)
	Button(login_frame, height=1, width=25, bg='#000000', fg='white', text='Enter', font='Cambria 13 bold', command=lambda: login_check(uname.get(), password.get())).place(x=200, y=340)
	Label(login_frame, text='Not a member?', bg='white', font='Cambria 8').place(x=200, y=380)
	Button(login_frame, text='Sign up now ➟', font='Cambria 8', width=15,  bg='#DCDCDC', bd=0, fg='black', command=sign_up_page).place(x=280, y=380)




def startprogram(e):
	global  frame, subframe, subframe2, subframe3
	subframe.destroy()
	subframe2.destroy()
	subframe3.destroy()
	for i in frame.winfo_children():
		i.destroy()
	login_page()




def splashscreen():
	global frame, subframe, subframe2, subframe3
	frame=Frame(login_frame, height=500, width=700, bg='white', bd=0)
	frame.grid(row=0, column=0)
	picture=PhotoImage(file="Capture.gif")
	lb=Label(frame, image=picture)
	lb.image=picture
	lb.bind('<Motion>', startprogram)
	lb.place(x=0, y=0)
	subframe=Frame( height=150, width=250, bg='#013554')
	subframe.place(x=390, y=0)
	Label(subframe, text='iManager', font='Times 30 bold', cursor='heart', fg='white', bg='#013554').place(x=38, y=60)
	subframe2=Frame( height=5, width=250, bg='#4A4C4C')
	subframe2.place(x=390, y=160)
	subframe3=Frame( height=5, width=250, bg='#CD342E')
	subframe3.place(x=390, y=170)
	Label(frame, text='Access any file, anywhere.', font='Times 13 italic', bg='white', fg='#4A4C4C', ).place(x=415, y=240)
	lb2=Label(frame, text='Made by: Soumya Mukhija\nEnrollment: 171B135\nEmail: soumyamukhija@gmail.com\nContact: 9039439659',font="Helvectica 10 bold", fg='#4A4C4C', bg='white').place(x=390, y=360)




splashscreen()
login_frame.mainloop()
