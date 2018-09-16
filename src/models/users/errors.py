class UserError(Exception):
    def __init__(self, message):
        self.message = message


class UserNotExistException(UserError):
    pass


class IncorrectPasswordException(UserError):
    pass


class UserAlreadyRegisterError(UserError):
    pass


class UserEmailInvalidError(UserError):
    pass
