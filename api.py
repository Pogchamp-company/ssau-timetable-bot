import re

from aiohttp import ClientSession, ClientTimeout
import asyncio

from bs4 import BeautifulSoup


class SsauAPI:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'
    }

    def __init__(self):
        self.host = 'https://ssau.ru'

    async def _request(self, url: str, tries_count=10):
        async with ClientSession(timeout=ClientTimeout(total=500), headers=self.HEADERS) as session:
            status = None
            while status != 200:
                if tries_count == 0:
                    raise ConnectionError('Не удалось получить данные')
                async with session.get(f'{self.host}{url}') as response:
                    status = response.status
                    if status != 200:
                        await asyncio.sleep(.5)
                        tries_count -= 1
                        continue
                    return await response.text()

    async def get_institutes_and_faculties(self):
        page = await self._request('/rasp')
        soup = BeautifulSoup(page, features='html.parser')
        return {item.a.text.strip(): int(re.search(r'\d+', item.a.attrs['href']).group())
                for item in soup.find_all('div', class_='faculties__item')}

    async def get_group_id_by(self, faculty: int, course: int, group_code: str):
        page = await self._request(f'/rasp/faculty/{faculty}?course={course}')

