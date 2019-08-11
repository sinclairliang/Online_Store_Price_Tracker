import uuid
from src.commom.database import Database
from src.commom.utils import Utils
import src.models.users.errors as UserErrors
from src.models.alerts.alert import Alert
import src.models.users.constants as UserConstants


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "---User {}---".format(self.email)

    @staticmethod
    def login_valid(email, password):
        """
        This method verifies weather email/password combination is valid or not
        Checks if the email exists, and the password is correct to it
        :param email: user's email
        :param password: a sha512 hashed password
        :return: Boolean value
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {
            "email": email})  # password in sha512->pbkdf2_sha512
        if user_data is None:
            raise UserErrors.UserNotExistException("Your user does not exist")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordException(
                "Your password is not correct")
        return True

    @staticmethod
    def register_user(email, password):
        """
        This method register an user using an email
        :param email: user's email
        :param password: sha512 hashed password
        :return: Boolean, to see if the process is successful (Exceptions might be raised)
        """

        user_data = Database.find_one(
            UserConstants.COLLECTION, {"email": email})

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisterError(
                "The user is already registered with us.")
        if not Utils.email_is_valid(email):
            raise UserErrors.UserEmailInvalidError(
                "The email address cannot be parsed. Questions?")
        User(email, Utils.hash_password(password)).save_to_mongo()
        return True

    def save_to_mongo(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            "email": self.email,
            "password": self.password,
            "_id": self._id
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'email': email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)
