import json
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit, QCheckBox, QPushButton

import maya.cmds as cmds

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
        self.setWindowTitle("Outliner Organiser") # titre du widget
        self.create_ui()
 
    def create_ui(self):
        #initialisation du layout du widget
        layout = QVBoxLayout(self)
        label = QLabel("enter JSON rule path")
        box = QTextEdit()
        self.checkbox_selection = QCheckBox("Apply on selection only")
        self.checkbox_colors = QCheckBox("Apply colors")
        self.checkbox_reorder = QCheckBox("Apply reorder")

        self.button = QPushButton("Organise Outliner")
        self.button.setEnabled(False)

        box.setFixedSize(450,27)

        #creation du layout du widget
        layout.addWidget(label)
        layout.addWidget(box)
        layout.addWidget(self.checkbox_selection)
        layout.addWidget(self.checkbox_colors)
        layout.addWidget(self.checkbox_reorder)
        layout.addWidget(self.button)

        self.box_input = box #self est utiliser seulement dans la classe, ca le met pour toute la classe

        #declanche une fonction dans ce cas update_button_state, si cheched 
        self.checkbox_colors.toggled.connect(self.update_button_state)
        self.checkbox_reorder.toggled.connect(self.update_button_state)

        self.button.clicked.connect(self.on_click)
        
    def update_button_state(self):
        # activate le bouton(Organise outliner) seulement si un des ces box est cheched  
        any_checked = ( 
            self.checkbox_colors.isChecked() or 
            self.checkbox_reorder.isChecked()
        )
        self.button.setEnabled(any_checked)

    def read_text_input(self):
        user_input_text = self.box_input.toPlainText()
        return user_input_text
   
    def on_click(self):
        
        user_json_path =  self.read_text_input()# path du user
        self.data = load_data(user_json_path)# appelle la fonction qui fetch le json

        selection_only = self.checkbox_selection.isChecked()

        if self.checkbox_colors.isChecked():
            if self.data:
                self.outline_objects_colors(self.data, selection_only)

        if self.checkbox_reorder.isChecked():
            self.outline_objects_reorder(selection_only)

    def outline_objects_colors(self, color_dictionnaire, selection_only=False):
        # tout les actions que ce fond entre les openChunk true et false, peuvent etre undo 
        cmds.undoInfo(openChunk=True)

        try:
            if selection_only:#prend seulement ce que le jouer a slectionner dans outliner 
                objet_maya = cmds.ls(selection=True, transforms=True)
            else:#prend tout dans le outliner 
                objet_maya = cmds.ls(dag=True, transforms=True)

            for obj in objet_maya:
                if '_' in obj:
                    parties = obj.split('_')
                    if parties:
                        prefixe = parties[0]+ '_' #extraire les prefixes

                        if prefixe in color_dictionnaire:
                            couleur = color_dictionnaire[prefixe]

                            cmds.setAttr(f"{obj}.useOutlinerColor", True)#enables la couleur custom 
                            cmds.setAttr(f"{obj}.outlinerColor", *couleur, type="float3")#met la couleur sur l'objet du outliner 
        finally:
            cmds.undoInfo(closeChunk=True) 

    def extraire_numero(self, nom_objet):
            chiffres= [char for char in nom_objet if char.isdigit()]# prend les chiffres dans le nom
            return int("".join(chiffres))
    
    def outline_objects_reorder(self, selection_only=False):
        cmds.undoInfo(openChunk=True) 
        try:
            if selection_only:#prend tout ce que le user a selectionner, if the checkbox unabled
                objet_maya = cmds.ls(selection=True, transforms=True)
            else:#prend tout
                objet_maya = cmds.ls(dag=True, transforms=True)

            objets = []#array

            for obj in objet_maya:
                if any(char.isdigit() for char in obj):#utilise seulement des des noms qui ont des chiffres 
                    objets.append(obj)
                
            objets.sort(key=self.extraire_numero)#met en ordre croissant 

            for obj in reversed(objets):#met les objets en ordre croissant de haut en bas dans le outliner
                cmds.reorder(obj, front=True)

        finally:
            cmds.undoInfo(closeChunk=True) 

def main():
    global widget
    try:
        widget.close()
    except Exception:
        pass
    widget = MessageBoard()
    widget.show()
main()