import requests
import pandas as pd


def get_top_collections_df():
    """Use solscan api to get top collections by 7day volume"""

    # Pull data
    url = "https://api.solscan.io/collection?sortBy=volume7day&offset=0&limit=1000"
    data = requests.get(url).json()["data"]
    df = pd.DataFrame(data)

    # Unpack
    collection_data = df.data.apply(pd.Series)
    df = df.join(collection_data)

    # Convert Lamprorts to SOL
    df["volume"] = df["volume"] / 10 ** 9
    df["floorPrice"] = df["floorPrice"] / 10 ** 9

    return df


def get_collection_trades_df(collectionId: str) -> pd.DataFrame:
    """Use solscan api to pull latest 10k trades for an NFT collection

    Args:
        collectionId (str): NFT collection ID, from get_top_collections_df

    Returns:
        pd.DataFrame
    """
    url = f"https://api.solscan.io/collection/trade?collectionId={collectionId}&offset=0&limit=10000"
    df = pd.DataFrame(requests.get(url).json()["data"])
    return df
