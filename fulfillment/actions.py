import dateutil.parser
import dateutil.relativedelta
import datetime
import inflect
import typing
import pytz
from django.utils import timezone
from . import models
import operator_interface.models

tz = pytz.timezone('Europe/London')
p = inflect.engine()


def get_one_or_none(**kwargs):
    query = models.OpeningHours.objects.filter(**kwargs)
    return query[0] if len(query) > 0 else None


def opening_hours(params, *_):
    def inner():
        def format_hours(time: typing.Union[models.OpeningHours, models.OpeningHoursOverride]):
            try:
                if time.closed:
                    return "Closed"
            except AttributeError:
                pass
            if time is None:
                return "Closed"
            open_t = time.open.strftime("%I:%M %p")
            close_t = time.close.strftime("%I:%M %p")
            return f"{open_t} - {close_t}"

        def format_day(day):
            if day[0] == day[1]:
                day_range = day[0]
            else:
                day_range = f"{day[0]}-{day[1]}"
            return f"{day_range}: {format_hours(day[2])}"

        def reduce_days(days):
            cur_day = 0
            while cur_day < len(days):
                next_day = cur_day + 1
                if next_day == len(days):
                    next_day = 0
                if (days[cur_day][2] is None) and (days[next_day][2] is None):
                    days[cur_day] = (days[cur_day][0], days[next_day][1], days[cur_day][2])
                    days.remove(days[next_day])
                    continue
                elif (days[cur_day][2] is None) or (days[next_day][2] is None):
                    pass
                elif (days[cur_day][2].open == days[next_day][2].open) and (
                        days[cur_day][2].close == days[next_day][2].close):
                    days[cur_day] = (days[cur_day][0], days[next_day][1], days[cur_day][2])
                    days.remove(days[next_day])
                    continue
                cur_day += 1
            return days

        opening_hours_defs = {
            "monday": get_one_or_none(monday=True),
            "tuesday": get_one_or_none(tuesday=True),
            "wednesday": get_one_or_none(wednesday=True),
            "thursday": get_one_or_none(thursday=True),
            "friday": get_one_or_none(friday=True),
            "saturday": get_one_or_none(saturday=True),
            "sunday": get_one_or_none(sunday=True),
        }

        want_date = params.get("date")
        want_date_period = params.get("date-period")
        if want_date is not None and want_date != "":
            want_date = dateutil.parser.parse(want_date).date()

            date_overrides = models.OpeningHoursOverride.objects.filter(day=want_date)
            if len(date_overrides) == 0:
                date_override = None
            else:
                date_override = date_overrides[0]

            is_today = want_date == datetime.date.today()
            weekday = want_date.weekday()
            hours = list(opening_hours_defs.values())[weekday] if date_override is None else \
                (None if date_override.closed else date_override)

            if is_today:
                if hours is None:
                    return f"We are closed today.\n\nDo you need help with anything else?"
                return f"Today we are open {format_hours(hours)}.\n\n" \
                       f"Do you need help with anything else?"
            else:
                next_of_weekday = datetime.date.today() + dateutil.relativedelta.relativedelta(weekday=weekday)
                is_next_of_weekday = want_date == next_of_weekday

                if is_next_of_weekday:
                    if hours is None:
                        return f"We are closed {want_date.strftime('%A')}.\n\n" \
                               f"Do you need help with anything else?"
                    return f"{want_date.strftime('%A')} we are open {format_hours(hours)}.\n\n" \
                           f"Do you need help with anything else?"
                else:
                    if hours is None:
                        return f"On {want_date.strftime('%A %B')} the {p.ordinal(want_date.day)} we are closed.\n\n" \
                               f"Do you need help with anything else?"
                    return f"On {want_date.strftime('%A %B')} the {p.ordinal(want_date.day)} we are open" \
                           f" {format_hours(hours)}.\n\nDo you need help with anything else?"

        days = [("Monday", "Monday", opening_hours_defs["monday"]),
                ("Tuesday", "Tuesday", opening_hours_defs["tuesday"]),
                ("Wednesday", "Wednesday", opening_hours_defs["wednesday"]),
                ("Thursday", "Thursday", opening_hours_defs["thursday"]),
                ("Friday", "Friday", opening_hours_defs["friday"]),
                ("Saturday", "Saturday", opening_hours_defs["saturday"]),
                ("Sunday", "Sunday", opening_hours_defs["sunday"])]

        future_overrides = models.OpeningHoursOverride.objects.filter(
            day__gt=datetime.date.today(), day__lte=datetime.date.today() + datetime.timedelta(weeks=2))

        if want_date_period is not None and want_date_period != "":
            want_date_start = dateutil.parser.parse(want_date_period["startDate"]).date()
            want_date_end = dateutil.parser.parse(want_date_period["endDate"]).date()

            days_in_period = {days[want_date_start.weekday()]}
            day_ids_in_period = {want_date_start.weekday()}
            cur_date = want_date_start
            while cur_date != want_date_end:
                cur_date += datetime.timedelta(days=1)
                days_in_period.add(days[cur_date.weekday()])
                day_ids_in_period.add(cur_date.weekday())

            days_in_period = reduce_days(list(days_in_period))
            days_in_period = map(format_day, days_in_period)
            days = "\n".join(days_in_period)

            future_overrides = filter(lambda f: f.day.weekday() in day_ids_in_period, future_overrides)
            future_overrides_txt = map(lambda d: f"\nOn {d.day.strftime('%A %B')} the {p.ordinal(d.day.day)} we will be"
                                                 f" {'closed' if d.closed else f'open {format_hours(d)}'}",
                                       future_overrides)
            future_overrides_txt = "".join(future_overrides_txt)

            return f"Our opening hours are:\n{days}{future_overrides_txt}\n\nDo you need help with anything else?"

        days = reduce_days(days)
        days = map(format_day, days)
        days = "\n".join(days)

        future_overrides_txt = map(lambda d: f"\nOn {d.day.strftime('%A %B')} the {p.ordinal(d.day.day)} we will be"
                                             f" {'closed' if d.closed else f'open {format_hours(d)}'}",
                                   future_overrides)
        future_overrides_txt = "".join(future_overrides_txt)
        return f"Our opening hours are:\n{days}{future_overrides_txt}\n\nDo you need help with anything else?"

    return {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        inner()
                    ]
                },
            },
            {
                "quickReplies": {
                    "quickReplies": [
                        "Yes",
                        "No",
                    ]
                }
            },
        ],
    }


