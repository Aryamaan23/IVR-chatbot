# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import datetime as dt 
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset


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

        product_name = tracker.get_slot("product_name")
        dispatcher.utter_message(text=f"Good bro {product_name}")

        return []


class ActionPaymentStatus(Action):
    def name(self) -> Text:
        return "action_payment_status"
    
   

    def search(id):
        for o in orders:
            if o['id'] == id:
                return o
            else:
                return "item not found!"
    
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
        
        ID = res["id"]
        status = res["payment_status"]
        dat = res["time"]
        if status == False:
            amount = "You have to pay ₹" + res["amount"] + " upto date " + str(dat)
        else:
            amount = "You have paid ₹" + res["amount"] + " at " + str(dat)

        dispatcher.utter_message(text=f"Payment Status for order Id {ID} is {status}. {amount}")
        
        return [AllSlotsReset()]