from sys import platform
from asyncio import sleep
from datetime import datetime
from statistics import median
from bs4 import BeautifulSoup
import pytz
import textwrap


if platform == "win32":
    from win10toast_persist import ToastNotifier


class NovaNotifier():
    def __init__(self, main):
        self.main = main
        self.network = self.main.network
        self.notify = {}
        self.market_data = {}
        self.history_data = {}
        self.icon_path = 'Files/Icons/App/main2.ico'
        self.table_result = {}

    async def start(self):
        await self.main.add.read_item()
        self.items = self.main.add.items

        if not self.main.acc.accounts:
            self.main.btn_login.click()
            self.main.exception('Please Add Your Account First!')

        self.market_data, self.history_data = await self.network.network_items(self.main, self.items)
        self.medians_history(self.items)
        self.formatting(self.items)
        await self.make_table(self.items)
        await self.save_item(self.items.items())
        await self.notification()

    async def refresh(self):
        self.market_data, self.history_data = await self.network.network_items(self.main, self.items)
        self.formatting(self.items)
        await self.make_table(self.items)
        await self.notification()

    def medians_history(self, items):
        today = datetime.now(pytz.timezone('US/Pacific')).replace(minute=0, second=0, microsecond=0)
        interval = [self.main.sett.settings['SM'], self.main.sett.settings['LM']]
        for item in items.values():
            med, long_med = [], []
            if 'Any' in item['property'] or "any" in item['property']:
                pass

            else:
                history = self.history_data[item['id']]
                for each in history:
                    if 'refine' in each['orders']:
                        item_refine = each['orders']['refine']
                        if item_refine == item['refine']:
                            if self.property_check(each, item['property']):
                                date = each['items']['date'].split(' ', 1)[0].split("/")
                                call = self.date(date, interval, today)
                                if call[0] is True:
                                    long_med.append(each['orders']['price'])
                                    if call[1] is True:
                                        med.append(each['orders']['price'])
                                else:
                                    break

                    else:
                        if self.property_check(each, item['property']):
                            date = each['items']['date'].split(' ', 1)[0].split("/")
                            call = self.date(date, interval, today)
                            if call[0] is True:
                                long_med.append(each['orders']['price'])
                                if call[1] is True:
                                    med.append(each['orders']['price'])
                            else:
                                break

            if med and long_med:
                item['short_med'], item['long_med'] = round(median(med)), round(median(long_med))
            elif med and not long_med:
                item['short_med'], item['long_med'] = round(median(med), None)
            elif not med and long_med:
                item['short_med'], item['long_med'] = None, round(median(long_med))
            elif not med and not long_med:
                item['short_med'], item['long_med'] = None, None

    async def notification(self, sell_item=None):
        # Save items first to prevent duplicate notifications
        items = []
        for key in self.notify:
            if self.notify[key]:
                items.append(self.items[key])
                self.notify[key] = False

        # Price Alert
        for item in items:
            if self.main.sett.settings['price_notification']:
                location = item['location'].replace('\n', '')
                url = 'https://www.novaragnarok.com/?module=vending&action=item&id=' + item['id']
                if self.main.sett.settings['discord_notification'] and self.main.disc.discord_channel:
                    msg = (f"{item['name']}\nRefine: {item['format_refine']}\nProperty: {item['format_property']}\n" +
                           f"Alert: {item['format_alert']}\nPrice: {item['format_price']}\nLocation: {location}\n\n{url}")
                    await self.main.db.price_alert(msg)
                if self.main.sett.settings['system_notification'] and platform == "win32":
                    msg = (f"{item['format_refine']} {item['name']}\nProp: {item['format_property']}\n\n" +
                           f"{item['format_price']} | {location}")
                    toast = ToastNotifier()
                    toast.show_toast("NovaMarket", msg, threaded=True, icon_path=self.icon_path, duration=None)
                    await sleep(1)

    def date(self, date, interval, today=None):
        result = [False, False]
        date = pytz.timezone('US/Pacific').localize(datetime(2000 + int(date[2]),
                                                    int(date[0]),
                                                    int(date[1])))
        time = today - date

        if time.days <= interval[1]:
            result[0] = True
            if time.days <= interval[0]:
                result[1] = True

        return result

    def formatting(self, items):
        for key, item in items.items():
            location, format_refine, format_prop = self.price_search(item, key)

            item['format_refine'] = format_refine
            item['format_property'] = ', '.join(format_prop)
            if location is not None:
                item['format_price'] = format(item['price'], ',d') + 'z'
                item['format_short_med'] = format(item['short_med'], ',d') + 'z' if item['short_med'] else None
                item['format_long_med'] = format(item['long_med'], ',d') + 'z' if item['long_med'] else None
                item['short_med_perc'], item['long_med_perc'] = self.percentage(item)
                item['format_alert'] = format(item['alert'], ',d') + 'z' if item['alert'] else None
                item['location'] = f"{location.split(',', 1)[0]}{location.split(',', 1)[1]}"
            else:
                item['format_price'] = None
                item['ea'] = None
                item['format_short_med'] = format(item['short_med'], ',d') + 'z' if item['short_med'] else None
                item['format_long_med'] = format(item['long_med'], ',d') + 'z' if item['long_med'] else None
                item['short_med_perc'], item['long_med_perc'] = None, None
                item['format_alert'] = format(item['alert'], ',d') + 'z' if item['alert'] else None
                item['location'] = None

    def price_search(self, item, key):
        """ Return: Cheapest Item Location and Format_Refine """

        info = {'median': item['short_med'], 'cheap_total': 0, 'cheapest_total': 0,
                'cheapest_location': None, 'cheapest_price': 1000000000, 'alert': item['alert']}
        minor_refine = item['refine']
        format_refine = f"+{item['refine']}"
        format_prop = item['property']

        for each in self.market_data[item['id']]:
            if 'refine' in each['orders']:
                refine = each['orders']['refine']
                if refine >= item['refine']:
                    if prop := self.property_check(each, item['property']):
                        if self.lowest_price(each, info, key):
                            minor_refine = refine
                            format_prop = prop

            else:  # Not Refinable
                if self.property_check(each, item['property']):
                    self.lowest_price(each, info, key)

        if minor_refine != item['refine']:
            format_refine = f"+{item['refine']} -> +{minor_refine}"
        else:
            format_refine = f"+{minor_refine}"

        item['price'] = info['cheapest_price']
        item['ea'] = f'{info["cheapest_total"]} / {info["cheap_total"]}'

        return info['cheapest_location'], format_refine, format_prop

    def lowest_price(self, item, info, item_key):
        if 'qty' in item['orders']:
            ea = item['orders']['qty']
        else:
            ea = 1

        info['cheap_total'] += ea
        price = item['orders']['price']

        if price == info['cheapest_price']:
            info['cheapest_total'] += ea

        elif price < info['cheapest_price']:
            info['cheapest_price'] = price
            info['cheapest_location'] = item['orders']['location'].strip()
            info['cheapest_total'] = ea
            if info['cheapest_price'] <= info['alert'] and item_key not in self.notify:
                self.notify[item_key] = True
            return True

        return False

    def property_check(self, web_prop, prop):
        """ Input: Properties from Website, Your Item Properties """

        local_item_prop = list(prop)

        if local_item_prop[-1] == '':
            local_item_prop.pop()

        # No Property Column
        if 'property' not in web_prop['orders'] or not web_prop['orders']['property']:
            if 'None' in local_item_prop:
                return prop
            else:
                return 0

        # Web Property Column
        else:
            props = (BeautifulSoup(web_prop['items']['property'], "html.parser")).get_text(strip=True)

            if props[-1] == '.':
                web_item_prop = props.split('. ')
                web_item_prop[-1] = web_item_prop[-1].replace('.', '')
            else:
                web_item_prop = props.split(',')

            # Comparison between item from website and requested property
            extra = False
            for item in local_item_prop:
                if item.upper() == 'ANY':
                    extra = True
                    continue
                else:
                    if item in web_item_prop:
                        web_item_prop.remove(item)
                        continue
                    else:
                        return 0

            if web_item_prop and not extra:
                return 0

            elif web_item_prop and extra:
                return local_item_prop + web_item_prop

            else:
                return local_item_prop

    def percentage(self, item):
        if item['long_med']:
            if item['long_med'] > item['price']:
                long_med_perc = '-' + str(round(abs(100 - (item['price'] / item['long_med']) * 100))) + '%'
            elif item['long_med'] < item['price']:
                long_med_perc = '+' + str(round(abs(100 - (item['price'] / item['long_med']) * 100))) + '%'
            else:
                long_med_perc = '0%'
        else:
            return None, None

        if long_med_perc == '+0%' or long_med_perc == '-0%':
            long_med_perc = '0%'

        if item['short_med']:
            if item['short_med'] > item['price']:
                med_perc = '-' + str(round(abs(100 - (item['price'] / item['short_med']) * 100))) + '%'
            elif item['short_med'] < item['price']:
                med_perc = '+' + str(round(abs(100 - (item['price'] / item['short_med']) * 100))) + '%'
            else:
                med_perc = '0%'
        else:
            med_perc = None

        if med_perc == '+0%' or med_perc == '-0%':
            med_perc = '0%'

        return med_perc, long_med_perc

    async def make_table(self, items):
        # Make table to main
        self.table_result = {}
        for key, item in items.items():
            self.table_result[key] = [item['id'], item['name'], item['format_refine'], item['format_property'],
                    item['ea'], item['format_price'], item['format_short_med'], item['format_long_med'],
                    item['short_med_perc'], item['long_med_perc'], item['format_alert'], item['location']]

        if self.main.disc.discord_channel:
            wrapper = textwrap.TextWrapper(width=12)
            table = []
            headers = ['Name', 'Refine', 'Prop', 'Price', 'Qty', 'Alert', 'Location']
            for key, item in items.items():
                table.append([wrapper.fill(item['name']), wrapper.fill(item['format_refine']),
                              wrapper.fill(item['format_property']), wrapper.fill(str(item['format_price'])),
                              wrapper.fill(str(item['ea'])), wrapper.fill(str(item['format_alert'])),
                              wrapper.fill(str(item['location']))])

            await self.main.db.database_table_save(headers, table)

    async def save_item(self, items):
        save = {}
        for key, value in items:
            save[key] = {'id': value['id'],
                         'name': value['name'],
                         'refine': value['refine'],
                         'alert': value['alert'],
                         'property': value['property']}

        if self.main.disc.discord_channel:
            await self.main.db.database_id_save(save)

    def retrieving(self):
        self.main.lbl_refresh.setText(f"Retrieving: {self.network_count}")
        self.network_count += 1


if __name__ == "__main__":
    import main
    main.windowLauncher()