import constants
import requests
import json
import random

def lambda_handler(event, context):
    """ Entry Point for Lambda Function. """
    # Extract intent object
    intent = event["sessionState"]["intent"]
    inputTranscript = event["inputTranscript"]
    sessionAttributes = event['sessionState'].get('sessionAttributes')
    inputMode = event.get('inputMode')
    
    # Handle input TRY_API to extended Fulfillment
    if inputTranscript == constants.TRY_API_INPUT:
        return handleTryAPI(sessionAttributes)
    
    # Handle Intent
    if intent["name"] == constants.FIND_API_INTENT_NAME: 
        # FindAPI Intent
        return handleIntentFindAPI(intent, inputTranscript, inputMode)
    elif intent["name"] == constants.TRY_API_INTENT_NAME:
        # TryAPI Intent
        return handleTryAPI(sessionAttributes)
    else: 
        # Default Action 
        return handleIntentDefault(intent, inputTranscript)

""" ===============
    Intent Handlers 
    ===============
"""
def handleIntentDefault(intent, inputTranscript):
    """ Handles Default Intent when no other intent is recognized. Returns intent object with state set to Failed. """
    # Default Response Object
    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": intent["name"],
                "state": constants.INTENT_FAILED_STATE
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "I'm sorry, I was unable to understand your request."
            }
        ],
        "inputTranscript": inputTranscript
    }
    return response

def handleIntentFindAPI(intent, inputTranscript, inputMode):
    """ Handles FindAPI intent. Retrieves relevant APIs based on values of slots. """
    # Default Response Object
    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": intent["name"],
                "state": constants.INTENT_FULFILLED_STATE
            },
            "sessionAttributes": {}
        },
        "messages": [],
        "inputTranscript": inputTranscript,
        "contentType": 'Text',
        "responseContentType": 'Text'
    }
    # Extract Slots
    slots = intent["slots"]
    #keywords = getSlotValues(slots[constants.KEYWORDS_SLOT_NAME])
    TFSBusinessDomain = getSlotValues(slots[constants.TFSBUSINESSDOMAIN_SLOT_NAME])
    InformationDomain = getSlotValues(slots[constants.INFORMATIONDOMAIN_SLOT_NAME])
    Process = getSlotValues(slots[constants.PROCESS_SLOT_NAME])
    APIType = getSlotValues(slots[constants.APITYPE_SLOT_NAME])
    
    # Get API from TFS API Portal Endpoint
    api, sessionAttributes, error = getAPI(inputTranscript, TFSBusinessDomain, InformationDomain, Process, APIType)
    
    # Add initial response message
    initial_response_index = random.randint(0, len(constants.FIND_API_INITIAL_RESPONSES) - 1)
    response['messages'].append({'contentType': "PlainText", 'content': constants.FIND_API_INITIAL_RESPONSES[initial_response_index]})
      
    # Return Response Object
    if error: # Error encountered in connecting to TFS API Portal endpoint
        firstMessage = {"contentType": "PlainText", "content": "Unfortunately, I was not able to connect to the TFS API Portal at this time."}
        response["messages"].append(firstMessage)
    elif api is None: # No APIs found
        firstMessage = {"contentType": "PlainText", "content": "I did not find an APIs matching your input. Please describe to me what you are looking for. For example, \"I need an API to view financial account information\"."}
        response["messages"].append(firstMessage)
    else: # Speech & text input
        buttons = None
        if sessionAttributes is not None and sessionAttributes.get('API_ENDPOINT') is not None:
            buttons = [{'text': "Try API", 'value': constants.TRY_API_INPUT}]
        # Lex V1 Reponse card for use with Voice Input only
        responseCard = {
            "version": "1",
            "contentType": "application/vnd.amazonaws.card.generic",
            "genericAttachments": [
                {
                'title': api['name'],
                'subtitle': api['description'],
                'buttons': buttons
                }
            ]
        }
        # Lex V2 Reponse Card
        responseCardV2 = {
            'title': api['name'],
            'subtitle': api['description'],
            'buttons': buttons
        }
        
        response['sessionState']['sessionAttributes'] = sessionAttributes
        if inputMode == "Speech":
            response['sessionState']['sessionAttributes']['appContext'] = json.dumps({
                'responseCard': responseCard
                })
            message_index = random.randint(0, len(constants.FIND_API_MESSAGES) - 1)
            response['messages'][0] = {"contentType": "PlainText", 'content': response['messages'][0]['content'] + " " + constants.FIND_API_MESSAGES[message_index]}
        else:
            message_index = random.randint(0, len(constants.FIND_API_MESSAGES) - 1)
            response['messages'].append({'contentType': "PlainText", 'content': constants.FIND_API_MESSAGES[message_index]})
        response['messages'].append({'contentType': "ImageResponseCard", "imageResponseCard": responseCardV2})
        
    return response
    
