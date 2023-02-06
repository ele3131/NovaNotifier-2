import css
from sys import argv
from asyncio import sleep, create_task, set_event_loop, Event, \
                    CancelledError, get_event_loop
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QIcon
from qasync import QEventLoop, asyncSlot
from additem import AddItem
from gui import MainWindow
from traceback import format_exc
from NovaNotifier import NovaNotifier
from discordwindow import Discord_window
from popup import Popup
from settings import Settings
from sells import Sells
from database import Database
from accounts import Accounts
from network import Network


class MainWindow0(QMainWindow, MainWindow):
    def __init__(self):
        super().__init__()

        try:
            self.timer_count = True
            self.not_running = True
            self.tasks = {}

            self.db = Database(self)
            self.network = Network()
            self.add = AddItem(self)
            self.nova_notifier = NovaNotifier(self)
            self.sett = Settings(self)
            self.acc = Accounts(self)
            self.disc = Discord_window(self)
            self.add = AddItem(self)

            loop = get_event_loop()
            loop.run_until_complete(self.db.database_check())
            loop.run_until_complete(self.disc.discord_check())
            loop.run_until_complete(self.acc.read())

            self.pause_event = Event()
            self.ui(self)

        except Exception:
            self.exception()

    def exception(self, msg=''):
        if msg:
            self.popup = Popup(msg)
            self.popup.info()
        else:
            self.popup = Popup(format_exc() + msg)
            self.popup.critical()
        try:
            self.btn_stop.click()
        except Exception:
            pass

    def open_settings(self):
        self.sett.start()

    @asyncSlot()
    async def discord_open(self):
        self.disc.start()

    @asyncSlot()
    async def start_program(self):
        if self.not_running:
            await self.main.acc.check_cookies()
            self.sells = Sells(self)
            self.tasks['sells'] = create_task(self.sells.search())
            self.tasks['start'] = create_task(self.start_routine())
            self.tasks['timer'] = create_task(self.timer())
            self.not_running = False
        else:
            self.timer_resume()

    async def start_routine(self):
        try:
            self.nova_notifier = NovaNotifier(self)
            await self.nova_notifier.start()
            self.timer_resume()
            self.show_table()
        except Exception:
            self.exception()

    @asyncSlot()
    async def refresh_notifier(self):
        try:
            self.tasks['refresh'] = await self.refresh_routine()
        except Exception:
            self.exception()

    async def refresh_routine(self):
        try:
            self.timer_pause()
            self.refresh_timer = self.sett.settings['timer_refresh']
            await self.nova_notifier.refresh()
            self.show_table()
            self.timer_resume()
            self.btn_start.click()
        except CancelledError:
            pass
        except Exception:
            self.exception()
            return

    def stop_notifier(self):
        try:
            for task in self.tasks.values():
                task.cancel()
        except Exception:
            pass

        self.pause_event.clear()

        self.tbl.setRowCount(0)
        self.tbl.horizontalHeader().hide()
        self.lbl_refresh.hide()
        self.lbl_acc.setText("")
        self.lbl_refresh.setText("")
        self.not_running = True

    @asyncSlot()
    async def add_open(self):
        await self.add.start()

    @asyncSlot()
    async def sells_open(self):
        try:
            await self.sells.start()
        except Exception:
            self.exception()

    @asyncSlot()
    async def accounts_open(self):
        await self.acc.start()

    def popup_help(self):
        self.popup = Popup()
        self.popup.help(self)

    async def timer(self):
        try:
            self.refresh_timer = self.sett.settings['timer_refresh']
            while True:
                await self.pause_event.wait()
                if self.refresh_timer > 0:
                    self.refresh_timer -= 1
                    self.lbl_refresh.setText(f"Next Refresh: {self.refresh_timer}")
                    await sleep(1)
                else:
                    await self.refresh_notifier()
        except Exception:
            self.exception()

    def timer_pause(self):
        self.pause_event.clear()

    def timer_resume(self):
        self.pause_event.set()

    def center_window(self, window):
        center_x = self.pos().x() + self.frameGeometry().width()/2 - window.frameGeometry().width()/2
        center_y = self.pos().y() + self.frameGeometry().height()/2 - window.frameGeometry().height()/2
        window.move(center_x, center_y)


def windowLauncher():
    app = QApplication(argv)
    app.setWindowIcon(QIcon('Files/Icons/App/main2.ico'))
    app.setStyleSheet(css.window())

    loop = QEventLoop(app)
    set_event_loop(loop)

    w = MainWindow0()
    w.show()
    loop.run_forever()


if __name__ == "__main__":
    windowLauncher()
