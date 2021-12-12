from config import unpickle_obj

df = unpickle_obj('dataset_500-crew')
print(df.describe())