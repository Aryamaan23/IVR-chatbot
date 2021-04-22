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
            for p in products:
                if p["name"] == value:
                    dispatcher.utter_message(text=f"{p}")

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
        
        ID = res["id"]
        status = res["payment_status"]
        dat = res["time"]
        if status == False:
            amount = "You have to pay ₹" + res["amount"] + " upto date " + str(dat)
        else:
            amount = "You have paid ₹" + res["amount"] + " at " + str(dat)

        dispatcher.utter_message(text=f"Payment Status for order Id {ID} is {status}. {amount}")

        return [AllSlotsReset()]