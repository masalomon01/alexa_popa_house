"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import random 

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Popa's house rules. " \
                    " You can ask me to randomly pick a member from the Salomon family. " \
                    "  Say, help, to find out more about this skill. " \

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "  Remember, you can earn 5 Noise points, if you finesse Emiliano. " 

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Popa's house rules. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Salomon' in intent['slots']:
        favorite_color = intent['slots']['Salomon']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite Salomon is " + \
                        favorite_color + \
                        ". You can ask me your favorite Salomon by saying, " \
                        "who's my favorite Salomon?"
        reprompt_text = "You can ask me your favorite Salomon by saying, " \
                        "who's my favorite Salomon?"
    else:
        speech_output = "I'm not sure who your favorite Salomon is. " \
                        "Please try again."
        reprompt_text = "I'm not sure who your favorite Salomon is. " \
                        "You can tell me your favorite Salomon by saying, " \
                        "my favorite Salomon is blank."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_color_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
        favorite_color = session['attributes']['favoriteColor']
        speech_output = "Your favorite Salomon is " + favorite_color + \
                        ". now get over it Goodbye." + \
                        ". PS.  " + favorite_color + ". is also my favorite."
        should_end_session = True
    else:
        speech_output = "I'm not sure who your favorite Salomon is. " \
                        "You can say, my favorite Salomon is,   and then say their name."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


def salomon_randomizer():
    salomons = ["Luisa", "Mario", "Omar", "Sebatian", "Rodrigo", "Paola", "Emiliano", "Baby Jullio", "Popa Mario", "Moma Bear"]
    guilty = random.choice(salomons)
    return guilty


def get_salomon(intent, session):
    # here we are going to get the list of salomons and pick one randomly
    session_attributes = {}
    card_title = intent['name']
    should_end_session = False
    chosen_dude = salomon_randomizer()
    speech_output = "Your randomized person of interest is:  " + chosen_dude + \
                        ".   I repeat,  the P.O.I. is:  " + chosen_dude + \
                        ".  Now get to work  " + chosen_dude + ", and better luck next time! " \
                        " ha ha ha"
    reprompt_text = "  Remember, you can earn 5 Noise points, if you finesse Emiliano. " 
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_first_question(intent, session):
    session_attributes = {}
    card_title = intent['name']
    speech_output = "The first rule of Fight Club is: you do not talk about Fight Club! "
    reprompt_text = "  Remember, you can earn 5 Noise points, if you finesse Emiliano. " 
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
        
# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "RandomSalomonIntent":
        return get_salomon(intent, session)
    elif intent_name == "MySalomonIsIntent":
        return set_color_in_session(intent, session)
    elif intent_name == "WhosMySalomonIntent":
        return get_color_from_session(intent, session)
    elif intent_name == "WhatsFirstRuleIntent":
        return get_first_question(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
