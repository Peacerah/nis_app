import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import *
from numpy import random
import sqlite3
#import secondpage
import pandas as pd
import numpy as np
import time
import resources

class NIS(QDialog):
    def __init__(self, parent = None):
        super(NIS, self).__init__(parent)
        fileh = QFile(':/ui/Nis_New_ui.ui')
        fileh.open(QFile.ReadOnly)
        loadUi(fileh, self)
        fileh.close()
        self.loadDataButton.clicked.connect(self.loadData)
        self.repostButton.clicked.connect(self.repost)
        self.refreshButton.clicked.connect(self.clearAll)
        #self.about.clicked.connect(self.showMessage("Succes","Successful reposting"))
        self.progressBar.hide()
        #self.about.clicked.connect(self.showMessage("About TRADEK", "Developer: Abdulazeez Abdulsalam Adekunle\nSoftware Name: TRADEK\nVersion: 1.1"))
        #self.clear_inputLabel.clicked.connect(self.clearInputDir)
        #self.clear_outputLabel.clicked.connect(self.clearOutputDir)
    #def clearInputDir(self):
    #    self.inputLabel.setText(" ")

    #def clearOutputDir(self):
    #    self.outputLabel.setText(" ")

    def clearAll(self):
        self.inputLabel.setText(" ")
        self.outputLabel.setText(" ")
        self.progressBar.hide()

    def loadData(self):
        #self.inputFilename = QFileDialog.getOpenFileName(self, "Open image file","c\\","Excel Workbook(*.xls *.xlsx)")
        #def loadFiles(self)
        self.inputFilename = QFileDialog.getOpenFileName(self, "Open the csv file containing the records of the staffs","c\\","Comma Seperated Value File(*.csv)")
        self.inputLabel.setText(str(self.inputFilename[0]))
        self.input_data =  str(self.inputFilename[0])
        #print(self.input_data)
        
    def showMessage(self, title, text):
        mesgbox = QMessageBox()
        mesgbox.setIcon(QMessageBox.Information)
        mesgbox.setWindowTitle(title)
        mesgbox.setText(text)
        mesgbox.setStandardButtons(QMessageBox.Ok)
        mesgbox.exec_()
    
        
    def repost(self):
        self.progressBar.show()
        for i in range(101):
            time.sleep(0.05)
            self.progressBar.setValue(i)
        self.showMessage("Succes","Successful reposting")
        self.outputFilename = QFileDialog.getSaveFileName(self, "Save the csv file containg the reposting records of the staffs","c\\","Comma Seperated Value File(*.csv)")
        self.outputLabel.setText(self.outputFilename[0])
        #self.output_data =  str(self.outputFilename[0])
        self.output_data =  str(self.outputFilename[0])
        print(self.output_data)
        self.nis_data = pd.read_csv(self.input_data,encoding='ISO-8859-1')
        
        # Conditioning of filtering the records of the staff that have spent greater than or equal to 3 years in services after the last transfer
        #present_date = pd.datetime.now()
        self.nis_data['Date_of_Present_Appointment']= pd.to_datetime(self.nis_data['Date_of_Present_Appointment'], errors='coerce')
        self.nis_data['Days_Spent_In_Service_After_The_Last_Posting'] = pd.Timestamp.now().normalize()- self.nis_data['Date_of_Present_Appointment']
        self.nis_data['Due_For_Reposting'] = np.where(self.nis_data['Days_Spent_In_Service_After_The_Last_Posting'] >= pd.Timedelta(1080,'D'), True, False)
        self.nis_data = self.nis_data.set_index("Service_Number")
        self.nis_data = self.nis_data[self.nis_data["Due_For_Reposting"]==True]
        
        #Begining of Department posting 
                
        
        #Begining of state posting        
        #beginning of automatic assignation of category to the previous_2_state using A,B and C
        conditions1 = [
                        (self.nis_data['Previous_Posting_2'] == "Lagos")|(self.nis_data['Previous_Posting_2'] == "Port-Harcourt")|(self.nis_data['Previous_Posting_2'] == "Kano")|(self.nis_data['Previous_Posting_2'] == "Abuja")|(self.nis_data['Previous_Posting_2'] == "Enugu")|(self.nis_data['Previous_Posting_2'] == "Borno"),
                        (self.nis_data['Previous_Posting_2'] == "Adamawa")|(self.nis_data['Previous_Posting_2'] == "Plateau")|(self.nis_data['Previous_Posting_2'] == "Ogun")|(self.nis_data['Previous_Posting_2'] == "Oyo")|(self.nis_data['Previous_Posting_2'] == "Sokoto")|(self.nis_data['Previous_Posting_2'] == "Kaduna")|(self.nis_data['Previous_Posting_2'] == "Katsina")|(self.nis_data['Previous_Posting_2'] == "Kebbi")|(self.nis_data['Previous_Posting_2'] == "Anambra")|(self.nis_data['Previous_Posting_2'] == "Calabar"),
                        (self.nis_data['Previous_Posting_2'] == "Abia")|(self.nis_data['Previous_Posting_2'] == "Imo")|(self.nis_data['Previous_Posting_2'] == "Zamfara")|(self.nis_data['Previous_Posting_2'] == "Benue")|(self.nis_data['Previous_Posting_2'] == "Ondo")|(self.nis_data['Previous_Posting_2'] == "Yobe")|(self.nis_data['Previous_Posting_2'] == "Niger")|(self.nis_data['Previous_Posting_2'] == "Taraba")|(self.nis_data['Previous_Posting_2'] == "Osun")|(self.nis_data['Previous_Posting_2'] == "Kwara")|(self.nis_data['Previous_Posting_2'] == "Nasarawa")|(self.nis_data['Previous_Posting_2'] == "Jigawa")|(self.nis_data['Previous_Posting_2'] == "Gombe")|(self.nis_data['Previous_Posting_2'] == "Kogi")|(self.nis_data['Previous_Posting_2'] == "Bayelsa")|(self.nis_data['Previous_Posting_2'] == "Ebonyi")|(self.nis_data['Previous_Posting_2'] == "Ekiti")|(self.nis_data['Previous_Posting_2'] == "Edo")|(self.nis_data['Previous_Posting_2'] == "Akwa Ibom")|(self.nis_data['Previous_Posting_2'] == "Delta")|(self.nis_data['Previous_Posting_2'] == "Bauchi"),

                        ]

        # create a list of the values we want to assign for each condition
        values1 = ['A', 'B', 'C']

        # create a new column and use np.select to assign values to it using our lists as arguments
        self.nis_data['previous_2_state_category'] = np.select(conditions1, values1)
        #self.nis_data=self.nis_data.set_index("Service_Number")
        self.nis_data['previous_2_state_category_correct'] =self.nis_data['previous_2_state_category'].apply(lambda x: "C" if x == "0" else x) 
        self.nis_data['previous_2_state_category'] =self.nis_data['previous_2_state_category_correct']
        #end of automatic assignation of category to the previous_2_state using A,B and C
        
        #beginning of Assignation of new states category
        conditions2 = [
                        (self.nis_data['previous_2_state_category'] == 'A'), 
                        (self.nis_data['previous_2_state_category'] == 'B'), 
                        (self.nis_data['previous_2_state_category'] == 'C') 

                        ]

        # create a list of the values we want to assign for each condition
        values2 = ['B', 'C', 'A']

        # create a new column and use np.select to assign values to it using our lists as arguments
        self.nis_data['new_state_category'] = np.select(conditions2, values2)
        
        #State posting
        conditions3 = [
                        (self.nis_data['new_state_category'] == 'A'), 
                        (self.nis_data['new_state_category'] == 'B'), 
                        (self.nis_data['new_state_category'] == 'C') 

                        ]

        # create a list of the values we want to assign for each condition
        a= ["Lagos","Port-Harcourt","Kano","Abuja","Enugu","Borno"]
        b= ["Adamawa","Plateau","Ogun","Oyo","Sokoto","Kaduna","Katsina","Kebbi","Anambra","Calabar"]
        c= ["Abia","Imo","Zamfara","Benue","Ondo","Yobe","Niger","Taraba","Osun","Kwara","Nasarawa","Jigawa","Gombe","Kogi","Bayelsa","Ebonyi","Ekiti","Edo","Akwa Ibom","Delta","Bauchi"]
        values3 = [random.choice(a, size=len(self.nis_data)), random.choice(b,size=len(self.nis_data)),random.choice(c,size=len(self.nis_data))]
        self.nis_data['new_state_post'] = np.select(conditions3, values3)
        # create a new column and use np.select to assign values to it using our lists as arguments
        
        #End of state posting 
        
        
        #Department posting
        conditions4 = [
                        (self.nis_data['Department'] == "Passport/Other Tavel Documents") | (self.nis_data['Department'] == "Border Management"),
                        (self.nis_data['Department'] == "Finance and Account") | (self.nis_data['Department'] == "Migration")| (self.nis_data['Department'] == "PRS"),
                        (self.nis_data['Department'] == "Human Resources") | (self.nis_data['Department'] == "Investigation/Compliance") | (self.nis_data['Department'] == "Visa/Residence"),

                        ]

        # create a list of the values we want to assign for each condition
        values4 = ['A', 'B', 'C']

        # create a new column and use np.select to assign values to it using our lists as arguments
        self.nis_data['previous_dept_category'] = np.select(conditions4, values4)
        
        
        conditions5 = [
                        (self.nis_data['previous_dept_category'] == 'A'), 
                        (self.nis_data['previous_dept_category'] == 'B'), 
                        (self.nis_data['previous_dept_category'] == 'C') 

                        ]

        # create a list of the values we want to assign for each condition
        values5 = ['B', 'C', 'A']

        # create a new column and use np.select to assign values to it using our lists as arguments
        self.nis_data['new_dept_category'] = np.select(conditions5, values5)
        
        
        conditions6 = [
                        (self.nis_data['new_dept_category'] == 'A'), 
                        (self.nis_data['new_dept_category'] == 'B'), 
                        (self.nis_data['new_dept_category'] == 'C') 

                        ]

        # create a list of the values we want to assign for each condition
        a= ["Passport/Other Tavel Documents","Border Management"]
        b= ["Finance and Account","Migration","PRS"]
        c= ["Human Resources","Investigation/Compliance", "Visa/Residence"]
        values6 = [random.choice(a, size=len(self.nis_data)), random.choice(b,size=len(self.nis_data)),random.choice(c,size=len(self.nis_data))]

        # create a new column and use np.select to assign values to it using our lists as arguments
        self.nis_data['new_dept_post'] = np.select(conditions6, values6)
        
        #Merging of Last Name and First Name to become one
        self.nis_data["Full_Name"] = self.nis_data["LastName"] + [" "] + self.nis_data["FirstName"]
        
        self.nis_data = self.nis_data[["Full_Name", "Rank", "Department","new_dept_post","Previous_Posting_2", "new_state_post"]]
        
        self.nis_data.to_csv(self.output_data)
        #self.showMessage("Succes","Successful reposting")
        
        #mesgbox = QMessageBox()
        #mesgbox.setIcon(QMessageBox.Warning)
        #mesgbox.setWindowTitle(title)
        #mesgbox.setText(text)
        #mesgbox.setStandardButtons(QMessageBox.Ok)
        #mesgbox.exec_()
        
        
        
        
        
        
app = QApplication(sys.argv)
app.setStyle("Fusion")
screen = NIS()
screen.show()
sys.exit(app.exec_())