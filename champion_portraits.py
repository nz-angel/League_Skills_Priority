import requests
import json
import urllib.request
import os


# Latest patch is pulled from Riot's static data
general_data = json.loads(requests.get('https://ddragon.leagueoflegends.com/realms/na.json').content)
patch = general_data['v']

# Information on champions for the latest patch is pulled from Riot's static data
ddragon_url = 'http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'.format(patch)
champion_data = json.loads(requests.get(ddragon_url).content)
champions = [x for x in champion_data['data'].keys()]

# Create directory for the images if it doesn't exist
img_dir = os.path.join(os.getcwd(), 'Champion portraits')
if not os.path.exists(img_dir):
    os.mkdir(img_dir)

# Save square image for each champion
for champ in champions:
    ddragon_img_url = 'http://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}.png'.format(patch, champ)
    img_path = os.path.join(img_dir, '{}.png'.format(champ))
    urllib.request.urlretrieve(ddragon_img_url, img_path)
