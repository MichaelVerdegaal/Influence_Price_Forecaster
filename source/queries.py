import matplotlib.pyplot as plt
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


def retrieve_events(contract_adress: str, token_id: int):
    stat_collection_request_url = f'https://api.opensea.io/api/v1/events?token_id={token_id}&' \
                                  f'asset_contract_address={contract_adress}'
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


def plot_fit_curves(fit_history, train_metric='loss', val_metric='val_loss', remove_first=True):
    """
    Plots the history of training a model into a line graph
    :param fit_history: history object from model.fit()
    :param train_metric: what to use for the training metrics (only use if you have custom metrics)
    :param val_metric: what to use for the validation metrics (only use if you have custom metrics)
    :param remove_first: whether to remove the first epoch from the history. This can be useful if your first epoch
    has a extremely high score, which messes with the visuals of the plot
    """
    if remove_first:
        train_hist = fit_history.history[train_metric][1:]
        val_hist = fit_history.history[val_metric][1:]
    else:
        train_hist = fit_history.history[train_metric]
        val_hist = fit_history.history[val_metric]
    plt.plot(train_hist)
    plt.plot(val_hist)
    plt.title('Training curve')
    plt.ylabel(train_metric)
    plt.xlabel('epochs')
    plt.legend(['train', 'val'], loc='upper left')
    plt.yscale('log')
    plt.show()
