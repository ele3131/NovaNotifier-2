import css
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, \
                            QLineEdit, QHBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt


class Popup(QWidget):
    def __init__(self, message=None):
        super().__init__()
        self.resize(300, 80)
        self.message = message
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def info(self):
        self.setWindowTitle("Information")
        self.setStyleSheet(css.popup())
        self.lbl_text = QLabel(self.message)
        self.lbl_text.setStyleSheet(css.lbl())
        self.lbl_text.setAlignment(Qt.AlignCenter)

        self.btn_close = QPushButton("Close")
        self.btn_close.setStyleSheet(css.btn())
        self.btn_close.clicked.connect(self.close)

        container_lyt_done = QWidget()
        container_lyt_done.setStyleSheet(css.container())
        self.lyt_submain = QVBoxLayout(container_lyt_done)
        self.lyt_submain.addWidget(self.lbl_text)
        self.lyt_submain.addWidget(self.btn_close)

        self.lyt_main = QVBoxLayout()
        self.lyt_main.addWidget(container_lyt_done)
        self.setLayout(self.lyt_main)
        self.show()

    def question(self):

        self.setWindowTitle("Question")
        self.setStyleSheet(css.popup())
        self.lbl_text = QLabel(self.message)
        self.lbl_text.setStyleSheet(css.lbl())
        self.lbl_text.setAlignment(Qt.AlignCenter)
        self.btn_yes = QPushButton("Yes")
        self.btn_yes.setStyleSheet(css.btn())
        self.btn_no = QPushButton("No")
        self.btn_no.setStyleSheet(css.btn())
        container_lyt_done = QWidget()
        container_lyt_done.setStyleSheet(css.container())
        self.lyt_button = QHBoxLayout()
        self.lyt_button.addWidget(self.btn_yes)
        self.lyt_button.addWidget(self.btn_no)
        self.lyt_submain = QVBoxLayout(container_lyt_done)
        self.lyt_submain.addWidget(self.lbl_text)
        self.lyt_submain.addLayout(self.lyt_button)

        self.lyt_main = QVBoxLayout()
        self.lyt_main.addWidget(container_lyt_done)
        self.setLayout(self.lyt_main)

        self.show()

    def help(self, main):

        self.setWindowTitle("Help")
        self.setStyleSheet(css.popup())

        msg = (
            """
            Welcome to NovaRO Notifier!

            This program was made with the purpose of making Market Managment easier.

            Features:

                - Search Items and receive Windows/Discord Notifications.
                - Check your Account/Character Zeny.
                - Check your Active Shop/Sold List.
                - Better Prices Estimations.
                - Multiple Accounts Support.

            About Cookies:

                - NovaRO Website uses reCaptcha to access Market.
                - Cookies are only used for retrieving information.

            Support:

                Discord: Michel#3659
                Forum: https://novaragnarok.com/forum/topic/11837-novaro-tag-system-program
                Source: Coming Soon [Stable]
            """
        )

        self.lbl_text = QLabel(msg)
        self.lbl_text.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lbl_text.setStyleSheet(css.lbl())
        self.lbl_text.setAlignment(Qt.AlignLeft)
        container_lyt_done = QWidget()
        container_lyt_done.setStyleSheet(css.container())
        self.lyt_submain = QVBoxLayout(container_lyt_done)
        self.lyt_submain.addWidget(self.lbl_text)

        self.lyt_main = QVBoxLayout()
        self.lyt_main.addWidget(container_lyt_done)
        self.setLayout(self.lyt_main)

        self.show()
        main.center_window(self)

    def discord(self):
        self.resize(500, 80)
        self.setWindowTitle("Discord")
        self.setStyleSheet(css.popup())
        self.setWindowTitle("Discord Integration")
        self.setWindowIcon(QIcon('Files/Icons/App/discord.svg'))
        self.lbl_integration = QLabel("DM !start to NovaNotifier Bot")
        self.lbl_enter = QLabel("Token: ")
        self.line_tkn = QLineEdit()
        self.line_tkn.setPlaceholderText("Enter Token ID | e.g. e4d2")
        self.btn_submit = QPushButton("Submit")

        # Layouts
        self.lyt_submission = QHBoxLayout()
        self.lyt_submission.addWidget(self.lbl_enter)
        self.lyt_submission.addWidget(self.line_tkn)
        self.lyt_main = QVBoxLayout()
        self.lyt_main.addWidget(self.lbl_integration)
        self.lyt_main.addLayout(self.lyt_submission)
        self.lyt_main.addWidget(self.btn_submit)

        # CSS Style
        self.lbl_integration.setStyleSheet(css.lbl())
        self.lbl_enter.setStyleSheet(css.lbl())
        self.line_tkn.setStyleSheet(css.line_edit())
        self.btn_submit.setStyleSheet(css.btn())

        self.setLayout(self.lyt_main)
        self.show()

        # Connections
        self.btn_submit.clicked.connect(self.submit_token)

    def warning(self):
        self.setStyleSheet(css.popup())
        self.setWindowTitle("Warning")
        # self.setWindowIcon(QMessageBox.warning)

        self.lbl = QLabel(self.message)
        self.lbl.setStyleSheet(css.lbl())
        self.lbl.setAlignment(Qt.AlignCenter)

        self.btn_close = QPushButton("Close")
        self.btn_close.setStyleSheet(css.btn())
        self.btn_close.clicked.connect(self.close)

        container_lyt_done = QWidget()
        container_lyt_done.setStyleSheet(css.container())

        self.lyt_submain = QVBoxLayout(container_lyt_done)
        self.lyt_submain.setContentsMargins(10, 10, 10, 10)
        self.lyt_submain.addWidget(self.lbl)
        self.lyt_submain.addWidget(self.btn_close)

        self.lyt_main = QVBoxLayout()
        self.lyt_main.addWidget(container_lyt_done)

        self.btn_close.clicked.connect(self.close)
        self.setLayout(self.lyt_main)
        self.show()

    def critical(self):
        self.resize(450, 80)
        self.setStyleSheet(css.popup())
        self.setWindowTitle("Critical")
        # self.setWindowIcon(QMessageBox.critical)

        self.lbl = QLabel(self.message)
        self.btn_close = QPushButton("Close")

        self.lyt_main = QVBoxLayout()
        self.lyt_main.addWidget(self.lbl)
        self.lyt_main.addWidget(self.btn_close)

        self.lbl.setStyleSheet(css.lbl())
        self.btn_close.setStyleSheet(css.btn())

        self.btn_close.clicked.connect(self.close)
        self.setLayout(self.lyt_main)
        self.show()
