class IntentMap():

    # Default constructor for init class
    def __init__(self):
        self.__map = {}

    # Matches one intent to a method to execute
    def add(self, intentName, method):
        self.__map[intentName] = method

    # execute an intent that matches with given in the response,
    # the response will be an error method if an intent does not match
    # return will be an dictionary 
    def execute_intent(self, request):
        intentName = request["queryResult"]["intent"]["displayName"]
        if intentName in self.__map:
            return self.__map[intentName](request)
        else:
            return self.errorMethod()

    # Error method triggered when intent does not match
    def errorMethod(self):
        agent = Agent()
        agent.add_message("Intent does not found on intentMap")
        return agent.get_response()

class Agent():

    # Constructor of message building class
    def __init__(self):
        self.__message = {}

    # This mettod appends a message on the response
    def add_message(self, msg):
        if not "fulfillmentText" in self.__message:
            self.__message["fulfillmentText"] = msg
        if not "fulfillmentMessages" in self.__message:
            self.__message["fulfillmentMessages"] = []
        # Appends message in message array section for multiple response
        self.__message["fulfillmentMessages"].append(
            {"text": {
                "text": [
                    msg
                ]
            }}
        )

    # Add card to response
    def add_card(self, title, subtitle, imageUri, buttonName, buttonLink):
        if not "fulfillmentMessages" in self.__message:
            self.__message["fulfillmentMessages"] = []
        self.__message["fulfillmentMessages"].append(
            {
                "card": {
                    "title": title,
                    "subtitle": subtitle,
                    "imageUri": imageUri,
                    "buttons": [
                    {
                        "text": buttonName,
                        "postback": buttonLink
                    }
                    ]
                }
            }
        )

    # Add custom payload response
    def add_custom_response(self, response):
        if not "fulfillmentMessages" in self.__message:
            self.__message["fulfillmentMessages"] = []
        self.__message["fulfillmentMessages"].append(response)

    # Add custon payload 
    def add_custom_payload(self, response):
        if not "payload" in self.__message:
            self.__message["payload"] = {}
        self.__message["payload"].update(response)


    # Get Response method
    def get_response(self):
        return self.__message

    # To String method
    def __str__(self):
        return str(self.__message)

