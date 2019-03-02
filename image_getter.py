import requests
import json
import urllib.request
import os


def get_champion_portraits(img_dir=os.path.join(os.getcwd(), 'Champion portraits')):
    # Latest patch is pulled from Riot's static data
    general_data = json.loads(requests.get('https://ddragon.leagueoflegends.com/realms/na.json').content)
    patch = general_data['v']

    # Information on champions for the latest patch is pulled from Riot's static data
    ddragon_url = 'http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'.format(patch)
    champion_data = json.loads(requests.get(ddragon_url).content)
    champions = [x for x in champion_data['data'].keys()]

    # Create directory for the images if it doesn't exist
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    # Save square image for each champion
    for champ in champions:
        ddragon_img_url = 'http://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png'.format(patch, champ)
        img_path = os.path.join(img_dir, '{}.png'.format(champ))
        urllib.request.urlretrieve(ddragon_img_url, img_path)


def get_spell_icons(img_dir=os.path.join(os.getcwd(), 'Spell icons'), N=15):
    # Latest patch is pulled from Riot's static data
    general_data = json.loads(requests.get('https://ddragon.leagueoflegends.com/realms/na.json').content)
    patch = general_data['v']

    # Information on champions for the latest patch is pulled from Riot's static data
    ddragon_url = 'http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'.format(patch)
    champion_data = json.loads(requests.get(ddragon_url).content)
    champions = [x for x in champion_data['data'].keys()]

    # Create directory for the icons of spells if it doesn't exist
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    # Save images of champion abilities up to the Nth champion
    for champ in champions[:N]:
        ddragon_champ_url = 'http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion/{}.json'.format(patch, champ)
        full_champion_data = json.loads(requests.get(ddragon_champ_url).content)

        for spell in range(3):
            spell_name = full_champion_data['data'][champ]['spells'][spell]['image']['full']
            spell_img_url = 'http://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}'.format(patch, spell_name)
            spell_img_path = os.path.join(img_dir, '{}_{}.png'.format(champ, spell))
            urllib.request.urlretrieve(spell_img_url, spell_img_path)


get_spell_icons(N=30)