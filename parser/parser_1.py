import json
import os
import re

import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

cookies = {
    'TimezoneOffset': '180',
    'TimezoneOffset': '180',
    'TimezoneOffset': '180',
    '.AspNetCore.Antiforgery.VyLW6ORzMgk': 'CfDJ8L56mmsXIihHn1UE28qo6FFJxya-hi5SAnMqT1tWaNLrYdcf6zvWreIw2VrEahwuC9TXnonOim-OxUmPmpLu_uzf8fds7MvYK08bunOFFD5ioXCjw8Xv3PAlgz9vRn9YWyU57dpZYI8GSyvNiAwpxi8',
    '.AspNetCore.Session': 'CfDJ8L56mmsXIihHn1UE28qo6FE1TexK6gHDxVEp53o0jkdhz95YQJUyHT9w%2Br3rgnRzqI5ipa76Y1IUsU6JiRr7x5eJqKV%2B19jKM16spV5%2BdKPWyI84LKCgFz6FENGg1Gkz8ivXjq5WgFiFmk0%2BZ9ciUaNsiSTyRxlF9Y2KXDbDeMre',
    '.AspNetCore.Cookies': 'CfDJ8L56mmsXIihHn1UE28qo6FGGxWnAeiZITOK76BLkfATpmrOspUYoSCK2ERmt6gjIfbhNSeM90Ak3ihtsZJ98uvEJIprWah1AsGNbRZXte8CewOpz2Q7U8X7Bgs0DjDAMQKrKqmikd3FUzS_5Za2nW5w6L4Rr-FYwWoIBAWDa1xR1j67EEA25Mwjt-S-pgLRSAR2mKSFrl1zP-P0MQadajRsL1nmDdIO_77GiNaOiNwOcM-evPIIwjtJ1-kSdFs7P9gadSGH-hQkH73GNWaVexsD7ARkRiaocMejXEppPRKmZbqHOUsSXrEbhYkG7SZWduQ',
}

def number_generator():
    params = {
        'period': 's2021-10-01T00-00e2024-07-24T00-00',
    }
    for page in range(338, 2955):
        print("Page: ", page)
        params["page"] = f"{page}"
        response = requests.get('https://qa-lk.voca.tech/monitoring/Audio/Records', params=params, cookies=cookies)
        soup = BeautifulSoup(response.text, 'html.parser')
        numbers = re.findall(r"#(\d+)", str(soup))
        for number in numbers:
            yield number


for number in number_generator():
    print("Record number: ", number)
    response = requests.get(f'https://qa-lk.voca.tech/monitoring/Audio/record/{number}', cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    download_links = soup.find_all('a', class_='dropdown-item')
    download_link = "https://qa-lk.voca.tech"
    for link in download_links:
        if ".wav" in link.text:
            download_link += link.get("href")
    transcription_block = soup.find('div', class_='transcription-block')
    text = ""
    if transcription_block:
        text = transcription_block.find_all(string=True, recursive=True)
        text = " ".join([str(word).replace("\n", "").strip() for word in text if word not in ["\n", " "]])
    save_folder = rf"O:\0parser.RUT\IT\Чекаловец\records\{number}"
    os.makedirs(save_folder, exist_ok=True)

    try:
        with open(os.path.join(save_folder, f"{number}-text.txt"), "w") as file:
            file.write(text)
    except Exception as ex:
        print(ex)

    if download_link:
        response = requests.get(download_link, cookies=cookies)
        if response.status_code == 200:
            try:
                with open(os.path.join(save_folder, f"{number}-audio.wav"), 'wb') as file:
                    file.write(response.content)
            except Exception as ex:
                print(ex)
