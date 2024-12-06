from flask import Flask, jsonify, abort
import json
import os

app = Flask(__name__)

json_enemy_data = {}
json_weapon_data = {}


def load_json_enemy_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            loaded_json = json.load(file)
            api_name = loaded_json['name'].lower().replace(' ', '_')
            json_enemy_data[api_name] = loaded_json
    else:
        abort(404, description=f"File not found: {file_path}")


def load_json_weapon_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            loaded_json = json.load(file)
            api_name = loaded_json['name'].lower().replace(' ', '_')
            json_weapon_data[api_name] = loaded_json
    else:
        abort(404, description=f"File not found: {file_path}")


@app.route('/demons')
def get_all_enemies():
    return jsonify(list(json_enemy_data.keys()))


@app.route('/demons/<path:name>')
def get_enemy(name):
    name = name.lower()
    if name in json_enemy_data:
        return jsonify(json_enemy_data[name])
    else:
        abort(404, description=f"Enemy {name} not on API")


@app.route('/weapons')
def get_all_wepons():
    return jsonify(list(json_weapon_data.keys()))


@app.route('/weapons/<path:name>')
def get_weapon(name):
    name = name.lower()
    if name in json_weapon_data:
        return jsonify(json_weapon_data[name])
    else:
        abort(404, description=f"Weapon {name} not on API")


if __name__ == '__main__':
    json_enemy_files = os.listdir('./Enemies')
    for file in json_enemy_files:
        load_json_enemy_file(os.path.join(os.getcwd(), 'Enemies', file))

    json_weapon_files = os.listdir('./Weapons')
    for file in json_weapon_files:
        load_json_weapon_file(os.path.join(os.getcwd(), 'Weapons', file))

    from waitress import serve
    serve(app, host='0.0.0.0', port=80)
    # app.run(debug=True)