def contact_email(params, text: str, *_):
    contact_details = models.ContactDetails.objects.get()

    return {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        text.replace("$email", contact_details.email)
                    ]
                },
            },
            {
                "quickReplies": {
                    "quickReplies": [
                        "Yes",
                        "No",
                    ]
                }
            },
        ],
    }


def contact_phone(params, text: str, *_):
    contact_details = models.ContactDetails.objects.get()

    return {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        text.replace("$phone", contact_details.phone_number.as_national)
                    ]
                },
            },
            {
                "quickReplies": {
                    "quickReplies": [
                        "Yes",
                        "No",
                    ]
                }
            },
        ],
    }


def contact(params, text: str, *_):
    contact_details = models.ContactDetails.objects.get()

    return {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        text.replace("$phone", contact_details.phone_number.as_national)
                            .replace("$email", contact_details.email)
                    ]
                },
            },
            {
                "quickReplies": {
                    "quickReplies": [
                        "Yes",
                        "No",
                    ]
                }
            },
        ],
    }


def location(params, text: str, *_):
    contact_details = models.ContactDetails.objects.get()

    return {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        text.replace("$link", contact_details.maps_link)
                    ]
                },
            },
            {
                "quickReplies": {
                    "quickReplies": [
                        "Yes",
                        "No",
                    ]
                }
            },
        ],
    }


def repair(params, _, data):
    session = data.get("session")
    brand = params.get("brand")
    iphone_model = params.get("iphone-model")
    ipad_model = params.get("ipad-model")
    repair_name = params.get("iphone-repair")

    if len(iphone_model) != 0:
        brand = "iPhone"

    if len(ipad_model) != 0:
        brand = "iPad"

    if brand is not None and len(brand) != 0:
        if brand == "iPhone":
            if iphone_model is not None and repair_name is not None:
                return generic_repair_fill("iphone", iphone_model, repair_name, models.IPhoneRepair, session)
        elif brand == "iPad":
            if ipad_model is not None and repair_name is not None:
                return generic_repair_fill("ipad", ipad_model, repair_name, models.IPadRepair, session)

    return {
        "fulfillmentText": "Sorry, we don't fix those"
    }


def generic_repair_fill(brand_name, model, repair_name, model_o, session):
    if len(model) == 0:
        text_out = "What model is it?"
    elif len(repair_name) == 0:
        text_out = "What needs fixing?"
    else:
        return generic_repair(model_o, brand_name, model, repair_name, session)

    return {
        "fulfillmentText": text_out,
        "outputContexts": [
            {
                "name": f"{session}/contexts/repair-{brand_name}",
                "lifespanCount": 2,
                "parameters": {
                    f"{brand_name}-model": model,
                    "iphone-repair": repair_name
                }
            }
        ],
    }


def repair_iphone(params, _, data):
    session = data.get("session")
    model = params.get("iphone-model")
    repair_name = params.get("iphone-repair")
    if models is not None and repair_name is not None:
        return generic_repair(models.IPhoneRepair, "iphone", model, repair_name, session)

    return {}


def repair_ipad(params, _, data):
    session = data.get("session")
    model = params.get("ipad-model")
    repair_name = params.get("iphone-repair")
    if models is not None and repair_name is not None:
        return generic_repair(models.IPadRepair, "ipad", model, repair_name, session)

    return {}


