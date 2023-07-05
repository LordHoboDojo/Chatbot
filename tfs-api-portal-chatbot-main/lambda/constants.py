""" Constants """
import os
# Slot Shapes
SCALAR_SLOT_SHAPE = "Scalar"
LIST_SLOT_SHAPE = "List"

# Intent States
INTENT_FULFILLED_STATE = "Fulfilled"
INTENT_FAILED_STATE = "Failed"

# Intent Names
FIND_API_INTENT_NAME = "FindAPI"
TRY_API_INTENT_NAME = "TryAPI"

# FindAPI Intent Slot Names
TFSBUSINESSDOMAIN_SLOT_NAME = "BusinessDomain"
INFORMATIONDOMAIN_SLOT_NAME = "InformationDomain"
PROCESS_SLOT_NAME = "Process"
APITYPE_SLOT_NAME = "APIType"

# TryAPI Intent input
TRY_API_INPUT = 'TRY_API'

# Elastic Beanstalk Server Attributes
BEANSTALK_QUERY_URL = os.environ['BEANSTALK_QUERY_URL']
BEANSTALK_QUERY_THRESHOLD = 0.3

# Possible transition messages for FIND_API fulfillment
FIND_API_INITIAL_RESPONSES = [
    "On it! Let me see what I can find for you.",
    "Got it! Looking for an API that you might want to use.",
    "Sure! Give me a few seconds to find something for you."
]
FIND_API_MESSAGES = [
    "Here is an API I found: ",
    "Is this what you are looking for? ",
    "Here is an API you may be interesed in: "
]
