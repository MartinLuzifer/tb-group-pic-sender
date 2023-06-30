import logging
import random
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from conf import BOT_TOKEN

API_TOKEN = BOT_TOKEN
logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

HEADERS = {
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Language': 'en-US,en;q=0.5',
    # 'Upgrade-Insecure-Requests': '1',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'RaccoonMartin/e621_test'
}


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(
        text="list command:\n"
             "\n"
             "/start - list commands\n"
             "/help - list commands\n"
             "\n"
             "/meow - get kitty\n"
             "/bark - get doggy\n"
             "/vulpes - get foxy\n"
             "/621 <em>tags count</em> - get pictures from <code>e621.net</code>",
        parse_mode="HTML"
    )


@dp.message_handler(commands=['meow'])
async def send_meow(message: types.Message):
    await message.reply("🐱 MEOW")

    meow_url = 'https://meow.senither.com/v1/random'

    response = requests.get(url=meow_url)
    print(f'INFO:requests.get():get object {response.text}')
    url = response.json()['data']['url']

    await message.answer_photo(url)


@dp.message_handler(commands=['bark'])
async def send_bark(message: types.Message):
    await message.reply("🐶 BARK")

    woof_url = 'https://random.dog/woof.json'
    response = requests.get(url=woof_url)
    url = response.json()['url']

    await message.answer_photo(url)


@dp.message_handler(commands=['vulpes'])
async def send_vulpes(message: types.Message):
    await message.reply("🦊 фыр")

    vulpes_url = 'https://randomfox.ca/floof/'
    response = requests.get(url=vulpes_url)
    url = response.json()['link']

    await message.answer_photo(url)


@dp.message_handler(commands=['621'])
async def send_link_e621(message: types.Message):

    # GET TAG
    image_tag = str(message.text.split(sep=" ")[1])

    # GET IMAGE COUNT FOR answer_media_group
    try:
        image_count = int(message.text.split(sep=" ")[2])
        if image_count > 9:
            await message.reply(text='не могу отправить больше 9,\nбудет отправлено 9')
            raise IndexError
    except IndexError:
        image_count = 9

    # GET RESPONSE FROM SITE
    data = requests.get(
        # https://e621.net/posts.json?tags=tinydeerguy+deer+rating:s+type:jpg&limit=320 (320 it's max number on API)
        url=f'https://e621.net/posts.json?'
            f'tags=type:png+type:jpg+rating:s+'
            f'{image_tag}&'
            f'limit=320&',
        headers=HEADERS,
        auth=(
            'Martin luzifer',
            '5JYLPJv7fp3LkjdfkAFA6hY4'
        )
    ).json()

    # GET ALL POSTS COUNT
    all_posts_count = len(data.get("posts"))

    # SEND IMAGES IN GROUP MEDIA
    images = []
    for i in range(1, image_count):
        current_post = random.randint(1, all_posts_count)
        images.append(types.InputMediaPhoto(data.get('posts')[current_post]['file']['url']))
    await message.answer_media_group(images)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
