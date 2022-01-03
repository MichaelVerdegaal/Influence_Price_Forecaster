from config import read_model
from config import unpickle_obj
from dataset_building import get_and_clean_single_asset

# Load static files
dtypes = unpickle_obj('dataset_influence-crew_dtypes')
model = read_model("model_influence_crew_10686")

# Config
to_predict = [2284, 6028, 6219, 6999, 7348]
traits_to_keep = ['Title', 'Class', 'Collection']  # Which trait types of the NFT to keep

# Tracking
predictions = []

for token_id in to_predict:
    # Prepare input
    asset_to_predict = get_and_clean_single_asset(token_id, dtypes, to_keep=traits_to_keep,
                                                  year=None, month=None, day=None)

    # Predict
    prediction = model.predict(asset_to_predict)[0][0]
    predictions.append(prediction)
    print(f"Predicted price for token {token_id} is: {round(prediction, 3)} ETH")
print(f"\nTotal predicted value of collection: {round(sum(predictions), 3)} ETH")
