import pandas as pd

class Pattern:
    def __init__(self, pattern_file_path) -> None:
        self.path = pattern_file_path

        self.read_file()

    def read_file(self):
        data = pd.read_csv(self.path)
        print(data)