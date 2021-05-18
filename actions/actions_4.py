from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused

import logging
import requests
import urllib
import re

logger = logging.getLogger(__name__)
URL = "http://ec2-3-23-130-174.us-east-2.compute.amazonaws.com:8000"

class ActionEntity(Action):
    ''' this class handles the all categories returned from api '''

    def name(self) -> Text:
        return "action_use_previous_category"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("previous category")
        CATEGORY = tracker.get_slot("category")
        DISTRICT = tracker.get_slot("district")
        
        print("------------\n", CATEGORY, DISTRICT)
        print(tracker.latest_message['intent'])

        if tracker.latest_message['intent']['name']=='deny': #check denial intent in user's latest message
            print("previous categories deny")
            response = requests.get(f"{URL}/categories").json() # requesting the api for states data
            message = ""
            for cat in response["data"]:
                message = message + cat + "\n"
            dispatcher.utter_message(message)
            dispatcher.utter_message(text = "Select your category")

            return []
        elif tracker.latest_message['intent']['name']=='affirm':
            print("previous categories affirm")
            if CATEGORY:
                try:
                    CATEGORY = re.sub("\(.*?\)","",CATEGORY).replace('&', 'and')
                    DISTRICT = re.sub("\(.*?\)","",DISTRICT).replace('&', 'and')
                    
                    cat = urllib.parse.quote(CATEGORY, safe='')
                    dist = urllib.parse.quote(DISTRICT, safe='')
                    
                    print(f"{URL}/resource?city={dist}&category={cat}")
                    
                    responses = requests.get(f"{URL}/resource?city={dist}&category={cat}").json()["data"]
                    # print(responses)
                    message = ""
                        
                    for response in responses:
                        message = message + response["category"] + "\n" + response["city"] + "\n" + response["contact"] + "\n" + response["description"] + "\n" + response["organisation"] + "\n" + response["phone"] + "\n" + response["state"]
                        dispatcher.utter_message(message)
                    if not responses:
                        dispatcher.utter_message("No resources found.")

                except:
                    dispatcher.utter_message('Please Enter valid PinCode !')
                    return []
            else:
                print("No category mentioned")
        else:
            dispatcher.utter_message(
            text=f"Do you want to get {CATEGORY}. Press yes to confirm or no to change?")

        return [SlotSet("category", CATEGORY)]