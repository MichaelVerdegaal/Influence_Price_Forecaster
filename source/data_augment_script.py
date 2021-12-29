from config import unpickle_obj, pickle_obj
import random

# Load dataset
dataset_name = 'dataset_influence-crew_1747'
df = unpickle_obj(dataset_name)


def duplicate(row, n=5):
    """
    Duplicates (augments) the row by modifying the sale price
    :param row: pandas series
    :param n: how many duplicates to return
    :return: duplicates in list
    """
    price = row['sales.price']
    lower, higher = price * 0.9, price * 1.1
    dupe_list = []
    for i in range(n):
        new_price = random.uniform(lower, higher)
        row_dupe = row.copy(deep=True)
        row['sales.price'] = new_price
        dupe_list.append(row_dupe)
    return dupe_list


for index, row in df.iterrows():
    print(f"Duping row {index}")
    for dupe in duplicate(row):
        df = df.append(dupe, ignore_index=True)

pickle_obj(df, f"{dataset_name}_augmented")
