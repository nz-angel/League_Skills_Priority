from time import sleep
from random import choice
import csv
import requests
import json
from lxml import html
from tqdm import tqdm


def get_skill_order(t):
    level_max = {1: 0, 2: 0, 3: 0}
    first_skill = 0
    skill_id = {1: 'Q', 2: 'W', 3: 'E'}
    for level in range(1, 19):
        for skill in level_max.keys():
            sq = t.cssselect(
                'div.skill-order:nth-child(2) > div:nth-child({}) > div:nth-child(2) > div:nth-child({})'
                .format(skill+1, level))
            if sq[0].attrib['class'] != '':
                level_max[skill] = level
                if level == 1:
                    first_skill = skill_id[skill]
    ls_tmp = sorted(level_max.keys(), key=lambda x: level_max[x])
    return [skill_id[x] for x in ls_tmp], first_skill


def main():

    # Latest patch is pulled from Riot's static data
    general_data = json.loads(requests.get('https://ddragon.leagueoflegends.com/realms/na.json').content)
    patch = general_data['v']

    # Information on champions for the lastest patch is pulled from Riot's static data
    ddragon_url = 'http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'.format(patch)
    champion_data = json.loads(requests.get(ddragon_url).content)
    champions = [x for x in champion_data['data'].keys()]

    # Skill leveling priority is pulled from champion.gg
    skill_priority = {champ: [] for champ in champions}
    first_lvl_skill = {champ: [] for champ in champions}
    wait_time = [1.5, 2]

    for c in tqdm(champions):
        page = requests.get('https://champion.gg/champion/'+c)
        tree = html.fromstring(page.content)
        skill_priority[c], first_lvl_skill[c] = get_skill_order(tree)
        sleep(choice(wait_time))
    wu_values = (skill_priority.pop('MonkeyKing'), first_lvl_skill.pop('MonkeyKing'))
    champions.remove('MonkeyKing')
    champions.append('Wukong')
    champions.sort()
    skill_priority['Wukong'] = wu_values[0]
    first_lvl_skill['Wukong'] = wu_values[1]

    # Get class, subclass and release date of every champion (pulled from League of Legends wiki)
    champion_rd = {champ: 2019 for champ in champions}
    champion_class = {champ: 0 for champ in champions}
    champion_subclass = {champ: 0 for champ in champions}
    subclass_belonging = {'Enchanter': 'Controller',
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
    wiki_class_page = requests.get('https://leagueoflegends.fandom.com/wiki/List_of_champions')
    tree = html.fromstring(wiki_class_page.content)
    for idx in range(2, len(champions)+2):
        # champ = tree.xpath('//*[@id="mw-content-text"]/table[2]/tr[{}]/td[1]/@data-sort-value'.format(idx))[0]
        champ = champions[idx-2]
        subclass = tree.xpath('//*[@id="mw-content-text"]/table[2]/tr[{}]/td[2]/@data-sort-value'.format(idx))[0]
        release_date = tree.xpath('//*[@id="mw-content-text"]/table[2]/tr[{}]/td[4]'.format(idx))[0].text
        if release_date == ' ':
            release_date = tree.xpath('//*[@id="mw-content-text"]/table[2]/tr[{}]/td[4]/span'.format(idx))[0].text

        champion_subclass[champ] = subclass
        champion_class[champ] = subclass_belonging[subclass]
        champion_rd[champ] = release_date.strip()[:4]

    # Get dates for champions who received a complete VGU (pulled from League of Legends wiki) who are described as
    # getting a 'Full relauch'
    champion_full_vgu = {champ: champion_rd[champ] for champ in champions}
    wiki_update_page = requests.get('https://leagueoflegends.fandom.com/wiki/Champion_updates')
    tree = html.fromstring(wiki_update_page.content)
    i = 2
    while True:
        try:
            update_desc = tree.xpath('//*[@id="mw-content-text"]/table[2]/tr[{}]/td[2]/a'.format(i))[0].text.strip()
        except IndexError:
            break

        if 'Full Relaunch' in update_desc:
            champ = tree.xpath('//*[@id="mw-content-text"]/table[2]/tr[{}]/td[1]/@data-sort-value'.format(i))[0]
            date = tree.xpath('//*[@id="mw-content-text"]/table[2]/tr[{}]/td[3]'.format(i))[0].text
            if date.strip().startswith('20'):
                champion_full_vgu[champ] = date.strip()[:4]
        i += 1
    champion_full_vgu['Aatrox'] = 2018  # Aatrox received a full VGU in 2018 but the Wiki only has 'VGU'

    # Information is classified and saved in a .csv file
    with open('champions.csv', 'w') as f:
        data_writer = csv.writer(f, dialect='excel')
        data_writer.writerow(['Champion', 'First Skill Maxed', 'Second Skill Maxed', 'Third Skill Maxed',
                              'First Skill', 'Skill Priority', 'Class', 'Subclass', 'Release Date', 'Release Date (VGU)'])
        for c in champions:
            data_writer.writerow([c, skill_priority[c][0], skill_priority[c][1], skill_priority[c][2],
                                  first_lvl_skill[c], ''.join(skill_priority[c]), champion_class[c],
                                  champion_subclass[c], champion_rd[c], champion_full_vgu[c]])


if __name__ == "__main__":
    main()
