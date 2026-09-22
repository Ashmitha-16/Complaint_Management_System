from tkinter import *
from tkinter.ttk import Button, Combobox, Scrollbar, Treeview
from tkinter.messagebox import showinfo
from db import DBConnect


class ListComp:
    def __init__(self, master=None):
        self._dbconnect = DBConnect()
        self._root = Toplevel(master) if master else Tk()
        self._root.title('Complaint Desk - All Registered Complaints')
        self._root.geometry('1080x600')
        self._root.minsize(850, 480)
        self._root.configure(background='#F4F7FB')
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(2, weight=1)
        self._build_header()
        self._build_filters()
        self._build_table()
        self._build_actions()
        self._refresh()

    def _build_header(self):
        header = Frame(self._root, background='#172A46', padx=25, pady=18)
        header.grid(row=0, column=0, sticky='ew')
        Label(header, text='ALL REGISTERED COMPLAINTS', background='#172A46', foreground='white', font=('Segoe UI', 20, 'bold')).pack(side='left')
        Label(header, text='Search, update, and resolve every complaint', background='#172A46', foreground='#B9C7DA', font=('Segoe UI', 10)).pack(side='left', padx=18, pady=7)

    def _build_filters(self):
        bar = Frame(self._root, background='#F4F7FB', padx=25, pady=14)
        bar.grid(row=1, column=0, sticky='ew')
        Label(bar, text='Search', background='#F4F7FB', foreground='#43536A', font=('Segoe UI', 10, 'bold')).pack(side='left')
        self._search = StringVar()
        Entry(bar, textvariable=self._search, width=28, font=('Segoe UI', 10)).pack(side='left', padx=(8, 20))
        Label(bar, text='Status', background='#F4F7FB', foreground='#43536A', font=('Segoe UI', 10, 'bold')).pack(side='left')
        self._status = StringVar(value='All')
        status_box = Combobox(bar, textvariable=self._status, values=('All', 'Unread', 'Read', 'In Progress', 'Solved'), state='readonly', width=15)
        status_box.pack(side='left', padx=8)
        Button(bar, text='Show all', command=self._show_all).pack(side='left', padx=8)
        self._search.trace_add('write', lambda *_: self._refresh())
        status_box.bind('<<ComboboxSelected>>', lambda event: self._refresh())

    def _build_table(self):
        frame = Frame(self._root, background='white', padx=12, pady=12)
        frame.grid(row=2, column=0, sticky='nsew', padx=25)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        self._tree = Treeview(frame, columns=('ID', 'Name', 'Category', 'Priority', 'Complaint', 'Created', 'Status'), show='headings', selectmode='browse')
        self._tree.grid(row=0, column=0, sticky='nsew')
        scrollbar = Scrollbar(frame, orient='vertical', command=self._tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self._tree.configure(yscrollcommand=scrollbar.set)
        for column, title, width in (('ID', 'ID', 55), ('Name', 'Name', 140), ('Category', 'Category', 110), ('Priority', 'Priority', 85), ('Complaint', 'Complaint', 330), ('Created', 'Submitted', 125), ('Status', 'Status', 100)):
            self._tree.heading(column, text=title)
            self._tree.column(column, width=width, anchor='w')
        self._tree.tag_configure('Solved', foreground='#16804B')
        self._tree.tag_configure('Unread', foreground='#B45309')

    def _build_actions(self):
        bar = Frame(self._root, background='#F4F7FB', padx=25, pady=14)
        bar.grid(row=3, column=0, sticky='ew')
        for label, status in (('Mark as read', 'Read'), ('Start progress', 'In Progress'), ('Mark as solved', 'Solved'), ('Reopen', 'Unread')):
            Button(bar, text=label, command=lambda value=status: self._set_status(value)).pack(side='left', padx=(0, 8))
        Button(bar, text='Add resolution note', command=self._add_resolution).pack(side='right')

    def _show_all(self):
        self._search.set('')
        self._status.set('All')
        self._refresh()

    def _refresh(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        rows = list(self._dbconnect.ListRequest(self._search.get(), self._status.get()))
        for row in rows:
            self._tree.insert('', 'end', iid=str(row['ID']), values=(row['ID'], row['Name'], row['Category'], row['Priority'], row['Comment'].strip(), row['CreatedAt'], row['Status']), tags=(row['Status'],))
        self._root.title('Complaint Desk - {} Registered Complaints'.format(len(rows)))

    def _selected_id(self):
        selected = self._tree.selection()
        return selected[0] if selected else None

    def _set_status(self, status):
        complaint_id = self._selected_id()
        if complaint_id:
            self._dbconnect.UpdateStatus(complaint_id, status)
            self._refresh()

    def _add_resolution(self):
        complaint_id = self._selected_id()
        if not complaint_id:
            return
        note_window = Toplevel(self._root)
        note_window.title('Resolution note')
        note_window.configure(background='#F4F7FB')
        Label(note_window, text='Resolution details', background='#F4F7FB', font=('Segoe UI', 11, 'bold')).pack(padx=15, pady=(15, 5))
        note = Text(note_window, width=55, height=6, font=('Segoe UI', 10))
        note.pack(padx=15, pady=5)

        def save_note():
            self._dbconnect.UpdateResolution(complaint_id, note.get('1.0', 'end').strip())
            note_window.destroy()
            showinfo('Saved', 'Resolution note saved.')

        Button(note_window, text='Save note', command=save_note).pack(pady=(5, 15))
