import json
from datetime import datetime, timezone

import boto3
import icalendar
import pytz
import requests

# Global Variables
schedule_url: str = "https://www.stanza.co/api/schedules/mls-dcunited/mls-dcunited.ics"
calendar_name = "DC-United-Schedule"


def get_ics_calendar(url: str = None) -> icalendar.Calendar:
    """

    Parameters
    ----------
    url

    Returns
    -------
    icalendar.Calendar object

    """
    response = requests.get(url)
    cal = icalendar.Calendar.from_ical(response.text)
    return cal


def build_ssm_calendar(source_calendar: icalendar.Calendar = None) -> str:
    """

    Parameters
    ----------
    source_calendar

    Returns
    -------

    """

    # Initialize a new calendar for SSM Change Calendar
    cal = icalendar.Calendar()
    cal.add("X-WR-CALDESC", f"A {calendar_name} Systems Manager Change Calendar")
    cal.add("X-CALENDAR-CMEVENTS", "ENABLED")
    cal.add("X-CALENDAR-TYPE", "DEFAULT_CLOSED")
    cal.add("prodid", "-//AWS//Change Calendar 1.0//EN")
    cal.add("version", "2.0")

    # Set dstamp constant for the loop
    dstamp = datetime.now()

    for component in source_calendar.walk():
        event = icalendar.Event()
        if component.name == "VEVENT":
            assert component.decoded("dtstart") <= component.decoded(
                "dtend"
            ), f"{component.get('SUMMARY')} timing issue."
            try:
                event.add(
                    "dtstamp",
                    dstamp.replace(tzinfo=timezone.utc).astimezone(
                        tz=pytz.timezone("US/Eastern")
                    ),
                )
                event.add(
                    "dtstart",
                    component.decoded("dtstart")
                    .replace(tzinfo=timezone.utc)
                    .astimezone(tz=pytz.timezone("US/Eastern")),
                )
                event.add(
                    "dtend",
                    component.decoded("dtend")
                    .replace(tzinfo=timezone.utc)
                    .astimezone(tz=pytz.timezone("US/Eastern")),
                )
                event.add("uid", component.get("uid"))
                event.add("sequence", "0")
                event.add("X-EVENT-TYPE", "STANDARD")
                event.add("SUMMARY", component.get("SUMMARY"))
                cal.add_component(event)
            except:
                print(f"{component.get('summary')} could not be added to the Calendar.")

    return cal.to_ical().decode("utf-8")


def delete_existing_change_calendar(cal_name: str = None) -> requests.Response:
    session = boto3.session.Session()
    client = session.client("ssm", region_name="us-east-1")

    return client.delete_document(Name=cal_name)


def create_change_calendar(
    cal_name: str = None, cal_content: str = None
) -> requests.Response:
    session = boto3.session.Session()
    client = session.client("ssm", region_name="us-east-1")

    return client.create_document(
        Content=cal_content,
        Name=cal_name,
        DocumentType="ChangeCalendar",
        DocumentFormat="TEXT",
    )


def handler(event, context) -> None:
    src_cal = get_ics_calendar(schedule_url)
    ssm_cal_doc = build_ssm_calendar(src_cal)

    try:
        delete_existing_change_calendar(calendar_name)
    except:
        print(f"{calendar_name} does not exist.")

    r = create_change_calendar(calendar_name, ssm_cal_doc)
    return r
