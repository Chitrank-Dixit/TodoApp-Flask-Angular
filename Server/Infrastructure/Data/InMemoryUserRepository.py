from Server.Domain.Core import Maybe
from Server.Domain.Entities import User
from Server.Domain.Interfaces import IUserRepository
from Server.Infrastructure.Services import WerkzeugPasswordHasher


class InMemoryUserRepository(IUserRepository):
    _hasher = WerkzeugPasswordHasher()
    _users = [User(email='danfromisrael@gmail.com', hashed_password=_hasher.encode('pass'), display_name='dandan'),
              User(email='maymay@gmail.com', hashed_password=_hasher.encode('pass'), display_name='may'),
              User(email='zuzu@gmail.com', hashed_password=_hasher.encode('pass'), display_name='zuzu')]

    def __init__(self):
        self._users_db = InMemoryUserRepository._users

    def get_by_id(self, user_id):
        user = next((u for u in self._users_db if u.id == user_id), None)
        user_doesnt_exist = user is None
        if user_doesnt_exist:
            return Maybe(None)
        else:
            return Maybe(value=user.copy_user())

    def get_by_facebook_id(self, facebook_id):
        user = next((u for u in self._users_db if u.facebook == facebook_id), None)
        user_doesnt_exist = user is None
        if user_doesnt_exist:
            return Maybe(None)
        else:
            return Maybe(value=user.copy_user())

    def get_by_google_id(self, google_id):
        user = next((u for u in self._users_db if u.google == google_id), None)
        user_doesnt_exist = user is None
        if user_doesnt_exist:
            return Maybe(None)
        else:
            return Maybe(value=user.copy_user())

    def update(self, user_id, user):
        maybe_db_user = next((u for u in self._users_db if u.id == user_id), None)
        if maybe_db_user is not None:
            db_user = maybe_db_user
        else:
            raise UserDoesntExistsError("invalid user_id")

        if db_user.facebook != user.facebook:
            db_user.facebook = user.facebook

        if db_user.email != user.email:
            db_user.email = user.email

        if db_user.twitter != user.twitter:
            db_user.twitter = user.twitter

        if db_user.google != user.google:
            db_user.google = user.google

        if db_user.github != user.github:
            db_user.github = user.github

        if db_user.display_name != user.display_name:
            db_user.display_name = user.display_name

        if db_user.pic_link != user.pic_link:
            db_user.pic_link = user.pic_link

    def get_by_email(self, email):
        user = next((u for u in self._users_db if u.email == email), None)
        user_doesnt_exist = user is None
        if user_doesnt_exist:
            return Maybe(None)
        else:
            return Maybe(value=user.copy_user())

    def delete(self, _id):
        pass

    def get_all(self):
        return (user.copy_user() for user in self._users_db)  # so we wont return the DB reference

    def add(self, user):
        self._users_db.append(user)


class UserDoesntExistsError(Exception):
    pass