import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QPushButton, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon


class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lynx Browser")
        self.setWindowIcon(QIcon("logo.ico"))

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Mise à jour de la couleur de fond de la fenêtre principale
        self.setStyleSheet("background-color: #1a1a1a;")  # Fond sombre pour toute la fenêtre

        # Layout principal
        layout = QVBoxLayout()

        # Création de l'onglet
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.update_address)

        # Appliquer un style CSS pour les onglets et les couleurs
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                background-color: #2d2d2d; /* Fond sombre */
                border: none;
            }
            QTabBar::tab {
                background: #2d2d2d; /* Couleur des onglets inactifs */
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                color: #cccccc;
                padding: 8px 16px;
                margin: 2px; /* Espacement entre les onglets */
            }
            QTabBar::tab:selected {
                background: #5e2ca5; /* Violet néon pour onglet actif */
                color: #ffffff; /* Texte blanc pour contraste */
                font-weight: bold;
            }
            QTabBar::close-button {
                subcontrol-position: right;
                margin: 2px;
            }
        """)
        layout.addWidget(self.tab_widget)

        # Barre d'adresse
        self.address_bar = QLineEdit(self)
        self.address_bar.returnPressed.connect(self.load_url)
        self.address_bar.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #5e2ca5;
                padding: 5px;
                border-radius: 5px;
            }
        """)

        # Boutons de navigation
        self.home_button = QPushButton("🏠", self)
        self.home_button.setStyleSheet("""
            QPushButton {
                color: #ffffff;  /* Texte blanc */
            }
        """)
        self.home_button.clicked.connect(self.go_home)

        self.back_button = QPushButton("←", self)
        self.back_button.setStyleSheet("""
            QPushButton {
                color: #ffffff;  /* Texte blanc */
            }
        """)
        self.back_button.clicked.connect(self.go_back)

        self.forward_button = QPushButton("→", self)
        self.forward_button.setStyleSheet("""
            QPushButton {
                color: #ffffff;  /* Texte blanc */
            }
        """)
        self.forward_button.clicked.connect(self.go_forward)

        self.reload_button = QPushButton("🔄", self)
        self.reload_button.setStyleSheet("""
            QPushButton {
                color: #ffffff;  /* Texte blanc */
            }
        """)
        self.reload_button.clicked.connect(self.reload_page)

        # Mise en page de la barre d'adresse et des boutons
        address_layout = QHBoxLayout()
        address_layout.addWidget(self.home_button)
        address_layout.addWidget(self.back_button)
        address_layout.addWidget(self.forward_button)
        address_layout.addWidget(self.reload_button)
        address_layout.addWidget(self.address_bar)

        # Ajouter la barre d'adresse et les boutons au layout principal
        layout.addLayout(address_layout)

        # Layout pour ajouter le bouton "+"
        top_layout = QHBoxLayout()
        top_layout.addStretch()  # Ajout d'un espace flexible pour pousser le bouton "+" à droite
        self.add_tab_button = QPushButton("+")
        self.add_tab_button.setFixedSize(30, 30)
        self.add_tab_button.setStyleSheet("""
            QPushButton {
                background-color: #5e2ca5;
                color: #ffffff;
                border-radius: 15px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #7a4bb0;
            }
        """)
        self.add_tab_button.clicked.connect(self.add_new_tab)
        top_layout.addWidget(self.add_tab_button)

        # Ajouter le layout du bouton "+" en haut à droite
        layout.addLayout(top_layout)

        # Ajouter les éléments à l'interface
        self.central_widget.setLayout(layout)

        # Ajouter un premier onglet avec une page de démarrage
        self.add_tab("https://lynx-blue.vercel.app/")  # Page par défaut

    def add_tab(self, url):
        """Ajoute un onglet avec une nouvelle instance de QWebEngineView."""
        tab = QWebEngineView()
        tab.setUrl(QUrl(url))

        # Optimisation GPU activée
        tab.page().settings().setAttribute(tab.page().settings().WebGLEnabled, True)
        tab.page().settings().setAttribute(tab.page().settings().Accelerated2dCanvasEnabled, True)

        tab.titleChanged.connect(lambda title: self.update_tab_title(tab))
        tab.iconChanged.connect(lambda icon: self.update_tab_icon(tab))
        tab.urlChanged.connect(lambda: self.update_address_bar(tab))
        index = self.tab_widget.addTab(tab, "Nouvel onglet")
        self.tab_widget.setCurrentIndex(index)

    def add_new_tab(self):
        """Créer un nouvel onglet vide."""
        self.add_tab("https://lynx-blue.vercel.app/")

    def update_tab_title(self, tab):
        """Met à jour le titre de l'onglet basé sur la page actuelle."""
        index = self.tab_widget.indexOf(tab)
        if index != -1:
            self.tab_widget.setTabText(index, tab.title())

    def update_tab_icon(self, tab):
        """Met à jour l'icône de l'onglet basé sur la page actuelle."""
        index = self.tab_widget.indexOf(tab)
        if index != -1:
            self.tab_widget.setTabIcon(index, tab.icon())

    def update_address(self, index):
        """Met à jour la barre d'adresse lorsqu'on change d'onglet."""
        current_tab = self.tab_widget.widget(index)
        if current_tab:
            self.address_bar.setText(current_tab.url().toString())

    def update_address_bar(self, tab):
        """Met à jour la barre d'adresse lorsque l'URL change dans un onglet."""
        self.address_bar.setText(tab.url().toString())

    def load_url(self):
        """Charge l'URL dans l'onglet actif."""
        url = self.address_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.setUrl(QUrl(url))

    def go_home(self):
        """Ramène l'utilisateur à la page d'accueil."""
        self.address_bar.setText("https://lynx-blue.vercel.app/")
        self.load_url()

    def go_back(self):
        """Revenir à la page précédente."""
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.back()

    def go_forward(self):
        """Aller à la page suivante."""
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.forward()

    def reload_page(self):
        """Recharger la page actuelle."""
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.reload()

    def close_tab(self, index):
        """Ferme l'onglet à l'index spécifié."""
        self.tab_widget.removeTab(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Activer l'accélération matérielle
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-gpu-rasterization --enable-zero-copy"

    browser = SimpleBrowser()
    browser.show()
    sys.exit(app.exec_())
