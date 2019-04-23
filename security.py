from models.user_model import UserModel
from werkzeug.security import safe_str_cmp


# when user hits auth endpoint with username and password
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    # another way of accessing a dict, which also
    # allows you to set a default value
    if user and safe_str_cmp(user.password, password):
        return user
    """
    be careful using == for string comparison, string encoding
    can mess things up, especially before Python3. try
    from werkzeug.security import safe_str_cmp
    """


# when user hits an endpoint that requires them to be authenticated
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