def handleTryAPI(sessionAttributes):
    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": constants.TRY_API_INTENT_NAME,
                "state": constants.INTENT_FULFILLED_STATE
            },
            "sessionAttributes": sessionAttributes
        },
        "messages": [],
        "inputTranscript": constants.TRY_API_INPUT,
    }
    if sessionAttributes is None or sessionAttributes.get('API_ENDPOINT') is None or sessionAttributes.get('API_URL') is None:
        response['messages'].append({'contentType': "PlainText", "content": "Unfortunately, I am unable to provide a sample endpoint for this API."})
    else:
        firstMessage = {'contentType': "PlainText", "content": "Here is a sample endpoint for the " + sessionAttributes['API_NAME'] + " API. Test the URL generated using an API client or your web browser!"}
        response['messages'].append(firstMessage)
        imageResponseCard = {
            'title': sessionAttributes['API_ENDPOINT'],
            'subtitle': sessionAttributes['API_URL']
        }
        response['messages'].append({'contentType': "ImageResponseCard", 'imageResponseCard': imageResponseCard})
    return response
    
""" ================
    Get APIs for Lex
    ================
"""

def getAPI(userText, TFSBusinessDomain, InformationDomain, Process, APIType):
    """ userText is a str, all other slots are a list of str. """
    queries = []
    if userText is not None:
        queries.append(userText)
    if TFSBusinessDomain is not None:
        queries = queries + TFSBusinessDomain
    if InformationDomain is not None:
        queries = queries + InformationDomain
    if Process is not None:
        queries = queries + Process
    if APIType is not None:
        queries = queries + APIType
    
    res = requests.get(constants.BEANSTALK_QUERY_URL, params={'queries': queries, 'threshold': constants.BEANSTALK_QUERY_THRESHOLD})
    if res.status_code != 200:
        return None, None, True # Error
    
    api = None
    content = json.loads(res.content)

    if content is None or len(content) == 0:
        return None, None, False # No results found, but not error
    
    sessionAttributes = {}
    if content[0].get('Name') is not None:
        api = {'name': content[0]['Name'], 'description': content[0]['Description']}
        sessionAttributes = {
            'API_NAME': content[0]['Name'],
            'API_ID': content[0]['Id'],
            'API_DESCRIPTION': content[0]['Description']
            }
        
    if content[0].get('API_ENDPOINT') is not None:
        sessionAttributes.update({
            'API_ENDPOINT': content[0]['API_ENDPOINT'],
            'API_URL': content[0].get('API_URL')
        })
    
    return api, sessionAttributes, False
    

""" ================
    Helper Functions 
    ================
"""
def getSlotValues(slot):
    """ Recursively Extract slot values and place them into single list. """
    if slot is None:
        return []
    if slot.get("shape") is None or slot["shape"] == constants.SCALAR_SLOT_SHAPE:
        # Base Case, the slot shape is Scalar.
        if len(slot["value"]["resolvedValues"]) == 0:
            # In this case, there were no resolved values by Lex.
            return [slot["value"]["interpretedValue"]]
        else:
            # Otherwise, Lex was able to resolve the user input to some other values, so use that.
            return slot["value"]["resolvedValues"]
    else:
        # Recursive Case, the slot shape is List.
        result = []
        for value in slot["values"]: # for each individual value (structured as a slot object itself), get the slot values.
            result = result + getSlotValues(value)
        return result

def apiToPlainText(api):
    """ api must be object with a 'name' and 'description' attribute """
    name = api['name']
    description = api['description']
    if len(description) > 250: # truncate description at 250 characters
        description = description[:247] + "..." # combined length is 250
    #text = name + ": " + description
    return [{'contentType': 'PlainText', 'content': "Here is an API I found: " + name}, {'contentType': 'PlainText', 'content': description}]
    
def apiToImageResponseCard(api):
    """ api must be object with a 'name' and 'description' attribute """
    name = api['name']
    description = api['description']
    if len(description) > 250: # Lex requirement that description is at most 250 characters
        description = description[:247] + "..." # combined length is 250
    imageResponseCard = {
        'title': name,
        'subtitle': description,
        'buttons': [
            {
                'text': "Try API",
                'value': constants.TRY_API_INPUT,
            }
        ]
    }
    return [{'contentType': "ImageResponseCard", 'imageResponseCard': imageResponseCard}]
