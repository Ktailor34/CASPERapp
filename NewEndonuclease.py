import sys, os
import subprocess as sub
from threading import Thread
from queue import Queue, Empty
from PyQt5 import QtWidgets, uic, QtGui, QtCore, Qt
from bioservices import KEGG
from NCBI_API import Assembly, GBFF_Parse
import GlobalSettings
import multitargeting
import populationAnalysis
from functools import partial
from Algorithms import SeqTranslate
from NCBI_Search_Window import NCBI_Search_File

class NewEndonuclease(QtWidgets.QDialog):
	
	def __init__(self):
		super(NewEndonuclease, self).__init__()
		uic.loadUi('newendonuclease.ui', self)
		self.setWindowTitle('New Endonuclease')
		self.k = KEGG()
		#self.info_path = info_path
		
		validPAM = ('A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y')
		
		self.button = self.findChild(QtWidgets.QDialogButtonBox, 'buttonBox') # Find the button
		
		self.name = self.findChild(QtWidgets.QLineEdit, 'lineEdit')
		self.abbr = self.findChild(QtWidgets.QLineEdit, 'lineEdit_2')
		self.pam = self.findChild(QtWidgets.QLineEdit, 'lineEdit_3')
		self.pam3 = self.findChild(QtWidgets.QRadioButton, 'radioButton')
		self.pam5 = self.findChild(QtWidgets.QRadioButton, 'radioButton_2')
		pamFlag = False;
		
		self.comboBox1 = self.findChild(QtWidgets.QComboBox, 'comboBox')
		self.comboBox2 = self.findChild(QtWidgets.QComboBox, 'comboBox_2')
		self.comboBox1.addItem('CRISPR_SCAN_DATA ')
		self.comboBox2.addItem('HSU_MATRIX_spCAS9-2013 ')	
	
		self.button.clicked.connect(self.printButtonPressed)
	
	def writeNewEndonuclease(self, newEndonucleaseStr):
		with open(GlobalSettings.CASPER_FOLDER_LOCATION + '/CASPERinfo', 'r') as f, open(GlobalSettings.CASPER_FOLDER_LOCATION + "/new_file",'w') as f1:
   			for line in f:
       				f1.write(line)
       				if 'ENDONUCLEASES' in line:
          				f1.write(newEndonucleaseStr+'\n')  # Move f1.write(line) above, to write above instead
		os.rename(GlobalSettings.CASPER_FOLDER_LOCATION + "/new_file", GlobalSettings.CASPER_FOLDER_LOCATION + "/CASPERinfo")  # Rename the new file  		

		
	def printButtonPressed(self):
		# This is executed when the button is pressed
		seed = '16'
		length = '20';
		
		if (self.pam5.isChecked() == False):
			myString = self.abbr.text() + ';' + self.pam.text() + ';' + seed + ';' + length + ';' + '5' + ';' + self.name.text() + ';' + 'U-A' + ';' +  '1'
			self.writeNewEndonuclease(myString)
			#print(myString)
		elif (self.pam3.isChecked() == False):
			myString = self.abbr.text() + ';' + self.pam.text() + ';' + seed + ';' + length + ';' + '3' + ';' + self.name.text() + ';' + 'U-A' + ';' +  '1'
			self.writeNewEndonuclease(myString)
			#print(myString)
		else:
			print("error")

