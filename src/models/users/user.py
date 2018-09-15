import uuid

from src.commom.database import Database
from src.commom.utils import Utils
import src.models.users.error as UserErrors


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return"---User {}---".format(self.email)

    @staticmethod
    def login_valid(email, password):
        """
        This method verifies email/password combo is valid or not
        Checks if the email exists, and the password is correct to it
        :param email: user's email
        :param password: a sha512 hashed password
        :return: Boolean value
        """
        user_data = Database.find_one("users", {"email": email}) # password in sha512->pbkdf2_sha512
        if user_data is None:
            raise UserErrors.UserNotExistException("Your user does not exist")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordException("Your password is not correct")
        return True
