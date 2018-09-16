from passlib.hash import pbkdf2_sha512
import re


class Utils(object):

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512, double encryption
        :param password: the sha512 password from Login/Register
        :return: a sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks the password user sent matches with the password stored in database
        The database password is encrypted more than the one user sent
        :param password: sha512 hashed
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: Boolean value
        """
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile("^[\w-]+@([\w-]+\.)+[\w]+$")
        return True if email_address_matcher.match(email) else False
