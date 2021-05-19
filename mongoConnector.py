import json

import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://tWalleApplicationServer:A68NkFe8OFdZHHhD@cluster0.mywnp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client["tWallet"]
users_collection = db["users"]


class Outcomes:
    def __init__(self, date, category, sum, name):
        self.date = date
        self.category = category
        self.sum = sum
        self.name = name


class Incomes:
    def __init__(self, date, sum, name):
        self.date = date
        self.sum = sum
        self.name = name


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.balance = 0
        self.currency = 0
        self.outcomes = []
        self.incomes = []


async def add_new_user(user_id):
    contains = await contains_user(user_id)
    if contains:
        return False
    user = User(user_id)
    users_collection.insert_one(user.__dict__)
    return True


async def contains_user(user_id):
    user = users_collection.find_one({"user_id": user_id})
    print(user)
    return not (user is None)


async def add_outcomes_item(user_id, category, sum, date, name):
    outcomes = Outcomes(date, category, sum, name)
    users_collection.update({"user_id": user_id}, {"$push": {"outcomes": outcomes.__dict__}})


async def add_incomes_item(user_id, date,sum, name):
    incomes = Incomes(date, sum, name)
    users_collection.update({"user_id": user_id}, {"$push": {"incomes": incomes.__dict__}})


async def get_outcomes_items(user_id):
    outcomes = users_collection.find_one({"user_id": user_id})
    return outcomes["outcomes"]
