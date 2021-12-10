# Config variables
from source.queries import multi_asset_retrieval

collection_slug = 'influence-crew'

# Retrieve a random owner
x = multi_asset_retrieval(limit=1)
x2 = multi_asset_retrieval(limit=50)
x3 = multi_asset_retrieval(limit=50, offset=1)
print()
