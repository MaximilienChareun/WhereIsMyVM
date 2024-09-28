import sys
import json
from PyQt5 import QtWidgets, QtCore, QtGui

class SearchApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Charger le fichier JSON (assurez-vous que 'data.json' est présent)
        with open('data.json', 'r') as json_file:
            self.data_dict = json.load(json_file)

        # Définir la taille et le titre de la fenêtre
        self.setWindowTitle("WHERE IS MY VM")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("background-color: #D3D3D3;")

        # Appliquer le style pour arrondir les bords de la fenêtre
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Utiliser un layout principal
        main_layout = QtWidgets.QVBoxLayout(self)

        # Conteneur principal avec un padding autour
        container = QtWidgets.QFrame(self)
        container.setStyleSheet("""
            QFrame {
                background-color: #e0e0e0;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        container_layout = QtWidgets.QVBoxLayout(container)

        # Titre
        title_label = QtWidgets.QLabel("WHERE IS MY VM", self)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
        title_label.setStyleSheet("color: black;")
        container_layout.addWidget(title_label)

        # Zone de recherche avec bouton
        search_layout = QtWidgets.QHBoxLayout()

        self.search_entry = QtWidgets.QLineEdit(self)
        self.search_entry.setPlaceholderText("Recherche ...")
        self.search_entry.setStyleSheet("border-radius: 10px; padding: 8px; background-color: lightgray;")
        self.search_entry.textChanged.connect(self.update_suggestions)  # Lier l'entrée pour mise à jour des suggestions
        self.search_entry.returnPressed.connect(self.search)  # Connecter la touche Enter à la fonction de recherche
        search_layout.addWidget(self.search_entry)

        self.search_button = QtWidgets.QPushButton("Search", self)
        self.search_button.setStyleSheet("border-radius: 10px; padding: 10px; background-color: #6B8E23; color: white;")
        self.search_button.clicked.connect(self.search)
        search_layout.addWidget(self.search_button)

        container_layout.addLayout(search_layout)

        # Zone pour afficher l'IP
        self.ip_label = QtWidgets.QLabel("IP: XXX", self)
        self.ip_label.setStyleSheet("background-color: lightgray; padding: 8px; border-radius: 10px; font-weight: bold")
        container_layout.addWidget(self.ip_label)

        # Zone de texte pour les résultats
        self.result_box = QtWidgets.QTextEdit(self)
        self.result_box.setReadOnly(True)
        self.result_box.setStyleSheet("border-radius: 10px; padding: 10px; background-color: lightgray;")
        container_layout.addWidget(self.result_box)

        # Listbox pour suggestions d'auto-complétion
        self.suggestions_list = QtWidgets.QListWidget(self)
        self.suggestions_list.setStyleSheet("background-color: white; padding: 8px;")
        self.suggestions_list.hide()  # Cacher la liste au départ
        self.suggestions_list.itemClicked.connect(self.on_select)
        container_layout.addWidget(self.suggestions_list)

        # Ajouter le conteneur au layout principal
        main_layout.addWidget(container)

        # Appliquer le masque arrondi à la fenêtre
        self.rounded_window()

    def search(self):
        query = self.search_entry.text().upper()  # Obtenir la requête utilisateur en majuscule
        self.result_box.clear()
        self.ip_label.setText("IP: XXX")

        found = False
        for key, values in self.data_dict.items():
            if any(query == value.upper() for value in values):
                self.result_box.setText('\n'.join(values))
                self.ip_label.setText(f"IP: {key}")
                found = True
                break
        
        if not found:
            self.result_box.setText("No results found")

        self.suggestions_list.hide()  # Cacher les suggestions après la recherche

    def update_suggestions(self):
        query = self.search_entry.text().upper()

        if not query:
            self.suggestions_list.hide()  # Cacher la liste si l'entrée est vide
            return

        self.suggestions_list.clear()  # Vider la liste avant mise à jour
        matches = set()

        for values in self.data_dict.values():
            for value in values:
                if value.upper().startswith(query):
                    matches.add(value)

        if matches:
            self.suggestions_list.show()  # Afficher la liste si des correspondances sont trouvées
            for match in matches:
                self.suggestions_list.addItem(match)
        else:
            self.suggestions_list.hide()

    def on_select(self, item):
        selected = item.text()
        self.search_entry.setText(selected)
        self.suggestions_list.hide()

    def rounded_window(self):
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), 20, 20)
        region = QtGui.QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.old_pos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPos()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    app.setStyleSheet("""
        QWidget {
            font-family: Arial;
            font-size: 15px;
        }
    """)

    window = SearchApp()
    window.show()

    sys.exit(app.exec_())
