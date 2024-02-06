import os
import pandas as pd
import numpy as np


def get_csv_sample(csv):
    if os.path.isfile("../../Samples/CSVs/" + csv):
        return pd.read_csv("../../Samples/CSVs/" + csv)


