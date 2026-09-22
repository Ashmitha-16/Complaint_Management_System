#!/usr/bin/python3
import sqlite3
from pathlib import Path
from datetime import datetime

class DBConnect:
	def __init__(self):
		self._db = sqlite3.connect(str(Path(__file__).with_name('information.db')))
		self._db.row_factory = sqlite3.Row
		self._db.execute('create table if not exists Comp(ID integer primary key autoincrement, Name varchar(255), Gender varchar(255), Comment text)')
		columns = [row['name'] for row in self._db.execute('pragma table_info(Comp)')]
		new_columns = {
			'Status': "varchar(20) not null default 'Unread'",
			'Priority': "varchar(20) not null default 'Medium'",
			'Category': "varchar(40) not null default 'General'",
			'CreatedAt': "varchar(30) not null default ''",
			'Resolution': "text not null default ''"
		}
		for name, definition in new_columns.items():
			if name not in columns:
				self._db.execute('alter table Comp add column {} {}'.format(name, definition))
		self._db.execute("update Comp set CreatedAt = ? where CreatedAt = ''", (datetime.now().strftime('%Y-%m-%d %H:%M'),))
		self._db.commit()
	def Add(self, name, gender, comment, priority, category):
		self._db.execute('insert into Comp (Name, Gender, Comment, Priority, Category, CreatedAt) values (?,?,?,?,?,?)',
			(name, gender, comment, priority, category, datetime.now().strftime('%Y-%m-%d %H:%M')))
		self._db.commit()
		return 'Your complaint has been submitted.'
	def ListRequest(self, search='', status='All'):
		query = 'select * from Comp where (Name like ? or Comment like ? or Category like ?)'
		params = ['%{}%'.format(search), '%{}%'.format(search), '%{}%'.format(search)]
		if status != 'All':
			query += ' and Status = ?'
			params.append(status)
		query += ' order by ID desc'
		cursor = self._db.execute(query, params)
		return cursor
	def UpdateStatus(self, complaint_id, status):
		self._db.execute('update Comp set Status = ? where ID = ?', (status, complaint_id))
		self._db.commit()
	def UpdateResolution(self, complaint_id, resolution):
		self._db.execute('update Comp set Resolution = ? where ID = ?', (resolution, complaint_id))
		self._db.commit()
	def Counts(self):
		return {status: self._db.execute('select count(*) from Comp where Status = ?', (status,)).fetchone()[0]
			for status in ('Unread', 'Read', 'In Progress', 'Solved')}
