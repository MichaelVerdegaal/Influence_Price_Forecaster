from datetime import datetime

import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_string_dtype

from queries import retrieve_events, get_single_asset


def unpack_traits(traits: list, to_keep: list = None):
    """
    Unpacks NFT traits into a processable formate
    :param traits: list of traits
    :param to_keep: if specified, only add the traits with these names
    :return: processed traits
    """
    if not to_keep:
        to_keep = []

    unpacked_traits = {}
    for trait in traits:
        if (trait['trait_type'] in to_keep) or (not to_keep):
            trait_name = f"{trait['trait_type'].replace(' ', '_').lower()}"
            trait_value = trait['value']
            if isinstance(trait_value, str):
                unpacked_traits[f'{trait_name}_traitvalue'] = str(trait_value).lower()
            else:
                unpacked_traits[f'{trait_name}_traitvalue'] = trait_value
    return unpacked_traits


def unpack_sale(sale_object: dict, num_sales: int):
    """
    Unpacks sale object for the relevant information
    :param sale_object: dict with sale information
    :param num_sales: number of sales of the relevant item
    :return: dict with processed information
    """
    timestamp = sale_object['transaction']['timestamp']
    timestamp = datetime.fromisoformat(timestamp)
    year, month, day = timestamp.year, timestamp.month, timestamp.day
    wei = float(sale_object['total_price'])
    ether = wei / (10 ** 18)
    return {'num_sales': num_sales, 'price': ether, 'date_year': year, 'date_month': month, 'date_day': day}


def clean_dataframe(df: pd.DataFrame):
    """
    Processes the values in the dataframe so it can be entered into a neural network
    :param df: Dataframe to clean
    :return: Cleaned dataframe
    """
    # One-hot encode all categorical traits
    for col in df.filter(like='traitvalue').columns:
        if is_string_dtype(df[col]):
            df[col].fillna('none', inplace=True)
            one_hot = pd.get_dummies(df[col])
            df = df.drop(col, axis=1)
            df = df.join(one_hot, rsuffix=f'{col}_')
    return df


def build_dataset(item_collection: list, traits_to_keep: list):
    """
    Builds the final dataset of the collected assets
    :param item_collection: list of NFT's
    :param traits_to_keep: if specified, only add the traits with these names
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
                print(f'Processing item {token_id}')
                contract_address = item['asset_contract']['address']
                # This is another OS request, and one that requires an API key. If you don't have one use last_sale
                events = retrieve_events(contract_address, token_id)
                for event in events['asset_events']:
                    if event['event_type'] == 'successful':
                        traits = item['traits']
                        if isinstance(traits, list):
                            asset = {'sales': unpack_sale(event, num_sales),
                                     'traits': unpack_traits(traits, traits_to_keep)}
                            dataset.append(asset)

    df = pd.json_normalize(dataset)
    df = clean_dataframe(df)
    return df


def get_and_clean_single_asset(token_id, dtypes, contract_address='0x746db7b1728af413c4e2b98216c6171b2fc9d00e',
                               to_keep=None, year=None, month=None, day=None):
    """
    Retrieves an asset and cleans it for model prediction use
    :param token_id: id of asset to retrieve
    :param dtypes: list of datatypes to expect. This can be generated when building a dataset
    :param contract_address: ethereum address that the asset belongs to
    :param to_keep: traits to keep
    :param year: custom year number, otherwise set to today
    :param month: custom month number, otherwise set to today
    :param day: custom day number, otherwise set to today
    :return: prediction ready item in (1, len(dtypes) dimensional array
    """
    asset = get_single_asset(token_id, contract_address)
    traits = unpack_traits(asset['traits'], to_keep=to_keep)

    # Build new list with specified columns
    dtypes = dtypes.drop(labels=['sales.price'])
    new_list = pd.Series(np.zeros(len(dtypes)), index=dtypes.index)

    # Set traits
    for trait_val in traits.values():
        if trait_val in new_list.index:
            new_list[trait_val] = 1.0

    # Set date
    today = datetime.today()
    if not year:
        new_list['sales.date_year'] = today.year
    else:
        new_list['sales.date_year'] = year
    if not month:
        new_list['sales.date_month'] = today.month
    else:
        new_list['sales.date_month'] = month
    if not day:
        new_list['sales.date_day'] = today.day
    else:
        new_list['sales.date_day'] = day

    new_list = new_list.to_numpy()
    return new_list.reshape((1, len(new_list)))
