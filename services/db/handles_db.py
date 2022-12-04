import pandas as pd

HANDLES_DB = "db/handles.csv"


def set_or_update_handle(handle: str, uid: int):
    """Update handle if uid exists. Otherwise, add new handle"""
    df = pd.read_csv(HANDLES_DB)
    if (df["uid"] == uid).any():
        df.loc[df["uid"] == uid, "handle"] = handle
    else:
        new_handle_df = pd.DataFrame([{"uid": uid, "handle": handle}])
        df = pd.concat([df, new_handle_df])
    df.to_csv(HANDLES_DB, index=False)


def uid_exists(uid: int) -> bool:
    """Returns true if uid exists. Otherwise, false"""
    df = pd.read_csv(HANDLES_DB)
    return (df["uid"] == uid).any()


def uid2handle(uid: int) -> str:
    """Returns the handle from uid if exists"""
    df = pd.read_csv(HANDLES_DB)
    s = df.loc[df["uid"] == uid, "handle"].to_list()
    if len(s) != 0:
        return s[0]
    raise UidDoesNotExist


def get_all_uid_handle():
    """Returns a list of all uid's and handles"""
    df = pd.read_csv(HANDLES_DB)
    return df["uid"].to_list(), df["handle"].to_list()


class UidDoesNotExist(Exception):
    ...


if __name__ == "__main__":
    print("Does uid 1234 exist?",uid_exists(1234))
    print("Does uid 693265856305692764 exist?",uid_exists(693265856305692764))
    print()
    print("Handle of 693265856305692764:", uid2handle(693265856305692764))
    print()
    print("All uids and handles: ", get_all_uid_handle())
