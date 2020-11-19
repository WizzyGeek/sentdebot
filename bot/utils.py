from typing import Any, Awaitable, Callable, NewType, Set, Tuple, Union

from discord import Guild
from discord.ext.commands import Command as _Command
from discord.ext.commands import Context, check

## Types ##

# Mypy docs used ellipses for *args, **kwargs, our case is similar
# we do not know the functions parameters, nor can we type them accurately;
# A Command can be a coroutine func as well as a Command object
Command = Union[Callable[..., Awaitable[Any]], _Command]
Check = Callable[[Command], Command]

# Dummy types for readability and type checking
Id = NewType("Id", int)
RoleId = NewType("RoleId", Id)
UserId = NewType("UserId", Id)
ChannelId = NewType("ChannelId", Id)

## Checks ##

# All the decorators made by factories are called
# i.e @produced_decorator()

# NOTE:: [Predicate should be a coroutine function,
#         but it works as sync function as well]

def in_users(Valid: Set[UserId]) -> Check:
    async def predicate(ctx) -> bool:
        return ctx.author.id in Valid
    # This returns another Function
    # This is not predicate
    return check(predicate)


def has_role(role_id: RoleId) -> Check:
    async def predicate(ctx: Context) ->  bool:
        return role_id in set(map(lambda x: x.id, ctx.author.roles[1:]))
    return check(predicate)

def has_any_roles(roles: Set[RoleId]) -> Check:
    async def predicate(ctx: Context) -> bool:
        return bool(roles & set(map(lambda x: x.id, ctx.author.roles[1:])))
    return check(predicate)

def has_all_roles(roles: Set[RoleId]) -> Check:
    async def predicate(ctx: Context) -> bool:
        return set(map(lambda x: x.id, ctx.author.roles[1:])).issuperset(roles)
    return check(predicate)


def community_report(guild: Guild) -> Tuple[int]:
    online = 0
    idle = 0
    offline = 0

    for m in guild.members:
        if m.raw_status == "online":
            online += 1
        elif m.raw_status == "offline":
            offline += 1
        else:
            idle += 1

    return online, idle, offline
