import os
import time
from argparse import ArgumentParser
from speechkit import model_repository, configure_credentials, creds
from speechkit.stt import AudioProcessingType


# Аутентификация через API-ключ.
configure_credentials(
    yandex_credentials=creds.YandexCredentials(
        api_key="AQVN0eDP5DNV_j3_iVqBXT-ODqEWoUr8MGI2fIdf"
    )
)
RECORDS_DIR = r"O:\01.RUT\IT\Chekalovets\records"


def recognize(records_directory: str = RECORDS_DIR):
    dirs = os.listdir(records_directory)
    print(dirs)
    total_duration = 0
    total_time = 0
    for directory in dirs:
        start = time.time()
        audio_file_name = f"{directory}-audio.wav"
        file = os.path.join(records_directory, directory, audio_file_name)
        if os.path.exists(file) and os.path.getsize(file) > 60000:
            model = model_repository.recognition_model()

            # Задайте настройки распознавания.
            model.model = "general"
            model.language = "ru-RU"
            model.audio_processing_type = AudioProcessingType.Full

            # Распознавание речи в указанном аудиофайле и вывод результатов в консоль.
            result = model.transcribe_file(file)
            for c, res in enumerate(result):
                text_file_name = f"{directory}-text-ysk.txt"
                text_file = os.path.join(records_directory, directory, text_file_name)
                text = res.normalized_text
                text = text.encode("utf-8")
                with open(text_file, "w", encoding="utf-8") as f:
                    f.write(text.decode("utf-8"))
                if res.has_utterances():
                    for utterance in res.utterances:
                        end = utterance.end_time_ms / 1000
                print("Создан:", text_file, time.time() - start, end)
                total_time += time.time() - start
                total_duration += end
                print(convert_seconds(total_time), "/", convert_seconds(total_duration))


def convert_seconds(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    remaining_seconds = seconds % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


if __name__ == "__main__":
    recognize()
