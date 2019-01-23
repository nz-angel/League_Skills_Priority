from time import sleep
from random import choice
import csv
import requests
import json
from lxml import html


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


general_data = json.loads(requests.get('https://ddragon.leagueoflegends.com/realms/na.json').content)
patch = general_data['v']

ddragon_url = 'http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'.format(patch)
champion_data = json.loads(requests.get(ddragon_url).content)
champions = [x for x in champion_data['data'].keys()]

skill_priority = {champ: [] for champ in champions}
first_lvl_skill = {champ: [] for champ in champions}
champion_class = {champ: champion_data['data'][champ]['tags'][0] for champ in champions}
wait_time = [1.5, 2]

for c in champions:
    page = requests.get('https://champion.gg/champion/'+c)
    tree = html.fromstring(page.content)
    skill_priority[c], first_lvl_skill[c] = get_skill_order(tree)
    sleep(choice(wait_time))

with open('champions.csv', 'w') as f:
    data_writer = csv.writer(f, dialect='excel')
    data_writer.writerow(['Champion', 'First Skill Maxed', 'Second Skill Maxed', 'Third Skill Maxed',
                          'First Skill', 'Skill Priority', 'Main Class'])
    for c in champions:
        data_writer.writerow([c, skill_priority[c][0], skill_priority[c][1], skill_priority[c][2],
                              first_lvl_skill[c], ''.join(skill_priority[c]), champion_class[c]])

