import requests

class Pokemon:
    def __init__(self, name, image, types=None, stats=None, abilities=None, height=None, weight=None):
        self.name = name
        self.image = image
        self.types = types or []
        self.stats = stats or {}
        self.abilities = abilities or []
        self.height = height
        self.weight = weight

    def fetch_data_from_api(self, name):
        url = f'https://pokeapi.co/api/v2/pokemon/{name.lower()}'
        response = requests.get(url)
        data = response.json()
        
        self.name = data['name']
        self.image = data['sprites']['front_default']
        self.types = [t['type']['name'] for t in data['types']]
        self.stats = {s['stat']['name']: s['base_stat'] for s in data['stats']}
        self.abilities = [a['ability']['name'] for a in data['abilities']]
        self.height = data['height']
        self.weight = data['weight']

    def set_name(self, name):
        self.name = name

    def set_image(self, image):
        self.image = image

    def set_types(self, types):
        self.types = types

    def set_stats(self, stats):
        self.stats = stats

    def set_abilities(self, abilities):
        self.abilities = abilities

    def set_height(self, height):
        self.height = height

    def set_weight(self, weight):
        self.weight = weight

    def get_info(self):
        return {
            'name': self.name,
            'image': self.image,
            'types': self.types,
            'stats': self.stats,
            'abilities': self.abilities,
            'height': self.height,
            'weight': self.weight
        }
        from aiogram import Bot, Dispatcher, executor, types
from pokemon import Pokemon

API_TOKEN = 'YOUR_BOT_API_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm the Pokemon bot. Send me a Pokemon name to get its details.")

@dp.message_handler(commands=['pokemon'])
async def send_pokemon_info(message: types.Message):
    pokemon_name = message.get_args().strip()
    if not pokemon_name:
        await message.reply("Please provide a Pokemon name.")
        return
    
    try:
        pokemon = Pokemon(name=pokemon_name, image='')
        pokemon.fetch_data_from_api(pokemon_name)
        info = pokemon.get_info()
        
        response = f"Name: {info['name']}\n" \
                   f"Types: {', '.join(info['types'])}\n" \
                   f"Height: {info['height']}\n" \
                   f"Weight: {info['weight']}\n" \
                   f"Abilities: {', '.join(info['abilities'])}\n" \
                   f"Stats: {info['stats']}\n"
        
        await message.reply_photo(photo=info['image'], caption=response)
    except Exception as e:
        await message.reply("Failed to fetch data for this Pokemon. Please check the name and try again.")

if __name__ == '__main__':
    executor.start_polling(dp)
