#!/usr/bin/python3
from tkinter import *
from tkinter.ttk import Button, Combobox, Entry, Style
from tkinter.messagebox import *
from db import DBConnect
from listComp import ListComp

conn = DBConnect()
root = Tk()
root.title('Complaint Management Dashboard')
root.geometry('760x680')
root.minsize(650, 600)
root.configure(background='#F4F7FB')

style = Style()
style.theme_use('clam')
style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=(12, 7))
style.configure('TCombobox', padding=5)

header = Frame(root, background='#172A46', padx=30, pady=24)
header.pack(fill='x')
Label(header, text='COMPLAINT DESK', background='#172A46', foreground='white', font=('Segoe UI', 25, 'bold')).pack(anchor='w')
Label(header, text='A clearer way to listen, respond, and resolve.', background='#172A46', foreground='#B9C7DA', font=('Segoe UI', 11)).pack(anchor='w', pady=(3, 0))

stats = Frame(root, background='#F4F7FB', padx=25, pady=18)
stats.pack(fill='x')
stat_labels = {}
for title, key, color in (('UNREAD', 'Unread', '#F59E0B'), ('IN PROGRESS', 'In Progress', '#2D7DD2'), ('SOLVED', 'Solved', '#18A66A')):
	card = Frame(stats, background='white', padx=18, pady=10)
	card.pack(side='left', fill='x', expand=True, padx=5)
	Label(card, text=title, background='white', foreground='#718096', font=('Segoe UI', 9, 'bold')).pack(anchor='w')
	stat_labels[key] = Label(card, text='0', background='white', foreground=color, font=('Segoe UI', 22, 'bold'))
	stat_labels[key].pack(anchor='w')

form = Frame(root, background='white', padx=25, pady=20)
form.pack(fill='both', expand=True, padx=25, pady=(0, 20))
Label(form, text='Submit a new complaint', background='white', foreground='#172A46', font=('Segoe UI', 16, 'bold')).grid(row=0, column=0, columnspan=4, sticky='w', pady=(0, 14))
Label(form, text='Full name', background='white', foreground='#43536A').grid(row=1, column=0, sticky='w', pady=7)
fullname = Entry(form, width=30, font=('Segoe UI', 10))
fullname.grid(row=1, column=1, sticky='ew', padx=12, pady=7)
Label(form, text='Gender', background='white', foreground='#43536A').grid(row=1, column=2, sticky='w', pady=7)
gender = StringVar(value='Not specified')
Combobox(form, textvariable=gender, values=('Not specified', 'Male', 'Female', 'Other'), state='readonly', width=16).grid(row=1, column=3, sticky='ew', padx=12, pady=7)
Label(form, text='Category', background='white', foreground='#43536A').grid(row=2, column=0, sticky='w', pady=7)
category = StringVar(value='General')
Combobox(form, textvariable=category, values=('General', 'Service', 'Staff', 'Product', 'Billing', 'Technical'), state='readonly', width=27).grid(row=2, column=1, sticky='ew', padx=12, pady=7)
Label(form, text='Priority', background='white', foreground='#43536A').grid(row=2, column=2, sticky='w', pady=7)
priority = StringVar(value='Medium')
Combobox(form, textvariable=priority, values=('Low', 'Medium', 'High', 'Urgent'), state='readonly', width=16).grid(row=2, column=3, sticky='ew', padx=12, pady=7)
Label(form, text='Complaint details', background='white', foreground='#43536A').grid(row=3, column=0, sticky='nw', pady=7)
comment = Text(form, height=7, font=('Segoe UI', 10), wrap='word')
comment.grid(row=3, column=1, columnspan=3, sticky='nsew', padx=12, pady=7)
form.columnconfigure(1, weight=1)
form.columnconfigure(3, weight=1)
form.rowconfigure(3, weight=1)

def update_stats():
	counts = conn.Counts()
	for key, label in stat_labels.items():
		label.config(text=str(counts[key]))

def save_data():
	if not fullname.get().strip() or not comment.get('1.0', 'end').strip():
		showerror('Missing information', 'Please enter a name and complaint description.')
		return
	conn.Add(fullname.get().strip(), gender.get(), comment.get('1.0', 'end').strip(), priority.get(), category.get())
	fullname.delete(0, 'end')
	comment.delete('1.0', 'end')
	update_stats()
	showinfo('Submitted', 'Your complaint has been submitted and marked as unread.')

buttons = Frame(form, background='white')
buttons.grid(row=4, column=0, columnspan=4, sticky='e', pady=(15, 0))
Button(buttons, text='View complaint desk', command=lambda: ListComp(root)).pack(side='right', padx=(10, 0))
Button(buttons, text='Submit complaint', command=save_data).pack(side='right')
update_stats()
root.mainloop()

#Style
style = Style()
style.theme_use('classic')
for elem in ['TLabel', 'TButton', 'TRadioutton']:
	style.configure(elem, background='#AEB6BF')

#Gridx1353
labels = ['Full Name:', 'Gender:', 'Comment:']
for i in range(3):
	Label(root, text=labels[i]).grid(row=i, column=0, padx=10, pady=10)

BuList = Button(root, text='List Comp.')
BuList.grid(row=4, column=1)
BuSubmit = Button(root, text='Submit Now')
BuSubmit.grid(row=4, column=2)

#Entries
fullname = Entry(root, width=40, font=('Arial', 14))
fullname.grid(row=0, column=1, columnspan=2)
SpanGender = StringVar()
Radiobutton(root, text='Male', value='male', variable=SpanGender).grid(row=1, column=1)
Radiobutton(root, text='Female', value='female', variable=SpanGender).grid(row=1, column=2)
comment = Text(root, width=35, height=5, font=('Arial', 14))
comment.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
#brought to you by code-projects.org
def SaveData():
	msg = conn.Add(fullname.get(), SpanGender.get(), comment.get(1.0, 'end'))
	fullname.delete(0, 'end')
	comment.delete(1.0, 'end')
	showinfo(title='Add Info', message=msg)

def ShowList():
	listrequest = ListComp()


BuSubmit.config(command=SaveData)
BuList.config(command=ShowList)

root.mainloop()
