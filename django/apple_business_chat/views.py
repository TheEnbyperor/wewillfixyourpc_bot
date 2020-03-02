from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import get_object_or_404
import operator_interface.tasks
from . import tasks
from operator_interface.models import Message, ConversationPlatform
import json
import logging

logger = logging.getLogger(__name__)


def check_auth(f):
    def new_f(request, *args, **kwargs):
        key: str = request.META.get('HTTP_AUTHORIZATION', "")
        if not key.startswith("Key "):
            return HttpResponseForbidden()
        key = key[4:]
        if key != settings.BLIP_KEY:
            return HttpResponseForbidden()

        return f(request, *args, **kwargs)

    return new_f


@csrf_exempt
@check_auth
def webhook(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest()

    logger.debug(f"Got event from ABC webhook: {data}")

    msg_from = data.get("from")
    msg_id = data.get("id")
    msg_type = data.get("type")
    if msg_type == "text/plain":
        tasks.handle_abc_text.delay(msg_id, msg_from, data)
    elif msg_type == "application/vnd.lime.media-link+json":
        tasks.handle_abc_media.delay(msg_id, msg_from, data)

    return HttpResponse("")


@csrf_exempt
@check_auth
def notif_webhook(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest()

    logger.debug(f"Got event from ABC notification webhook: {data}")

    msg_id = data.get("id")
    from_id = data.get("from")
    msg_event = data.get("event")
    conv: ConversationPlatform = ConversationPlatform.objects.filter(
       platform=ConversationPlatform.ABC, platform_id=from_id
    ).first()
    msg: Message = Message.objects.filter(message_id=msg_id).first()

    if msg_event == "failed":
        msg_fail_reason = data.get("reason", {})
        msg_error_code = msg_fail_reason.get("code")
        if msg_error_code == 87 and conv:
            m = Message(
                platform=conv,
                platform_message_id=msg_id,
                end=True,
                direction=Message.FROM_CUSTOMER
            )
            m.save()
            operator_interface.tasks.process_message.delay(m.id)
        if msg:
            msg.state = Message.FAILED
            msg.save()
    elif msg_event == "accepted" and msg:
        msg.state = Message.DELIVERED
        msg.save()
    elif msg_event == "consumed" and msg:
        msg.state = Message.READ
        msg.save()

    return HttpResponse("")