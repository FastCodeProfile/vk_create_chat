import asyncio
import json
import random
from contextlib import suppress

import aiohttp
from loguru import logger


class VkApi:
    def __init__(self, token: str):
        self.host = 'https://api.vk.com/method/'
        self.params = {'v': 5.131}
        self.headers = {'Authorization': f"Bearer {token}"}

    async def create_chat(self, user_id: int, title: str) -> tuple[bool, str]:
        method = 'messages.createChat'
        self.params["title"] = title
        self.params["user_ids"] = user_id
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(self.host + method, params=self.params) as response:
                json_response = await response.json()
                return 'error' not in json_response


def load_data(filename: str) -> dict:
    with open(filename, encoding='utf-8') as file:
        return json.load(file)


async def main():
    title = input('Введите желаемое название беседы: ')
    data = load_data('data.json')
    main_user = data.pop("0")
    while True:
        for key, user in data.items():
            vk_api = VkApi(user["access_token"])
            result = await vk_api.create_chat(main_user["user_id"], title)
            if result:
                logger.success(f'Беседа "{title}" создана - {user["url_profile"]}')
            else:
                logger.error(f'Возникла проблема - {user["url_profile"]}')
                logger.warning('Используйте скрипт, что бы отсеять невалидные аккаунты. '
                               'Ссылка на скрипт: https://github.com/FastCodeProfile/vk_check_token.git')
            await asyncio.sleep(random.randint(5, 10))


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
