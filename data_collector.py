from time import sleep
import csv
import requests
import json
from lxml import html
from tqdm import tqdm


class Champion:
    subclass_to_class_dict = {'Enchanter': 'Controller',
                          'Catcher': 'Controller',
                          'Diver': 'Fighter',
                          'Juggernaut': 'Fighter',
                          'Burst': 'Mage',
                          'Battlemage': 'Mage',
                          'Artillery': 'Mage',
                          'Marksman': 'Marksman',
                          'Assassin': 'Slayer',
                          'Skirmisher': 'Slayer',
                          'Vanguard': 'Tank',
                          'Warden': 'Tank',
                          'Specialist': 'Specialist'}

    def __init__(self, name):
        if name == 'MonkeyKing':
            name = 'Wukong'
        self.name = name
        self.skill_order = ()
        self.lvl_1 = ''
        self.class_ = ''
        self.subclass = ''
        self.release_ = ''
        self.vgu = ''

    def get_skill_info(self):
        page = requests.get('https://u.gg/lol/champions/{}/build'.format(self.name))
        tree = html.fromstring(page.content)
        order = []
        for i in range(1,4):
            path = '//*[@id="content"]/div/div/div[3]/div/div[3]/div[1]/div[2]/div/div[1]/div[{}]/div'.format(i)
            order.append(tree.xpath(path)[0].text)
        self.skill_order = tuple(order)

        for idx, skill in enumerate(['Q', 'W', 'E'], 1):
            path = '//*[@id="content"]/div/div/div[3]/div/div[3]/div[2]/div[2]/div/div/div/div[{}]/div[3]/div[1]' \
                .format(idx)
            if tree.xpath(path)[0].attrib['class'] == 'skill-up ':
                self.lvl_1 = skill
                break

    def get_info(self, webpage_tree, idx):
        self.subclass = webpage_tree.xpath('//*[@id="mw-content-text"]/table[2]/tr[{}]/td[2]/@data-sort-value'.
                                           format(idx))[0]
        self.class_ = self.subclass_to_class_dict[self.subclass]
        release_date = webpage_tree.xpath('//*[@id="mw-content-text"]/table[2]/tr[{}]/td[4]'.format(idx))[0].text
        if release_date == ' ':
            release_date = webpage_tree.xpath('//*[@id="mw-content-text"]/table[2]/tr[{}]/td[4]/span'.format(idx))[
                0].text
        self.release_ = release_date.strip()[:4]
        assert self.release_
        self.vgu = self.release_

    def set_vgu_info(self, year):
        self.vgu = year


def main():

    # Latest patch is pulled from Riot's static data
    general_data = json.loads(requests.get('https://ddragon.leagueoflegends.com/realms/na.json').content)
    patch = general_data['v']

    # Information on champions for the latest patch is pulled from Riot's static data and Champion objects are created
    ddragon_url = 'http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'.format(patch)
    champion_data = json.loads(requests.get(ddragon_url).content)
    champions = [Champion(x) for x in champion_data['data'].keys()]

    # Skill leveling priority is pulled from u.gg
    for champ in tqdm(champions):
        champ.get_skill_info()
        sleep(1)

    # Reorder the champions list alphabetically according to champion name. Swap Dr. Mundo with Draven to get the
    # correct order in the Wiki's champion list.
    dr_mundo = next(c for c in champions if c.name == 'DrMundo')
    dr_mundo.name = 'Dr. Mundo'
    champions.sort(key=lambda c: c.name)


    # Get class, subclass and release date of every champion (pulled from League of Legends wiki)
    wiki_class_page = requests.get('https://leagueoflegends.fandom.com/wiki/List_of_champions')
    tree = html.fromstring(wiki_class_page.content)
    for idx, champ in enumerate(champions, 2):
        # champ = tree.xpath('//*[@id="mw-content-text"]/table[2]/tr[{}]/td[1]/@data-sort-value'.format(idx))[0]
        champ.get_info(tree, idx)

    # Get dates for champions who received a complete VGU (pulled from League of Legends wiki) who are described as
    # getting a 'Full relaunch'
    wiki_update_page = requests.get('https://leagueoflegends.fandom.com/wiki/Champion_updates')
    tree = html.fromstring(wiki_update_page.content)
    i = 2
    while True:
        try:
            update_desc = tree.xpath('//*[@id="mw-content-text"]/table[2]/tr[{}]/td[2]/a'.format(i))[0].text.strip()
        except IndexError:
            break

        if 'Full Relaunch' in update_desc:
            champ_name = tree.xpath('//*[@id="mw-content-text"]/table[2]/tr[{}]/td[1]/@data-sort-value'.format(i))[0]
            date = tree.xpath('//*[@id="mw-content-text"]/table[2]/tr[{}]/td[3]'.format(i))[0].text
            if date.strip().startswith('20'):
                champ = next(c for c in champions if c.name == champ_name)
                champ.set_vgu_info(date.strip()[:4])
            else:
                break
        i += 1

    # Correction: Aatrox got a full relaunch in 2018 and Morgana only got a visual upgrade in 2019, not a full relaunch
    aatrox = next(c for c in champions if c.name == 'Aatrox')
    aatrox.vgu = '2018'
    morgana = next(c for c in champions if c.name == 'Morgana')
    morgana.vgu = morgana.release_

    # Information is classified and saved in a .csv file
    with open('champions.csv', 'w') as f:
        data_writer = csv.writer(f, dialect='excel')
        data_writer.writerow(['Champion', 'First Skill Maxed', 'Second Skill Maxed', 'Third Skill Maxed',
                              'Skill Priority', 'LVL 1 Skill', 'Class', 'Subclass', 'Release Date',
                              'Release Date (VGU)'])
        for champ in champions:
            data_writer.writerow([champ.name, champ.skill_order[0], champ.skill_order[1], champ.skill_order[2],
                                  ''.join(champ.skill_order), champ.lvl_1, champ.class_, champ.subclass,
                                  champ.release_, champ.vgu])


if __name__ == "__main__":
    main()
