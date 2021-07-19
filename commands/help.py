import json

with open('./botconfig.json', 'r', encoding='utf-8') as json_file:
    BOT_CONFIG = json.load(json_file)
commands: str = 'Список доступных команд:\n'

for index, command in enumerate(BOT_CONFIG['intents']['commands']):
    commands += f'{index + 1}) {command}\n'

print(commands)
