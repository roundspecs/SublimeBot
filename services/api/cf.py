import requests
import json


def handle_exists(handle: str):
    params = {"handles": [handle]}
    try:
        __query_api("user.info", params=params)
    except KeyError:
        return False
    return True


def get_all_attempted_probs(handle: str):
    params = {"handle": handle}
    submissions = __query_api("user.status", params=params)
    subs = set()
    for submission in submissions:
        subs.add((submission.get("contestId"), submission.get("problem").get("index")))
    return subs


def get_all_accepted_probs(handle: str):
    params = {"handle": handle}
    submissions = __query_api("user.status", params=params)
    subs = dict()
    for submission in submissions:
        if submission.get("verdict") == "OK":
            prob = (
                submission.get("contestId"),
                submission.get("problem").get("index"),
            )
            creationTime = submission.get("creationTimeSeconds")
            subs[prob] = creationTime
    return subs


def get_all_problemset_probs(rating: int = None):
    _probs = get_problemset_json()
    probs = set()
    for _prob in _probs:
        _rating = _prob.get("rating")
        if rating in [None, _rating]:
            probs.add((_prob.get("contestId"), _prob.get("index")))
    return probs


def get_problemset_json():
    with open("problemsets.json") as json_file:
        return json.load(json_file)


def set_problemset_json():
    _probs = __query_api("problemset.problems")["problems"]
    with open("problemsets.json", "w") as json_file:
        json.dump(_probs, json_file)


def __query_api(path: str, params=None):
    API_BASE_URL = "https://codeforces.com/api/"
    res = requests.get(url=API_BASE_URL + path, params=params)
    return res.json()["result"]


if __name__ == "__main__":
    # print(handle_exists("roundspecs"))
    # print(handle_exists("roundspec"))
    # print(get_all_attempted_probs("roundspecs"))
    # print(get_all_problemset_probs(rating=800))
    # set_problemset_json()
    print(get_all_accepted_probs("roundspecs"))
