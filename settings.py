import css
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, \
                            QLineEdit, QHBoxLayout, \
                            QFormLayout, QCheckBox
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtCore import Qt
from json import load, dump


class Settings(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.settings = {}
        self.resize(450, 200)
        self.setStyleSheet(css.popup())
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon('Files/Icons/App/settings.svg'))
        self.read_settings()
        self.UI()

    def UI(self):
        # Widgets
        self.btn_save = QPushButton("Save")
        self.line_short_median = QLineEdit()
        self.line_short_median.setPlaceholderText(f"Current: {self.settings['SM']} days")
        self.line_long_median = QLineEdit()
        self.line_long_median.setPlaceholderText(f"Current: {self.settings['LM']} days")
        self.line_sell_filter = QLineEdit()
        self.line_sell_filter.setPlaceholderText(f"Current: {format(self.settings['sell_filter'], ',d')}z")
        self.line_time_interval = QLineEdit()
        self.line_time_interval.setPlaceholderText(f"Current: {self.settings['timer_refresh']} seconds")
        self.lbl_short_median = QLabel("Short Median: ")
        self.lbl_long_median = QLabel("Long Median: ")
        self.lbl_sell_filter = QLabel("Sell Filter: ")
        self.lbl_time_interval = QLabel("Refresh Time: ")
        self.lbl_notifications = QLabel("Notifications: ")
        self.lbl_tray = QLabel("Tray Minimize: ")

        # Tray CheckBox
        self.tray_icon = QCheckBox("Tray Icon")

        if self.settings['tray_icon']:
            self.tray_icon.setChecked(True)

        # Notification CheckBoxes
        self.system_notification = QCheckBox("System")
        self.discord_notification = QCheckBox("Discord")
        self.sell_notification = QCheckBox("Sell")
        self.price_notification = QCheckBox("Price")

        if self.settings['system_notification']:
            self.system_notification.setChecked(True)
        if self.settings['discord_notification']:
            self.discord_notification.setChecked(True)
        if self.settings['sell_notification']:
            self.sell_notification.setChecked(True)
        if self.settings['price_notification']:
            self.price_notification.setChecked(True)

        # Stylesheet
        self.lbl_notifications.setStyleSheet(css.lbl())
        self.system_notification.setStyleSheet(css.checkbox())
        self.discord_notification.setStyleSheet(css.checkbox())
        self.sell_notification.setStyleSheet(css.checkbox())
        self.price_notification.setStyleSheet(css.checkbox())
        self.btn_save.setStyleSheet(css.btn())
        self.lbl_tray.setStyleSheet(css.lbl())
        self.tray_icon.setStyleSheet(css.checkbox())

        # Connects
        self.btn_save.clicked.connect(self.submit_settings)

        # Groups
        self.lines = [self.line_short_median, self.line_long_median, self.line_time_interval, self.line_sell_filter]
        self.labels = [self.lbl_short_median, self.lbl_long_median, self.lbl_time_interval, self.lbl_sell_filter]
        self.notifications = [self.system_notification, self.discord_notification, self.sell_notification, self.price_notification]

        # Layouts
        self.lyt_inputs = QFormLayout()

        for line, label in zip(self.lines, self.labels):
            line.setValidator(QIntValidator())
            line.setStyleSheet(css.line_edit())
            label.setStyleSheet(css.lbl())
            self.lyt_inputs.addRow(label, line)

        self.lyt_notifications = QHBoxLayout()
        self.lyt_notifications.addWidget(self.system_notification)
        self.lyt_notifications.addWidget(self.discord_notification)
        self.lyt_notifications.addWidget(self.sell_notification)
        self.lyt_notifications.addWidget(self.price_notification)

        self.lyt_minimize = QHBoxLayout()
        self.lyt_minimize.addWidget(self.tray_icon)

        self.lyt_inputs.addRow(self.lbl_notifications, self.lyt_notifications)
        self.lyt_inputs.addRow(self.lbl_tray, self.lyt_minimize)

        self.lyt_buttons = QVBoxLayout()
        self.lyt_buttons.addWidget(self.btn_save)
        width = self.frameGeometry().width()/3
        self.lyt_buttons.setContentsMargins(width, 5, width, 5)

        self.lyt_main = QVBoxLayout()
        self.lyt_main.setSpacing(6)
        self.lyt_main.addLayout(self.lyt_inputs)
        self.lyt_main.addLayout(self.lyt_buttons)

        self.setLayout(self.lyt_main)
        self.setFocusPolicy(Qt.StrongFocus)

    def start(self):
        self.read_settings()
        self.show()
        self.main.center_window(self)

    def notification_select(self):
        for notification in self.notifications:
            text = (notification.text() + "_notification").lower()
            self.settings[text] = eval(f"{notification.isChecked()}")

    def tray_select(self):
        if self.tray_icon.isChecked():
            self.settings['tray_icon'] = True
        else:
            self.settings['tray_icon'] = False

    def read_settings(self):
        with open('Files/Settings.json', 'r') as f:
            self.settings = load(f)

    def submit_settings(self):
        key = ['SM', 'LM', 'timer_refresh', 'sell_filter']
        for no, i in enumerate(self.lines):
            if i.text():
                self.settings[key[no]] = int(i.text())
                if no == 0 or no == 1:
                    i.setPlaceholderText(f"Current: {int(i.text())} days")
                elif no == 2:
                    time = int(i.text())
                    if time < 10:
                        time = 10
                        self.settings[key[no]] = int(i.text())
                    i.setPlaceholderText(f"Current: {time} seconds")
                else:
                    i.setPlaceholderText(f"Current: {int(i.text())}z")
            i.setText("")
        self.notification_select()
        self.tray_select()
        self.save_settings()

    def save_settings(self):
        with open('Files/Settings.json', 'w') as f:
            dump(self.settings, f, indent=4)
        self.close()