import css
from sys import exit
from popup import Popup
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, \
                              QLineEdit
from PySide6.QtGui import QIcon
from qasync import asyncSlot
from asyncio import Event
from json import load, dump, JSONDecodeError


class Discord_window(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.discord_channel = ''
        self.token = ""
        self.confirm_discord = Event()

        self.setFocusPolicy(Qt.StrongFocus)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.resize(240, 240)
        self.setFocus()
        self.UI()

    def start(self):
        self.line_tkn.setText('')
        self.loading_label()
        self.show()
        self.main.center_window(self)

    def UI(self):

        self.setWindowTitle("Discord")
        self.setWindowIcon(QIcon('Files/Icons/App/discord.svg'))

        # Widgets

        self.lbl0 = QLabel("\n<font color=\"#d9d9d9\">Loading...</font>")
        self.lbl0.setAlignment(Qt.AlignCenter)

        self.lbl1 = QLabel("1- Join Discord Server: " +
                           "<a href=\'https://discord.com/invite/r8qnHkQ'>" +
                           "<font size=4 color=#7289da>Link</a>")

        self.lbl1.setOpenExternalLinks(True)
        self.lbl1.setAlignment(Qt.AlignCenter)

        self.lbl2 = QLabel("2- Send !start to NovaNotifier Bot")

        self.lbl2.setOpenExternalLinks(True)
        self.lbl2.setAlignment(Qt.AlignCenter)

        self.lbl3 = QLabel("3- Insert Token:")
        self.lbl3.setAlignment(Qt.AlignCenter)

        self.line_tkn = QLineEdit()
        self.line_tkn.setPlaceholderText("Token")
        self.line_tkn.setAlignment(Qt.AlignCenter)
        self.btn_submit = QPushButton("Submit")
        self.btn_discord = QPushButton("Reset Discord")

        # CSS Style
        self.setStyleSheet(css.popup())
        self.lbl0.setStyleSheet(css.lbl())
        self.lbl1.setStyleSheet(css.lbl())
        self.lbl2.setStyleSheet(css.lbl())
        self.lbl3.setStyleSheet(css.lbl())
        self.line_tkn.setStyleSheet(css.line_edit())
        self.btn_submit.setStyleSheet(css.btn())
        self.btn_discord.setStyleSheet(css.btn())

        # Layouts
        self.lyt_main = QVBoxLayout()
        self.lyt_main.addWidget(self.lbl0)
        self.lyt_main.addWidget(self.lbl1)
        self.lyt_main.addWidget(self.lbl2)
        self.lyt_main.addWidget(self.lbl3)
        self.lyt_main.addWidget(self.line_tkn)
        self.lyt_main.addWidget(self.btn_submit)
        self.lyt_main.addWidget(self.btn_discord)

        self.setLayout(self.lyt_main)

        # Connections
        self.btn_submit.clicked.connect(self.submit_token)
        self.btn_discord.clicked.connect(self.discord_reset)

    def read_token(self):
        try:
            with open('Files/Discord.json', 'r') as f:
                self.token = load(f)
        except JSONDecodeError:
            self.token = {}

    def save_token(self):
        with open('Files/Discord.json', 'w') as f:
            dump(self.token, f)

    def loading_label(self):
        if self.discord_channel:
            self.lbl0.setText(f"\n<font color=\"#2ED03C\">Online: {self.discord_name}</font>")
        else:
            self.lbl0.setText("\n<font color=\"#E32037\">Offline</font>")

    @asyncSlot()
    async def submit_token(self):
        if data := await self.main.db.token_check(self.line_tkn.text()):
            self.token = data['token']
            self.discord_channel = data['channel']
            self.discord_name = data['discord']
            self.save_token()
            self.confirm_discord.set()
            self.close()

    def discord_reset(self):
        self.popup = Popup('Reset Discord ?\n\n(This will close Notifier)')
        self.popup.question()
        self.popup.btn_yes.clicked.connect(self.discord_reset_confirm)
        self.popup.btn_yes.clicked.connect(self.popup.close)
        self.popup.btn_no.clicked.connect(self.popup.close)

    def discord_reset_confirm(self):
        self.discord_channel = None
        self.token = {}
        with open('Files/Accounts.json', 'w'): pass
        with open('Files/Discord.json', 'w'): pass
        self.main.btn_stop.click()
        exit()

    async def discord_check(self):
        try:
            self.read_token()
            if data := await self.main.db.token_check(self.token):
                self.token = data['token']
                self.discord_channel = data['channel']
                self.discord_name = data['discord']
            else:
                self.start()
                await self.confirm_discord.wait()
        except Exception:
            self.main.exception()

    def closeEvent(self, event):
        if not self.discord_channel:
            exit()
        self.close()