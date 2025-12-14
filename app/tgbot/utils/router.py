from aiogram import Dispatcher, Router


def print_router_tree(router: Router, indent: int = 0) -> str:
    if isinstance(router, Dispatcher):
        result = " " * indent + "dispatcher"
    else:
        result = " " * indent + router.name
    for in_router in router.sub_routers:
        result += "\n" + print_router_tree(in_router, indent + 2)
    return result
