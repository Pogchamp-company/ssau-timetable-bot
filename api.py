import re
from datetime import datetime

from aiohttp import ClientSession, ClientTimeout
import asyncio

from bs4 import BeautifulSoup


class SsauAPI:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'
    }
    HOST = 'https://ssau.ru'

    async def _request(self, url: str, tries_count=10):
        async with ClientSession(timeout=ClientTimeout(total=500), headers=self.HEADERS) as session:
            status = None
            while status != 200:
                if tries_count == 0:
                    raise ConnectionError('Не удалось получить данные')
                async with session.get(f'{self.HOST}{url}') as response:
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

    async def get_groups(self, faculty: int, course: int):
        page = await self._request(f'/rasp/faculty/{faculty}?course={course}')
        soup = BeautifulSoup(page, features='html.parser')
        return [int(re.search(r'\d+', container.attrs['href']).group())
                  for container in soup.find_all('a', class_='group-catalog__group')]

    async def get_timetable_by(self, group_id: int, week: int):
        page = await self._request(f'/rasp?groupId={group_id}&selectedWeek={week}')
        soup = BeautifulSoup(page, features='html.parser')
        raw_table = soup.find('div', class_='schedule__items')

        table = []

        for cell in raw_table.find_all('div', class_='schedule__item'):
            pass
            # if 'schedule__head' in cell.attrs['class']:
            #     date_container = cell.find('div', class_='schedule__head-date')
            #     if date_container:
            #         table[datetime.strptime(date_container.text, '%d.%m.%Y').date()] = []
