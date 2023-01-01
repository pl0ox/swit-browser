


import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import urllib
from PyQt5.QtGui import QIcon
import urllib.parse

class BookmarksDialog(QDialog):
    def __init__(self, bookmarks, parent=None):
        super(BookmarksDialog, self).__init__(parent)
        self.bookmarks = bookmarks

        # Create the list widget and populate it with the bookmarks
        self.bookmarks_list = QListWidget()
        for bookmark in self.bookmarks:
            url, title = bookmark
            item = QListWidgetItem(title)
            item.setData(Qt.UserRole, url)
            self.bookmarks_list.addItem(item)

        # Create the layout and add the list widget
        layout = QVBoxLayout()
        layout.addWidget(self.bookmarks_list)
        self.setLayout(layout)

        # Connect the item clicked signal to the open bookmark slot
        self.bookmarks_list.itemClicked.connect(self.openBookmark)

    def openBookmark(self, item):
        # Get the URL of the selected bookmark
        url = item.data(Qt.UserRole)

        # Open the URL in the web browser
        self.parent().browser.setUrl(QUrl(url))

        # Close the dialog
        self.accept()
    



class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)

        
        # Create the layout
        layout = QVBoxLayout()

        # Homepage setting
        homepage_label = QLabel("Homepage:")
        self.homepage_edit = QLineEdit()
        self.homepage_edit.setText(parent.browser.url().toString())
        homepage_layout = QHBoxLayout()
        homepage_layout.addWidget(homepage_label)
        homepage_layout.addWidget(self.homepage_edit)
        layout.addLayout(homepage_layout)

        # Default search engine setting
        search_engine_label = QLabel("Default search engine:")
        self.search_engine_combo = QComboBox()
        self.search_engine_combo.addItems(["Google", "Bing", "DuckDuckGo"])
        self.search_engine_combo.currentIndexChanged.connect(self.updateDefaultSearchEngine)
        search_engine_layout = QHBoxLayout()
        search_engine_layout.addWidget(search_engine_label)
        search_engine_layout.addWidget(self.search_engine_combo)
        layout.addLayout(search_engine_layout)

        # Theme setting


        # Save and cancel buttons
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.saveSettings)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)





    def updateDefaultSearchEngine(self):
        # Get the current index of the combo box
        index = self.search_engine_combo.currentIndex()

        # Get the text of the selected item
        search_engine = self.search_engine_combo.itemText(index)

        # Update the default search engine in the main window
        self.parent().default_search_engine = search_engine



    def saveSettings(self):
        # Get the values of the settings
        homepage = self.homepage_edit.text()
        index = self.search_engine_combo.currentIndex()
        search_engine = self.search_engine_combo.itemText(index)

        # Save the values to the main window
        self.parent().browser.setUrl(QUrl(homepage))
        self.parent().default_search_engine = search_engine
        

        # Close the dialog
        self.accept()



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://google.com'))
        self.setCentralWidget(self.browser)
        self.default_search_engine = "Google"
        self.showMaximized()
        self.bookmarks = []

        #navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        self.back_button = QPushButton(QIcon('back.png'), '')
        self.back_button.clicked.connect(self.browser.back)
        self.forward_button = QPushButton(QIcon('forward.png'), '')
        self.forward_button.clicked.connect(self.browser.forward)
        self.refresh_button = QPushButton(QIcon('refresh.png'), '')
        self.refresh_button.clicked.connect(self.browser.reload)
        self.bookmarks_button = QPushButton(QIcon('bookmarks.png'), '')
        self.bookmarks_button.clicked.connect(self.showBookmarks)
        self.add_bookmark_button = QPushButton(QIcon('add_bookmark.png'), '')
        self.add_bookmark_button.clicked.connect(self.addBookmark)
        self.settings = QPushButton(QIcon('settings.png'), '')
        self.settings.clicked.connect(self.showSettings)
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.back_button)
        navbar.addWidget(self.forward_button)
        navbar.addWidget(self.refresh_button)
        navbar.addWidget(self.url_bar)
        navbar.addWidget(self.bookmarks_button)
        navbar.addWidget(self.add_bookmark_button)
        navbar.addWidget(self.settings)


        self.browser.urlChanged.connect(self.update_url)


        

    def addBookmark(self):
        # Get the current page URL and title
        url = self.browser.url().toString()
        title = self.browser.title()

        # Add the bookmark to the list
        self.bookmarks.append((url, title))

    def showBookmarks(self):
        # Create the bookmarks dialog
        dialog = BookmarksDialog(self.bookmarks, self)

        # Show the dialog
        dialog.exec_()

    def showSettings(self):
        # Create the settings dialog
        dialog = SettingsDialog(self)

        # Show the dialog
        dialog.exec_()


    def navigate_home(self):
        self.browser.setUrl(QUrl('https://www.google.com'))

    def is_web_address(self, url):
        try:
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def navigate_to_url(self):
        url = self.url_bar.text()

        if self.is_web_address(url):
            if not url.startswith("http"):
                url = "http://" + url
            self.browser.setUrl(QUrl(url))
        else:
            self.search(url, self.default_search_engine)

    def search(self, query, engine):
        if engine == "Google":
            url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)
        elif engine == "Bing":
            url = "https://www.bing.com/search?q=" + urllib.parse.quote_plus(query)
        elif engine == "DuckDuckGo":
            url = "https://duckduckgo.com/?q=" + urllib.parse.quote_plus(query)

        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())


    def showBookmarksBar(self, show):
        if show:
            self.bookmarks_toolbar.show()
        else:
            self.bookmarks_toolbar.hide()
            

app = QApplication(sys.argv)
QApplication.setApplicationName('Swit Browser')
window = MainWindow()
app.exec_()

