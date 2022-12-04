import os
import pandas as pd


def new(guild_id: int, channel_id: int, uid1: int, uid2: int, rating: int):
    df = __get_df(guild_id, channel_id)
    new_duel = pd.DataFrame([{"uid1": uid1, "uid2": uid2, "rating": rating}])
    df = pd.concat([df, new_duel])
    __put_df(df, guild_id, channel_id)


def add_problem_and_time(
    guild_id: int,
    channel_id: int,
    uid: int,
    contestId: int,
    index: str,
    start: int,
):
    """Adds problem and time to the duel"""
    df = __get_df(guild_id, channel_id)
    df.loc[
        ((df["uid1"] == uid) | (df["uid2"] == uid)), ["contestId", "index", "start"]
    ] = [contestId, index, start]
    __put_df(df, guild_id, channel_id)


def drop(guild_id: int, channel_id: int, uid: int):
    """Drop the challenge if it exists and is not ongoing"""
    df = __get_df(guild_id, channel_id)
    df = df.loc[((df["uid1"] != uid) & (df["uid2"] != uid))]
    __put_df(df, guild_id, channel_id)


def get_duel_details(
    guild_id: int,
    channel_id: int,
    uid: int = None,
    uid1: int = None,
    uid2: int = None,
):
    df = __get_df(guild_id, channel_id)
    if uid:
        return df.loc[((df["uid1"] == uid) | (df["uid2"] == uid))].to_dict("records")[0]
    if uid1:
        return df.loc[df["uid1"] == uid1].to_dict("records")[0]
    if uid2:
        return df.loc[df["uid2"] == uid2].to_dict("records")[0]
    raise Exception("You must provide exactly one argument")


def duel_exists(
    guild_id: int,
    channel_id: int,
    uid: int = None,
    uid2: int = None,
) -> bool:
    df = __get_df(guild_id, channel_id)
    if uid:
        return ((df["uid1"] == uid) | (df["uid2"] == uid)).any()
    if uid2:
        return (df["uid2"] == uid2).any()
    raise Exception("You must provide exactly one argument")


def duel_is_ongoing(
    guild_id: int,
    channel_id: int,
    uid: int = None,
    uid2: int = None,
) -> bool:
    df = __get_df(guild_id, channel_id)
    if uid:
        return (
            duel_exists(guild_id, channel_id, uid=uid)
            and str(df.loc[((df["uid1"] == uid) | (df["uid2"] == uid)), "start"][0])
            != "nan"
        )
    if uid2:
        return (
            duel_exists(guild_id, channel_id, uid2=uid2)
            and str(df.loc[(df["uid2"] == uid2), "start"][0]) != "nan"
        )
    raise Exception("You must provide exactly one argument")


def __get_df(guild_id: int, channel_id: int):
    db_dir = f"db/{guild_id}/{channel_id}.csv"
    try:
        return pd.read_csv(db_dir)
    except FileNotFoundError:
        try:
            os.makedirs(os.path.dirname(db_dir))
        except FileExistsError:
            ...
        columns = ["uid1", "uid2", "rating", "contestId", "index", "start"]
        pd.DataFrame(columns=columns).to_csv(db_dir, index=False)
        return pd.read_csv(db_dir)


def __put_df(df: pd.DataFrame, guild_id: int, channel_id: int):
    db_dir = f"db/{guild_id}/{channel_id}.csv"
    df.to_csv(db_dir, index=False)


if __name__ == "__main__":
    __get_df(123, 1234)
