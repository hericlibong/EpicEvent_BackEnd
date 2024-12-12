from functools import wraps  # Import nécessaire
from utils.logger import log_error, get_logger


def log_exceptions(logger_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger(logger_name)
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_error(logger, f"Erreur dans {func.__name__}", exception=e)
                raise  # Relever l'exception pour que la couche supérieure puisse la gérer
        return wrapper
    return decorator
