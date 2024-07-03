from contextlib import redirect_stdout
import io
import sys
import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QPlainTextEdit
)


class CodeInputWindow(QMainWindow):
    def __init__(self):
        super(CodeInputWindow, self).__init__()

        # window properties
        self.setWindowTitle("Proof of concept")
        self.width=600
        self.height=600
        self.left = 600
        self.top = 200
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Qt layout and widgets
        layout = QVBoxLayout()
        # code input textbox
        self.textbox =QPlainTextEdit(self)
        self.textbox.resize(280, 500)
        self.textbox.setTabStopDistance(20) # tabs are historically too wide
        layout.addWidget(self.textbox)
        
        # scrolling output textbox
        outputScroll = QScrollArea(self)
        self.outputBox = QPlainTextEdit(self)
        self.outputBox.setReadOnly(True)
        self.outputBox.resize(580, 300) # TODO: figure out automatic size fitting
        self.outputBox.setTabStopDistance(20) # tabs are historically too wide
        outputScroll.setWidget(self.outputBox)
        layout.addWidget(outputScroll)
        
        # run button for code
        run_button =QPushButton('Run', self)
        # connect button to function
        run_button.clicked.connect(self.on_click)
        layout.addWidget(run_button)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()
    
    def on_click(self):
        # read from the textbox
        code_input = self.textbox.toPlainText()
        # redirect terminal output
        temp_out = io.StringIO()
        sys.stdout = temp_out

        try: 
            # actually execute the input code
            exec(code_input)
            # get output from redirected terminal output
            message = temp_out.getvalue() 
            # remove excess newline from print statements
            if len(message) > 0:
                message = message[:-1] if message[-1] in ("\n", "\r") else message
            if len(message) > 0:
                # display output
                self.outputBox.appendPlainText("> "+message)
        except Exception as e:
            # display error 
            # remove excess newline
            message = str(e) # + traceback.format_exc()
            if len(message) > 0:
                message = message[:-1] if message[-1] in ("\n", "\r") else message
            if len(message) > 0:
                # display output
                self.outputBox.appendPlainText("!> "+message)

            

class TestObject():
    data = 1
    def __init__(self, x) -> None:
        self.data = x
    def testMethod(self):
        print(f"test Method works: {self.data}")
    def testSet(self,x):
        self.data = x
    def testGet(self):
        return self.data

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CodeInputWindow()
    ex.show()
    
    testLambda = lambda : print("lambda worked :)")
    testObject = TestObject(1)
    
    sys.exit(app.exec())

''' ========== TRY =============

with open("main.py","r") as f:
  print(f.read())

==============================

self.setWindowTitle("oh no")

==============================



'''