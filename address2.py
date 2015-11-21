'''
Joseph Labrum
Assignment 3 - Address Book
CSCI310 - Python

This is an GUI contact storage program.
tutorialspoints.com/sqlite/sqlite_select_query.html
'''

import tkinter
import tkinter.messagebox
import os.path
import sqlite3

class AddressBook(tkinter.Frame):
	results = ["","","","","","","","","","","","", 0, 0, 0, 0]
	selectID = 0

	def __init__(self, parent):
		tkinter.Frame.__init__(self, parent)
		self.parent = parent
		self.parent.title('Address Book')

		self.initUI()
		self.pack(expand=True, fill=tkinter.BOTH)
		
		self.conn = sqlite3.connect('addressbook.db') #create a connection
		self.curse = self.conn.cursor()
		
		self.CreateAddressBookTable()
		
	def initUI(self):

		titles = ['First Name:','Last Name:','Phone Number:']
	
		self.searchlabel = tkinter.Label(self, text = "Search by first name:")
		self.searchlabel.pack()
		self.searchlabel.place(x = 20, y = 30, height=25)

		self.resultlabel = tkinter.Label(self, text = "Search Results:")
		self.resultlabel.pack()
		self.resultlabel.place(x = 440, y = 30, height=25)
		
		for i in range(3):
			l = tkinter.Label(self, text=titles[i], fg='black')
			l.place(x = 20, y = 30 + (i+2)*30, height=25)

		self.eFName = tkinter.Entry()
		self.eFName.place(x = 160, y = 90, width=140, height=25)
		self.eLName = tkinter.Entry()
		self.eLName.place(x = 160, y = 120, width=140, height=25)
		self.ePhone = tkinter.Entry()
		self.ePhone.place(x = 160, y = 150, width=140, height=25)

		self.SearchEntry = tkinter.Entry()
		self.SearchEntry.place(x = 160, y = 30, width=140, height=25)
		self.searchButton = tkinter.Button(text = "Search", command=self.bSearch)
		self.searchButton.pack()
		self.searchButton.place(x = 330, y = 30, width=80, height=25)
		self.addButton = tkinter.Button(self, text = "Update", command=self.updateB)
		self.addButton.pack()
		self.addButton.place(x = 330, y = 90, width=80, height=25)
		self.delButton = tkinter.Button(self, text = "Update", command=self.updateB)
		self.delButton.pack()
		self.delButton.place(x = 330, y = 120, width=80, height=25)
		self.updateButton = tkinter.Button(self, text = "Update", command=self.updateB)
		self.updateButton.pack()
		self.updateButton.place(x = 330, y = 150, width=80, height=25)
		self.prevButton = tkinter.Button(self, text = "Add", command=self.addB)
		self.prevButton.pack()
		self.prevButton.place(x = 160, y = 190, width=60, height=25)
		self.nextButton = tkinter.Button(self, text = "Delete", command=self.deleteB)
		self.nextButton.pack()
		self.nextButton.place(x = 240, y = 190, width=60, height=25)

		self.fButton1 = tkinter.Button(self, text = (self.results[0], self.results[4]), background='white', command=self.bFill(0))
		self.fButton1.pack()
		self.fButton1.place(x = 440, y = 60, width=180, height=30)
		self.fButton2 = tkinter.Button(self, text = (self.results[1], self.results[5]), background='white', command=self.bFill(1))
		self.fButton2.pack()
		self.fButton2.place(x = 440, y = 90, width=180, height=30)
		self.fButton3 = tkinter.Button(self, text = (self.results[2], self.results[6]), background='white',command=self.bFill(2))
		self.fButton3.pack()
		self.fButton3.place(x = 440, y = 120, width=180, height=30)
		self.fButton4 = tkinter.Button(self, text = (self.results[3], self.results[7]), background='white', command=self.bFill(3))
		self.fButton4.pack()
		self.fButton4.place(x = 440, y = 150, width=180, height=30)
		

	def CreateAddressBookTable(self):
		sql = '''CREATE TABLE IF NOT EXISTS AddressBook (FirstName text, LastName text, Phone text, ID integer PRIMARY KEY AUTOINCREMENT)'''
		self.dbCursor.execute(sql)
		self.dbConnection.commit()

	def bSearch(self):
		if len(self.SearchEntry.get()) == 0:
			tkinter.messagebox.showinfo('Error', 'Search Field Is Blank')
		else:
			name = (self.SearchEntry.get(),)
			sql = '''SELECT * FROM AddressBook where FirstName = ?'''
			self.curse.execute(sql, name)
			rows = self.curse.fetchall()
			if rows:
				print("if rows")
				counter = 0
				for row in rows[:4]:
					print("For rows")
					print(row[1])
					self.results[counter] = row[0]
					self.results[counter+4] = row[1]
					self.results[counter+8] = row[2]
					self.results[counter+12] = row[3]
					counter += 1
				if counter < 3:
					while counter < 4:
						self.results[counter] = ""
						self.results[counter+4] = ""
						self.results[counter+8] = ""
						self.results[counter+12] = 0
						counter+=1					
				self.initUI()
				for row in rows[:1]:
					self.SetEntryText(self.eFName, row[0])
					self.SetEntryText(self.eLName, row[1])
					self.SetEntryText(self.ePhone, row[2])

			else:
				print("ELSE!")
				name = " "
				self.SetEntryText(self.eFName, name)
				self.SetEntryText(self.eLName, name)
				self.SetEntryText(self.ePhone, name)
				self.results = ["","","","","","","","","","","","", 0, 0, 0, 0]
				self.selectID = 0
				self.initUI()
				tkinter.messagebox.showinfo('Error', 'Not Found')

	def bFill(self, n):
		self.SetEntryText(self.eFName, self.results[n])
		self.SetEntryText(self.eLName, self.results[n+4])
		self.SetEntryText(self.ePhone, self.results[n+8])

	def updateB(self):
		print('updating')

	def addB(self):
		print('adding')
		sql = '''INSERT INTO AddressBook (FirstName, LastName, Phone) VALUES (?,?,?)'''
		self.curse.execute(sql, (self.eFName.get(), self.eLName.get(), self.ePhone.get()))
		self.conn.commit() #must save/commit the changes or will be lost if the connection is closed.
		tkinter.messagebox.showinfo('Success', 'Added successfully!')

	def deleteB(self):
		sql = '''DELETE FROM AddressBook WHERE FirstName = ? and LastName = ? '''
		self.curse.execute(sql, (self.eFName.get(), self.eLName.get()))
		self.conn.commit()
		tkinter.messagebox.showinfo('Success', 'Deleted Successfully!')
		
	def CreateAddressBookTable(self):
		sql = '''CREATE TABLE IF NOT EXISTS AddressBook (FirstName text, LastName text, Phone text)'''
		self.curse.execute(sql)
		self.conn.commit()
			
	def SetEntryText(self, txtObject, value):
		txtObject.delete(0, tkinter.END)
		txtObject.insert(0, value)
	
	def __del__(self):
		self.conn.close() #close the connection when the Window is closed
		

def main():
	root = tkinter.Tk()
	#root.geometry('600x400+300+200')
	root.geometry('640x230')
	root.resizable(width='false', height='false')
	app = AddressBook(root)
	
	root.mainloop()
	
	
if __name__ == "__main__":
	main()