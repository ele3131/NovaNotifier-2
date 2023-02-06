import css
from PySide6.QtWidgets import QWidget, QTableWidget, QLineEdit, \
                            QPushButton, QTableWidgetItem, QVBoxLayout, \
                            QAbstractScrollArea, QHeaderView, \
                            QLabel, QTableView, QAbstractItemView, QHBoxLayout, \
                            QGraphicsColorizeEffect
from PySide6.QtGui import QIcon, QIntValidator, QPixmap, QColor
from PySide6.QtCore import Qt, QTimer, QSize
from qasync import asyncSlot
from popup import Popup


class AddItem(QWidget):
    def __init__(self, main):
        super().__init__()

        self.tbl_order = self.tbl_index = self.header_click = 0
        self.main = main
        self.db_names = {}
        self.items = {}

        self.setStyleSheet(css.popup())
        self.setWindowTitle("Add Item")
        self.setWindowIcon(QIcon('Files/Icons/App/add-file.svg'))
        self.setFocusPolicy(Qt.StrongFocus)
        self.resize(self.frameGeometry().width()*1/2, self.frameGeometry().height())
        self.UI()

    async def start(self):
        if not self.items:
            await self.read_item()
        self.show_table()
        self.setFocus()
        self.show()
        self.main.center_window(self)

    async def read_item(self):
        self.db_names = await self.main.db.database_name_get()
        if (items := await self.main.db.database_id_get()):
            self.items = items

    def UI(self):
        """
            Widgets
        """

        self.headers = ["Item", "Name", "Refine", "Prop", "Alert"]

        self.timer = QTimer()

        self.tbl = QTableWidget(0, len(self.headers))
        self.tbl.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tbl.setSelectionBehavior(QTableView.SelectRows)
        self.tbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.tbl.setSelectionMode(QAbstractItemView.MultiSelection)

        self.tbl.setHorizontalHeaderLabels(self.headers)
        self.tbl.verticalHeader().hide()
        self.tbl.setFocusPolicy(Qt.NoFocus)
        self.tbl.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tbl.viewport().installEventFilter(self)

        # Top Buttons
        btn_names = ["btn_delete", "btn_edit", "btn_add"]

        self.buttons = []

        for button in btn_names:
            button_self = f"self.{button}"
            effect = f"self.{button}_effect"
            setattr(self, button, QPushButton(objectName=button_self))
            setattr(self, button + '_effect', QGraphicsColorizeEffect(self))
            eval(effect).setColor(Qt.white)
            eval(button_self).setGraphicsEffect(eval(effect))
            eval(button_self).setIconSize(QSize(32, 32))
            eval(button_self).installEventFilter(self)
            self.buttons.append(eval(button_self))

        self.line_id = QLineEdit()
        self.line_id.setValidator(QIntValidator(0, 1_000_000_000))
        self.line_id.setPlaceholderText("ID")
        self.line_id.setToolTip("Example: 32641")
        self.line_id.setAlignment(Qt.AlignHCenter)

        self.line_refine = QLineEdit()
        self.line_refine.setValidator(QIntValidator(0, 100))
        self.line_refine.setPlaceholderText("Refine")
        self.line_refine.setToolTip("Example: 10 \nDefault: 0")
        self.line_refine.setAlignment(Qt.AlignHCenter)

        self.line_property = QLineEdit()
        self.line_property.setPlaceholderText("Properties")
        self.line_property.setToolTip("Example: Fire, Fighting Spirit, Any \nDefault: None\nOptional: Any")
        self.line_property.setAlignment(Qt.AlignHCenter)

        self.line_alert_price = QLineEdit()
        self.line_alert_price.setValidator(QIntValidator())
        self.line_alert_price.setPlaceholderText("Alert Price")
        self.line_alert_price.setToolTip("Example: 20.000.000 \nDefault: 0")
        self.line_alert_price.setAlignment(Qt.AlignHCenter)

        self.btn_submit = QPushButton("Add")
        self.btn_save = QPushButton("Save")

        """
            Layouts
        """

        width = self.frameGeometry().width()/6

        self.lyt_buttons = QHBoxLayout()
        self.lyt_buttons.setContentsMargins(width, 0, width, 0)
        self.lyt_buttons.addWidget(self.btn_add)
        self.lyt_buttons.addWidget(self.btn_edit)
        self.lyt_buttons.addWidget(self.btn_delete)

        self.lyt_mid = QVBoxLayout()
        self.lyt_mid.setContentsMargins(width, 10, width, 10)
        self.lyt_mid.addWidget(self.line_id)
        self.lyt_mid.addWidget(self.line_refine)
        self.lyt_mid.addWidget(self.line_property)
        self.lyt_mid.addWidget(self.line_alert_price)

        self.lyt_main = QVBoxLayout()
        self.lyt_main.addWidget(self.tbl)
        self.lyt_main.addLayout(self.lyt_buttons)
        self.lyt_main.addLayout(self.lyt_mid)

        self.setLayout(self.lyt_main)

        """
            Connects
        """
        self.tbl.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)

        self.btn_edit.clicked.connect(self.edit_item)
        self.btn_delete.clicked.connect(self.delete_confirmation)
        self.btn_add.clicked.connect(self.submit_items)

        """
            Styling
        """

        self.tbl.setStyleSheet(css.tbl())
        self.tbl.horizontalHeader().setStyleSheet(css.header())
        self.tbl.verticalHeader().setStyleSheet(css.header())
        self.tbl.verticalScrollBar().setStyleSheet(css.scrollbar())
        self.tbl.horizontalScrollBar().setStyleSheet(css.scrollbar())

        self.btn_delete.setStyleSheet(css.btn_main("url(Files/Icons/App/delete.svg)"))
        self.btn_edit.setStyleSheet(css.btn_main("url(Files/Icons/App/edit.svg)"))
        self.btn_add.setStyleSheet(css.btn_main("url(Files/Icons/App/plus.svg)"))

        self.line_id.setStyleSheet(css.line_edit())
        self.line_refine.setStyleSheet(css.line_edit())
        self.line_property.setStyleSheet(css.line_edit())
        self.line_alert_price.setStyleSheet(css.line_edit())

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

        return super(AddItem, self).eventFilter(source, event)

    def delete_confirmation(self):
        self.popup = Popup("Remove from List?")
        self.popup.question()
        self.popup.btn_yes.clicked.connect(self.delete_item)
        self.popup.btn_yes.clicked.connect(self.popup.close)
        self.popup.btn_no.clicked.connect(self.popup.close)

    def edit_item(self):
        self.selected_index = self.tbl.selectionModel().selectedRows()
        for index in self.selected_index:
            lines = [self.line_id, self.line_refine, self.line_property, self.line_alert_price]
            item_row = index.row()
            lines[0].setText(self.tbl.cellWidget(item_row, 0).children()[2].text().split('</a>')[0].split('>')[1])
            lines[1].setText(self.tbl.item(item_row, 2).text().replace('+', ''))
            lines[2].setText(self.tbl.item(item_row, 3).text())
            lines[3].setText(self.tbl.item(item_row, 4).text().replace('z', '').replace(',', '.'))

    def delete_item(self):
        self.main.btn_stop.click()
        self.remove_indexes = self.tbl.selectionModel().selectedRows()
        for index in self.remove_indexes:
            row_id = self.tbl.cellWidget(index.row(), 0).layout().itemAt(1).widget().text().split('</a>')[0].split('>')[1]
            for key in self.items.keys():
                list_id = key.split("'")[1].split("'")[0]
                if row_id == list_id:
                    del self.items[key]
                    break
        self.show_table()
        self.save_item()

    def show_table(self):
        icon = None
        self.tbl.setRowCount(0)
        for row, each in enumerate(self.items.values()):
            self.tbl.setRowCount(row + 1)
            icon = QLabel()
            icon.setAlignment(Qt.AlignCenter)
            img = QPixmap()
            if each['id'] in self.db_names:
                img.loadFromData(self.db_names[each['id']]['icon'])
            icon.setPixmap(img)
            # ID text
            url = f"'https://www.novaragnarok.com/?module=vending&action=item&id={each['id']}'"
            txt = QLabel(f"<a href={url} style='color:#2ED03C'>{each['id']}</a>")
            txt.setStyleSheet("QLabel{color: white; font: 10px; font-weight:bold;}")
            txt.setOpenExternalLinks(True)
            txt.setAlignment(Qt.AlignCenter)
            # Layout
            layout = QVBoxLayout()
            layout.addWidget(icon)
            layout.addWidget(txt)
            # Widget
            cellWidget = QWidget()
            cellWidget.setStyleSheet("QWidget{background-color: transparent;}")
            cellWidget.setLayout(layout)
            self.tbl.setCellWidget(row, 0, cellWidget)

            col = 1
            table = [each['name'], '+' + str(each['refine']), ', '.join(each['property']), format(each['alert'], ',d') + 'z']
            for item in table:
                cell = QTableWidgetItem(item)
                cell.setTextAlignment(Qt.AlignCenter)
                self.tbl.setItem(row, col, cell)
                col += 1

        self.tbl.resizeRowsToContents()

        if self.header_click:
            if not self.tbl_index:
                pass
            else:
                self.tbl.sortItems(self.tbl_index, order=self.tbl_sort)

        self.tbl.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

    @asyncSlot()
    async def submit_items(self):
        self.db_names = await self.main.db.database_name_get()
        new_item = self.filter_inputs()
        if not new_item:
            return
        self.add_data(new_item)
        self.show_table()
        self.popup = Popup("Item Added!")
        self.popup.info()
        self.line_id.setText("")
        self.line_refine.setText("")
        self.line_property.setText("")
        self.line_alert_price.setText("")
        await self.save_item()

    def filter_inputs(self):
        new_item = {}

        if line := (self.line_id.text().strip()).replace('.', ''):
            new_item['id'] = line
        else:
            self.popup = Popup('ID Empty!')
            self.popup.warning()
            return

        if line := (self.line_refine.text()).replace('.', ''):
            new_item['refine'] = int(line)
        else:
            new_item['refine'] = 0

        if line := (self.line_property.text().strip()).replace('.', ','):
            new_item['property'] = line
        else:
            new_item['property'] = 'None'

        if line := (self.line_alert_price.text()).replace('.', ''):
            new_item['alert'] = int(line)
        else:
            new_item['alert'] = 0

        if new_item['id'] in self.db_names:
            new_item['name'] = self.db_names[new_item['id']]['name']
        else:
            #new_item['name'] = f"Unknown • {new_item['id']}"
            new_item['name'] = "Unknown"

        return new_item

    def add_data(self, new_item):
        self.main.btn_stop.click()
        prop = [item.strip() for item in new_item['property'].split(',')]
        prop_key = ', '.join(prop)
        self.items[str((new_item['id'], new_item['refine'], prop_key))] = {'id': new_item['id'],
                                                                'name': new_item['name'],
                                                                'refine': new_item['refine'],
                                                                'property': prop,
                                                                'alert': new_item['alert']}

    @asyncSlot()
    async def save_item(self):
        await self.main.db.database_id_save(self.items)

    def closeEvent(self, event):
        self.close()
