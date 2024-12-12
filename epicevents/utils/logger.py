import logging
import sentry_sdk

# Créer un logger spécifique pour l'application
parent_logger = logging.getLogger('epicevents')
parent_logger.setLevel(logging.INFO)

# Créer un handler pour la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Créer un formateur pour le handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Ajouter le handler au logger
parent_logger.addHandler(console_handler)


def get_logger(name):
    """
    Récupérer un logger spécifique.
    """
    return logging.getLogger(f'epicevents.{name}')


def log_info(logger, message, **kwargs):
    """
    Enregistrer un message d'information et l'envoyer à Sentry avec un contexte supplémentaire.
    """
    logger.info(message, extra=kwargs)
    with sentry_sdk.push_scope() as scope:
        for key, value in kwargs.items():
            scope.set_extra(key, value)
        sentry_sdk.capture_message(message, level="info")


def log_error(logger, message, exception=None, **kwargs):
    """
    Enregistrer un message d'erreur et capturer l'exception avec Sentry, en ajoutant un contexte supplémentaire.
    """
    if exception:
        logger.error(message, exc_info=True, extra=kwargs)
        with sentry_sdk.push_scope() as scope:
            for key, value in kwargs.items():
                scope.set_extra(key, value)
            sentry_sdk.capture_exception(exception)
    else:
        logger.error(message, extra=kwargs)
        with sentry_sdk.push_scope() as scope:
            for key, value in kwargs.items():
                scope.set_extra(key, value)
            sentry_sdk.capture_message(message, level="error")
