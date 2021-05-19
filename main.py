from aiohttp import web
from mongoConnector import add_new_user, add_outcomes_item, add_incomes_item, get_items, MoneyType
import json

routes = web.RouteTableDef()


# accept 'user_id', return message about user status
@routes.post('/newUser')
async def new_user(request: web.Request):
    data = await request.json()
    user_id = data["id"]
    result = await add_new_user(user_id)
    if result:
        return web.Response(text="User has been added", status=200)
    return web.Response(text="User already added", status=200)


# accept 'user_id', 'category', 'sum', 'date', 'name', return None
@routes.post('/outcomes')
async def add_outcomes(request: web.Request):
    data = await request.json()
    await add_outcomes_item(data["user_id"], data["category"], data["sum"], data["date"], data["name"])
    return web.Response(status=200)


# accept 'user_id', 'date', 'sum', 'name', return None
@routes.post('/incomes')
async def add_incomes(request: web.Request):
    data = await request.json()
    await add_incomes_item(data["user_id"], data["date"], data["sum"], data["name"])
    return web.Response(status=200)


# accept 'user_id', return array of outcomes
@routes.get('/outcomes')
async def get_outcomes(request: web.Request):
    data = await request.json()
    result = await get_items(data["user_id"], MoneyType.Outcomes)
    return web.json_response(result)


@routes.get('/incomes')
async def get_incomes(request: web.Request):
    data = await request.json()
    result = await get_items(data["user_id"], MoneyType.Incomes)
    return web.json_response(result)

app = web.Application()
app.add_routes(routes)
web.run_app(app)
