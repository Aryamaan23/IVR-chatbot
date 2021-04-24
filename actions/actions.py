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

class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text,Any]]:

         SendEmail(
             tracker.get_slot("email"),
             tracker.get_slot("subject"),
             tracker.get_slot("message")
         )
         dispatcher.utter_message("Thanks for providing the feedback. We have sent your queries and feedbacks to {}".format(tracker.get_slot("email")))
         return []

def SendEmail(toaddr,subject,message):
    fromaddr = "aryamaan231101@gmail.com"
    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = subject

    # string to store the body of the mail
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    # filename = "/home/ashish/Downloads/webinar_rasa2_0.png"
    # attachment = open(filename, "rb")
    #
    # # instance of MIMEBase and named as p
    # p = MIMEBase('application', 'octet-stream')
    #
    # # To change the payload into encoded form
    # p.set_payload((attachment).read())
    #
    # # encode into base64
    # encoders.encode_base64(p)
    #
    # p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    #
    # # attach the instance 'p' to instance 'msg'
    # msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()


    # Authentication
    try:
        s.login(fromaddr, "7752912609")

        # Converts the Multipart msg into a string
        text = msg.as_string()

        # sending the mail
        s.sendmail(fromaddr, toaddr, text)
    except:
        print("An Error occured while sending email.")
    finally:
        # terminating the session
        s.quit()

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
