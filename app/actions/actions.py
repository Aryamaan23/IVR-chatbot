# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from __future__ import print_function


# This is a simple example for a custom action which utters "Hello World!"
import datetime as dt
from typing import Any, Text, Dict, List
from difflib import get_close_matches

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.types import DomainDict

from twilio.rest import Client
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from databaseconn import DataUpdate

import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


ottp = random.randint(1000, 9999)
SCOPES = ['https://www.googleapis.com/auth/calendar']


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"{dt.datetime.now()}")

        return []


class ActionSearch(Action):
    def name(self) -> Text:
        return "action_search_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        products = [
            {
                "name": "Budweiser",
                "price": 400,
                "alchohal_content": 12
            },
            {
                "name": "Corona Extra",
                "price": 500,
                "alchohal_content": 13
            },
            {
                "name": "Stella Artois",
                "price": 1225,
                "alchohal_content": 11
            },
            {
                "name": "Aguila",
                "price": 1250,
                "alchohal_content": 10
            },
            {
                "name": "Becks Blue",
                "price": 525,
                "alchohal_content": 15
            },
            {
                "name": "Bogota Lager",
                "price": 700,
                "alchohal_content": 16
            },
            {
                "name": "Contender",
                "price": 625,
                "alchohal_content": 19
            },
            {
                "name": "Brahma Chopp",
                "price": 1100,
                "alchohal_content": 20
            },
            {
                "name": "Bud Light",
                "price": 900,
                "alchohal_content": 13
            },
            {
                "name": "Cass Fresh",
                "price": 825,
                "alchohal_content": 21
            },
            {
                "name": "Castle Lager",
                "price": 1000,
                "alchohal_content": 14
            },
            {
                "name": "Cusquena Dorada",
                "price": 2000,
                "alchohal_content": 25
            },
            {
                "name": "Eagle Lager",
                "price": 785,
                "alchohal_content": 24
            },
            {
                "name": "Goose Island Bourbon County Brand Stout",
                "price": 2125,
                "alchohal_content": 27
            },
            {
                "name": "Harbin",
                "price": 1230,
                "alchohal_content": 23
            },
            {
                "name": "Haywards 5000",
                "price": 500,
                "alchohal_content": 20
            },
            {
                "name": "Hero",
                "price": 725,
                "alchohal_content": 29
            },
            {
                "name": "Hoegarden",
                "price": 890,
                "alchohal_content": 30
            },
            {
                "name": "Jupiler",
                "price": 925,
                "alchohal_content": 17
            },
            {
                "name": "Labatt Blue",
                "price": 1175,
                "alchohal_content": 16
            },
            {
                "name": "Leffe",
                "price": 910,
                "alchohal_content": 32
            },
            {
                "name": "Micheblob ULTRA",
                "price": 650,
                "alchohal_content": 23
            },
            {
                "name": "Modelo Especial",
                "price": 699,
                "alchohal_content": 13
            },
            {
                "name": "Patagonia 24.7",
                "price": 1500,
                "alchohal_content": 29
            },
            {
                "name": "Quilmes",
                "price": 1700,
                "alchohal_content": 20
            },
            {
                "name": "Salva Vida",
                "price": 1800,
                "alchohal_content": 34
            },
            {
                "name": "Skol",
                "price": 2000,
                "alchohal_content": 38
            },
            {
                "name": "Victoria",
                "price": 2200,
                "alchohal_content": 33
            },
            {
                "name": "Wals Brut",
                "price": 2500,
                "alchohal_content": 39
            }

        ]

        def closest(lst, K):
            return lst[min(range(len(lst)), key=lambda i: abs(lst[i]-K))]

        choice = tracker.get_slot("search_prod_choice")
        value = tracker.get_slot("search_prod_value")

        if choice == "1":
            pr = []
            for p in products:
                pr.append(p["name"])
            nearest = get_close_matches(value, pr)

            for p in products:
                if p["name"] == nearest[0]:
                    dispatcher.utter_message(text="Here is your search result")
                    dispatcher.utter_message(
                        text=f"Name: {p['name']}\nPrice:  ₹{p['price']}\nAlcohal Content: {p['alchohal_content']}%")
                    break

        elif choice == "2":
            pr = []
            for p in products:
                pr.append(p["price"])
            nearest = closest(pr, int(value))
            for p in products:
                if p["price"] == nearest:
                    dispatcher.utter_message(text="Here is your search result")
                    dispatcher.utter_message(
                        text=f"Name: {p['name']}\nPrice:  ₹{p['price']}\nAlcohal Content: {p['alchohal_content']}%")
                    break

        elif choice == "3":
            pr = []
            for p in products:
                pr.append(p["alchohal_content"])
            nearest = closest(pr, int(value))
            for p in products:
                if p["alchohal_content"] == nearest:
                    dispatcher.utter_message(text="Here is your search result")
                    dispatcher.utter_message(
                        text=f"Name: {p['name']}\nPrice:  ₹{p['price']}\nAlcohal Content: {p['alchohal_content']}%")
                    break

        else:
            dispatcher.utter_message(text=f"sorry product not found!")

        return [AllSlotsReset()]


