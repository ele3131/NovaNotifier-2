from aiohttp import ClientSession
from asyncio import create_task, gather, sleep, BoundedSemaphore, Event
from bs4 import BeautifulSoup
from popup import Popup


class Network():
    def __init__(self):
        self.sema = BoundedSemaphore(4)
        self.network_fail = Event()
        self.market_data = {}
        self.history_data = {}

    async def search(self, url, account):
        async with ClientSession(cookies=account) as session:
            html = await self.network_request(url, session)
        return html

    async def network_request(self, url, session):
        while True:
            try:
                async with self.sema:
                    async with session.get(url, timeout=5) as response:
                        stat = response.status
                        if stat == 200:
                            return await response.text()
                        else:
                            await self.network_retry(stat)
            except Exception as e:
                await self.network_retry(e)

    async def network_items(self, main, items):
        self.main = main
        self.market_data = {}
        self.db_items = self.main.add.db_names

        # Start All Network Search
        async with ClientSession() as session:
            await gather(*[self.network_market_request(item, session) for item in items.values()])

        async with ClientSession() as session:
            await gather(*[self.network_history_request(item, session) for item in items.values()])

        cookie = list(self.main.acc.accounts.values())[0]["cookie"]
        async with ClientSession(cookies=cookie) as session:
            await gather(*[self.network_name_request(item, session) for item in items.values()])

        async with ClientSession() as session:
            await gather(*[self.network_icon_request(item, session) for item in items.values()])

        self.popup_active = False
        await self.main.db.database_name_save(self.db_items)
        return self.market_data, self.history_data

    async def network_market_request(self, item, session):
        if item['id'] not in self.market_data:
            url = f"https://www.novaragnarok.com/data/cache/ajax/item_{item['id']}.json"
            self.market_data[item['id']] = True
            while True:
                try:
                    async with self.sema:
                        async with session.get(url, timeout=5) as response:
                            stat = response.status
                            if stat == 200:
                                self.main.lbl_refresh.setText("Searching: " + item['name'])
                                self.market_data[item['id']] = (await response.json())['data']
                                return
                            else:
                                await self.network_retry(stat)
                except Exception as e:
                    await self.network_retry(e)

    async def network_history_request(self, item, session):
        if item['id'] not in self.history_data:
            self.history_data[item['id']] = True
            url = f"https://www.novaragnarok.com/data/cache/ajax/history_{item['id']}.json"
            while True:
                try:
                    async with self.sema:
                        async with session.get(url, timeout=5) as response:
                            stat = response.status
                            if stat == 200:
                                self.history_data[item['id']] = (await response.json())['data']
                                return
                            else:
                                await self.network_retry(stat)
                except Exception as e:
                    await self.network_retry(e)

    async def network_name_request(self, item, session):
        if item['id'] not in self.db_items:
            url = f"https://www.novaragnarok.com/?module=vending&action=item&id={item['id']}"
            while True:
                try:
                    async with self.sema:
                        async with session.get(url, timeout=5) as response:
                            stat = response.status
                            if stat == 200:
                                html = await response.text()
                                soup = BeautifulSoup(html, "html.parser")
                                name = soup.find("div", {"class": "item-name"})
                                item['name'] = name.get_text().strip()
                                self.db_items[item['id']] = {"name": item['name']}
                                return
                            else:
                                await self.network_retry(stat)
                except Exception as e:
                    await self.network_retry(e)
        else:
            item['name'] = self.db_items[item['id']]['name']

    async def network_icon_request(self, item, session):
        if 'icon' not in self.db_items[item['id']]:
            url = 'https://www.novaragnarok.com/data/items/icons2/' + item['id'] + '.png'
            while True:
                try:
                    async with self.sema:
                        async with session.get(url, timeout=5) as response:
                            stat = response.status
                            if stat == 200:
                                self.db_items[item['id']]['icon'] = await response.read()
                                return
                            else:
                                await self.network_retry(stat)
                except Exception as e:
                    await self.network_retry(e)

    async def network_retry(self, msg):
        self.network_fail.clear()
        self.timer_task = create_task(self.network_timer(msg))
        self.popup = Popup(f"Search Fail, Retry? (30) \n\nError: {msg}")
        self.popup.question()
        self.popup.btn_yes.clicked.connect(self.network_confirm)
        self.popup.btn_no.clicked.connect(self.network_cancel)
        self.popup.closeEvent = self.popup_close
        await self.network_fail.wait()

    def network_confirm(self):
        self.network_fail.set()
        self.popup.close()

    def network_cancel(self):
        self.main.btn_stop.click()
        self.popup.close()

    async def network_timer(self, msg):
        i = 30
        while i > 0:
            self.popup.lbl_text.setText(f"Search Fail, Retry? ({i}) \n\nError: {msg}")
            await sleep(1)
            i -= 1
        self.network_fail.set()
        self.popup.close()

    def popup_close(self, e):
        self.timer_task.cancel()
        if not self.network_fail.is_set():
            self.network_fail.set()
            self.main.btn_stop.click()
