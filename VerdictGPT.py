import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def reach_verdict(statement: str) -> dict:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
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
                            "description": "opening_statement_for_true *must* start with 'The statement is *true* because... '. opening_statement_for_true *must* agree with the original user message, claiming that the verdict should be 'true', including reasons why the verdict should be 'true'."
                        },
                        "opening_statement_for_false": {
                            "type": "string",
                            "description": "opening_statement_for_false *must* start with 'The statement is *false* because... '. opening_statement_for_false must oppose the original user message, claiming that the verdict should be 'false', including reasons why the verdict should be 'false'."
                        },
                        "rebuttal_statement_for_true": {
                            "type": "string",
                            "description": "Rebuttal statement against opening_statement_for_false, insisting that the verdict should be 'true', including new reasons why the verdict should be 'true'."
                        },
                        "rebuttal_statement_for_false": {
                            "type": "string",
                            "description": "Rebuttal statement against rebuttal_statement_for_true, insisting that the verdict should be 'false', including new reasons why the verdict should be 'false'."
                        },
                        "closing_statement_for_true": {
                            "type": "string",
                            "description": "Closing statement insisting that the verdict should be 'true', including reasons why rebuttal_statement_for_false is incorrect."
                        },
                        "closing_statement_for_false": {
                            "type": "string",
                            "description": "Closing statement insisting that the verdict should be 'false', including reasons why closing_statement_for_true is incorrect."
                        },
                        "verdict": {
                            "type": "boolean",
                            "description": "Whether to return 'true' or 'false' based on all the statements above.",
                        },
                        "reason_for_verdict": {
                            "type": "string",
                            "description": "Reason for choosing 'true' for 'false' after taking all the statements above into consideration."
                        },
                        "confidence_level": {
                            "type": "integer",
                            "description": "Confidence level from 0 to 100 for the verdict, 0 being least confident while 100 being most confident."
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
                        "confidence_level"
                    ],
                },
            }
        ],
        function_call={"name": "reach_verdict"}
    )

    response = json.loads(completion.choices[0].message["function_call"]["arguments"])

    return response


statement = "Bitcoin is a ponzi."
print(f'Statement: {statement}')

response = json.dumps(reach_verdict(statement), indent=2)
print(f'Response:\n{response}')