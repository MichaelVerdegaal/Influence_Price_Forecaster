from source.queries import multi_asset_retrieval, retrieve_crew_amount

# Config
collection_slug = 'influence-crew'

# Get minted crew count, necessary for pagination
crew_count = retrieve_crew_amount(collection_slug)
print(f"Retrieving {crew_count} total crew members")

# Placeholder
random_address = multi_asset_retrieval(slug=collection_slug, limit=1)