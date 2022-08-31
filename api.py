import asyncio
import re
from datetime import datetime

from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup

from structs import ScheduleForTheDay, Lesson


class SsauAPI:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'
    }
    HOST = 'https://ssau.ru'

    async def _request(self, url: str, tries_count=10) -> str:
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

    async def get_institutes_and_faculties(self) -> dict[str, int]:
        page = await self._request('/rasp')
        soup = BeautifulSoup(page, features='html.parser')
        return {item.a.text.strip(): int(re.search(r'\d+', item.a.attrs['href']).group())
                for item in soup.find_all('div', class_='faculties__item')}

    async def get_groups(self, faculty: int, course: int) -> dict[str, int]:
        page = await self._request(f'/rasp/faculty/{faculty}?course={course}')
        soup = BeautifulSoup(page, features='html.parser')
        return {container.text.strip(): int(re.search(r'\d+', container.attrs['href']).group())
                for container in soup.find_all('a', class_='group-catalog__group')}

    async def get_timetable_by(self, group_id: int, week: int) -> list[ScheduleForTheDay]:
        page = await self._request(f'/rasp?groupId={group_id}&selectedWeek={week}')
        soup = BeautifulSoup(page, features='html.parser')
        raw_table = soup.find('div', class_='schedule__items')

        cells = iter(raw_table.find_all('div', class_='schedule__item'))
        time = [next(cells).text.strip()]
        table = [[] for _ in range(6)]
        for i, cell in enumerate(cells):
            table[i % 6].append(cell)

        time.extend([tuple(t.text.strip() for t in cell.find_all('div', class_='schedule__time-item'))
                     for cell in raw_table.find_all('div', class_='schedule__time')])

        timetable = []

        for day in table:
            day = iter(day)
            title = next(day)
            date_container = title.find('div', class_='schedule__head-date')
            date = datetime.strptime(date_container.text.strip(), '%d.%m.%Y').date()
            lessons = []
            for i, raw_lesson in enumerate(day, start=1):
                if not raw_lesson.text:
                    break
                start, end = time[i]
                place = raw_lesson.find('div', class_='schedule__place').text.strip()

                lessons.append(Lesson(
                    title=raw_lesson.find('div', class_='schedule__discipline').text.strip(),
                    is_online='online' in ''.join(filter(str.isalpha, place)).lower(),
                    place=place,
                    teacher=raw_lesson.find('div', class_='schedule__teacher').a.text.strip(),
                    groups=[c.text.strip() for c in
                            raw_lesson.find('div', class_='schedule__groups').find_all(class_='caption-text')],
                    start=start,
                    end=end
                ))
            timetable.append(ScheduleForTheDay(date=date,
                                               lessons=lessons))

        return timetable
