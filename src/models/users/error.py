# class UserError(Exception):
#     def __init__(self, message):
#         self.message = message
#
#
# class UserNotExistException(UserError):
#         pass
#
#
# class IncorrectPasswordException(UserError):
#         pass


class UserNotExistException(Exception):
    def __init__(self, message):
        self.message = message


class IncorrectPasswordException(Exception):
    def __init__(self, message):
        self.message = message