class GoogleResponse():

    # Constructor that defines if google must expet user response
    def __init__(self, expectResponse=True):
        self.hasSimpleResponse = False
        self.hasSuggestionChips = False
        self.hasDefaultSimpleResponse = False
        self.hasDefaultSuggestionChip = False
        self.__googleMessage = {
            "google": {
                "expectUserResponse": expectResponse,
                "richResponse": {
                    "items": []
                }
            }
        }

    # Add Simple response
    def add_simple_response(self, text):
        # Change default message if its present
        if self.hasDefaultSimpleResponse:
            # search index of default response
            for val,item in enumerate(self.__googleMessage["google"]["richResponse"]["items"]):
                if "simpleResponse" in item:
                    index = val
                    break
            self.__googleMessage["google"]["richResponse"]["items"][index]["simpleResponse"]["textToSpeech"] = text
            self.hasDefaultSimpleResponse = False
        else:
            self.__googleMessage["google"]["richResponse"]["items"].append(
                self.__simple_response(text)
            )
        self.hasSimpleResponse = True


    # Add card with ActionsOnGoogle style
    def add_card(self, title, subtitle, imageUri, imageAccecibilityText, *objButtons):
        self.__add_default_simple_response()

        # Append card response
        self.__googleMessage["google"]["richResponse"]["items"].append(
            self.__basic_card(title, subtitle, imageUri, imageAccecibilityText, *objButtons)
        )
    
    # Add browse carrousel to response
    def add_browse_carrousel(self, *items):
        self.__add_default_simple_response()

        self.__googleMessage["google"]["richResponse"]["items"].append(
            self.__browse_carrousel(*items)
        )

    # Add Media Response
    def add_media_response(self, name, description, iconUrl, iconAccessibilityText, mediaUrl):
        # Required simple response
        self.__add_default_simple_response()
        # Required suggestion chip
        self.__add_default_suggestion_chip()
        # Append media response
        self.__googleMessage["google"]["richResponse"]["items"].append(
            self.__media_response( name, description, iconUrl, iconAccessibilityText, mediaUrl)
        )

    # Add Suggestion Chip to Response
    def add_suggestion_chips(self, *names):
        # Required default empty response 
        self.__add_default_simple_response()
        # Sets the Suggestions array
        if not "suggestions" in self.__googleMessage["google"]["richResponse"]:
            self.__googleMessage["google"]["richResponse"]["suggestions"] = []
        # Drop default suggestion chip
        if self.hasDefaultSuggestionChip:
            self.__googleMessage["google"]["richResponse"]["suggestions"].pop()
            self.hasDefaultSuggestionChip = False
        # Add suggestions
        for name in names:
            self.__googleMessage["google"]["richResponse"]["suggestions"].append(
                self.__suggestion_chip(name)
            )
        self.hasSuggestionChips = True

    # Add table to response
    def add_table(self, header, *rows, **extraElements):
        # Required simple response
        self.__add_default_simple_response()
        self.__googleMessage["google"]["richResponse"]["items"].append(
            self.__complex_table(header, *rows, **extraElements)
        )

    # Add list to response
    def add_list(self, *items, **extraElements):
        # Set up systemIntent if there is not present
        if not "systemIntent" in self.__googleMessage["google"]:
            self.__googleMessage["google"]["systemIntent"] = {}
            self.__googleMessage["google"]["systemIntent"]["intent"] = "actions.intent.OPTION"
            self.__googleMessage["google"]["systemIntent"]["data"] = {}
            self.__googleMessage["google"]["systemIntent"]["data"]["@type"] = "type.googleapis.com/google.actions.v2.OptionValueSpec"
        # Required simple response
        self.__add_default_simple_response()
        # append list response
        self.__googleMessage["google"]["systemIntent"]["data"].update(
            self.__list(*items,**extraElements)
        )

    # Add Carrousel to response
    def add_carrousel(self, *items):
        # Set up systemIntent if there is not present
        if not "systemIntent" in self.__googleMessage["google"]:
            self.__googleMessage["google"]["systemIntent"] = {}
            self.__googleMessage["google"]["systemIntent"]["intent"] = "actions.intent.OPTION"
            self.__googleMessage["google"]["systemIntent"]["data"] = {}
            self.__googleMessage["google"]["systemIntent"]["data"]["@type"] = "type.googleapis.com/google.actions.v2.OptionValueSpec"
        # Required simple response
        self.__add_default_simple_response()
        # append list response
        self.__googleMessage["google"]["systemIntent"]["data"].update(
            self.__carrousel(*items)
        )
        

    # Add default simple response
    def __add_default_simple_response(self):
        # Add a white message because Google assistant need at least one simple message to display card
        if not self.hasSimpleResponse:
            self.add_simple_response(" ")
            self.hasDefaultSimpleResponse = True

    # Add default suggestion chips
    def __add_default_suggestion_chip(self):
        # Add suggestion chip named "Required suggestion" for media response and others that neeed suggestions
        if not self.hasSuggestionChips:
            # Add suggestions and set hasSuggestionChips to True
            self.add_suggestion_chips("Required Suggestion")
            self.hasDefaultSuggestionChip = True

    # Simple response dictionary format
    def __simple_response(self, text):
        return {
            "simpleResponse": {
              "textToSpeech": text
            }
          }

    # Basic Card dictionary format
    def __basic_card(self, title, subtitle, imageUri, imageAccecibilityText, *buttons):
        card = {
                "basicCard": {
                    "title": title,
                    "subtitle": subtitle,
                    "formattedText": "",
                    "image": {
                        "url": imageUri,
                        "accessibilityText": imageAccecibilityText
                    },
                    "buttons": [],
                    "imageDisplayOptions": "WHITE"
                }
            }
        for button in buttons:
            card["basicCard"]["buttons"].append(button)
        return card

    # Browse Carrousel dictionary format
    def __browse_carrousel(self, *items):
        result = {
                    "carouselBrowse": {
                        "items": []
                    }
                 }
        for item in items:
            result["carouselBrowse"]["items"].append(item)
        return result

    # Media Response dictioonary format
    def __media_response(self, name, description, iconUrl, iconAccessibilityText, mediaUrl):
        return {
                    "mediaResponse": {
                    "mediaType": "AUDIO",
                    "mediaObjects": [
                        {
                        "contentUrl": mediaUrl,
                        "description": description,
                        "icon": {
                            "url": iconUrl,
                            "accessibilityText": iconAccessibilityText
                        },
                        "name": name
                        }
                    ]
                    }
                }

    # Suggestion chips dictionary format
    def __suggestion_chip(self, name):
        return {
            "title": name
          }

    # Simple Table in dictionary format
    def __simple_table(self, header, *rows):
        result = {
                    "tableCard":{
                        "rows": []
                    }
                }
        # append header and rows
        result["tableCard"].update(header)
        for row in rows:
            result["tableCard"]["rows"].append(row)
        return result
        
    # Complex Table in dictionary format
    def __complex_table(self, header, *rows, **extraElements):
        result = self.__simple_table(header, *rows)
        # if it has a subtitle, it needs title
        if "title" in extraElements and "subtitle" in extraElements:
            result["tableCard"]["title"] = extraElements["title"]
            result["tableCard"]["subtitle"] = extraElements["subtitle"]
        elif "title" in extraElements: 
            result["tableCard"]["title"] = extraElements["title"]
        # if there is an image
        if "imageUrl" in extraElements and "imageAccessibilityText" in extraElements:
            result["tableCard"]["image"] = {
                                                "url": extraElements["imageUrl"],
                                                "accessibilityText": extraElements["imageAccessibilityText"]
                                            }
        # If there is not accessibilityText
        elif "imageUrl" in extraElements:
            result["tableCard"]["image"] = {
                                                "url": extraElements["imageUrl"],
                                                "accessibilityText": "Alt Text"
                                            }
        # if there is a button
        if "buttonText" in extraElements and "buttonUrl":
            result["tableCard"]["buttons"] = [self.generate_button(extraElements["buttonText"], extraElements["buttonUrl"])]
        return result

    # List in dictionary Format
    def __list(self, *items, **extraElements ):
        result =  {
                    "listSelect": {
                    "items": []
                    }
                }
        # if Extra parameter "title" is there
        if "title" in extraElements:
            result["listSelect"]["title"] = extraElements["title"]
        # append every item found
        for item in items:
            result["listSelect"]["items"].append(
                item
            )
        return result

    # Carrousel in dictionary Format
    def __carrousel(self, *items):
        result = {
                    "carouselSelect": {
                    "items": []
                    }
                }
        # append every item found
        for item in items:
            result["carouselSelect"]["items"].append(
                item
            )
        return result

    # Generate carrousel item in dictionary format
    def generate_carrousel_item(self, title, key, synonymsList = [], description = "", imageUrl = "", imageAccecibilityText ="Alt Text"):
        # These are same items, so we return an item list
        return self.generate_list_item(title, key, synonymsList, description, imageUrl, imageAccecibilityText)

    # Generate item list in dictionary format
    def generate_list_item(self, title, key, synonymsList = [], description = "", imageUrl = "", imageAccecibilityText ="Alt Text"):
        result = {
                    "optionInfo": {
                        "key": key
                    },
                    "title": title
                 }
        if len(synonymsList) > 0:
            result["optionInfo"]["synonyms"] = synonymsList
        if description:
            result["description"] = description
        if imageUrl:
            result["image"] = {}
            result["image"]["url"] = imageUrl
            result["image"]["accessibilityText"] = imageAccecibilityText
        return result

    # Row for Table response in dictionary format
    def generate_table_row(self,*texts, **kwargs):
        dividerAfter = True
        if "dividerAfter" in kwargs:
            dividerAfter = kwargs["dividerAfter"]
        result = {
                  "cells": [],
                  "dividerAfter": dividerAfter
                }
        for text in texts:
            result["cells"].append({"text": text})
        return result

    # Row of Headers for Table Response in dictionary format
    def generate_table_header_row(self,*items):
        result = {
                    "columnProperties": []
                 }
        for item in items:
            result["columnProperties"].append(item)
        return result

    # Header item for Table in dictionary format
    def generate_table_header(self, text, alignment="CENTER"):
        # TODO: add enum for alignment options
        return {
                  "header": text,
                  "horizontalAlignment": alignment
                }

    # Item dictionary format
    def generate_browse_carrousel_item(self, title, description, footer, imageUrl, imageAccecibilityText, urlAction):
        return {
                "title": title,
                "description": description,
                "footer": footer,
                "image": {
                        "url": imageUrl,
                        "accessibilityText": imageAccecibilityText
                },
                "openUrlAction": {
                    "url": urlAction
                }
                }

    # Generate a button of Actions on Google format
    def generate_button(self, title, url):
        return {
                    "title": title,
                    "openUrlAction": {
                        "url": url
                    }
                }

    def get_response(self):
        return self.__googleMessage

# Class designed to manage request for Google Assistant
class GoogleRequest():
    
    # Constructor with request in dictionary format
    def __init__(self, request):
        self.__request = request
    
    # Search Arguments to handle input like list or carrousel
    def get_option_arguments(self):
        result = []
        # get inputs
        for element in self.__request["originalDetectIntentRequest"]["payload"]["inputs"]:
            # get args 
            for arg in element["arguments"]:
                # search for OPTION
                if "name" in arg:
                    if arg["name"] == "OPTION":
                        result.append(arg["textValue"])
        return result

    # Search Capabilities of Google Assistant
    def get_capabilities(self):
        if "availableSurfaces" in self.__request["originalDetectIntentRequest"]["payload"]:
            return self.__request["originalDetectIntentRequest"]["payload"]["availableSurfaces"][0]["capabilities"]
        else:
            return self.__request["originalDetectIntentRequest"]["payload"]["surface"]["capabilities"]
        