import pandas as pd


class Dictionary:
    def __init__(self):
        self.dictionary = None

    def from_csv(self, csv_path: str):
        self.dictionary = pd.read_csv(
            csv_path,
            sep=";",
            on_bad_lines="skip",
        )
        self.dictionary.set_index("Name", inplace=True)

    def to_json(self, json_path):
        self.dictionary.to_json(json_path)


if __name__ == "__main__":
    dictionary = Dictionary()
    dictionary.from_csv(r"D:\a.chekalovets\Projects\WebAudioBadges\temp\dictionary.csv")
    dictionary.to_json(r"D:\a.chekalovets\Projects\WebAudioBadges\temp\dictionary.json")
