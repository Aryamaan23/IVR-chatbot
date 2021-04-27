# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


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


ottp = random.randint(1000, 9999)



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
                "name": "abc",
                "price": 556,
                "alchohal_content": 10
            },
            {
                "name": "def",
                "price": 224,
                "alchohal_content": 100
            },
            {
                "name": "aryamaan",
                "price": 12135,
                "alchohal_content": 98
            },
            {
                "name": "ankit",
                "price": 5789,
                "alchohal_content": 5
            },
            {
                "name": "yo",
                "price": 7898,
                "alchohal_content": 50
            },
            {
                "name": "brio",
                "price": 68,
                "alchohal_content": 67
            }
        ]

        def closest(lst, K):
            return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

        choice = tracker.get_slot("search_prod_choice")
        value = tracker.get_slot("search_prod_value")

        if choice == "1":
            pr = []
            for p in products:
                pr.append(p["name"])
            nearest = get_close_matches(value, pr)
            
            for p in products:
                if p["name"] == nearest[0]:
                    dispatcher.utter_message(text=f"{p}")
                    break

        elif choice == "2":
            pr = []
            for p in products:
                pr.append(p["price"])
            nearest = closest(pr, int(value))
            for p in products:
                if p["price"] == nearest:
                    dispatcher.utter_message(text=f"{p} {nearest}")
                    break
                    
        elif choice == "3":
            pr = []
            for p in products:
                pr.append(p["alchohal_content"])
            nearest = closest(pr, int(value))
            for p in products:
                if p["alchohal_content"] == nearest:
                    dispatcher.utter_message(text=f"{p} {nearest}")
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
            amount = "You have to pay ₹" + res["amount"] + " upto date " + str(dat)
        else:
            amount = "You have paid ₹" + res["amount"] + " at " + str(dat)

        dispatcher.utter_message(text=f"Payment Status for order Id {ID} is {status}. {amount}")

        return [AllSlotsReset()]


class ActionAuth(Action):

    def name(self) -> Text:
        return "action_auth"
    
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
                to='+91'+phone
            )

        return {'phone_number': slot_value}

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        otp = tracker.get_slot("otp")
        if str(otp) == str(ottp):
            dispatcher.utter_message(text=f"Your phone is verified successfully!")
        else:
            dispatcher.utter_message(text=f"Unauthorized!")

        return [AllSlotsReset()]


class ValidateAuthForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_auth_form"
    
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

class ActionEmailSubmit(Action):
    def name(self) -> Text:
        return "action_mail_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text,Any]]:

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
        dispatcher.utter_message("Thanks for providing the feedback. We have sent your queries and feedbacks to {}".format(email))
        return [AllSlotsReset()]

def SendEmail(toaddr,subject,message):
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

        dispatcher.utter_message(text=f"Thanks for contacting us! We have notified our agents regaurding your query, you will soon recieve a call reguarding your issue.\n\nTicket {n} opened\nissue: {tracker.get_slot('query_brief')}")
    
        return []



class Actionbeerdiscounts(Action):
    
    def name(self) -> Text:
        return "action_discount_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            beers=[
               {
                 "id":"1",
                 "name":"Budweiser",
                 "discount":"22.2% off on Budweiser"
               },
               {
                   "id":"2",
                   "name":"Corona Extra",
                   "discount":"23.567% off on Corona Extra"
               },
               {
                   "id":"3",
                   "name":"Stella Artois",
                   "discount":"29% off on Corona Extra"
               },
               {
                   "id":"4",
                   "name":"Aguila",
                   "discount":"24.678% off on Aguila"
               },
               {
                   "id":"5",
                   "name":"Becks Blue",
                   "discount":"23.54% off on Becks Blue"
               },
               {
                   "id":"6",
                   "name":"Bogota Lager",
                   "discount":"24% off on Corona Extra"
               },
               {
                   "id":"7",
                   "name":"Contender",
                   "discount":"51% off on Corona Extra"
               },
               {
                   "id":"8",
                   "name":"Brahma Chopp",
                   "discount":"21% off on Brahma Chopp"
               },
               {
                   "id":"9",
                   "name":"Bud Light",
                   "discount":"19.5% off on Bud Light"
               },
               {
                   "id":"10",
                   "name":"Cass Fresh",
                   "discount":"18% off on Cass Fresh"
               },
               {
                   "id":"11",
                   "name":"Castle Lager",
                   "discount":"16% off on Corona Extra"
               },
               {
                   "id":"12",
                   "name":"Cusquena Dorada",
                   "discount":"10.5% off on Cusquena Dorada"
               },
               {
                   "id":"13",
                   "name":"Eagle Lager",
                   "discount":"11% off on Eagle Lager"
               },
               {
                   "id":"14",
                   "name":"Goose Island Bourbon County Brand Stout",
                   "discount":"12.38% off on Goose Island Bourbon County Brand Stout"
               },
               {
                   "id":"15",
                   "name":"Harbin",
                   "discount":"15% off on Harbin"
               },
               {
                   "id":"16",
                   "name":"Haywards 5000",
                   "discount":"9.5% off on Haywards 5000"
               },
               {
                   "id":"17",
                   "name":"Hero",
                   "discount":"12.34% off on Hero"
               },
               {
                   "id":"18",
                   "name":"Hoegarden",
                   "discount":"20% off on Hoegarden"
               },
               {
                   "id":"19",
                   "name":"Jupiler",
                   "discount":"32% off on Jupiler"
               },
               {
                   "id":"20",
                   "name":"Labatt Blue",
                   "discount":"27% off on Labatt Blue"
               },
               {
                   "id":"21",
                   "name":"Leffe",
                   "discount":"14% off on Leffe"
               },
               {
                   "id":"22",
                   "name":"Michelob ULTRA",
                   "discount":"12% off on Michleblob ULTRA"
               },
               {
                   "id":"23",
                   "name":"Modelo Especial",
                   "discount":"15% off on Modelo Especial"
               },
               {
                   "id":"24",
                   "name":"Patagonia 24.7",
                   "discount":"17.7% off on Patagonia"
               },
               {
                   "id":"25",
                   "name":"Quilmes",
                   "discount":"22.5% off on Quilmes"
               },
               {
                   "id":"26",
                   "name":"Salva Vida",
                   "discount":"28% off on Salva Vida"
               },
               {
                   "id":"27",
                   "name":"Skol",
                   "discount":"31% off on Skol"
               },
               {
                   "id":"28",
                   "name":"Victoria",
                   "discount":"29% off on Victoria"
               },
               {
                   "id":"29",
                   "name":"Wals Brut",
                   "discount":"32.2% off on Wals Brut"
               },
               {
                   "id":"30",
                   "name":"Heineken",
                   "discount":"11.1% off on Heineken"
               }
               
            ]
            beer_id=tracker.get_slot("beer_id")

            a="beer is unavailable!!"
           

            for b in beers:
                if b["id"]==beer_id:
                    discount=b["discount"]
                    dispatcher.utter_message(text=f"{discount}")
                    return [AllSlotsReset()]
            
            dispatcher.utter_message(text=f"{a}")

            return [AllSlotsReset()]