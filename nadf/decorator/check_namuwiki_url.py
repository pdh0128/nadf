from nadf.exception.not_namuwiki_exception import NotNamuwikiException


def check_namuwiki_url(func):
    def wrapper(*args, **kwargs):
        url = kwargs.get("url")

        if not url or "namu.wiki" not in url:
            raise NotNamuwikiException()

        return func(*args, **kwargs)
    return wrapper
