import requests
import os


def make_request(request_url):
    """
    Send a GET request
    :param request_url: request url to get
    :return: response
    """
    headers = {"X-API-KEY": os.environ.get('OS_API_KEY', '')}
    response = requests.request("GET", request_url, headers=headers)
    return response.json()


def multi_asset_retrieval(slug: str, limit: int = None, offset: int = None):
    """
    Retrieves multiple assets from OpenSea
    :param slug: slug of the collection to retrieve from
    :param limit: limit the amount of NFT's returned. Minimum 1, maximum 50, 20 if left out.
    :param offset: number to offset pagination with
    :return: list of dictionaries with assets
    """
    multi_asset_request_url = f'https://api.opensea.io/api/v1/assets?order_direction=desc&collection={slug}'
    if limit and (1 <= limit <= 50):
        multi_asset_request_url += f'&limit={limit}'
    if offset:
        multi_asset_request_url += f'&offset={offset}'
    response = make_request(multi_asset_request_url)
    multi_asset_json = response['assets']
    return multi_asset_json


def retrieve_crew_amount(slug: str):
    """
    Retries the number of items available on this OpenSea collection
    :param slug: slug of the collection to retrieve from
    :return: number of minted crew as integer
    """
    stat_collection_request_url = f'https://api.opensea.io/api/v1/collection/{slug}/stats'
    response = make_request(stat_collection_request_url)
    item_count = int(response['stats']['count'])
    return item_count


def retrieve_events(contract_address: str, token_id: int):
    """
    Retries OpenSea evednts of a specified asset
    :param contract_address: ethereum address that the asset belongs to
    :param token_id: id of asset to retrieve
    :return: asset events
    """
    stat_collection_request_url = f'https://api.opensea.io/api/v1/events?token_id={token_id}&' \
                                  f'asset_contract_address={contract_address}'
    response = make_request(stat_collection_request_url)
    return response


def retrieve_all_assets(slug: str, item_count: int):
    """
    Retrieves all assets from a collection
    :param slug: slug of the collection to retrieve from
    :param item_count: number of items in collection
    :return: list of assets
    """
    item_list = []
    iteration_counter = 0

    for i in range(int(item_count / 50) + 1):
        print(f"Collecting item {iteration_counter * 50}/{item_count}")
        item_response = multi_asset_retrieval(slug=slug, limit=50, offset=(iteration_counter * 50))
        for item in item_response:
            item_list.append(item)
        iteration_counter += 1
    return item_list


def get_single_asset(token_id, contract_address='0x746db7b1728af413c4e2b98216c6171b2fc9d00e'):
    """
    Retrieve a single asset from OS
    :param token_id: id of asset to retrieve
    :param contract_address: ethereum address that the asset belongs to
    :return: asset as dict
    """
    url = f"https://api.opensea.io/api/v1/asset/{contract_address}/{token_id}"
    asset = make_request(url)
    return asset

