from time import sleep
from random import choice
import csv
import requests
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


champions = ['Aatrox', 'Ahri', 'Akali', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Ashe', 'Aurelionsol', 'Azir', 'Bard',
             'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Darius', 'Diana',
             'Draven', 'Drmundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio',
             'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern',
             'Janna', 'Jarvaniv', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Karma', 'Karthus', 'Kassadin',
             'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred', 'Kled', 'Kogmaw', 'Leblanc', 'Leesin', 'Leona',
             'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'Masteryi', 'Missfortune',
             'Monkeyking', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nocturne',
             'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Quinn', 'Rakan', 'Rammus', 'Reksai',
             'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Sejuani', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion',
             'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Syndra', 'Tahmkench', 'Taliyah', 'Talon', 'Taric', 'Teemo',
             'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'Twistedfate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne',
             'Veigar', 'Velkoz', 'Vi', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'Xinzhao',
             'Yasuo', 'Yorick', 'Zac', 'Zed', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']

skill_priority = {champ: [] for champ in champions}
first_lvl_skill = {champ: [] for champ in champions}
wait_time = [1.5, 2]

for c in champions:
    page = requests.get('https://champion.gg/champion/'+c)
    tree = html.fromstring(page.content)
    skill_priority[c], first_lvl_skill[c] = get_skill_order(tree)
    sleep(choice(wait_time))

with open('champions.csv', 'w') as f:
    data_writer = csv.writer(f, dialect='excel')
    data_writer.writerow(['Champion', 'First Skill Maxed', 'Second Skill Maxed', 'Third Skill Maxed',
                          'First Skill', 'Skill Order'])
    for c in champions:
        data_writer.writerow([c, skill_priority[c][0], skill_priority[c][1], skill_priority[c][2],
                              first_lvl_skill[c], ''.join(skill_priority[c])])

