import css
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, \
                            QTableWidgetItem, QVBoxLayout, QHBoxLayout, \
                            QRadioButton, QFormLayout, QAbstractScrollArea, \
                            QAbstractItemView, QTableWidget, QHeaderView
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from bs4 import BeautifulSoup
from datetime import datetime
from asyncio import gather, sleep
from sys import platform
import pytz
from network import Network


if platform == "win32":
    from win10toast_persist import ToastNotifier


class Sells(QWidget):
    def __init__(self, main):
        super().__init__()
        try:
            self.main = main
            self.active_account = 0
            self.active_username = ''
            self.shop_tbl_order = self.sold_tbl_order = 0
            self.shop_tbl_index = self.sold_tbl_index = 0
            self.url = 'https://www.novaragnarok.com/?module=account&action=sellinghistory'
            self.sell_htmls = []
            self.network = Network()
            self.setStyleSheet(css.popup())
            self.setWindowTitle("Market")
            self.setWindowIcon(QIcon('Files/Icons/App/shopping.svg'))
            self.icon_path = 'Files/Icons/App/main2.ico'
            self.setMinimumSize(240, 480)
            self.resize(self.frameGeometry().width(), self.frameGeometry().height())
            self.UI()

        except Exception:
            self.main.exception()

    async def start(self):
        self.account_change()
        self.show()

    def UI(self):

        """
            Widgets
        """

        self.lbl_usernames = QLabel('Account:')
        self.lbl_characters_zeny = QLabel('Character:')
        self.lbl_total_zeny = QLabel('Total Zeny:')
        self.lbl_server_time = QLabel('Server Time: ')

        self.lbl_shop = QLabel('Active Shop:')
        self.lbl_sold = QLabel('Sell History:')

        # Characters Table
        headers = ["Character", "Zeny"]

        self.character_tbl = QTableWidget(0, len(headers))
        self.character_tbl.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.character_tbl.setSelectionBehavior(QTableWidget.SelectRows)
        self.character_tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.character_tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.character_tbl.setHorizontalHeaderLabels(headers)
        self.character_tbl.verticalHeader().hide()
        self.character_tbl.setFocusPolicy(Qt.NoFocus)

        # Radio Buttons
        self.radio_buttons = []
        for username in self.main.acc.accounts.keys():
            btn = QRadioButton(username, self)
            btn.setStyleSheet(css.rbtn())
            btn.clicked.connect(self.account_change)
            self.radio_buttons.append(btn)

        if self.radio_buttons:
            self.radio_buttons[0].setChecked(True)

        # Reload
        self.btn_reload = QPushButton("Reload")

        # Selling Table
        self.selling_headers = ['Name', 'Prop', 'Qty', 'Price']
        self.shop_tbl = QTableWidget(0, len(self.selling_headers))
        self.shop_tbl.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.shop_tbl.setHorizontalHeaderLabels(self.selling_headers)
        self.shop_tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.shop_tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.shop_tbl.setSelectionMode(QAbstractItemView.NoSelection)
        self.shop_tbl.setFocusPolicy(Qt.NoFocus)
        self.shop_tbl.verticalHeader().hide()

        # Sold Table
        self.sold_headers = ['Time', 'Name', 'Prop', 'Qty', 'Price', 'Total']
        self.sold_tbl = QTableWidget(0, len(self.sold_headers))
        self.sold_tbl.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.sold_tbl.setHorizontalHeaderLabels(self.sold_headers)
        self.sold_tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sold_tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.sold_tbl.setSelectionMode(QAbstractItemView.NoSelection)
        self.sold_tbl.setFocusPolicy(Qt.NoFocus)
        self.sold_tbl.verticalHeader().hide()

        """
            Stylesheets
        """

        self.character_tbl.setStyleSheet(css.tbl())
        self.character_tbl.horizontalHeader().setStyleSheet(css.header())
        self.character_tbl.horizontalScrollBar().setStyleSheet(css.scrollbar())
        self.character_tbl.verticalScrollBar().setStyleSheet(css.scrollbar())

        self.shop_tbl.setStyleSheet(css.tbl())
        self.shop_tbl.horizontalHeader().setStyleSheet(css.header())
        self.shop_tbl.horizontalScrollBar().setStyleSheet(css.scrollbar())
        self.shop_tbl.verticalScrollBar().setStyleSheet(css.scrollbar())

        self.sold_tbl.setStyleSheet(css.tbl())
        self.sold_tbl.horizontalHeader().setStyleSheet(css.header())
        self.sold_tbl.horizontalScrollBar().setStyleSheet(css.scrollbar())
        self.sold_tbl.verticalScrollBar().setStyleSheet(css.scrollbar())

        self.lbl_usernames.setStyleSheet(css.lbl())
        self.lbl_characters_zeny.setStyleSheet(css.lbl())
        self.lbl_total_zeny.setStyleSheet(css.lbl())
        self.lbl_server_time.setStyleSheet(css.lbl())
        self.lbl_shop.setStyleSheet(css.lbl())
        self.lbl_sold.setStyleSheet(css.lbl())
        self.btn_reload.setStyleSheet(css.btn())

        """
            Layouts
        """

        self.lyt_rbtn = QHBoxLayout()

        for button in self.radio_buttons:
            self.lyt_rbtn.addWidget(button)
        self.lyt_rbtn.addStretch()

        self.lyt_info = QFormLayout()
        #self.lyt_info.setRowWrapPolicy(QFormLayout.WrapAllRows)
        self.lyt_info.addRow(self.lbl_usernames, self.lyt_rbtn)
        self.lyt_info.addRow(self.lbl_characters_zeny, self.character_tbl)
        self.lyt_info.addRow(self.lbl_shop, self.shop_tbl)
        self.lyt_info.addRow(self.lbl_sold, self.sold_tbl)

        self.lyt_foot = QHBoxLayout()
        self.lyt_foot.addWidget(self.lbl_total_zeny)
        self.lyt_foot.addStretch()
        self.lyt_foot.addWidget(self.lbl_server_time)

        self.lyt_main = QVBoxLayout()
        self.lyt_main.addLayout(self.lyt_info)
        self.lyt_main.addLayout(self.lyt_foot)

        self.setLayout(self.lyt_main)

        """
            Connect
        """

        self.shop_tbl.horizontalHeader().sectionClicked.connect(self.onShopHeaderClicked)
        self.sold_tbl.horizontalHeader().sectionClicked.connect(self.onSoldHeaderClicked)

    def onShopHeaderClicked(self, index):
        if self.shop_tbl_order:
            self.shop_tbl.sortItems(index, order=Qt.DescendingOrder)
        else:
            self.shop_tbl.sortItems(index, order=Qt.AscendingOrder)

        self.shop_tbl_index = index
        self.shop_tbl_order = not self.shop_tbl_order

    def onSoldHeaderClicked(self, index):
        if self.sold_tbl_order:
            self.sold_tbl.sortItems(index, order=Qt.DescendingOrder)
        else:
            self.sold_tbl.sortItems(index, order=Qt.AscendingOrder)

        self.sold_tbl_index = index
        self.sold_tbl_order = not self.sold_tbl_order

    async def search(self):
        try:
            self.start_time = datetime.now(pytz.timezone('US/Pacific')).replace(second=0, microsecond=0)
            count_last = [0]*len(self.main.acc.accounts)
            self.sold_items = [[] for i in range(len(self.main.acc.accounts))]
            while True:
                cookies = list(self.main.acc.accounts.values())
                self.sell_htmls = (await gather(*[self.network.search(self.url, each["cookie"]) for each in cookies]))
                self.main.btn_sells.show()

                for account, html in enumerate(self.sell_htmls):
                    # cookies[account]['username']
                    soup = BeautifulSoup(html, "html.parser")
                    table = soup.find(id="itemtable")
                    items = []
                    count_now = 0
                    if table:
                        for row in table.findAll("tr"):
                            row_contet = row.findAll("td")
                            item = {}
                            item['time'] = row_contet[0].get_text(strip=True)
                            item['name'] = row_contet[2].get_text(strip=True)
                            item['prop'] = row_contet[3].get_text(strip=True)
                            item['ea'] = row_contet[4].get_text(strip=True)
                            item['price'] = row_contet[5].get_text(strip=True)
                            item['total'] = row_contet[6].get_text(strip=True)
                            if self.date(item['time'], self.start_time):
                                item_price = int(item['price'].replace(',', '').replace('z', ''))
                                if item_price >= self.main.sett.settings['sell_filter'] * 0.95:
                                    items.append(item)
                                    count_now += 1

                        if (dif := count_now - count_last[account]) > 0:
                            await self.notification(items[0:dif])
                            self.sold_items[account] += items[0:dif]
                            count_last[account] = count_now
                # Update Account Info
                await self.main.acc.check_cookies()
                await self.main.acc.account_zeny()

                if self.active_username:
                    self.update()

                server_time = datetime.now(pytz.timezone('US/Pacific')).strftime('%H:%M')
                self.lbl_server_time.setText(f"Server Time: <font color=\"#2ED03C\">{server_time}</font>")
                await sleep(10)
        except Exception:
            self.main.exception()

    def show_table(self):
        if self.sell_htmls:
            html = self.sell_htmls[self.active_account]
            soup = BeautifulSoup(html, "html.parser")
            table_items = soup.find(id="itemtable2")
            self.shop_tbl.setRowCount(0)
            if table_items:
                for rows in table_items.findAll("tr"):
                    row = self.shop_tbl.rowCount()
                    self.shop_tbl.setRowCount(row + 1)
                    row_content = rows.findAll("td")
                    col = 0
                    table = []

                    # Table
                    table.append(row_content[1].get_text(strip=True))
                    table.append(row_content[2].get_text(strip=True))
                    table.append(row_content[3].get_text(strip=True))
                    table.append(row_content[4].get_text(strip=True))
                    for item in table:
                        cell = QTableWidgetItem(item)
                        cell.setTextAlignment(Qt.AlignCenter)
                        cell.setFlags(Qt.ItemIsEnabled)
                        self.shop_tbl.setItem(row, col, cell)
                        col += 1
                self.shop_tbl.resizeRowsToContents()
                if not self.shop_tbl_order:
                    self.shop_tbl.sortItems(self.shop_tbl_index, order=Qt.DescendingOrder)
                else:
                    self.shop_tbl.sortItems(self.shop_tbl_index, order=Qt.AscendingOrder)

    def show_sold_table(self):
        self.sold_tbl.setRowCount(0)
        if self.sold_items and self.sold_items[self.active_account]:
            for rows in self.sold_items[self.active_account]:
                row = self.sold_tbl.rowCount()
                self.sold_tbl.setRowCount(row + 1)
                col = 0
                for item in rows.values():
                    cell = QTableWidgetItem(item)
                    cell.setTextAlignment(Qt.AlignCenter)
                    cell.setFlags(Qt.ItemIsEnabled)
                    self.sold_tbl.setItem(row, col, cell)
                    col += 1
            self.sold_tbl.resizeRowsToContents()
            if not self.sold_tbl_order:
                self.sold_tbl.sortItems(self.sold_tbl_index, order=Qt.DescendingOrder)
            else:
                self.sold_tbl.sortItems(self.sold_tbl_index, order=Qt.AscendingOrder)

    def show_character_table(self):
        self.character_tbl.setRowCount(0)
        if self.active_username:
            characters = self.main.acc.accounts[self.active_username]['characters']
            characters_zeny = self.main.acc.accounts[self.active_username]['characters_zeny']
            for i, character in enumerate(characters):
                row = self.character_tbl.rowCount()
                self.character_tbl.setRowCount(row + 1)
                col = 0
                cell = QTableWidgetItem(character)
                cell.setTextAlignment(Qt.AlignCenter)
                self.character_tbl.setItem(row, col, cell)
                cell.setFlags(Qt.ItemIsEnabled)
                col = 1
                cell = QTableWidgetItem(characters_zeny[i])
                cell.setTextAlignment(Qt.AlignCenter)
                self.character_tbl.setItem(row, col, cell)
                cell.setFlags(Qt.ItemIsEnabled)
            self.character_tbl.resizeRowsToContents()

    def account_change(self):
        for b, btn in enumerate(self.radio_buttons):
            if btn.isChecked():
                self.active_account = b
                self.active_username = btn.text()
                total_zeny = f"<font color=\"#2ED03C\">{self.main.acc.accounts[self.active_username]['total_zeny']}z</font>"
                self.lbl_total_zeny.setText("Total Zeny: " + total_zeny)
                break

        self.update()

        if not self.active_account and self.radio_buttons:
            self.radio_buttons[0].setChecked(True)

    def date(self, date, interval):
        date1 = date.split('-')[0].replace(' ', '').split('/')
        date2 = date.split('-')[1].replace(' ', '').split(':')
        date1[2] = '20' + date1[2]
        date = pytz.timezone('US/Pacific').localize(datetime(int(date1[2]),
                                                    int(date1[0]),
                                                    int(date1[1]),
                                                    hour=int(date2[0]),
                                                    minute=int(date2[1])))
        if date >= interval:
            return 1  # sold
        else:
            return 0  # old

    def update(self):
        self.show_character_table()
        self.show_table()
        self.show_sold_table()

    async def notification(self, items):
        # Sell Alert
        for item in items:
            if self.main.sett.settings['sell_notification']:
                if self.main.sett.settings['discord_notification'] and self.main.disc.discord_channel:
                    msg = f"Name: {item['name']}\nProp: {item['prop']}\nQty: {item['ea']}x \nPrice: {item['price']}\nTotal: {item['total']}"
                    await self.main.db.sell_alert(msg)
                if self.main.sett.settings['system_notification'] and platform == "win32":
                    msg = f"{item['ea']}x {item['name']}\nProp: {item['prop']}\n\nSold: {item['price']}z"
                    toast = ToastNotifier()
                    toast.show_toast("NovaMarket", msg, threaded=True, icon_path=self.icon_path, duration=None)
                    await sleep(1)
