from telegram.ext import Dispatcher

from ._callback import callback_handler
from ._error import error_handler
from .admin import admin_handler
from .get import get_handler
from .help import help_handler
from .my import my_handler
from .open import open_handler, open_message_handler
from .start import start_handler
from ..env import env

DEBUG = env.bool('DEBUG', default=False)


def register_commands(dispatcher: Dispatcher):
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)

    dispatcher.add_handler(get_handler)
    dispatcher.add_handler(my_handler)
    dispatcher.add_handler(open_handler)
    dispatcher.add_handler(open_message_handler)

    dispatcher.add_handler(admin_handler)

    dispatcher.add_handler(callback_handler)

    if not DEBUG:
        dispatcher.add_error_handler(error_handler)
