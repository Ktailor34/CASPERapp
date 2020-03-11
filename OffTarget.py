"""This file runs the off target analysis for CASPER. Use the CASPEROfflist.txt file to set up the information you want
    to run with this program.
    WARNING: Running this protocol on a large number of sequences is unwise and may take significant computing power/time."""

"""Called:
O = OffTargetAlgorithm()"""


import os, sys
from PyQt5 import QtWidgets, uic, QtCore
from functools import partial
import GlobalSettings


class OffTarget(QtWidgets.QDialog):

    def __init__(self):

        super(OffTarget, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(sys.argv[0]), 'OffTargetAnalysis.ui'), self)
        self.setWindowTitle("Off-Target Analysis")
        self.show()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.reset()
        self.Run.clicked.connect(self.run_analysis)
        self.tolerancehorizontalSlider.valueChanged.connect(self.tol_change)
        self.tolerancehorizontalSlider.setMaximum(100)
        self.tolerancehorizontalSlider.setMinimum(0)
        self.tolerance = 0.0
        self.tolerancelineEdit.setText("0")
        self.pushButton.clicked.connect(self.tol_change)
        self.cancelButton.clicked.connect(self.exit)
        self.fill_data_dropdown()
        self.perc = False
        self.bool_temp = False
        self.running = False
        self.process = QtCore.QProcess()

        # make sure to intialize the class variable in init. That way elsewhere and other classes can access it
        self.output_path = ''

    #copied from MT to fill in the chromo and endo dropdowns based on CSPR files user provided at the startup
    def fill_data_dropdown(self):
        #fill in chromosome and endo dropdowns
        onlyfiles = [f for f in os.listdir(GlobalSettings.filedir) if os.path.isfile(os.path.join(GlobalSettings.filedir , f))]
        self.orgsandendos = {}
        self.shortName = {}
        for file in onlyfiles:
            if file.find('.cspr') != -1:
                newname = file[0:-4]
                s = newname.split('_')
                hold = open(os.path.join(GlobalSettings.filedir , file))
                buf = (hold.readline())
                species = buf[8:buf.find('\n')]
                endo = str(s[1])
                if species not in self.shortName:
                    self.shortName[species] = s[0]
                if species in self.orgsandendos:
                    self.orgsandendos[species].append(endo)
                else:
                    self.orgsandendos[species] = [endo]
                    self.OrgcomboBox.addItem(species)
        self.data = self.orgsandendos
        self.shortHand = self.shortName
        temp = self.data[str(self.OrgcomboBox.currentText())]
        temp1 = []
        for i in temp:
            i = i.strip('.')
            temp1.append(i)
        self.EndocomboBox.addItems(temp1)
        self.OrgcomboBox.currentIndexChanged.connect(self.changeEndos)

        #fill in Max Mismatch dropdown
        mismatch_list = ['1','2','3','4','5','6','7','8','9','10']
        self.mismatchcomboBox.addItems(mismatch_list)

    #updated endo dropdown based on chromo
    def changeEndos(self):
        self.EndocomboBox.clear()
        temp = self.data[str(self.OrgcomboBox.currentText())]
        temp1 = []
        for i in temp:
            i = i.strip('.')
            temp1.append(i)
        self.EndocomboBox.addItems(temp1)

    #tolerance slider / entry box. Allows for slider to update, or the user to input in text box
    def tol_change(self):
        if(self.tolerance == float(self.tolerancelineEdit.text())):
            self.tolerance = self.tolerancehorizontalSlider.value() / 100 * 0.5
            self.tolerance = round(self.tolerance, 3)
            self.tolerancelineEdit.setText(str(self.tolerance))
        else:
            self.tolerance = float(self.tolerancelineEdit.text())
            self.tolerance = round(self.tolerance, 3)
            self.tolerancehorizontalSlider.setValue(round(self.tolerance/0.5 * 100))

    #run button linked to run_analysis, which is linked to the run button
    def run_command(self):
        #reset bools for new command to run
        self.perc = False
        self.bool_temp = False
        self.running = False

        #get user specified paramters from the UI
        file_name_1 = self.shortName[str(self.OrgcomboBox.currentText())]
        file_name_2 = self.orgsandendos[str(self.OrgcomboBox.currentText())]
        file_name = str(file_name_1) + '_' + str(file_name_2[0]) + 'cspr'

        if (self.AVG.isChecked()):
            avg_output = r' True '
            detailed_output = r' False '
        else:
            avg_output = r' False '
            detailed_output = r' True '

        #setup arguments for C++ .exe
        app_path = GlobalSettings.appdir
        exe_path = os.path.join(os.path.dirname(sys.argv[0]), 'OffTargetFolder/./OT')
        exe_path = '"' +  exe_path + '"'
        data_path = ' "' + os.path.join(os.path.dirname(sys.argv[0]), 'OffTargetFolder/temp.txt') + '" ' ##
        compressed = r' True ' ##
        cspr_path = ' "' + os.getcwd() + '/' + file_name + '" '
        self.output_path = ' "' + os.getcwd() + '/' + self.FileName.text() + '_OffTargetResults.txt" '
        filename = self.output_path
        filename = filename[:len(filename) - 1]
        filename = filename[1:]
        filename = filename.replace(r'\\', '/')
        filename = filename.replace('"', '')
        exists = os.path.isfile(filename)
        CASPER_info_path = r' "' + os.path.join(os.path.dirname(sys.argv[0]), 'CASPERinfo') + '" '
        num_of_mismathes = int(self.mismatchcomboBox.currentText())
        tolerance = self.tolerance

        #create command string
        cmd = exe_path + data_path + compressed + cspr_path + self.output_path + CASPER_info_path + str(num_of_mismathes) + ' ' + str(tolerance) + detailed_output + avg_output
        print(cmd)
        #used to know when the process is done
        def finished():
            self.running = False
            self.progressBar.setValue(100)

        #used to know when data is ready to read from stdout
        def dataReady(p):
            #filter the data from stdout, bools used to know when the .exe starts outputting the progress
            #percentages to be able to type cast them as floats and update the progress bar. Also, must
            #split the input read based on '\n\ characters since the stdout read can read multiple lines at
            #once and is all read in as raw bytes
            line = str(p.readAll())
            line = line[2:]
            line = line[:len(line)-1]
            for lines in filter(None,line.split(r'\r\n')):
                if(lines.find("Running Off Target Algorithm for") != -1 and self.perc == False):
                    self.perc = True
                if(self.perc == True and self.bool_temp == False and lines.find("Running Off Target Algorithm for") == -1):
                    lines = lines[32:]
                    lines = lines.strip(r'\\n')
                    lines = lines.replace("%","")
                    if lines.isnumeric():
                        if(float(lines) < 99):
                            num = float(lines)
                            self.progressBar.setValue(num)
                        else:
                            self.bool_temp = True


        #connect QProcess to the dataReady func, and finished func, reset progressBar only if the outputfile name
        #given does not already exist
        if(exists == False):
            self.process.readyReadStandardOutput.connect(partial(dataReady,self.process))
            self.progressBar.setValue(0)
            self.process.start(cmd)
            #QtCore.QTimer.singleShot(100, partial(self.process.start, cmd))
            self.process.finished.connect(finished)
        else: #error message about file already being created
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.setText("Output file already exists. Please choose a new output file name.")
            msg.exec()

    #linked to run button
    def run_analysis(self):
        #make sure an analysis isn't already running before starting
        if(self.running == False):
            self.running = True
            self.run_command()


    #exit linked to user clicking cancel, resets bools, and kills process if one was running
    def exit(self):
        self.perc = False
        self.bool_temp = False
        self.running = False
        self.process.kill()
        self.hide()

    #closeEvent linked to user pressing the x in the top right of windows, resets bools, and
    #kills process if there was one running
    def closeEvent(self, event):
        self.process.kill()
        self.perc = False
        self.bool_temp = False
        self.running = False
        event.accept()

