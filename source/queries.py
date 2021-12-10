import requests

from source.data_feed_script import collection_slug


def multi_asset_retrieval(slug: str = collection_slug, limit: int = None, offset: int = None):
    """
    Retrieves multiple assets from OpenSea
    :param slug: slug of the collection to retrieve from
    :param limit: limit the amount of NFT's returned. Minimum 1, maximum 50, 20 if left out.
    :param offset: number to offset pagination with
    :return: list of dictionaries with assets
    """
    multi_asset_request_url = f"https://api.opensea.io/api/v1/assets?collection={slug}"
    if limit and (1 <= limit <= 50):
        multi_asset_request_url += f'&limit={limit}'
    if offset:
        multi_asset_request_url += f'&offset={offset}'
    response = requests.request("GET", multi_asset_request_url)
    multi_asset_json = response.json()['assets']
    return multi_asset_json