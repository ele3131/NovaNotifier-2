from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from table2ascii import table2ascii, PresetStyle
from dotenv import load_dotenv
import os
#import sys

# Pyinstaller Database Token
#if getattr(sys, 'frozen', False):
#    os.chdir(sys._MEIPASS)
#else:
#    application_path = os.path.dirname(os.path.abspath(__file__))


class Database():
    def __init__(self, main):
        load_dotenv("Files/Database.env")
        mongo_token = os.getenv("mongo_token")
        if not mongo_token:
            raise Exception("Database file missing MondoDB Token.")

        self.db = AsyncIOMotorClient(mongo_token)
        self.main = main

    async def database_check(self):
        names = await self.db.list_database_names()
        if 'nova' not in names:
            self.db["nova"]

    async def token_check(self, token):
        return (await self.db.nova.users.find_one({"token": token}))

    async def token_update(self):
        await self.db.nova.users.update_one({'discord': self.main.disc.discord_name}, {'$set': {'date': datetime.now()}})

    async def database_name_get(self):
        db = self.db.nova.items.find()
        db_items = {}
        for item in await db.to_list(length=None):
            db_items[item['id']] = {'name': item['name'], 'icon': item['icon']}

        return db_items

    async def database_name_save(self, items):
        for key, value in items.items():
            await self.db.nova.items.update_one({"id": key}, {'$set': {"name": value['name'], "icon": value['icon']}}, upsert=True)

    async def database_id_save(self, items):
        await self.db.nova.users.update_one({"channel": self.main.disc.discord_channel}, {'$set': {"search": items}}, upsert=True)

    async def database_id_get(self):
        return (await self.db.nova.users.find_one({"channel": self.main.disc.discord_channel}))['search']

    async def database_cookie_key_get(self):
        return (await self.db.nova.users.find_one({"channel": self.main.disc.discord_channel}))['cookie_key']

    async def database_table_save(self, headers, table):
        discord_table = table2ascii(
                        header=headers,
                        body=table,
                        style=PresetStyle.thin_compact_rounded,
                        max_size=1850)

        if discord_table:
            discord_table[-1] += f"\nLast Refresh: {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}"
            await self.db.nova.users.update_one({'channel': self.main.disc.discord_channel}, {'$set': {'table': discord_table}})

    async def price_alert(self, msg):
        await self.db.nova.users.update_one({'channel': self.main.disc.discord_channel}, {'$push': {'price_alert': msg}, '$set': {'price_flag': True}})

    async def sell_alert(self, msg):
        await self.db.nova.users.update_one({'channel': self.main.disc.discord_channel}, {'$push': {'sold_alert': msg}, '$set': {'sold_flag': True}})
