import os, sys
from PyQt5 import QtWidgets, uic, QtCore

class show_names_table(QtWidgets.QDialog):
    def __init__(self):
        super(show_names_table, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'name_form.ui'), self)
        self.name_table.setColumnCount(1)

    def fill_table(self, names):
        index = 0
        labels = []
        self.name_table.setRowCount(0)
        for name in names:
            self.name_table.setRowCount(index+1)
            n = QtWidgets.QTableWidgetItem()
            n.setData(QtCore.Qt.EditRole, str(name))
            self.name_table.setItem(index, 0, n)
            labels.append(str(index))
            index += 1
        self.name_table.resizeColumnsToContents()
        self.name_table.setVerticalHeaderLabels(labels)


    def closeEvent(self, event):
        self.hide()
        event.accept()
