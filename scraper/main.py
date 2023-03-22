import re
import json
import pathlib

import requests
from bs4 import BeautifulSoup

master_path = pathlib.Path(__file__).parent


class Bot:
    def __init__(self):
        self.session = requests.Session()

    def main(self):
        cards_links = self.get_card_links()

        parsed_cards = []
        for i, link in enumerate(cards_links, start=1):
            print(f"Getting card: {i}/{len(cards_links)} -> {link}")
            card_info = self.get_card_info(link, _id=i)
            parsed_cards.append(card_info)

        with open(master_path / 'card_info.json', 'w') as file:
            json.dump(parsed_cards, file, indent=2)

    def get_card_links(self):
        r = self.session.get('https://ccsakura.fandom.com/wiki/Clow_Cards')
        html = BeautifulSoup(r.content, 'html.parser')
        raw_links = html.select('#gallery-0 div.lightbox-caption a')

        return ['https://ccsakura.fandom.com' + link['href'] for link in raw_links]

    def get_card_info(self, link, _id):
        r = self.session.get(link)
        html = BeautifulSoup(r.content, 'html.parser')

        title = html.select_one('#firstHeading').text.strip()
        desc = html.select_one('div.mw-parser-output > p')
        if '"' in desc.text:
            desc = html.select('div.mw-parser-output > p')[1]

        desc = desc.text.strip().replace('\xa0', ' ')
        clow_card, sakura_card = [el['href'].split('.jpg')[0] + '.jpg' for el in
                                  html.select('div.wds-tab__content > p > a')[:2]]

        table_info = html.select('table.infobox tr')
        table_info = [row.text.strip().split('\n\n') for row in table_info]
        table_info = [x for x in table_info if len(x) == 2]
        table_info = {x[0]: x[1] for x in table_info}

        kanji = None if 'Kanji' not in table_info else table_info['Kanji']
        katakana = None if 'Katakana' not in table_info else table_info['Katakana']
        sign = None if 'Sign' not in table_info else table_info['Sign']
        hierarchy = None if 'Hierarchy' not in table_info else table_info['Hierarchy']
        magic_type = None if 'Magic Type' not in table_info else table_info['Magic Type']
        temperament = None if 'Temperament' not in table_info else table_info['Temperament']
        if '[' in desc:
            print(re.sub(r'\[\d+\]', '', desc))
            exit()

        card_info = {'id': _id,
                     'title': title,
                     'desc': re.sub(r'\[\d+]', '', desc),
                     'clowCard': {'front': clow_card,
                                  'back': 'https://static.wikia.nocookie.net/ccs/images/7/7b/CCS_Clow_Card.jpg'},
                     'sakuraCard': {'front': sakura_card,
                                    'back': 'https://static.wikia.nocookie.net/ccs/images/3/3f/CCS_Sakura_Card.jpg'},
                     'kanji': kanji,
                     'katakana': katakana,
                     'sign': sign,
                     'hierarchy': hierarchy,
                     'magicType': magic_type,
                     'temperament': temperament}

        return card_info

    @staticmethod
    def extract_info_from_row(row):
        return ' '.join(row.text.strip().split(' ')[1:]).title()


if __name__ == '__main__':
    bot = Bot()
    bot.main()