class ActionPaymentStatus(Action):
    def name(self) -> Text:
        return "action_payment_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        orders = [
            {
                "id": "1",
                "payment_status": True,
                "amount": "6864",
                "time": dt.datetime.now()
            },
            {
                "id": "2",
                "payment_status": True,
                "amount": "43437",
                "time": dt.datetime.now()
            },
            {
                "id": "3",
                "payment_status": False,
                "amount": "46643",
                "time": dt.datetime.now()
            }
        ]

        order_id = tracker.get_slot("order_id")

        res = "item not found!"

        for o in orders:
            if o['id'] == order_id:
                res = o
                break

        if res == "item not found!":
            dispatcher.utter_message(text=f"sorry item not found")
            return [AllSlotsReset()]

        ID = res["id"]
        status = res["payment_status"]
        dat = res["time"]
        if status == False:
            amount = "You have to pay ₹" + \
                res["amount"] + " upto date " + str(dat)
        else:
            amount = "You have paid ₹" + res["amount"] + " at " + str(dat)

        dispatcher.utter_message(
            text=f"Payment Status for order Id {ID} is {status}. {amount}")
        dispatcher.utter_image_url(image="https://5.imimg.com/data5/NI/BH/MY-3360774/gst-bill-2finvoice-book-500x500.jpg")

        return [AllSlotsReset()]


# class ActionAuth(Action):

#     def name(self) -> Text:
#         return "action_auth"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         otp = tracker.get_slot("otp")
#         if str(otp) == str(ottp):
#             dispatcher.utter_message(
#                 text=f"Your phone is verified successfully!")
#         else:
#             dispatcher.utter_message(text=f"Unauthorized!")

#         return [AllSlotsReset()]


class ValidatePaymentForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_payment_form"

    def validate_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        print("yoyoyoyoyoyoyoyoy")
        account_sid = "AC083274c578353fe67a0eaad634de69d8"
        auth_token = "f631eddc42197d50a3b440dcd1bd1891"
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
                body='Your OTP for ABInBev Bot is ' + str(ottp),
                from_='+16123240764',
                to='+91'+slot_value
            )

        return {'phone_number': slot_value}

    def validate_otp(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        otp = tracker.get_slot("otp")
        if str(otp) == str(ottp):
            dispatcher.utter_message(
                text=f"Your phone is verified successfully!")
            return {'otp': slot_value}
        else:
            dispatcher.utter_message(text=f"Unauthorized!")
            return {'otp': None}


class ActionEmailSubmit(Action):
    def name(self) -> Text:
        return "action_mail_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

        email = "feedback@abinbev.com"
        dep = tracker.get_slot("department")
        if dep == "1":
            email = "productions@abinbev.com"
        elif dep == "2":
            email = "rnd@abinbev.com"
        elif dep == "3":
            email = "purchasing@abinbev.com"
        elif dep == "4":
            email = "marketing@abinbev.com"
        elif dep == "5":
            email = "hrm@abinbev.com"
        elif dep == "6":
            email = "accountsfinance@abinbev.com"
        elif dep == "7":
            email = "complaints@abinbev.com"

        SendEmail(
            "ankithans1947@gmail.com",
            tracker.get_slot("subject"),
            tracker.get_slot("message")
        )
        SendEmail(
            "pandeyaryamaan@gmail.com",
            tracker.get_slot("subject"),
            tracker.get_slot("message")
        )
        dispatcher.utter_message(
            "Thanks for providing the feedback. We have sent your queries and feedbacks to {}".format(email))
        return [AllSlotsReset()]


def SendEmail(toaddr, subject, message):
    fromaddr = "aryamaan231101@gmail.com"
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    try:
        s.login(fromaddr, "7752912609")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
    except:
        print("An Error occured while sending email.")
    finally:
        s.quit()


class ActionactionAppointment(Action):

    def name(self) -> Text:
        return "action_appointment_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        query_type = tracker.get_slot("query_type")

        contact = 9998887776
        if query_type == "1":
            contact = 9998889998
        elif query_type == "2":
            contact = 9998887778
        elif query_type == "3":
            contact = 6663354577
        elif query_type == "4":
            contact = 6667788875

        # notify the agent that they need to call

        n = random.randint(100, 999)

        dispatcher.utter_message(
            text=f"Thanks for contacting us! We have notified our agents regaurding your query, you will soon recieve a call reguarding your issue.\n\nTicket {n} opened\nissue: {tracker.get_slot('query_brief')}")

        slot = tracker.get_slot('select_date_time')
        if slot == 1:
            slot = '2021-05-05'
        elif slot == 2:
            slot = '2021-05-06'
        elif slot == 3:
            slot = '2021-05-07'
        else:
            slot = '2021-05-05'
        date = '2021-05-05'
        start_time = '4:00pm'
        end_time = '11:00pm'

        start_date_str = date + start_time
        end_date_str = date + end_time

        start_date = dt.datetime.strptime(start_date_str, '%Y-%m-%d%I:%M%p')
        end_date = dt.datetime.strptime(end_date_str, '%Y-%m-%d%I:%M%p')
        e = create_event(tracker.get_slot("query_type"), start_date.isoformat(
        ), end_date.isoformat(), tracker.get_slot('query_brief'), tracker.get_slot('prefered_email'))
        dispatcher.utter_message(
            text=f"Event has been added to your calender. Follow the url to procees further {e}")

        return [AllSlotsReset()]


def create_event(name, start, end, description, email):
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'actions\secret.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': name,
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': description,
        'start': {
            'dateTime': start,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'attendees': [
            {'email': email},
            {'email': 'sbrin@example.com'},
            {'email': 'ankithans1947@gmail.com'},
            {'email': 'pandeyaryamaan@gmail.com'}
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    return event.get('htmlLink')


class Actionbeerdiscounts(Action):

    def name(self) -> Text:
        return "action_discount_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        beers = [
            {
                "id": "1",
                "name": "Budweiser",
                "discount": "22.2% off on Budweiser"
            },
            {
                "id": "2",
                "name": "Corona Extra",
                "discount": "23.567% off on Corona Extra"
            },
            {
                "id": "3",
                "name": "Stella Artois",
                "discount": "29% off on Stella Artois"
            },
            {
                "id": "4",
                "name": "Aguila",
                "discount": "24.678% off on Aguila"
            },
            {
                "id": "5",
                "name": "Becks Blue",
                "discount": "23.54% off on Becks Blue"
            },
            {
                "id": "6",
                "name": "Bogota Lager",
                "discount": "24% off on Bogota Lager"
            },
            {
                "id": "7",
                "name": "Contender",
                "discount": "51% off on Contender"
            },
            {
                "id": "8",
                "name": "Brahma Chopp",
                "discount": "21% off on Brahma Chopp"
            },
            {
                "id": "9",
                "name": "Bud Light",
                "discount": "19.5% off on Bud Light"
            },
            {
                "id": "10",
                "name": "Cass Fresh",
                "discount": "18% off on Cass Fresh"
            },
            {
                "id": "11",
                "name": "Castle Lager",
                "discount": "16% off on Castle Lager"
            },
            {
                "id": "12",
                "name": "Cusquena Dorada",
                "discount": "10.5% off on Cusquena Dorada"
            },
            {
                "id": "13",
                "name": "Eagle Lager",
                "discount": "11% off on Eagle Lager"
            },
            {
                "id": "14",
                "name": "Goose Island Bourbon County Brand Stout",
                "discount": "12.38% off on Goose Island Bourbon County Brand Stout"
            },
            {
                "id": "15",
                "name": "Harbin",
                "discount": "15% off on Harbin"
            },
            {
                "id": "16",
                "name": "Haywards 5000",
                "discount": "9.5% off on Haywards 5000"
            },
            {
                "id": "17",
                "name": "Hero",
                "discount": "12.34% off on Hero"
            },
            {
                "id": "18",
                "name": "Hoegarden",
                "discount": "20% off on Hoegarden"
            },
            {
                "id": "19",
                "name": "Jupiler",
                "discount": "32% off on Jupiler"
            },
            {
                "id": "20",
                "name": "Labatt Blue",
                "discount": "27% off on Labatt Blue"
            },
            {
                "id": "21",
                "name": "Leffe",
                "discount": "14% off on Leffe"
            },
            {
                "id": "22",
                "name": "Michelob ULTRA",
                "discount": "12% off on Michleblob ULTRA"
            },
            {
                "id": "23",
                "name": "Modelo Especial",
                "discount": "15% off on Modelo Especial"
            },
            {
                "id": "24",
                "name": "Patagonia 24.7",
                "discount": "17.7% off on Patagonia"
            },
            {
                "id": "25",
                "name": "Quilmes",
                "discount": "22.5% off on Quilmes"
            },
            {
                "id": "26",
                "name": "Salva Vida",
                "discount": "28% off on Salva Vida"
            },
            {
                "id": "27",
                "name": "Skol",
                "discount": "31% off on Skol"
            },
            {
                "id": "28",
                "name": "Victoria",
                "discount": "29% off on Victoria"
            },
            {
                "id": "29",
                "name": "Wals Brut",
                "discount": "32.2% off on Wals Brut"
            },
            {
                "id": "30",
                "name": "Heineken",
                "discount": "11.1% off on Heineken"
            }

        ]
        beer_id = tracker.get_slot("beer_id")

        a = "beer is unavailable!!"

        for b in beers:
            if b["id"] == beer_id:
                discount = b["discount"]
                dispatcher.utter_message(text=f"{discount}")
                return [AllSlotsReset()]

        dispatcher.utter_message(text=f"{a}")

        return [AllSlotsReset()]


class ActionMailSignups(Action):

    def name(self) -> Text:
        return "action_mail_signups"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name_of_customer23 = tracker.get_slot("name_of_customer")
        email_of_customer23 = tracker.get_slot("email_of_customer")
        contact_of_customer23 = tracker.get_slot("contact_of_customer")

        dispatcher.utter_message(text=f"{dt.datetime.now()}")
        DataUpdate(name_of_customer23, email_of_customer23,
                   contact_of_customer23)
        dispatcher.utter_message(
            "Thanks for providing the details. We are so happy that one more gem got added to our communtiy!")

        return [AllSlotsReset()]


class ActionWarehouse(Action):

    def name(self) -> Text:
        return "action_warehouse"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"{dt.datetime.now()}")

        warehousedb = [
            {
                "id": "1Abinbev",
                "location": "Carton of Budweiser is present in drawer 2 of rack 5."
            },
            {
                "id": "2Abinbev",
                "location": "Carton of Corona is present in drawer 1 of rack 7."
            },
            {
                "id": "3Abinbev",
                "location": "Carton of Stella Artois is present in drawer 5 of rack 8."
            },
            {
                "id": "4Abinbev",
                "location": "Carton of Aguila is present in drawer 11 of rack 42."
            },
            {
                "id": "5Abinbev",
                "location": "Carton of Becks Blue is present in drawer 12 of rack 25."
            },
            {
                "id": "6Abinbev",
                "location": "Carton of Bogota Lager is present in drawer 13 of rack 23."
            },
            {
                "id": "7Abinbev",
                "location": "Carton of Contender is present in drawer 17 of rack 85.",
            },
            {
                "id": "8Abinbev",
                "location": "Carton of Brahma Chopp is present in drawer 18 of rack 57."
            },
            {
                "id": "9Abinbev",
                "location": "Carton of Bud Light is present in drawer 14 of rack 55."
            },
            {
                "id": "10Abinbev",
                "location": "Carton of Cass Fresh is present in drawer 19 of rack 65."
            },
            {
                "id": "11Abinbev",
                "location": "Carton of Castle Lager is present in drawer 22 of rack 73."
            },
            {
                "id": "12Abinbev",
                "location": "Carton of Cusquena Dorada is present in drawer 25 of rack 79."
            },
            {
                "id": "13Abinbev",
                "location": "Carton of Eagle Lager is present in drawer 7 of rack 92."
            },
            {
                "id": "14Abinbev",
                "location": "Carton of Goose Island Bourbon County Brand Stout is present in drawer 19 of rack 67."
            },
            {
                "id": "15Abinbev",
                "location": "Carton of Harbin is present in drawer 13 of rack 53."
            },
            {
                "id": "16Abinbev",
                "location": "Carton of Haywards 5000 is present in drawer 8 of rack 99."
            },
            {
                "id": "17Abinbev",
                "location": "Carton of Hero is present in drawer 4 of rack 43."
            },
            {
                "id": "18Abinbev",
                "location": "Carton of Hoegarden is present in drawer 9 of rack 22."
            },
            {
                "id": "19Abinbev",
                "location": "Carton of Jupiler is present in drawer 7 of rack 61.",
            },
            {
                "id": "20Abinbev",
                "location": "Carton of Labatt Blue is present in drawer 6 of rack 52."
            },
            {
                "id": "21Abinbev",
                "location": "Carton of Leffe is present in drawer 7 of rack 32."
            },
            {
                "id": "22Abinbev",
                "location": "Carton of Michleblob ULTRA is present in drawer 6 of rack 11."
            },
            {
                "id": "23Abinbev",
                "location": "Carton of Modelo Especial is present in drawer 7 of rack 41."
            },
            {
                "id": "24Abinbev",
                "location": "Carton of Patagonia is present in drawer 9 of rack 17. "
            },
            {
                "id": "25Abinbev",
                "location": "Carton of Quilmes is present in drawer 2 of rack 5."
            },
            {
                "id": "26Abinbev",
                "location": "Carton of Salva Vida is present in drawer 5 of rack 40."
            },
            {
                "id": "27Abinbev",
                "location": "Carton of Skol is present in drawer 7 of rack 88."
            },
            {
                "id": "28Abinbev",
                "location": "Carton of Victoria is present in drawer 13 of rack 44."
            },
            {
                "id": "29Abinbev",
                "location": "Carton of Wals Brut is present in drawer 11 of rack 33."
            },
            {
                "id": "30Abinbev",
                "location": "Carton of Heineken is present in drawer 8 of rack 11."
            }

        ]
        a = "Sorry you are entering the wrong unique ID.Failed to authorize, please write the correct ID to know the location of product in warehouse."

        unique_id = tracker.get_slot("id_of_product")

        for i in warehousedb:
            if i["id"] == unique_id:
                location23 = i["location"]
                dispatcher.utter_message(text=f"{location23}")
                return [AllSlotsReset()]

        dispatcher.utter_message(text=f"{a}")

        return [AllSlotsReset()]
