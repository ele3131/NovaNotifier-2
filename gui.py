import css
from sys import exit
from PySide6.QtCore import Qt, QSize, QTimer, QEvent
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QTableWidget, \
                            QAbstractScrollArea, QAbstractItemView, QHBoxLayout, \
                            QVBoxLayout, QHeaderView, QGraphicsColorizeEffect, \
                            QSystemTrayIcon, QMenu, QTableWidgetItem
from PySide6.QtGui import QIcon, QColor, QPixmap, QAction


class MainWindow(QWidget):

    def ui(self, main):
        self.setWindowTitle('Nova Notifier')
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.tbl_order = self.tbl_index = self.header_click = 0
        self.font_color = {"gold": QColor("#FFD500"), "green": QColor("#2ED03C"),
                           "red": QColor("#E32037"), "white": QColor(255, 255, 255),
                           "gray": QColor("#999999")}

        # Logo
        self.logo = QLabel()
        self.logo_img = QPixmap('Files/Icons/App/logo.png')
        self.logo_img = self.logo_img.scaled(160, 64, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.logo.setPixmap(self.logo_img)

        # Tray Menu
        self.tray_menu = QMenu()
        self.quit_action = QAction("Exit", self)
        self.tray_menu.addAction(self.quit_action)
        self.tray_menu.setStyleSheet(css.menu())

        # Tray
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('Files/Icons/App/main2.ico'))
        self.tray_icon.setContextMenu(self.tray_menu)

        # Top Buttons
        btn_names = ["btn_stop", "btn_pause", "btn_start",
                     "btn_refresh", "btn_opt", "btn_add",
                     "btn_discord", "btn_help", "btn_sells",
                     "btn_login"]

        self.buttons = []

        for button in btn_names:
            button_self = f"self.{button}"
            effect = f"self.{button}_effect"
            setattr(self, button, QPushButton(objectName=button_self))
            setattr(self, button + '_effect', QGraphicsColorizeEffect(self))
            eval(effect).setColor(Qt.white)
            eval(button_self).setGraphicsEffect(eval(effect))
            eval(button_self).setIconSize(QSize(64, 64))
            eval(button_self).installEventFilter(self)
            self.buttons.append(eval(button_self))

        # Timer
        self.resize_timer = QTimer()

        # Accounts
        self.lbl_refresh = QLabel()
        self.lbl_refresh.setAlignment(Qt.AlignCenter)
        self.lbl_accounts = QLabel('Accounts: ')
        self.lbl_acc = QLabel()
        self.lbl_acc.setAlignment(Qt.AlignCenter)
        self.lbl_acc.setWordWrap(True)

        # Table
        headers = ['Item', 'Name', 'Refine', 'Prop', 'Qty', 'Price',
                   'Short Med', 'Long Med', 'SM%', 'LM%', 'Alert', 'Location']
        self.tbl = QTableWidget(0, len(headers))
        self.tbl.setHorizontalHeaderLabels(headers)
        self.tbl.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tbl.setSelectionMode(QAbstractItemView.NoSelection)
        self.tbl.setFocusPolicy(Qt.NoFocus)

        # Layouts
        self.lyt_top = QHBoxLayout()
        self.lyt_top.addWidget(self.logo)
        self.lyt_top.addStretch()
        self.lyt_top.addWidget(self.btn_stop)
        self.lyt_top.addWidget(self.btn_start)
        self.lyt_top.addWidget(self.btn_pause)
        self.lyt_top.addWidget(self.btn_refresh)
        self.lyt_top.addStretch()
        self.lyt_top.addWidget(self.btn_help)

        self.lyt_bottom = QHBoxLayout()
        self.lyt_bottom.addWidget(self.btn_opt)
        self.lyt_bottom.addStretch()
        self.lyt_bottom.addWidget(self.btn_login)
        self.lyt_bottom.addWidget(self.btn_sells)
        self.lyt_bottom.addWidget(self.btn_add)
        self.lyt_bottom.addStretch()
        self.lyt_bottom.addWidget(self.btn_discord)

        self.lyt_main = QVBoxLayout()
        self.lyt_main.setContentsMargins(0, 0, 0, 0)
        self.lyt_main.addLayout(self.lyt_top)
        self.lyt_main.addWidget(self.lbl_refresh)
        self.lyt_main.addWidget(self.tbl)
        self.lyt_main.addLayout(self.lyt_bottom)

        widget = QWidget()
        widget.setLayout(self.lyt_main)
        self.setCentralWidget(widget)
        self.resize(self.frameGeometry().width()*1.5, self.frameGeometry().height())

        # Styling
        self.btn_start.setStyleSheet(css.btn_main("url(Files/Icons/App/play.svg)"))
        self.btn_stop.setStyleSheet(css.btn_main("url(Files/Icons/App/stop.svg)"))
        self.btn_pause.setStyleSheet(css.btn_main("url(Files/Icons/App/pause.svg)"))
        self.btn_refresh.setStyleSheet(css.btn_main("url(Files/Icons/App/refresh.svg)"))
        self.btn_opt.setStyleSheet(css.btn_main("url(Files/Icons/App/settings.svg)"))
        self.btn_login.setStyleSheet(css.btn_main("url(Files/Icons/App/people.svg)"))
        self.btn_add.setStyleSheet(css.btn_main("url(Files/Icons/App/add-file.svg)"))
        self.btn_discord.setStyleSheet(css.btn_main("url(Files/Icons/App/discord.svg)"))
        self.btn_help.setStyleSheet(css.btn_main("url(Files/Icons/App/info.svg)"))
        self.btn_sells.setStyleSheet(css.btn_main("url(Files/Icons/App/shopping.svg)"))

        # Table
        self.tbl.setStyleSheet(css.tbl())
        self.tbl.horizontalHeader().setStyleSheet(css.header())
        self.tbl.horizontalScrollBar().setStyleSheet(css.scrollbar())
        self.tbl.verticalScrollBar().setStyleSheet(css.scrollbar())

        # Labels
        self.lbl_acc.setStyleSheet(css.lbl_acc())
        self.lbl_refresh.setStyleSheet(css.lbl_refresh())

        # Hides
        self.btn_stop.hide()
        self.btn_pause.hide()
        self.btn_refresh.hide()
        self.lbl_refresh.hide()
        self.tbl.verticalHeader().hide()
        self.tbl.horizontalHeader().hide()
        self.btn_sells.hide()

        # Connects
        self.btn_start.clicked.connect(self.start_program)
        self.btn_stop.clicked.connect(self.stop_notifier)
        self.btn_pause.clicked.connect(self.timer_pause)
        self.btn_opt.clicked.connect(self.open_settings)
        self.btn_discord.clicked.connect(self.discord_open)
        self.btn_refresh.clicked.connect(self.refresh_notifier)
        self.btn_add.clicked.connect(self.add_open)
        self.btn_sells.clicked.connect(self.sells_open)
        self.btn_login.clicked.connect(self.accounts_open)
        self.btn_help.clicked.connect(self.popup_help)

        self.tray_icon.activated.connect(self.restore_window)
        self.btn_stop.clicked.connect(self.switch_stop)
        self.btn_start.clicked.connect(self.switch_start)
        self.btn_pause.clicked.connect(self.switch_pause)

        self.tbl.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)

        self.main = main

    def eventFilter(self, source, event):
        num = event.type()
        if source.__class__.__name__ == "QPushButton":
            if num == 127:
                name = source.objectName()
                effect = name + '_effect'
                eval(effect).setColor(QColor(255, 213, 0))
            elif num == 128:
                name = source.objectName()
                effect = name + '_effect'
                eval(effect).setColor(Qt.white)
        return 0
        #return super(MainWindow, self).eventFilter(source, event)

    def onHeaderClicked(self, index):
        self.header_click = 1
        self.tbl_order = not self.tbl_order
        self.tbl_index = index

        if not index:
            self.show_table()
        elif self.tbl_order:
            self.tbl.sortItems(index, order=Qt.DescendingOrder)
            self.tbl_sort = Qt.DescendingOrder
        else:
            self.tbl.sortItems(index, order=Qt.AscendingOrder)
            self.tbl_sort = Qt.AscendingOrder

    def switch_start(self):
        self.btn_start.hide()
        self.lbl_refresh.show()
        self.btn_refresh.show()
        self.tbl.horizontalHeader().show()
        self.btn_pause.show()
        self.btn_stop.show()

    def switch_stop(self):
        self.btn_stop.hide()
        self.btn_refresh.hide()
        self.btn_pause.hide()
        self.btn_start.show()
        self.btn_sells.hide()
        self.not_running = True

    def switch_pause(self):
        self.btn_pause.hide()
        self.btn_stop.hide()
        self.btn_start.show()
        self.btn_stop.show()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                if self.main.sett.settings["tray_icon"]:
                    self.tray_icon.show()
                    self.hide()

    def closeEvent(self, event):
        if not self.main.sett.settings["tray_icon"]:
            exit()

    def restore_window(self, event):
        if event == QSystemTrayIcon.Trigger:
            self.showNormal()
            self.activateWindow()

    def show_table(self):
        self.tbl.setRowCount(0)

        for key, table_row in self.nova_notifier.table_result.items():
            col = 0
            row = self.tbl.rowCount()
            self.tbl.setRowCount(row + 1)
            for col, att in enumerate(table_row):
                if not col:
                    # Icon
                    id_num = att
                    icon = QLabel()
                    icon.setAlignment(Qt.AlignCenter)
                    img = QPixmap()
                    img.loadFromData(self.add.db_names[id_num]['icon'])
                    icon.setPixmap(img)
                    # ID text
                    url = f"'https://www.novaragnarok.com/?module=vending&action=item&id={table_row[0]}'"
                    txt = QLabel(f"<a href={url} style='color:#2ED03C'>{table_row[0]}</a>")
                    txt.setStyleSheet("QLabel{color: white; font: 10px; font-weight:bold;}")
                    txt.setOpenExternalLinks(True)
                    txt.setAlignment(Qt.AlignCenter)
                    # Layout
                    layout = QVBoxLayout()
                    layout.addWidget(icon)
                    layout.addWidget(txt)
                    # Widget
                    iconWidget = QWidget()
                    iconWidget.setLayout(layout)
                    self.tbl.setCellWidget(row, 0, iconWidget)
                    continue
                else:
                    cell = QTableWidgetItem(att)
                    cell.setTextAlignment(Qt.AlignCenter)
                    if att and col == 11:
                        if key in self.nova_notifier.notify:  # Alert
                            cell.setForeground(self.font_color["gold"])
                            txt.setStyleSheet("QLabel{ color: #FFD500; }")

                    elif col == 8:
                        if table_row[8]:
                            if "+" in table_row[8]:  # Short med
                                cell.setForeground(self.font_color["red"])
                            else:
                                cell.setForeground(self.font_color["green"])

                    elif col == 9:
                        if table_row[9]:
                            if "+" in att:  # Long med
                                cell.setForeground(self.font_color["red"])
                            else:
                                cell.setForeground(self.font_color["green"])

                    elif att and col == 11:
                        if key in self.nova_notifier.notify:  # Alert
                            cell.setForeground(self.font_color["gold"])
                            txt.setStyleSheet("QLabel{ color: #FFD500; }")

                    if not att:
                        att = '-'
                        cell = QTableWidgetItem(att)
                        cell.setTextAlignment(Qt.AlignCenter)
                        cell.setForeground(self.font_color["gray"])

                self.tbl.setItem(row, col, cell)

        self.tbl.resizeRowsToContents()
        if self.header_click:
            if not self.tbl_index:
                pass
            else:
                self.tbl.sortItems(self.tbl_index, order=self.tbl_sort)

        self.tbl.horizontalHeader().setSectionResizeMode(11, QHeaderView.ResizeToContents)


if __name__ == "__main__":
    import main
    main.windowLauncher()
