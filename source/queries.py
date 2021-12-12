import matplotlib.pyplot as plt
import pandas as pd
import requests
from pandas.api.types import is_string_dtype
from sklearn.preprocessing import LabelEncoder


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
    response = requests.request('GET', multi_asset_request_url)
    multi_asset_json = response.json()['assets']
    return multi_asset_json


def retrieve_crew_amount(slug: str):
    """
    Retries the number of items available on this OpenSea collection
    :param slug: slug of the collection to retrieve from
    :return: number of minted crew as integer
    """
    stat_collection_request_url = f'https://api.opensea.io/api/v1/collection/{slug}/stats'
    response = requests.request('GET', stat_collection_request_url)
    item_count = int(response.json()['stats']['count'])
    return item_count


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


def unpack_traits(traits: list):
    """
    Unpacks NFT traits into a processable formate
    :param traits: list of traits
    :return: processed traits
    """
    unpacked_traits = {}
    for trait in traits:
        trait_name = f"{trait['trait_type'].replace(' ', '_').lower()}"
        trait_value = trait['value']
        if isinstance(trait_value, str):
            unpacked_traits[f'{trait_name}_traitvalue'] = str(trait_value).lower()
        else:
            unpacked_traits[f'{trait_name}_traitvalue'] = trait_value
        unpacked_traits[f'{trait_name}_traitcount'] = trait['trait_count']
    return unpacked_traits


def unpack_sale(sale_object: dict, num_sales: int):
    """
    Unpacks sale object for the relevant information
    :param sale_object: dict with sale information
    :param num_sales: number of sales of the relevant item
    :return: dict with processed information
    """
    date = sale_object['event_timestamp']  # TODO: this is harder to convert to a feature, so we'll leave it for now
    wei = float(sale_object['total_price'])
    ether = wei / (10 ** 18)
    return {'num_sales': num_sales, 'price': ether}


def clean_dataframe(df: pd.DataFrame):
    """
    Processes the values in the dataframe so it can be entered into a neural network
    :param df: Dataframe to clean
    :return: Cleaned dataframe
    """
    enc = LabelEncoder()
    # One-hot encode all categorical traits
    for col in df.filter(like='traitvalue').columns:
        if is_string_dtype(df[col]):
            df[col].fillna('none', inplace=True)
            one_hot = pd.get_dummies(df[col])
            df = df.drop(col, axis=1)
            df = df.join(one_hot, rsuffix=f'{col}_')

    # Label encode all numerical traits
    for col in df.filter(like='traitcount').columns:
        total_nan = int(df[col].isna().sum())
        df[col].fillna(total_nan, inplace=True)
        df[col] = enc.fit_transform(df[col])
    return df


def build_dataset(item_collection: list):
    """
    Builds the final dataset of the collected assets
    :param item_collection: list of NFT's
    :return: dataframe
    """
    dataset = []
    for item in item_collection:
        num_sales = item['num_sales']
        # Only if the item has any sales we'll continue
        if num_sales > 0:
            last_sale = item['last_sale']
            if last_sale:
                token_id = int(item['token_id'])
                traits = item['traits']
                item = {'token_id': token_id,
                        'sales': unpack_sale(last_sale, num_sales),
                        'traits': unpack_traits(traits)}
                dataset.append(item)

    df = pd.json_normalize(dataset)
    df = clean_dataframe(df)
    return df


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
