from time import sleep
import requests
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from random import choice
from lxml import html


def get_champions():
    tri = 0
    while True:
        try:
            page = requests.get('https://na.leagueoflegends.com/en/game-info/champions/')
            break
        except requests.exceptions.ConnectionError:
            tri += 1
            if tri % 50 == 0:
                print(tri)
            pass
    tree = html.fromstring(page.content)
    champ_names = tree.xpath('//*[@class="champ-name"]')
    for name in champ_names:
        print(name.find('a').text)
    print(champ_names)


def get_skill_order(t):
    level_max = {1: 0, 2: 0, 3: 0}
    skill_id = {1: 'Q', 2: 'W', 3: 'E'}
    for level in range(1, 19):
        for skill in level_max.keys():
            sq = t.cssselect(
                'div.skill-order:nth-child(2) > div:nth-child({}) > div:nth-child(2) > div:nth-child({})'
                .format(skill+1, level))
            if sq[0].attrib['class'] != '':
                level_max[skill] = level
    ls_tmp = sorted(level_max.keys(), key=lambda x: level_max[x])
    return [skill_id[x] for x in ls_tmp]


# champions = get_champions()
champions = ['Ahri', 'Jinx', 'Lux', 'Nasus', 'Singed', 'Jax']
skill_priority = {champ: [] for champ in champions}
wait_time = [1.5, 2, 2.5, 3]

for c in champions:
    page = requests.get('https://champion.gg/champion/'+c)
    tree = html.fromstring(page.content)
    skill_priority[c] = get_skill_order(tree)
    sleep(choice(wait_time))
print(skill_priority)
