import logging
from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted, UserUtteranceReverted, ConversationPaused

import requests
URL = "https://api.postalpincode.in/pincode"

logger = logging.getLogger(__name__)

class ActionEntity(Action):
    ''' this class performs the action of remembering pincode of the user if
        there was any pincode input before '''
    def name(self) -> Text:
        return "action_use_previous_pincode"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        PINCODE = tracker.get_slot('pincode1')
        print("previous pincode")
        print("------------\n", PINCODE)
        print(tracker.latest_message['intent'])


        if tracker.latest_message['intent']['name']=='deny':
            print("previous pincode deny")
            dispatcher.utter_message(text = "Please share the pincode?")
            return []
        
        elif tracker.latest_message['intent']['name']=='affirm':
            print("previous pincode affirm")
            response = requests.get(f"{URL}/{tracker.get_slot('pincode1')}").json()
            result = ""
            DISTRICT = ""
            try:
                if(response[0]["Status"]=="Success" and response[0]["PostOffice"]):
                    DISTRICT = str(response[0]['PostOffice'][0]['District'])
                    STATE    = response[0]['PostOffice'][0]['State']
                    result = DISTRICT + " " + STATE
                elif(response[0]["Status"] == "Error"):
                    result = "No address found for given pincode"
                
                dispatcher.utter_message(text = result)
            except:
                pass
            print('action3 affirm')
            return [SlotSet("district", DISTRICT)]
        else:
            dispatcher.utter_message(
            text=f"Do you want to get the resources for - {PINCODE}. Press yes to confirm and no to change another pincode?")

        return []