def generic_repair(model_o, brand_name, model, repair_name, session):
    repair_m = model_o.objects.filter(name__startswith=model, repair_name=repair_name)

    if len(repair_m) > 0:
        repair_strs = list(map(lambda r: f"A{p.a(f'{r.name} {repair_name}')[1:]} will cost £{r.price}"
                                         f" and will take roughly {r.repair_time}", repair_m))

        return {
            "fulfillmentText": "\n".join(repair_strs),
            "outputContexts": [
                {
                    "name": f"{session}/contexts/repair-{brand_name}",
                    "lifespanCount": 2,
                    "parameters": {
                        f"{brand_name}-model": model,
                        "iphone-repair": repair_name
                    }
                }
            ],
        }
    else:
        return {
            "fulfillmentText": f"Sorry, but we do not fix {model} {p.plural(repair_name)}",
            "outputContexts": [
                {
                    "name": f"{session}/contexts/repair-{brand_name}",
                    "lifespanCount": 2,
                    "parameters": {
                        f"{brand_name}-model": model,
                        "iphone-repair": repair_name
                    }
                }
            ],
        }


def rate(params, _, data):
    session = data.get("session")
    rating = operator_interface.models.ConversationRating(sender_id=session, rating=int(params["rating"]))
    rating.save()
    return {}


def is_open():
    opening_hours_defs = [
        get_one_or_none(monday=True),
        get_one_or_none(tuesday=True),
        get_one_or_none(wednesday=True),
        get_one_or_none(thursday=True),
        get_one_or_none(friday=True),
        get_one_or_none(saturday=True),
        get_one_or_none(sunday=True),
    ]
    today = datetime.date.today()
    weekday = today.weekday()
    hours = opening_hours_defs[weekday]

    if hours is None:
        return False

    now = datetime.datetime.now().time()
    time_open = timezone.make_naive(timezone.make_aware(
        datetime.datetime.combine(today, hours.open), tz)
                                    .astimezone(pytz.utc)).time()
    time_close = timezone.make_naive(timezone.make_aware(
        datetime.datetime.combine(today, hours.close), tz)
                                     .astimezone(pytz.utc)).time()

    if now < time_open:
        return False
    elif now > time_close:
        return False

    return True


def human_needed(params, text, _):
    if is_open():
        return {
            "fulfillmentText": f"{text}Someone will be here to help you shortly..."
        }
    else:
        return {
            "fulfillmentText": f"{text}We're currently closed but this conversation has been flagged and someone"
                               f" will be here to help you as soon as we're open again"
        }


def unlock(params, text, data):
    query = data.get('queryResult')
    outputContexts = query.get('outputContexts')

    if not params.get("brand"):
        return {
            "fulfillmentText": text
        }
    elif params.get("brand") == "iPhone" and not params.get("iphone-model"):
        outputContexts.append({
            "name": f"{data.get('session')}/contexts/unlock-iphone-model",
            "lifespanCount": 1,
            "parameters": params
        })
        return {
            "fulfillmentText": "What model is it?",
            "outputContexts": outputContexts
        }
    elif not params.get("network") or not params.get("name") or not params.get("phone-number")\
            or not params.get("email"):
        return {
            "fulfillmentText": text
        }
    else:
        return {
            "followupEventInput": {
                "name": "unlock-imei",
                "parameters": params
            }
        }


def unlock_iphone_model(params, _, data):
    return {
        "followupEventInput": {
            "name": "unlock",
            "parameters": params
        }
    }


def luhn_checksum(number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10


def unlock_imei(params, _, data):
    imei = int(params.get("imei"))

    if not luhn_checksum(imei) or len(str(imei)) != 15:
        return {
            "fulfillmentText": "Hmmm, that doesn't look like an IMEI, try again...",
            "outputContexts": [{
                "name": f"{data.get('session')}/contexts/unlock",
                "lifespanCount": 2,
                "parameters": params
            }]
        }
    else:
        network = models.Network.objects.filter(name=params.get("network"))
        if not len(network):
            return {
                "fulfillmentText": f"Sorry we can't unlock from {params.get('network-original')}"
            }
        network = network[0]

        brand = models.Brand.objects.filter(name=params.get("brand"))
        if not len(network):
            return {
                "fulfillmentText": f"Sorry we can't unlock {params.get('brand')} phones"
            }
        brand = brand[0]


ACTIONS = {
    'support.opening_hours': opening_hours,
    'support.contact': contact,
    'support.contact.phone': contact_phone,
    'support.contact.email': contact_email,
    'support.location': location,
    'repair': repair,
    'repair.iphone': repair_iphone,
    'repair.ipad': repair_ipad,
    'rate': rate,
    'human_needed': human_needed,
    'unlock': unlock,
    'unlock.iphone-model': unlock_iphone_model,
    'unlock.imei': unlock_imei,
}
