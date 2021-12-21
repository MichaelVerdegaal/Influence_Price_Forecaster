from source.queries import retrieve_crew_amount, retrieve_all_assets
from source.dataset_building import build_dataset
from config import pickle_obj

# Config
collection_slug = 'influence-crew'  # Which collection to query
traits_to_keep = ['Title', 'Class', 'Collection']  # Which trait types of the NFT to keep

# Get minted crew count, necessary for pagination
item_count = retrieve_crew_amount(collection_slug)
# item_count = 100  # TODO: remove when done with script. Used so we don't have to wait for the full collection
print(f"Retrieving {item_count} total items for {collection_slug}")

# Retrieve all indidivual assets of collection
item_list = retrieve_all_assets(collection_slug, item_count)

# Build up dataset
dataset = build_dataset(item_list, traits_to_keep)
pickle_obj(dataset, f"dataset_{collection_slug}_{len(dataset)}")
print()
