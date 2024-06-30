from contextlib import redirect_stdout
import io
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
    QVBoxLayout,
    QWidget,
    QPlainTextEdit
)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # window properties
        self.setWindowTitle("Proof of concept")
        self.width=600
        self.height=800
        self.left = 10
        self.top = 10
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Qt layout and widgets
        layout = QVBoxLayout()
        self.textbox =QPlainTextEdit(self)
        self.textbox.resize(280, 500)
        self.textbox.setTabStopDistance(20) #tabs are historically too wide
        layout.addWidget(self.textbox)
        run_button =QPushButton('Run', self)
        
        #connect button to function
        run_button.clicked.connect(self.on_click)
        layout.addWidget(run_button)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()
    
    def on_click(self):
        # read from the textbox
        tv = self.textbox.toPlainText()
        # redirect terminal output
        temp_out = io.StringIO()
        sys.stdout = temp_out
        temp_err = io.StringIO()
        sys.stderr = temp_err

        try: 
            # actually execute the input code
            exec(tv)
            #display output in message box
            message = temp_out.getvalue()
            if len(message) > 0:
                QMessageBox.question(self,"Output", message, QMessageBox.Yes)
        except:
            #display error in message box
            # actually not quite working rn
            QMessageBox.question(self,"Error", temp_err.getvalue(), QMessageBox.Yes)
            




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())

''' ========== TRY =============

with open("main.py","r") as f:
  print(f.read())

==============================

self.setWindowTitle("oh no")

==============================



'''