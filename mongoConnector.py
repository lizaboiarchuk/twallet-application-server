import json
from enum import Enum

import pymongo

import monobankConnection

client = pymongo.MongoClient(
    "mongodb+srv://tWalleApplicationServer:A68NkFe8OFdZHHhD@cluster0.mywnp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client["tWallet"]
users_collection = db["users"]


class MoneyType(Enum):
    Incomes = "incomes"
    Outcomes = "outcomes"


class Outcomes:
    def __init__(self, date, category, sum, name, currency):
        self.date = date
        self.category = category
        self.sum = sum
        self.name = name
        self.currency = currency


class Incomes:
    def __init__(self, date, sum, name, currency):
        self.date = date
        self.sum = sum
        self.name = name
        self.currency = currency


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.balance = 0
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


async def add_outcomes_item(user_id, category, sum, date, name, currency):
    sum = await exchange(sum, int(currency))
    outcomes = Outcomes(date, category, sum, name, currency)
    users_collection.update({"user_id": user_id}, {"$push": {"outcomes": outcomes.__dict__}})
    balance = await get_user_balance(user_id)
    balance -= int(sum)
    users_collection.update({"user_id":user_id}, {"$set": {"balance": balance}})


async def add_incomes_item(user_id, date, sum, name, currency):
    sum = await exchange(sum, int(currency))
    incomes = Incomes(date, sum, name, currency)
    users_collection.update({"user_id": user_id}, {"$push": {"incomes": incomes.__dict__}})
    balance = await get_user_balance(user_id)
    balance += int(sum)
    users_collection.update({"user_id": user_id}, {"$set": {"balance": balance}})


async def exchange(sum, currency):
    if currency == 980:
        return sum

    course_exchange = {"errorDescription": ""}
    while "errorDescription" in course_exchange:
        course_exchange = await monobankConnection.get_currency()

    for exchange_rate in course_exchange:
        if exchange_rate["currencyCodeA"] == currency:
            if "rateCross" in exchange_rate:
                return sum * float(exchange_rate["rateCross"])
            return sum * float(exchange_rate["rateBuy"])


async def get_items(user_id, flag: MoneyType):
    outcomes = users_collection.find_one({"user_id": user_id})
    return outcomes[flag.value]


async def get_user_balance(user_id):
    user = users_collection.find_one({"user_id": user_id})

    return user["balance"]
