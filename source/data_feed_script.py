from source.queries import retrieve_crew_amount, retrieve_all_assets, build_dataset

# Config
collection_slug = 'influence-crew'

# Get minted crew count, necessary for pagination
item_count = retrieve_crew_amount(collection_slug)
item_count = 1000  # TODO: remove when done with script. Used so we don't have to wait for the entire collection
print(f"Retrieving {item_count} total items for {collection_slug}")

# Retrieve all indidivual assets of collection
item_list = retrieve_all_assets(collection_slug, item_count)

# Build up dataset
dataset = build_dataset(item_list)
print()