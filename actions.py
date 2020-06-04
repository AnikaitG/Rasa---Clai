# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import random
import yaml


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    # Validation to be added -Anikait
    @staticmethod
    def extract_metadata_from_tracker(tracker: Tracker):
        events = tracker.current_state()['events']
        user_events = []
        for e in events:
            if e['event'] == 'user':
                user_events.append(e)

        return user_events[-1]['metadata']

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        metadata = ActionHelloWorld.extract_metadata_from_tracker(tracker)
        print(metadata)
        dispatcher.utter_message(text="Hello World!")

        return []


class ActionName(Action):

    def name(self) -> Text:
        return "action_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        self.names = ["Partho", "Priyanka", "Anikait"]
        resp = "You can call me " + random.choice(self.names)
        dispatcher.utter_message(text=resp)

        metadata = ActionHelloWorld.extract_metadata_from_tracker(tracker)
        print(metadata) 

        return []


class ActionGiveHelp(Action):

    def name(self) -> Text:
        return "action_give_help"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        metadata = ActionHelloWorld.extract_metadata_from_tracker(tracker)
        # print(metadata)
        page = metadata['pageContext']

        fr=open('domain.yml','r')
        data=yaml.load(fr, Loader=yaml.FullLoader)

        fr.close()

        print(data)

        # helpDict = {"project":"This is project-related help", "resource":"This is resource-related help"}
        helpDict = {
            "projects": data.get("responses").get("utter_kb_3")[0].get("text"),
            "project details": data.get("responses").get("utter_kb_3")[0].get("text"),
            "resource": data.get("responses").get("utter_kb_11")[0].get("text"),
        }
        resp = helpDict.get(page, "To be done")

        dispatcher.utter_message(text=resp)

        return []
