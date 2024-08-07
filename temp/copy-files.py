import os
import shutil


def sync_files():
    while True:
        for root, _, files in os.walk(r"D:\records", topdown=False):
            for name in files:
                path = os.path.join(root, name)
                if "whisper" in name:
                    obmen_path = path.replace(
                        r"D:\records", r"O:\01.RUT\IT\Чекаловец\records"
                    )
                    shutil.copyfile(path, obmen_path)


if __name__ == "__main__":
    sync_files()
