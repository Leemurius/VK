from app.models import User


def get_user_avatar_url(url_or_path):
    """
    Returns '' if url_or_path is User.CONST_DEFAULT_PHOTO
    else returns url_or_path as it presents.
    :param url_or_path: str
    :rtype str
    """
    return '' if url_or_path == User.CONST_DEFAULT_PHOTO else url_or_path
