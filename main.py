import json
import sys
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit, QCheckBox, QPushButton


def load_data(json_file):

    try:
        with open(json_file,"r",encoding="utf-8") as file:
            data = json.load(file)
    except:
            data = None
    return data

class MessageBoard(QWidget):
    def __init__(self): # Constructeur
        super().__init__() # Constructeur QWidget
        self.setWindowTitle("Outliner Organiser")
        self.create_ui()
 
    def create_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel("enter JSON rule path")
        box = QTextEdit()
        checkbox_selection = QCheckBox("Apply on selection only")
        checkbox_colors = QCheckBox("Apply colors")
        checkbox_reorder = QCheckBox("Apply reorder")
        button = QPushButton("Organise Outliner")

        box.setFixedSize(450,27)

        layout.addWidget(label)
        layout.addWidget(box)
        layout.addWidget(checkbox_selection)
        layout.addWidget(checkbox_colors)
        layout.addWidget(checkbox_reorder)
        layout.addWidget(button)

        self.box_input = box #self est utiliser seulement dans la classe, ca le met pour toute la classe
        button.clicked.connect(self.on_click)
        
        # QTextEdit
 
        # QPushButton
    
    def read_text_input(self):
        user_input_text = self.box_input.toPlainText()
        print(user_input_text)
        return user_input_text
   
    def on_click(self):
        
        user_json_path =  self.read_text_input()
        self.data = load_data(user_json_path)# appelle la fonction qui fetch le json

        print("on click called")
        print(user_json_path)
        # QMessageBox
        print(self.data)
   
 

def main():
    global widget
    try:
        widget.close()
    except Exception:
        pass
    widget = MessageBoard()
    widget.show()
 
main()