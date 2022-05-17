import json
from typing import Optional

from telegram import Update

from .cache import put_oc


def encode_data(event_type: Optional[str], force_oc=False, **kwargs) -> str:
    kwargs['type'] = event_type
    json_data = json.dumps(kwargs)
    if len(json_data.encode()) > 50 or force_oc:
        return 'oc:' + put_oc(kwargs)
    else:
        return json_data


def is_group(update: Update):
    return 'group' in update.effective_chat.type
