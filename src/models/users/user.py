import uuid

from src.commom.database import Database
from src.commom.utils import Utils

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
        user_date = Database.find_one("users", {"email": email})
        if user_date is None:
            # user does not exist
            pass
        if not Utils.check_hashed_password(password, user_data['password']):
            # the password is not valid
            pass
        return True
