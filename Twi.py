from twilio.rest import Client
from time import sleep

import methods


def get_phonenumbers(account_sid: str, auth_token: str):
    """
    Get a list of incoming phone numbers from a Twilio account.

    Args:
        account_sid (str): Twilio Account SID.
        auth_token (str): Twilio Auth Token.

    Returns:
        list: List of incoming phone numbers.
    """
    client                          = Client(account_sid, auth_token)
    incoming_phone_numbers          = client.incoming_phone_numbers.list(limit=20)
    # incoming_phone_numbers.pop(-1)
    return incoming_phone_numbers


def SendBulk(account_sid, auth_token, sleeptime, letter, leads_list):
    """
    Send bulk SMS messages using the Twilio API, cycling through a list of sender phone numbers.

    Args:
        account_sid (str):          Twilio Account SID.
        auth_token (str):           Twilio Auth Token.
        sleeptime (int):            Time in seconds to sleep between sending messages.
        letter (str):               The message content.
        leads_list (str):           List of String containing recipient phone numbers.

    Returns:
        None
    """
    try:
        i                           = 0                                                        # Initialize a counter for sent SMS
        client                      = Client(account_sid, auth_token)                          # Create Twilio client instance
        phone_list_index            = 0                                                        # Initialize index to track phone numbers in phone_list

        # Get sender phone numbers using Twilio API
        # phone_list (list of str):   List of sender phone numbers.
        phone_list                  = methods.to_str_phones_list(get_phonenumbers(account_sid, auth_token))

        for number in leads_list:
            try:
                choice              = phone_list[phone_list_index]                              # Select sender phone number
                phone_list_index    = (phone_list_index + 1) % len(phone_list)                  # Cycle through phone_list
                # Send SMS using Twilio API
                client.messages.create(
                    body            = letter,
                    from_           = choice,
                    to              = number.strip()
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
                if "Authenticate" in str(p):
                    print("ACCOUNT SUSPENDED (TOPUP OR POLICY BREACH)")
                    exit()

                print(p)

    except Exception as e:
        print(e)
    else:
        print("DONE SENDING.")




