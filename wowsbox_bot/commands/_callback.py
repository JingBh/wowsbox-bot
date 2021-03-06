import json

from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler

from .get import get_callback
from .my import my_callback
from .open import open_callback
from ..cache import get_oc

callbacks = {
    'get': get_callback,
    'my': my_callback,
    'open': open_callback
}


def answer(update: Update, context: CallbackContext):
    try:
        context.bot.answer_callback_query(update.callback_query.id)
    except Exception:  # What may this method throw?
        pass


def callback(update: Update, context: CallbackContext):
    raw_data = update.callback_query.data
    if raw_data:
        if raw_data[:3] == 'oc:':
            data: dict = get_oc(raw_data[3:], update)
        else:
            data: dict = json.loads(update.callback_query.data)
        if data:
            event_type = data.pop('type', None)
            if event_type in callbacks.keys():
                callbacks[event_type](update, context, **data)
    answer(update, context)


callback_handler = CallbackQueryHandler(callback)
