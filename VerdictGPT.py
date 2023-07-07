import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def reach_verdict(statement: str) -> dict:
    completion = openai.ChatCompletion.create(
        model="gpt-4-0613",
        temperature=0,
        messages=[
            {"role": "system", "content": "You provide a verdict after coming up and considering statements on both sides of a topic."},
            {"role": "user", "content": statement}
        ],
        functions=[
            {
                "name": "reach_verdict",
                "description": "Coming up with arguments from both sides of a topic (provided by the user) and reach a verdict in the form of a boolean. Must start with a supporting statement agreeing with the original user message. Then an oppsing statement. Then a new supporting statement. Then a new opposing statement. Then a supporting closing statement. Then an opposing closing statemtent. Then reach verdict in the form of a boolean. Then provide reasons for the verdict. Then provide a confidence level of the verdict.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "opening_statement_for_true": {
                            "type": "string",
                            "description": f"You truly agree with the user message. opening_statement_for_true *must* start with '[{statement}] is true because... '. opening_statement_for_true *must* agree with the original user message, claiming that the verdict should be 'true', including reasons why the verdict should be 'true'."
                        },
                        "opening_statement_for_false": {
                            "type": "string",
                            "description": f"You disagree with the user message. opening_statement_for_false *must* start with '[{statement}] is false because... '. opening_statement_for_false must oppose the original user message, claiming that the verdict should be 'false', including reasons why the verdict should be 'false'. It should also provide reasons why opening_statement_for_true is incorrect."
                        },
                        "rebuttal_statement_for_true": {
                            "type": "string",
                            "description": "Rebuttal statement against opening_statement_for_false, insisting that the verdict should be 'true', including new reasons why the verdict should be 'true'. It should also provide reasons why opening_statement_for_false is incorrect."
                        },
                        "rebuttal_statement_for_false": {
                            "type": "string",
                            "description": "Rebuttal statement against rebuttal_statement_for_true, insisting that the verdict should be 'false', including new reasons why the verdict should be 'false'. It should also provide reasons why rebuttal_statement_for_true is incorrect."
                        },
                        "closing_statement_for_true": {
                            "type": "string",
                            "description": "Closing statement insisting that the verdict should be 'true', concluding all the points mentioned before. It should also provide reasons why rebuttal_statement_for_false is incorrect."
                        },
                        "closing_statement_for_false": {
                            "type": "string",
                            "description": "Closing statement insisting that the verdict should be 'false', concluding all the points mentioned before. It should also provide reasons why closing_statement_for_true is incorrect."
                        },
                        "verdict": {
                            "type": "boolean",
                            "description": "Whether to return 'true' or 'false' based on all the statements above. Consider all statements and make a decision based on the strongeest statement.",
                        },
                        "reason_for_verdict": {
                            "type": "string",
                            "description": "Reason for choosing 'true' for 'false' after taking all the statements above into consideration."
                        },
                        "confidence_level": {
                            "type": "integer",
                            "description": "Confidence level from 0 to 100 for the verdict, 0 being least confident while 100 being most confident."
                        },
                        "reason_for_confidence_level": {
                            "type": "string",
                            "description": "Explain how confidence_level was calculated."
                        },
                    },
                    "required": [
                        "opening_statement_for_true",
                        "opening_statement_for_false",
                        "rebuttal_statement_for_true",
                        "rebuttal_statement_for_false",
                        "closing_statement_for_true",
                        "closing_statement_for_false",
                        "verdict",
                        "reason_for_verdict",
                        "confidence_level",
                        "reason_for_confidence_level"
                    ],
                },
            }
        ],
        function_call={"name": "reach_verdict"}
    )

    response = json.loads(completion.choices[0].message["function_call"]["arguments"])

    return response


# statement = "America is racist."
# statement = "America is not racist."

# statement = "Gay people will go to hell."
# statement = "Gay people will go to heaven."

# statement = "Pepsi is superior to Coca-Cola."
# statement = "Coca-Cola is superior to Pepsi."

# statement = "Earth is round."
statement = "Earth is flat."

# statement = "Men who like the color pink are homosexual."
# statement = "Men who like the color pink are straight."

# statement = "It is raining right now."
# statement = "It is sunny right now."

# statement = "2 + 2 = 4"
# statement = "2 + 2 = 5"

# statement = "Dogs are cuter than cats."
# statement = "Cats are cuter than dogs."

# statement = "AI will destroy the world."
# statement = "AI will save the world."

# statement = "Bitcoin is a scam."
# statement = "US Dollars are a scam."

# Serious Debate Topics
# statement = "Guns should be banned in the US."
# statement = "Global warming is going to destroy humanity in 12 years or less."
# statement = "We should give Universal Basic Income to everyone."
# statement = "US should ban immigration."
# statement = "Doing drugs should be decriminalized."

# Conspiracy Theories
# statement = "Vaccines are dangerous or can cause autism."
# statement = "The 9/11 terrorist attacks were an inside job carried out by the US government."
# statement = "The moon landing was faked and NASA has been lying to the public for decades."
# statement = "There is a secret, powerful group of people controlling world events, known as the 'New World Order.'"
# statement = "Certain celebrities or politicians are actually reptilian aliens in disguise."
# statement = "The world is ruled by pedophiles."

# Dumb Statements
# statement = "Satoshi Nakamoto is Japanese."
# statement = "Barack Obama was born in America."
# statement = "The world will end in 2012."
# statement = "Caitlyn Jenner is a hero."
# statement = "This statement is false."
# statement = "Make America Great Again!"
# statement = "WW3 has already started."
# statement = "There are aliens already living among us."

print(f'Statement: {statement}')

response = json.dumps(reach_verdict(statement), indent=2)
print(f'Response:\n{response}')