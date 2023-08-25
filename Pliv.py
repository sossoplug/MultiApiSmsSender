from plivo import RestClient as PlivoClient
from time import sleep
import methods

def get_phonenumbers(auth_id: str, auth_token: str):
    """
    Get a list of incoming phone numbers from a Plivo account.

    Args:
        auth_id (str):      Plivo Auth ID.
        auth_token (str):   Plivo Auth Token.

    Returns:
        list: List of incoming phone numbers.
    """
    try:
        client              = PlivoClient(auth_id, auth_token)
        response            = client.numbers.list()
        numbers             = response[0]['objects']
        return numbers
    except Exception as e:
        print(e)
        return []


def get_plivo_phonenumbers(auth_id: str, auth_token: str):
    """
    Get a list of incoming phone numbers from a Plivo account.

    Args:
        auth_id (str):      Plivo Auth ID.
        auth_token (str):   Plivo Auth Token.

    Returns:
        list: List of incoming phone numbers.
    """
    try:
        client                  = PlivoClient(auth_id, auth_token)
        response                = client.numbers.list()
        numbers                 = response[0]['objects']
        return numbers
    except Exception as e:
        print(e)
        return []


def SendPlivoBulk(auth_id, auth_token, sleeptime, letter, leads_list):
    """
    Send bulk SMS messages using the Plivo API, cycling through a list of sender phone numbers.

    Args:
        auth_id (str):              Plivo Auth ID.
        auth_token (str):           Plivo Auth Token.
        sleeptime (int):            Time in seconds to sleep between sending messages.
        letter (str):               The message content.
        leads_list (str):           List of String containing recipient phone numbers.

    Returns:
        None
    """
    try:
        i                   = 0                                                        # Initialize a counter for sent SMS
        client              = PlivoClient(auth_id, auth_token)                         # Create Plivo client instance
        phone_list          = methods.to_str_phones_list(get_plivo_phonenumbers(auth_id, auth_token))  # Get sender phone numbers using Plivo API
        phone_list_index    = 0                                                        # Initialize index to track phone numbers in phone_list


        for number in leads_list:
            try:
                choice              = phone_list[phone_list_index]                 # Select sender phone number
                phone_list_index    = (phone_list_index + 1) % len(phone_list)     # Cycle through phone_list
                # Send SMS using Plivo API
                response = client.messages.create(
                    src=choice,
                    dst=number.strip(),
                    text=letter
                )
                i += 1                                                             # Increment the counter
                # Print a report for the sent SMS
                print(f'Sending From  {choice}')
                print(f'Sending SMS to {number.strip()}')
                print(f'=== {i} SMS Sent ==== ==== from {leads_list}')
                print('---------------------')
                sleep(sleeptime)                                                   # Sleep before sending the next SMS
            except Exception as p:
                # Check if authentication issue
                if "Authentication" in str(p):
                    print("ACCOUNT SUSPENDED (TOPUP OR POLICY BREACH)")
                    exit()

                print(p)

    except Exception as e:
        print(e)
    else:
        print("DONE SENDING.")