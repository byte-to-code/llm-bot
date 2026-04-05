from dishka import Provider, Scope, provide_all

from src.bot.usecases.users.users import UsersUsecase


class UsecaseProvider(Provider):
    _get_usecases = provide_all(
        UsersUsecase,
        scope=Scope.REQUEST,
    )
