import os
import time

from faster_whisper import WhisperModel

# RECORDS_DIR = r"O:\01.RUT\IT\Чекаловец\records"
RECORDS_DIR = r"/data/records"


def transcribe(records_directory: str = RECORDS_DIR):
    dirs = os.listdir(records_directory)
    print(dirs)
    total_duration = 0
    total_time = 0
    for directory in dirs:
        start = time.time()
        audio_file_name = f"{directory}-audio.wav"
        file = os.path.join(records_directory, directory, audio_file_name)
        if os.path.exists(file) and os.path.getsize(file) > 60000:
            model = WhisperModel("medium", device="cuda", compute_type="int8_float16")
e                text = ""
                segments, info = model.transcribe(file, language="ru", beam_size=5, vad_filter=True)
                for segment in segments:
                    text += segment.text
                text_file_name = f"{directory}-text-whisper.txt"
                text_file = os.path.join(records_directory, directory, text_file_name)
                text = text.encode("utf-8")
                with open(text_file, "w", encoding="utf-8") as f:
                    f.write(text.decode("utf-8"))
                print(
                    "Создан:", text_file, time.time() - start, segment.end
                )
                total_time += time.time() - start
                total_duration += segment.end
                print(convert_seconds(total_time), "/", convert_seconds(total_duration))
            except Exception as ex:
                print(file, ex)

def convert_seconds(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    remaining_seconds = seconds % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

if __name__ == "__main__":
    transcribe()
