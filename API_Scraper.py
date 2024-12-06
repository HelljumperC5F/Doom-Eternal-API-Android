import os
import requests
import json
import subprocess
from bs4 import BeautifulSoup
from bs4.element import Tag

KEY_VALUES = {
    'name': 'hp',
    'speed': 'speed',
    'description': 'class',
    'rank': 'rank',
}


class Enemy:
    def __init__(self, name, hp, speed, description, rank, image):
        self.name = name
        self.hp = hp
        self.speed = speed
        self.description = description
        self.rank = rank
        self.image = image

    def __str__(self):
        message = ''
        for key, value in self.__dict__.items():
            message += f'{key}: {value}\n'
        return message


def scrap_enemy(url):
    response = requests.get(url)

    enemy = Enemy('', '', '', '', '', '')
    soup = BeautifulSoup(response.text, 'html.parser')
    enemy.name = soup.find('h2', attrs={'data-source': 'name'}).contents[0]

    element = soup.find('div', attrs={'data-source': 'hp'})
    if element is not None:
        enemy.hp = element.div.contents[0]
    element = soup.find('div', attrs={'data-source': 'speed'})
    if element is not None:
        enemy.speed = element.div.contents[0]
    element = soup.find('div', attrs={'data-source': 'class'})
    if element is not None:
        enemy.description = element.div.contents[0]
    element = soup.find('div', attrs={'data-source': 'type'})
    if element is not None:
        rank = element.div.contents[0]
        if type(rank) is Tag:
            rank = rank.contents[0]
        enemy.rank = rank
    else:
        element = soup.find('div', attrs={'data-source': 'rank'})
        if element is not None:
            rank = element.div.contents[0]
            if type(rank) is Tag:
                rank = rank.contents[0]
            enemy.rank = rank
    element = soup.find('figure', attrs={'data-source': 'image'})
    if element is not None:
        enemy.image = element.a['href']
    else:
        element = soup.find('div', attrs={'data-source': 'image'})
        if element is not None:
            enemy.image = element.find('a')['href']

    img_command = f'curl --silent --output - {enemy.image} | wezterm imgcat --height 25%'
    subprocess.run(img_command, shell=True)
    print(enemy)

    for key, value in enemy.__dict__.items():
        if value == '':
            new_value = input(f'{key}: ')
            setattr(enemy, key, new_value)

    cwd = os.getcwd()
    enemy_dir_path = os.path.join(cwd, 'Enemies')
    if not os.path.exists(enemy_dir_path):
        os.makedirs(enemy_dir_path)

    enemy_file_path = os.path.join(enemy_dir_path, f'{enemy.name}.txt')
    with open(enemy_file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(enemy.__dict__))


urls = [
    # 'https://doom.fandom.com/wiki/Cyberdemon/Doom_Eternal',
    # 'https://doom.fandom.com/wiki/Buff_Totem',
    # 'https://doom.fandom.com/wiki/Cueball',
    # 'https://doom.fandom.com/wiki/Tentacle',
    # 'https://doom.fandom.com/wiki/Gargoyle_(Doom_Eternal)',
    # 'https://doom.fandom.com/wiki/Imp_(Doom_Eternal)',
    # 'https://doom.fandom.com/wiki/Lost_Soul_(Doom_Eternal)',
    # 'https://doom.fandom.com/wiki/Mecha_Zombie',
    # 'https://doom.fandom.com/wiki/Soldier',
    # 'https://doom.fandom.com/wiki/Zombie_(Doom_Eternal)',
    # 'https://doom.fandom.com/wiki/Arachnotron_(Doom_Eternal)',
    # 'https://doom.fandom.com/wiki/Cacodemon_(Doom_Eternal)',
    # 'https://doom.fandom.com/wiki/Carcass',
    # 'https://doom.fandom.com/wiki/Cyber-Mancubus/Doom_Eternal',
    # 'https://doom.fandom.com/wiki/Dread_Knight',
    # 'https://doom.fandom.com/wiki/Hell_Knight_(Doom_Eternal)',
    # 'https://doom.fandom.com/wiki/Maykr_Drone',
    # 'https://doom.fandom.com/wiki/Mancubus_(Doom_Eternal)',
    # 'https://doom.fandom.com/wiki/Pain_Elemental_(Doom_Eternal)',
    # 'https://doom.fandom.com/wiki/Pinky_(Doom_Eternal)',
    # 'https://doom.fandom.com/wiki/Prowler/Doom_Eternal',
    # 'https://doom.fandom.com/wiki/Revenant_(Doom_Eternal)',
    # 'https://doom.fandom.com/wiki/Spectre/Doom_Eternal',
    # 'https://doom.fandom.com/wiki/Whiplash',
    # 'https://doom.fandom.com/wiki/Arch-vile/Doom_Eternal',
    # 'https://doom.fandom.com/wiki/Baron_of_Hell_(Doom_Eternal)',
    # 'https://doom.fandom.com/wiki/Doom_Hunter',
    # 'https://doom.fandom.com/wiki/Marauder',
    # 'https://doom.fandom.com/wiki/Tyrant',
    # 'https://doom.fandom.com/wiki/Doom_Hunter',
    # 'https://doom.fandom.com/wiki/Marauder',
    # 'https://doom.fandom.com/wiki/The_Gladiator',
    # 'https://doom.fandom.com/wiki/Khan_Maykr',
    # 'https://doom.fandom.com/wiki/Icon_of_Sin/Doom_Eternal',
]
for url in urls:
    scrap_enemy(url)

# with open('./soup.html', 'w', encoding='utf-8') as file:
#     file.write(str(soup))
