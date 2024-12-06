import os
import requests
import json
import subprocess
from bs4 import BeautifulSoup
from bs4.element import Tag

KEY_VALUES = {
    'name': 'name',
    'weapon_type': 'weapon_type',
    'fire_mode': 'fire_mode',
    'location': 'location',
}


class Weapon:
    def __init__(self, name, weapon_type, fire_mode, location, damage, ammo_type, image):
        self.name = name
        self.weapon_type = weapon_type
        self.fire_mode = fire_mode
        self.location = location
        self.damage = damage
        self.ammo_type = ammo_type
        self.image = image

    def __str__(self):
        message = ''
        for key, value in self.__dict__.items():
            message += f'{key}: {value}\n'
        return message


def scrap_weapon(url):
    response = requests.get(url)
    weapon = Weapon('', '', '', '', '', '', '')
    soup = BeautifulSoup(response.text, 'html.parser')

    with open('./soup.html', 'w', encoding='utf-8') as file:
        print('writing...')
        file.write(str(soup))

    weapon.name = soup.find('h2', attrs={'data-source': 'title'}).contents[0]

    element = soup.find('div', attrs={'data-source': 'weapon_type'})
    if element is not None:
        if type(element.div.contents[0]) is Tag:
            weapon.weapon_type = element.div.contents[0].contents[0]
            print('weapon_type:', weapon.weapon_type)
        else:
            weapon.weapon_type = element.div.contents[0]
            print('weapon_type:', weapon.weapon_type)

    element = soup.find('div', attrs={'data-source': 'fire_mode'})
    if element is not None:
        weapon.fire_mode = element.div.contents[0]
        print('fire_mode:', weapon.fire_mode)

    element = soup.find('div', attrs={'data-source': 'location'})
    if element is not None:
        if type(element.div.contents[0]) is Tag:
            weapon.location = element.div.contents[0].contents[0]
            print('location:', weapon.location)
        else:
            weapon.location = element.div.contents[0]
            print('location:', weapon.location)

    element = soup.find('div', attrs={'data-source': 'ammo_type'})
    if element is not None:
        if type(element.div.contents[0]) is Tag:
            weapon.ammo_type = element.div.contents[0].contents[0]
            print('ammo_type:', weapon.ammo_type)
        else:
            weapon.ammo_type = element.div.contents[0]
            print('ammo_type:', weapon.ammo_type)

    element = soup.find('div', attrs={'data-source': 'damage'})
    if element is not None:
        weapon.damage = element.contents[0]
        print('damage:', weapon.damage)

    element = soup.find('figure', attrs={'data-source': 'image'})
    if element is not None:
        weapon.image = element.a['href']
        print('image:', weapon.image)

    img_command = f'curl --silent --output - {weapon.image} | wezterm imgcat --height 25%'
    subprocess.run(img_command, shell=True)
    # print(weapon)

    for key, value in weapon.__dict__.items():
        if value == '':
            new_value = input(f'{key}: ')
            setattr(weapon, key, new_value)

    cwd = os.getcwd()
    weapon_dir_path = os.path.join(cwd, 'Weapons')
    if not os.path.exists(weapon_dir_path):
        os.makedirs(weapon_dir_path)

    weapon_file_path = os.path.join(weapon_dir_path, f'{weapon.name}.txt')
    with open(weapon_file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(weapon.__dict__))


urls = [
    # Maybe later
    # 'https://doom.fandom.com/wiki/Meat_Hook',

    # 'https://doom.fandom.com/wiki/Ballista',
    # 'https://doom.fandom.com/wiki/BFG9000/Doom_Eternal',
    # 'https://doom.fandom.com/wiki/Heavy_Cannon',
    # 'https://doom.fandom.com/wiki/Chaingun/Doom_Eternal',
    # 'https://doom.fandom.com/wiki/Chainsaw/Doom_Eternal',
    # 'https://doom.fandom.com/wiki/Combat_Shotgun/Doom_Eternal',
    # 'https://doom.fandom.com/wiki/Crucible',
    # 'https://doom.fandom.com/wiki/Plasma_gun/Doom_Eternal',
    # 'https://doom.fandom.com/wiki/Doomblade',
    # 'https://doom.fandom.com/wiki/Rocket_launcher/Doom_Eternal',
    # 'https://doom.fandom.com/wiki/Sentinel_Hammer',
    'https://doom.fandom.com/wiki/Super_shotgun/Doom_Eternal',
    # 'https://doom.fandom.com/wiki/Equipment_Launcher',
    'https://doom.fandom.com/wiki/Unmaker/Doom_Eternal',
]
for url in urls:
    scrap_weapon(url)
