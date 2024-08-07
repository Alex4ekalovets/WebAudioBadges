import json
import os.path
import re
import time
from datetime import datetime
from itertools import islice
from multiprocessing import Process
from threading import Thread
from typing import Iterable, Any

import requests
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

LOGIN_DATA = {"username": "60@zoloto55.ru", "password": "MC3twWrz"}
THREAD_COUNT = 8


def register(driver: WebDriver) -> requests.Session:
    driver.get("https://qa-lk.voca.tech")

    driver.find_element(by=By.ID, value="UserName").send_keys(LOGIN_DATA["username"])
    driver.find_element(by=By.ID, value="RememberMe").click()

    password = driver.find_element(by=By.ID, value="Password")
    password.send_keys(LOGIN_DATA["password"])
    password.send_keys(Keys.ENTER)

    time.sleep(5)

    s = requests.Session()

    for cookie in driver.get_cookies():
        s.cookies.set(cookie['name'], cookie['value'])

    return s


def get_page_count(session: requests.Session, period: str = "Yesterday") -> int:
    url = (f"https://qa-lk.voca.tech/monitoring/audio/records"
           f"?period={period}&state=Any&duration=AnyDuration")
    r = session.get(url)

    html = r.content

    soup = BeautifulSoup(html, "lxml")

    total_element = soup.find_all("span", class_="total")[0]
    total_count_str = total_element.text.split("из")[1].replace(" ", "")

    pages = (int(total_count_str) // 30) + 1

    return pages


def get_transcription_from_html(html: str) -> str:
    text = ""
    soup = BeautifulSoup(html, "lxml")

    transcription_results = soup.find_all("div", class_="transcription-result")

    for t in transcription_results:
        result = t.find_next("span").text.replace("\n", " ").replace("  ", " ")
        text += re.sub(' +', " ", result)

    return text


def chunk(it: Iterable[Any], size: int) -> Iterable[Any]:
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def save_data_to_file(*, audio_id: str | int, transcription: str, audio: bytes) -> None:
    if not os.path.exists(fr"D:\rec\{audio_id}"):
        os.mkdir(fr"D:\rec\{audio_id}")

    with open(fr"D:\rec\{audio_id}\{audio_id}-text.txt", "w") as f:
        f.write(transcription)

    with open(fr"D:\rec\{audio_id}\{audio_id}-audio.ogg", "wb") as f:
        f.write(audio)


def save_all_records(session: requests.Session, period: str = "Yesterday") -> None:
    if not os.path.exists(r"D:\rec"):
        os.mkdir(r"D:\rec")

    # page_count = get_page_count(session, period)
    page_count = 2955

    all_pages = list(range(1, page_count))
    pages_numbers_lists = chunk(all_pages, page_count // THREAD_COUNT)
    for l in pages_numbers_lists:
        print(l)
        Thread(target=save_records_on_pages, args=[session, period, l]).start()


def save_records_on_pages(session: requests.Session, period: str, pages: Iterable[Any]):
    for page in pages:
        url = (f"https://qa-lk.voca.tech/monitoring/audio/records"
               f"?period=s2021-10-01T00-00e2024-07-24T00-00&state=Any&duration=AnyDuration&page={page}")

        r = session.get(url)

        html = r.content

        soup = BeautifulSoup(html, "lxml")

        records_on_page = soup.find("tbody").find_all("tr")

        for r in records_on_page:
            audio_page_link = r.find_next("a", class_="details-link")["href"]
            audio_id = audio_page_link.split("/")[4]
            audio_link = f"https://qa-lk.voca.tech/download/audio/{audio_id}"

            t_page = session.get(f"https://qa-lk.voca.tech/monitoring/Audio/record/{audio_id}").content

            transcription = get_transcription_from_html(t_page)

            if not transcription:
                continue

            p = Thread(target=save_data_to_file, kwargs={"audio_id": audio_id,
                                                          "transcription": transcription,
                                                          "audio": session.get(audio_link).content})
            p.start()


def main() -> None:
    driver = Firefox()

    s = register(driver)

    driver.close()

    save_all_records(s, "Month")


if __name__ == '__main__':
    main()
