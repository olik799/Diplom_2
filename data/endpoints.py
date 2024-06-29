class Endpoints:

    URL_MAIN = 'https://stellarburgers.nomoreparties.site'

    AUTH = f'{URL_MAIN}/api/auth/'
    CREATE_USER = f'{AUTH}/register'
    DELETE_OR_UPDATE_USER = f'{AUTH}/user'
    LOGIN = f'{AUTH}/login'

    CREATE_ORDER = f'{URL_MAIN}/api/orders'
    INGREDIENTS = f'{URL_MAIN}/api/ingredients'
