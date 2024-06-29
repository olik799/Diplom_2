class TextResponse:

    CREATE_USER_WITH_SAME_PARAMS = "User already exists"
    CREATE_USER_WITHOUT_ONE_PARAMS = "Email, password and name are required fields"
    LOGIN_USER_WRONG_ONE_PARAMS = "email or password are incorrect"
    UPDATE_USER_WITHOUT_AUTH = "You should be authorised"

    CREATE_ORDER_WITHOUT_INGREDIENTS = "Ingredient ids must be provided"
    GET_ORDER_WITHOUT_AUTH = "You should be authorised"
