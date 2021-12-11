import requests


def multi_asset_retrieval(slug: str, limit: int = None, offset: int = None):
    """
    Retrieves multiple assets from OpenSea
    :param slug: slug of the collection to retrieve from
    :param limit: limit the amount of NFT's returned. Minimum 1, maximum 50, 20 if left out.
    :param offset: number to offset pagination with
    :return: list of dictionaries with assets
    """
    multi_asset_request_url = f'https://api.opensea.io/api/v1/assets?collection={slug}'
    if limit and (1 <= limit <= 50):
        multi_asset_request_url += f'&limit={limit}'
    if offset:
        multi_asset_request_url += f'&offset={offset}'
    response = requests.request('GET', multi_asset_request_url)
    multi_asset_json = response.json()['assets']
    return multi_asset_json


def retrieve_crew_amount(slug: str):
    stat_collection_request_url = f'https://api.opensea.io/api/v1/collection/{slug}/stats'
    response = requests.request('GET', stat_collection_request_url)
    item_count = int(response.json()['stats']['count'])
    return item_count
