import random

from services.api import cf
from services.db import duels_db, handles_db


def get_duel_prob(uid1: int, uid2: int, rating: int):
    handle1 = handles_db.uid2handle(uid1)
    handle2 = handles_db.uid2handle(uid2)
    subs1 = cf.get_all_attempted_probs(handle1)
    subs2 = cf.get_all_attempted_probs(handle2)
    u_subs = subs1.union(subs2)
    problems = list(cf.get_all_problemset_probs(rating=rating))
    random.shuffle(problems)
    for prob in problems:
        if prob in u_subs:
            continue
        return prob