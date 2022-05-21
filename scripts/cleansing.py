import pandas as pd

def read_data(path, *args):
    dataFrame = pd.read_csv(path, *args)
    return dataFrame


def fill_NaN_with_mean(dataFrame, columns):
    dataFrame[columns]= dataFrame[columns].fillna(dataFrame[columns].mean())
    return dataFrame


df = read_data('data/game_analysis.csv')
df = fill_NaN_with_mean(df, ['averageplaytime'])
print(df.info(), '\n')
print(str(df.head()))