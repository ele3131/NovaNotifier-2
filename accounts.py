import css
from PySide6.QtWidgets import QWidget, QTableWidget, \
                            QPushButton, QTableWidgetItem, QVBoxLayout, \
                            QAbstractScrollArea, QHeaderView, \
                            QAbstractItemView, QLabel, QRadioButton, \
                            QFormLayout, QHBoxLayout, QGraphicsColorizeEffect
from PySide6.QtGui import QIcon, QColor
from PySide6.QtCore import Qt, QTimer, QSize
from popup import Popup
from json import load, dumps

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Driver Manager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from bs4 import BeautifulSoup
from cryptography.fernet import Fernet
from asyncio import gather
from ast import literal_eval


class Accounts(QWidget):
    def __init__(self, main):
        try:
            super().__init__()
            self.main = main
            self.url = "https://www.novaragnarok.com/?module=account&action=view"
            self.my_browser = None
            self.accounts = {}
            self.settings = {}
            self.network = self.main.network

            self.setStyleSheet(css.popup())
            self.setWindowTitle("Add Account")
            self.setWindowIcon(QIcon('Files/Icons/App/people.svg'))
            self.setFocusPolicy(Qt.StrongFocus)
            self.resize(self.frameGeometry().width()*1/2, self.frameGeometry().height()*1/2)
            self.UI()

        except Exception as e:
            raise NameError(e)

    def UI(self):
        """
            Widgets
        """

        headers = ["Username"]

        self.timer = QTimer()
        self.tbl = QTableWidget(0, len(headers))
        self.tbl.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self.tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl.setHorizontalHeaderLabels(headers)
        self.tbl.verticalHeader().hide()
        self.tbl.setFocusPolicy(Qt.NoFocus)
        self.tbl.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tbl.viewport().installEventFilter(self)

        self.lbl_browser_cookie = QLabel("Browser: ")

        # Browsers Buttons
        self.rbtn_chromium = QRadioButton("Chromium", self)
        self.rbtn_chrome = QRadioButton("Chrome", self)
        self.rbtn_brave = QRadioButton("Brave", self)
        self.rbtn_firefox = QRadioButton("Firefox", self)
        self.rbtn_edge = QRadioButton("Edge", self)
        self.rbtn_chrome.setChecked(1)

        # Buttons
        btn_names = ["btn_delete", "btn_add"]

        self.buttons = []

        for button in btn_names:
            button_self = f"self.{button}"
            effect = f"self.{button}_effect"
            setattr(self, button, QPushButton(objectName=button_self))
            setattr(self, button + '_effect', QGraphicsColorizeEffect(self))
            eval(effect).setColor(Qt.white)
            eval(button_self).setGraphicsEffect(eval(effect))
            eval(button_self).setIconSize(QSize(48, 48))
            eval(button_self).installEventFilter(self)
            self.buttons.append(eval(button_self))

        self.btn_submit = QPushButton("Add Account")

        """
            Layouts
        """
        self.browsers = [self.rbtn_chromium, self.rbtn_chrome, self.rbtn_brave, self.rbtn_firefox, self.rbtn_edge]
        width = self.frameGeometry().width()/6

        self.lyt_mid = QFormLayout()
        self.lyt_rbtn = QHBoxLayout()
        self.lyt_rbtn.addWidget(self.rbtn_chromium)
        self.lyt_rbtn.addWidget(self.rbtn_chrome)
        self.lyt_rbtn.addWidget(self.rbtn_brave)
        self.lyt_rbtn.addWidget(self.rbtn_firefox)
        self.lyt_rbtn.addWidget(self.rbtn_edge)
        self.lyt_mid.addRow(self.lbl_browser_cookie, self.lyt_rbtn)

        self.lyt_btn = QHBoxLayout()
        self.lyt_btn.setContentsMargins(width, 0, width, 0)
        self.lyt_btn.addStretch()
        self.lyt_btn.addWidget(self.btn_add)
        self.lyt_btn.addWidget(self.btn_delete)
        self.lyt_btn.addStretch()

        self.lyt_main = QVBoxLayout()
        self.lyt_main.addWidget(self.tbl)
        self.lyt_main.addLayout(self.lyt_mid)
        self.lyt_main.addLayout(self.lyt_btn)

        self.setLayout(self.lyt_main)

        """
            Styling
        """

        self.tbl.setStyleSheet(css.tbl())
        self.tbl.horizontalHeader().setStyleSheet(css.header())
        self.tbl.verticalHeader().setStyleSheet(css.header())
        self.tbl.verticalScrollBar().setStyleSheet(css.scrollbar())
        self.tbl.horizontalScrollBar().setStyleSheet(css.scrollbar())

        self.lbl_browser_cookie.setStyleSheet(css.lbl())

        self.rbtn_chromium.setStyleSheet(css.rbtn())
        self.rbtn_chrome.setStyleSheet(css.rbtn())
        self.rbtn_brave.setStyleSheet(css.rbtn())
        self.rbtn_firefox.setStyleSheet(css.rbtn())
        self.rbtn_edge.setStyleSheet(css.rbtn())

        self.btn_delete.setStyleSheet(css.btn_main("url(Files/Icons/App/delete.svg)"))
        self.btn_add.setStyleSheet(css.btn_main("url(Files/Icons/App/plus.svg)"))

        """
            Connects
        """

        for browser in self.browsers:
            browser.toggled.connect(self.browser_select)

        self.btn_add.clicked.connect(self.add_cookie)
        self.btn_delete.clicked.connect(self.delete_confirmation)

    async def start(self):
        try:
            eval(f"self.rbtn_{self.my_browser}.setChecked(True)")
            self.show_table()
            self.show()
            self.main.center_window(self)
        except Exception:
            self.main.exception()

    def add_cookie(self):
        driver_cookies = None

        try:
            if self.my_browser == 'firefox':
                from webdriver_manager.firefox import GeckoDriverManager
                driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
                driver.get(self.url)
            elif self.my_browser == 'chromium':
                from selenium.webdriver.chrome.service import Service as ChromiumService
                driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
                driver.get(self.url)
            elif self.my_browser == 'chrome':
                from selenium.webdriver.chrome.service import Service as ChromeService
                options = webdriver.ChromeOptions()
                options.add_experimental_option("excludeSwitches", ["enable-logging"])
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
                driver.get(self.url)
            elif self.my_browser == 'brave':
                driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())
                driver.get(self.url)
            else:
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                driver = webdriver.Edge(EdgeChromiumDriverManager().install())
                driver.get(self.url)
        except Exception:
            self.main.exception()

        try:
            WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, "nova-table")))
            driver_cookies = driver.get_cookies()
            item = driver.page_source
            driver.quit()
        except Exception:
            return

        for each in driver_cookies:
            if each['name'] == "fluxSessionData":
                cookie = {"fluxSessionData": each["value"]}
                break

        soup = BeautifulSoup(item, "html.parser")
        text = soup.find("li", class_="login-form-right").find("strong")
        if text:
            username = text.get_text()
            self.accounts[username] = {'username': username, 'cookie': cookie}

        if not self.accounts:
            raise NameError('Cookies Not Found')

        self.show_table()
        self.save()
        self.close()

    def reset_question(self):
        self.popup = Popup('Delete Program Accounts?')
        self.popup.question()
        self.popup.btn_yes.clicked.connect(self.reset_cookie)
        self.popup.btn_yes.clicked.connect(self.popup.close)
        self.popup.btn_no.clicked.connect(self.popup.close)

    async def check_cookies(self):
        cookies = list(self.accounts.values())
        htmls = (await gather(*[self.network.search(self.url, each["cookie"]) for each in cookies]))
        for item in htmls:
            soup = BeautifulSoup(item, "html.parser")
            try:
                username = (soup.find("li", class_="login-form-right").find("strong")).get_text()
                if username:
                    self.accounts[username]["html"] = item
                if not username:
                    del self.accounts[username]
            except Exception:
                pass

    async def account_zeny(self):
        for account in self.accounts.values():
            username = account["username"]
            characters = []
            characters_zeny = []
            soup = BeautifulSoup(account["html"], "html.parser")
            if text := soup.find_all(class_="link-to-character"):
                for character in text:
                    characters.append(character.get_text())
                table = soup.find(id="nova-table-chars")
                for row in table.findAll("tr"):
                    zeny = row.findAll("td")[5].get_text()
                    characters_zeny.append(zeny)
                total_zeny = soup.find_all("strong")[1].get_text()
                self.accounts[username]['characters'] = characters
                self.accounts[username]['characters_zeny'] = characters_zeny
                self.accounts[username]['total_zeny'] = total_zeny
            else:
                self.accounts[username]['characters'] = ['']
                self.accounts[username]['characters_zeny'] = ['']
                self.accounts[username]['total_zeny'] = '0'

    async def read(self):
        with open('Files/Settings.json', 'r') as f:
            self.settings = load(f)

        self.my_browser = self.settings['browser']
        self.cookie_key = await self.main.db.database_cookie_key_get()
        fernet = Fernet(self.cookie_key)

        with open('Files/Accounts.json', 'rb') as g:
            try:
                cookie_crypt = g.read()
                self.accounts = literal_eval(fernet.decrypt(cookie_crypt).decode())
            except Exception:
                self.accounts = {}

    def save(self):
        self.main.btn_stop.click()

        self.settings['browser'] = self.my_browser
        self.main.sett.save_settings()

        fernet = Fernet(self.cookie_key)
        cookie_crypt = fernet.encrypt(dumps(self.accounts).encode('utf-8'))

        with open('Files/Accounts.json', 'wb+') as f:
            f.write(cookie_crypt)

    def browser_select(self):
        self.my_browser = self.sender().text().lower()

    def eventFilter(self, source, event):
        num = event.type()
        if source.__class__.__name__ == "QPushButton":
            if num == 127:
                name = source.objectName()
                effect = name + '_effect'
                eval(effect).setColor(QColor(255, 213, 0))
                if name == 'self.btn_delete':
                    eval(effect).setColor(Qt.red)
                if name == 'self.btn_add':
                    eval(effect).setColor(Qt.green)
            elif num == 128:
                name = source.objectName()
                effect = name + '_effect'
                eval(effect).setColor(Qt.white)

        return super(Accounts, self).eventFilter(source, event)

    def show_table(self):
        self.tbl.setRowCount(0)
        for row, username in enumerate(self.accounts.keys()):
            self.tbl.setRowCount(row + 1)
            col = 0
            cell = QTableWidgetItem(username)
            cell.setTextAlignment(Qt.AlignCenter)
            self.tbl.setItem(row, col, cell)
        self.tbl.resizeRowsToContents()

    def delete_confirmation(self):
        self.popup = Popup('Remove from the List?')
        self.popup.question()
        self.popup.btn_yes.clicked.connect(self.delete_account)
        self.popup.btn_yes.clicked.connect(self.popup.close)
        self.popup.btn_no.clicked.connect(self.popup.close)

    def delete_account(self):
        current_cell = self.tbl.currentRow()
        del_item = list(self.accounts.keys())[current_cell]
        del self.accounts[del_item]
        self.tbl.removeRow(current_cell)
        self.save()

    def closeEvent(self, event):
        self.close()
