import os
import sqlite3
import sys

from PIL import Image
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import *

con = sqlite3.connect('students.db')
cur = con.cursor()
defaultImg = "person.png"
person_id=None


class Main(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Nasi uczniowie")
		self.setGeometry(450, 250, 750, 600)
		self.UI()
		self.show()

	def UI(self):
		self.mainDesign()
		self.layouts()
		self.getStudents()
		self.displayFirstRecord()

	def mainDesign(self):
		self.setStyleSheet("background-color: #FFFFF0;font-size:12pt;font-family:Calibre")
		self.studentsList = QListWidget()
		self.studentsList.itemClicked.connect(self.singleClick)
		self.btnNew = QPushButton("Nowy")
		self.btnNew.setStyleSheet("background-color:#FC0300 ; color: #FFFFFF;  ")
		self.btnNew.clicked.connect(self.addStudents)
		self.btnUpdate = QPushButton("Uaktualnij")
		self.btnUpdate.setStyleSheet("background-color:#FC0300 ; color: #FFFFFF;  ")
		self.btnUpdate.clicked.connect(self.updateStudents)
		self.btnDelete = QPushButton("Skasuj")
		self.btnDelete.setStyleSheet("background-color:#FC0300 ; color: #FFFFFF;  ")
		self.btnDelete.clicked.connect(self.deleteStudent)

	def layouts(self):
		###########################Layouts###################################
		self.mainLayout = QHBoxLayout()
		self.leftLauout = QFormLayout()
		self.rightMainLayout = QVBoxLayout()
		self.rightTopLayout = QHBoxLayout()
		self.rightBottomLayout = QHBoxLayout()
		############################Adding child layouts to main lauout########
		self.rightMainLayout.addLayout(self.rightTopLayout)
		self.rightMainLayout.addLayout(self.rightBottomLayout)
		self.mainLayout.addLayout(self.leftLauout, 45)
		self.mainLayout.addLayout(self.rightMainLayout, 55)
		############################Adding wigets to layout#####################
		self.rightTopLayout.addWidget(self.studentsList)
		self.rightBottomLayout.addWidget(self.btnNew)
		self.rightBottomLayout.addWidget(self.btnUpdate)
		self.rightBottomLayout.addWidget(self.btnDelete)

		############################Seting main widow layout#####################
		self.setLayout(self.mainLayout)

	def addStudents(self):
		self.newStudents = AddStudent()
		self.close()

	def getStudents(self):
		query = "SELECT id, name,surname FROM students"
		students = cur.execute(query).fetchall()
		for student in students:
			self.studentsList.addItem(str(student[0]) + "-" + student[1] + " " + student[2])

	def displayFirstRecord(self):
		query = "SELECT * FROM students ORDER BY ROWID ASC LIMIT 1"
		student = cur.execute(query).fetchone()
		img = QLabel()
		img.setPixmap(QPixmap("/home/krzysiek/PycharmProjects/MySchool/images/" + student[6]))
		name = QLabel(student[1])
		surname = QLabel(student[2])
		pesel = QLabel(student[3])
		phone = QLabel(student[4])
		email = QLabel(student[5])
		address = QLabel(student[7])
		team = QLabel(student[8])
		medreport = QLabel(student[9])
		diagnosis = QLabel(student[10])
		comments = QLabel(student[11])
		self.leftLauout.setVerticalSpacing(20)
		self.leftLauout.addRow("", img)
		self.leftLauout.addRow("Imie :", name)
		self.leftLauout.addRow("Nazwisko :", surname)
		self.leftLauout.addRow("PESEL :", pesel)
		self.leftLauout.addRow("Nr telefonu :", phone)
		self.leftLauout.addRow("Email :", email)
		self.leftLauout.addRow("Adres :", address)
		self.leftLauout.addRow("Grupa :", team)
		self.leftLauout.addRow("Orzeczenie :", medreport)
		self.leftLauout.addRow("Diagnoza :", diagnosis)
		self.leftLauout.addRow("Uwagi :", comments)

	def singleClick(self):
		for i in reversed(range(self.leftLauout.count())):
			widget = self.leftLauout.takeAt(i).widget()

			if widget is not None:
				widget.deleteLater()
		student = self.studentsList.currentItem().text()
		id = student.split("-")[0]
		query = ("SELECT * FROM students WHERE id =?")
		person = cur.execute(query, (id,)).fetchone()  # single item tuple=(1,)
		img = QLabel()
		img.setPixmap(QPixmap("/home/krzysiek/PycharmProjects/MySchool/images/" + person[6]))
		name = QLabel(person[1])
		surname = QLabel(person[2])
		pesel = QLabel(person[3])
		phone = QLabel(person[4])
		email = QLabel(person[5])
		address = QLabel(person[7])
		team = QLabel(person[8])
		medreport = QLabel(person[9])
		diagnosis = QLabel(person[10])
		comments = QLabel(person[11])
		self.leftLauout.setVerticalSpacing(20)
		self.leftLauout.addRow("", img)
		self.leftLauout.addRow("Imie :", name)
		self.leftLauout.addRow("Nazwisko :", surname)
		self.leftLauout.addRow("PESEL :", pesel)
		self.leftLauout.addRow("Nr telefonu :", phone)
		self.leftLauout.addRow("Email :", email)
		self.leftLauout.addRow("Adres :", address)
		self.leftLauout.addRow("Grupa :", team)
		self.leftLauout.addRow("Orzeczenie :", medreport)
		self.leftLauout.addRow("Diagnoza :", diagnosis)
		self.leftLauout.addRow("Uwagi :", comments)

	def deleteStudent(self):
		if self.studentsList.selectedItems():
			person = self.studentsList.currentItem().text()
			id = person.split("-")[0]
			mbox = QMessageBox.question(self, "Uwaga", "Czy napewno usunąć ucznia z listy?",
			                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if mbox == QMessageBox.Yes:
				try:
					query = "DELETE FROM students WHERE id=?"
					cur.execute(query, (id,))
					con.commit()
					QMessageBox.information(self, "Info", "Uczeń został usunięty z listy")
					self.close()
					self.main = Main()

				except:
					QMessageBox.question(self, "Uwaga", "Osoba nie została usunięta")

		else:
			QMessageBox.information(self,"Uwaga","Proszę zaznacz osobę z listy\n"
			                                     "usunięcie z listy")

	def updateStudents(self):
		global person_id
		if self.studentsList.selectedItems():
			person = self.studentsList.currentItem().text()
			person_id=person.split("-")[0]
			self.updateWindow=UpdateStudents()

		else:
			QMessageBox.information(self, "Uwaga", "Proszę zaznacz osobę z listy\n"
			                                       "uaktualnienie danych")

class UpdateStudents(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Uaktualnij dane ucznia")
		self.setGeometry(350, 150, 750, 800)
		self.UI()
		self.show()

	def UI(self):
		self.getPerson()
		self.mainDesign()
		self.layouts()

	def closeEvent(self, event):
		self.main = Main()

	def getPerson(self):
		global person_id
		query = "SELECT * FROM students WHERE id=?"
		student = cur.execute(query,(person_id,)).fetchone()
		self.name = student[1]
		self.surname = student[2]
		self.pesel = student[3]
		self.phone = student[4]
		self.email = student[5]
		self.img = student[6]
		self.address = student[7]
		self.team = student[8]
		self.medreport = student[9]
		self.diagnosis = student[10]
		self.comments = student[11]



	def mainDesign(self):
		######################Top Layout Widget#################
		self.setStyleSheet("background-color: #FFFFF0; font-size:12pt;font-family:calibre")
		self.title = QLabel("Aktualizuj dane")
		self.title.setStyleSheet('font-size: 16pt;font-family:Arial Bold;background-colour:')
		self.imgAdd = QLabel()
		self.imgAdd.setPixmap(QPixmap("/home/krzysiek/PycharmProjects/MySchool/images/{}".format(self.img)))
		##########################Bottom layout Widgets###########
		self.nameLbl = QLabel("Imię :")
		self.nameEntry = QLineEdit()
		self.nameEntry.setText(self.name)
		self.surnameLbl = QLabel("Nazwisko :")
		self.surnameEntry = QLineEdit()
		self.surnameEntry.setText(self.surname)
		self.peselLbl = QLabel("PESEL :")
		self.peselEntry = QLineEdit()
		self.peselEntry.setText(self.pesel)
		self.phoneLbl = QLabel("Nr telefonu :")
		self.phoneEntry = QLineEdit()
		self.phoneEntry.setText(self.phone)
		self.emailLbl = QLabel("Email :")
		self.emailEntry = QLineEdit()
		self.emailEntry.setText(self.email)
		self.imgLbl = QLabel("Obrazek :")
		self.imgButton = QPushButton("Wstaw obrazek")
		self.imgButton.setStyleSheet("background-color:#FC0300 ; color: #FFFFFF;  ")
		self.imgButton.clicked.connect(self.uploadImage)
		self.addressLbl = QLabel("Adres :")
		self.addressEditor = QTextEdit()
		self.addressEditor.setText(self.address)
		self.teamLbl = QLabel("Grupa :")
		self.teamEntry = QLineEdit()
		self.teamEntry.setText(self.team)
		self.medreportLbl = QLabel("Orzeczenie :")
		self.medreportEditor = QTextEdit()
		self.medreportEditor.setText(self.medreport)
		self.diagnosisLbl = QLabel("Diagnoza :")
		self.diagnosisEditor = QTextEdit()
		self.diagnosisEditor.setText(self.diagnosis)
		self.commentsLbl = QLabel("Uwagi :")
		self.commentsEntry = QLineEdit()
		self.commentsEntry.setText(self.diagnosis)
		self.updateButton = QPushButton("Aktualizuj")
		self.updateButton.setStyleSheet("background-color:#FC0300 ; color: #FFFFFF;  ")
		self.updateButton.clicked.connect(self.updateStudent)


	def layouts(self):
		################Layouts ################################
		self.mainLayout = QVBoxLayout()
		self.topLayout = QVBoxLayout()
		self.bottomLayout = QFormLayout()

		################adding child layout to main layout#######
		self.mainLayout.addLayout(self.topLayout)
		self.mainLayout.addLayout(self.bottomLayout)

		#################adding widgets to layouts#################
		###############top layout################
		self.topLayout.addStretch()
		self.topLayout.addWidget(self.title)
		self.topLayout.addWidget(self.imgAdd)
		self.topLayout.addStretch()
		self.topLayout.setContentsMargins(325, 10, 10, 10)
		################button layout################
		self.bottomLayout.addRow(self.nameLbl, self.nameEntry)
		self.bottomLayout.addRow(self.surnameLbl, self.surnameEntry)
		self.bottomLayout.addRow(self.peselLbl, self.peselEntry)
		self.bottomLayout.addRow(self.phoneLbl, self.phoneEntry)
		self.bottomLayout.addRow(self.emailLbl, self.emailEntry)
		self.bottomLayout.addRow(self.imgLbl, self.imgButton)
		self.bottomLayout.addRow(self.addressLbl, self.addressEditor)
		self.bottomLayout.addRow(self.teamLbl, self.teamEntry)
		self.bottomLayout.addRow(self.medreportLbl, self.medreportEditor)
		self.bottomLayout.addRow(self.diagnosisLbl, self.diagnosisEditor)
		self.bottomLayout.addRow(self.commentsLbl, self.commentsEntry)
		self.bottomLayout.addRow("", self.updateButton)

		#################setting main layout for window###########
		self.setLayout(self.mainLayout)

	def uploadImage(self):
		global defaultImg
		size = (128, 128)
		self.fileName, ok = QFileDialog.getOpenFileName(self, 'Dodaj zdjęcie', '', 'Image Files (*.jpg *.png)')

		if ok:
			defaultImg = os.path.basename(self.fileName)
			img = Image.open(self.fileName)
			img = img.resize(size)
			img.save("/home/krzysiek/PycharmProjects/MySchool/images/{}".format(defaultImg))

	def updateStudent(self):
		global defaultImg
		global person_id
		name = self.nameEntry.text()
		surname = self.surnameEntry.text()
		pesel = self.peselEntry.text()
		phone = self.phoneEntry.text()
		email = self.emailEntry.text()
		img = defaultImg
		address = self.addressEditor.toPlainText()
		team = self.teamEntry.text()
		medreport = self.medreportEditor.toPlainText()
		diagnosis = self.diagnosisEditor.toPlainText()
		comments = self.commentsEntry.text()
		if (name and surname != ""):
			try:
				query = "UPDATE students set name =?, surname=?,pesel=?,phone=?,email=?,img=?,address=?," \
				        "team=?,medreport=?,diagnosis=?,comments=? WHERE id=? "
				cur.execute(query,
				            (name, surname, pesel, phone, email, img, address, team, medreport, diagnosis, comments,person_id))
				con.commit()
				QMessageBox.information(self, "Sukces", "Dane osoby zostały ")
				self.close()
				self.main = Main()

			except:
				QMessageBox.information(self, "Uwaga", "Osoba nie została dodana")

		else:
			QMessageBox.information(self, "Uwaga", "Pozycje nie mogą być puste")



class AddStudent(QWidget):  # copy class AddParents
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Dane ucznia")
		self.setGeometry(350, 150, 750, 800)
		self.UI()
		self.show()

	def UI(self):
		self.mainDesign()
		self.layouts()

	def closeEvent(self, event):
		self.main = Main()

	def mainDesign(self):
		######################Top Layout Widget#################
		self.setStyleSheet("background-color: #FFFFF0; font-size:12pt;font-family:calibre")
		self.title = QLabel("Dodaj ucznia")
		self.title.setStyleSheet('font-size: 16pt;font-family:Arial Bold;background-colour:')
		self.imgAdd = QLabel()
		self.imgAdd.setPixmap(QPixmap('/home/krzysiek/PycharmProjects/MySchool/ikony/school_1.png'))
		##########################Bottom layout Widgets###########
		self.nameLbl = QLabel("Imię :")
		self.nameEntry = QLineEdit()
		self.nameEntry.setPlaceholderText("Wpisz imie ucznia")
		self.surnameLbl = QLabel("Nazwisko :")
		self.surnameEntry = QLineEdit()
		self.surnameEntry.setPlaceholderText("Wpisz nazwisko ucznia")
		self.peselLbl = QLabel("PESEL :")
		self.peselEntry = QLineEdit()
		self.peselEntry.setPlaceholderText("Wpisz PESEL ucznia")
		self.phoneLbl = QLabel("Nr telefonu :")
		self.phoneEntry = QLineEdit()
		self.phoneEntry.setPlaceholderText("Wpisz nr telefonu ucznia")
		self.emailLbl = QLabel("Email :")
		self.emailEntry = QLineEdit()
		self.emailEntry.setPlaceholderText("Wpisz email ucznia")
		self.imgLbl = QLabel("Obrazek :")
		self.imgButton = QPushButton("Wstaw obrazek")
		self.imgButton.setStyleSheet("background-color:#FC0300 ; color: #FFFFFF;  ")
		self.imgButton.clicked.connect(self.uploadImage)
		self.addressLbl = QLabel("Adres :")
		self.addressEditor = QTextEdit()
		self.teamLbl = QLabel("Grupa :")
		self.teamEntry = QLineEdit()
		self.teamEntry.setPlaceholderText("Wpisz grupę ucznia")
		self.medreportLbl = QLabel("Orzeczenie :")
		self.medreportEditor = QTextEdit()
		self.diagnosisLbl = QLabel("Diagnoza :")
		self.diagnosisEditor = QTextEdit()
		self.commentsLbl = QLabel("Uwagi :")
		self.commentsEntry = QLineEdit()
		self.commentsEntry.setPlaceholderText("Wpisz uwagi")
		self.addButton = QPushButton("Dodaj")
		self.addButton.setStyleSheet("background-color:#FC0300 ; color: #FFFFFF;  ")
		self.addButton.clicked.connect(self.addStudent)

	def layouts(self):
		################Layouts ################################
		self.mainLayout = QVBoxLayout()
		self.topLayout = QVBoxLayout()
		self.bottomLayout = QFormLayout()

		################adding child layout to main layout#######
		self.mainLayout.addLayout(self.topLayout)
		self.mainLayout.addLayout(self.bottomLayout)

		#################adding widgets to layouts#################
		###############top layout################
		self.topLayout.addStretch()
		self.topLayout.addWidget(self.title)
		self.topLayout.addWidget(self.imgAdd)
		self.topLayout.addStretch()
		self.topLayout.setContentsMargins(325, 10, 10, 10)
		################button layout################
		self.bottomLayout.addRow(self.nameLbl, self.nameEntry)
		self.bottomLayout.addRow(self.surnameLbl, self.surnameEntry)
		self.bottomLayout.addRow(self.peselLbl, self.peselEntry)
		self.bottomLayout.addRow(self.phoneLbl, self.phoneEntry)
		self.bottomLayout.addRow(self.emailLbl, self.emailEntry)
		self.bottomLayout.addRow(self.imgLbl, self.imgButton)
		self.bottomLayout.addRow(self.addressLbl, self.addressEditor)
		self.bottomLayout.addRow(self.teamLbl, self.teamEntry)
		self.bottomLayout.addRow(self.medreportLbl, self.medreportEditor)
		self.bottomLayout.addRow(self.diagnosisLbl, self.diagnosisEditor)
		self.bottomLayout.addRow(self.commentsLbl, self.commentsEntry)
		self.bottomLayout.addRow("", self.addButton)

		#################setting main layout for window###########
		self.setLayout(self.mainLayout)

	def uploadImage(self):
		global defaultImg
		size = (128, 128)
		self.fileName, ok = QFileDialog.getOpenFileName(self, 'Dodaj zdjęcie', '', 'Image Files (*.jpg *.png)')

		if ok:
			defaultImg = os.path.basename(self.fileName)
			img = Image.open(self.fileName)
			img = img.resize(size)
			img.save("/home/krzysiek/PycharmProjects/MySchool/images/{}".format(defaultImg))

	def addStudent(self):
		global defaultImg
		name = self.nameEntry.text()
		surname = self.surnameEntry.text()
		pesel = self.peselEntry.text()
		phone = self.phoneEntry.text()
		email = self.emailEntry.text()
		img = defaultImg
		address = self.addressEditor.toPlainText()
		team = self.teamEntry.text()
		medreport = self.medreportEditor.toPlainText()
		diagnosis = self.diagnosisEditor.toPlainText()
		comments = self.commentsEntry.text()
		if (name and surname != ""):
			try:
				query = "INSERT INTO students (name,surname,pesel,phone,email,img,address," \
				        "team,medreport,diagnosis,comments) VALUES (?,?,?,?,?,?,?,?,?,?,?) "
				cur.execute(query,
				            (name, surname, pesel, phone, email, img, address, team, medreport, diagnosis, comments))
				con.commit()
				QMessageBox.information(self, "Sukces", "Osoba została dodana pomyślnie")
				self.close()
				self.main = Main()

			except:
				QMessageBox.information(self, "Uwaga", "Osoba nie została dodana")

		else:
			QMessageBox.information(self, "Uwaga", "Pozycje nie mogą być puste")


def main():
	APP = QApplication(sys.argv)
	window = Main()
	sys.exit(APP.exec_())


if __name__ == '__main__':
	main()
