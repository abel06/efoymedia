import pandas as pd


class Update():
    def __init__(self, DF1, DF2, FILE_NAME):
        self.frames = [DF1, DF2]
        self.result = pd.concat(self.frames, sort=False)
        self.result.to_csv(FILE_NAME, index=False)


class Create():
    def __init__(self, COLUMNS, FILE_NAME):
        self.df = pd.DataFrame(columns=COLUMNS)
        self.df.to_csv(FILE_NAME, index=False)


class ReadFile():
    def __init__(self, FILE_NAME):
        self.result = pd.read_csv(FILE_NAME)
