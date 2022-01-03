from config import read_model
from config import unpickle_obj
from dataset_building import get_and_clean_single_asset

# Split dataset
dtypes = unpickle_obj('dataset_influence-crew_dtypes')

# Config
prediction_number = 1530
traits_to_keep = ['Title', 'Class', 'Collection']  # Which trait types of the NFT to keep


# Retrieve single asset
asset_to_predict = get_and_clean_single_asset(prediction_number, dtypes, to_keep=traits_to_keep,
                                              year=None, month=None, day=None)

# Split dataset
model = read_model("model_influence_crew_10686")

# Predict
prediction = model.predict(asset_to_predict)[0][0]
print(f"Predicted price for crew choice is: [{prediction}]")
