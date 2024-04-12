import pandas as pd

def convert_dat_to_csv(DAT_PATH):
    df = pd.read_csv(DAT_PATH, sep="\s+")
    df.to_csv("./DATA/Green/ienergy00005_parallel.csv", index = False)
DAT_PATH = "/home/b/b37986/Hsieh_etal_2020/DATA/Green/ienergy00005_parallel.dat"
convert_dat_to_csv(DAT_PATH)