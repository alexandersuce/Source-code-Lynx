import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QPushButton, QTabWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QIcon

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lynx Browser")
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowIcon(QIcon("logo.ico"))

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        layout = QVBoxLayout(self.central_widget)

        # Barre d'adresse et boutons de navigation
        self.address_bar = QLineEdit(self)
        self.address_bar.returnPressed.connect(self.load_url)

        self.home_button = QPushButton("🏠")
        self.home_button.clicked.connect(self.go_home)

        self.back_button = QPushButton("←")
        self.back_button.clicked.connect(self.go_back)

        self.forward_button = QPushButton("→")
        self.forward_button.clicked.connect(self.go_forward)

        self.reload_button = QPushButton("🔄")
        self.reload_button.clicked.connect(self.reload_page)

        # Barre de navigation horizontale
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.home_button)
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.reload_button)
        nav_layout.addWidget(self.address_bar)

        # Ajouter le bouton "+" à droite dans la barre de navigation
        self.add_tab_button = QPushButton("+")
        self.add_tab_button.clicked.connect(self.add_tab)
        nav_layout.addWidget(self.add_tab_button, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(nav_layout)

        # Onglets
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.update_address)
        layout.addWidget(self.tab_widget)

        # Ajouter un onglet de démarrage
        self.add_tab("https://lynx-blue.vercel.app/")

    def add_tab(self, url="https://lynx-blue.vercel.app/"):
        """Ajoute un nouvel onglet avec une page Web."""
        if not isinstance(url, str) or not url:
            url = "https://lynx-blue.vercel.app/"
        
        tab = QWebEngineView()
        tab.setUrl(QUrl(url))  # Utilisation de QUrl pour charger l'URL
        self.tab_widget.addTab(tab, "Nouvel onglet")
        self.tab_widget.setCurrentWidget(tab)

        # Activer le GPU rasterization pour améliorer la performance
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-gpu-rasterization --enable-zero-copy"

        # Connecte les signaux de mise à jour du titre et de l'URL
        tab.titleChanged.connect(lambda title: self.update_tab_title(tab, title))
        tab.urlChanged.connect(lambda: self.update_address(self.tab_widget.currentIndex()))

    def update_tab_title(self, tab, title):
        """Met à jour le titre de l'onglet."""
        index = self.tab_widget.indexOf(tab)
        if index != -1:
            self.tab_widget.setTabText(index, title)

    def update_address(self, index):
        """Met à jour la barre d'adresse lorsqu'on change d'onglet."""
        current_tab = self.tab_widget.widget(index)
        if current_tab:
            self.address_bar.setText(current_tab.url().toString())

    def load_url(self):
        """Charge l'URL saisie dans la barre d'adresse."""
        url = self.address_bar.text()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.setUrl(QUrl(url))

    def go_home(self):
        """Navigue vers la page d'accueil."""
        self.address_bar.setText("https://lynx-blue.vercel.app/")
        self.load_url()

    def go_back(self):
        """Navigue vers la page précédente."""
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.back()

    def go_forward(self):
        """Navigue vers la page suivante."""
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.forward()

    def reload_page(self):
        """Recharge la page actuelle."""
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            current_tab.reload()

    def close_tab(self, index):
        """Ferme un onglet par son index."""
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)
        else:
            self.close()

if __name__ == "__main__":
    # Activer l'accélération matérielle pour améliorer la performance
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-gpu-rasterization --enable-zero-copy"

    app = QApplication(sys.argv)
    browser = SimpleBrowser()
    browser.show()
    sys.exit(app.exec()) 
