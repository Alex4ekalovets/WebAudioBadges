"""
Модуль содержит класс, который позволяет привести аудио к нужному формату (16К mono wav) и затем разбить его на части
(длина каждой из которых ограничена) по участкам тишины, которые в основном семантически возникают на стыке предложений.
Эти части далее называются **чанками (chunks)**.
"""
import os
import time
from typing import List

from pydub import AudioSegment, silence


class Audio2Chunks:
    """
    Класс позволяет привести аудио к нужному формату (16К mono wav) и затем разбить его на части
    (длина каждой из которых ограничена) по участкам тишины, которые в основном семантически возникают на стыке предложений.
    Эти части далее называются **чанками (chunks)**.
    """

    def __init__(self, path2audio: str, max_chunk_duration: int = 150, verbose: int = 0):
        """
        Инициализация класса.
        Args:
            path2audio (str): Путь до аудио, которое нужно разбить на чанки.
            max_chunk_duration (int): Максимальная длительность чанка в секундах.
            verbose (int): Уровень подробности. Если =2, то выводить промежуточные данные.
        """
        self.path2audio = path2audio
        self.audio_duration = None
        self.audio = None
        self.verbose = verbose
        self.chunks = []
        self.chunks_durations = []
        self.paths2chunks: List[str] = []
        self.max_chunk_duration = max_chunk_duration
        self.split_audio_duration = None

    def load_audio(self):
        """
        Считывание аудиофайла и его преобразование к необходимому формату.
        """
        self.audio = AudioSegment.from_file(self.path2audio)

        # Set to 16K mono wav format (because Nemo Model can accept only this!)
        self.audio = self.audio.set_frame_rate(16000)
        self.audio = self.audio.set_channels(1)
        self.audio = self.audio.set_sample_width(2)
        self.audio_duration = self.audio.duration_seconds

    def _get_chunks_for_given_audio(self, sample_audio, min_silence_len, silence_thresh):
        """
        Функция находит чанки для произвольного аудио. Причем не ограничивает их по длине.
        Args:
            sample_audio (AudioSegment): Аудио, которое надо разбить на чанки.
            min_silence_len (int): Минимальная длина для промежутка тишины.
            silence_thresh: (int): Фрагменты аудио с амплитудой меньше *silence_thresh* dBFS будут считаться тишиной.

        Returns:
            Чанки, полученные разделением аудио по участкам тишины.
        """
        silence_thresh = self.audio.dBFS + silence_thresh
        silence_sectors = silence.detect_silence(audio_segment=sample_audio,
                                                 min_silence_len=min_silence_len,
                                                 silence_thresh=silence_thresh)
        silence_sectors = [((start / 1000), (stop / 1000)) for start, stop in silence_sectors]  # convert to sec
        split_times = [round((items[0] + items[1]) / 2, 2) for items in silence_sectors]  # choose middle time point

        chunks = []
        chunks_durations = []
        start_time = 0
        for i, end_time in enumerate(split_times):
            chunk = sample_audio[start_time * 1000: end_time * 1000]
            chunks.append(chunk)
            chunks_durations.append(round((end_time - start_time), 2))
            start_time = end_time

        chunks.append(sample_audio[start_time * 1000: sample_audio.duration_seconds * 1000])
        chunks_durations.append(round((sample_audio.duration_seconds - start_time), 2))
        return chunks, chunks_durations

    def get_chunks(self):
        """
        Функция разбивает исходное аудио на чанки, ограниченные по продолжительности.
        Делается это в 4 этапа, где с каждым этапом, условия на "тишину" ослабляются, тем самым, чанки, которые на
        предыдущем этапе не смогли уложиться в ограничения по продолжительности, начинают укладываться в них.

        Если по достижении последнего этапа чанк не укладывается в рамки продолжительности, то аудио считается
        неразделимым на ограниченные чанки. Потому что последнее ограничение очень "мягкое".

        Returns:
            Ограниченные по времени чанки, на которые разделилось исходное аудио.
        """

        # 1 level chunks
        if self.audio_duration > self.max_chunk_duration:
            if self.verbose == 2:
                print("1st level chunk processing...")
            first_level_chunks, first_level_chunks_durations = self._get_chunks_for_given_audio(
                self.audio,
                min_silence_len=1500,
                silence_thresh=-20)

            # 2 level chunks
            for first_level_chunk, first_level_chunk_duration in zip(first_level_chunks, first_level_chunks_durations):
                if first_level_chunk.duration_seconds > self.max_chunk_duration:
                    if self.verbose == 2:
                        print("2nd level chunk processing...")
                    second_level_chunks, second_level_chunks_durations = self._get_chunks_for_given_audio(
                        first_level_chunk,
                        min_silence_len=1100,
                        silence_thresh=-20)

                    # 3 level chunks
                    for second_level_chunk, second_level_chunk_duration in zip(second_level_chunks,
                                                                               second_level_chunks_durations):
                        if second_level_chunk.duration_seconds > self.max_chunk_duration:
                            if self.verbose == 2:
                                print("3rd level chunk processing...")
                            third_level_chunks, third_level_chunks_durations = self._get_chunks_for_given_audio(
                                second_level_chunk,
                                min_silence_len=800,
                                silence_thresh=-20)

                            # 4 level chunks
                            for third_level_chunk, third_level_chunk_duration in zip(third_level_chunks,
                                                                                     third_level_chunks_durations):
                                if third_level_chunk.duration_seconds > self.max_chunk_duration:
                                    if self.verbose == 2:
                                        print("4th level chunk processing...")
                                    fourth_level_chunks, fourth_level_chunks_durations = self._get_chunks_for_given_audio(
                                        third_level_chunk,
                                        min_silence_len=500,
                                        silence_thresh=-16)

                                    for fourth_level_chunk, fourth_level_chunk_duration in zip(fourth_level_chunks,
                                                                                               fourth_level_chunks_durations):
                                        if fourth_level_chunk.duration_seconds > self.max_chunk_duration:
                                            raise Exception('No silence!')

                                        else:
                                            self.chunks.append(fourth_level_chunk)
                                            self.chunks_durations.append(fourth_level_chunk_duration)
                                else:
                                    self.chunks.append(third_level_chunk)
                                    self.chunks_durations.append(third_level_chunk_duration)
                        else:
                            self.chunks.append(second_level_chunk)
                            self.chunks_durations.append(second_level_chunk_duration)
                else:
                    self.chunks.append(first_level_chunk)
                    self.chunks_durations.append(first_level_chunk_duration)
        else:
            self.chunks.append(self.audio)
            self.chunks_durations.append(self.audio_duration)

    def save_chunks(self):
        """
        Сохранение чанков локально.
        """
        audio_name = os.path.splitext(os.path.split(self.path2audio)[1])[0]
        chunks_directory_path = os.path.join(os.path.split(self.path2audio)[0], f"{audio_name}_chunks")

        if not os.path.exists(chunks_directory_path):
            os.mkdir(chunks_directory_path)
        else:
            for file in os.listdir(chunks_directory_path):
                os.remove(os.path.join(chunks_directory_path, file))

        chunk_name_template = "{}_{}.wav"
        for i, chunk in enumerate(self.chunks):
            chunk_path = os.path.join(chunks_directory_path, chunk_name_template.format(audio_name, i))
            self.paths2chunks.append(chunk_path)
            chunk.export(chunk_path, format="wav")

    def split_and_save_chunks(self):
        """
        Разделение аудио на чанки и их сохранение.
        """
        split_audio_start_time = time.time()
        self.load_audio()
        self.get_chunks()
        self.save_chunks()
        self.split_audio_duration = time.time() - split_audio_start_time

        if self.verbose == 2:
            print("---------------")
            print(f"Number of chunks = {len(self.chunks)}")
            for i, chunk_duration in enumerate(self.chunks_durations):
                print(f"\tduration of chunk {i} = {chunk_duration}")