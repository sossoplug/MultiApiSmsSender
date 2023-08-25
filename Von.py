from vonage import Client, Account
from time import sleep
import vonage
import methods


# def get_phonenumbers(api_key: str, api_secret: str):
#     """
#     Get a list of incoming phone numbers from a Vonage (Nexmo) account.
#
#     Args:
#         api_key (str):      Vonage API Key.
#         api_secret (str):   Vonage API Secret.
#
#     Returns:
#         list:               List of incoming phone numbers.
#     """
#     try:
#         client                  = VonageClient(key=api_key, secret=api_secret)
#         response                = client.get_incoming_numbers()                                 # Get incoming numbers using the Vonage API
#         numbers                 = response['_embedded']['numbers']                              # Extract the list of numbers from the response
#         return numbers
#     except Exception as e:
#         print(e)
#         return []


def get_vonage_phonenumbers(api_key: str, api_secret: str):
    """
    Get a list of incoming phone numbers from a Vonage (Nexmo) account.

    Args:
        api_key (str):      Vonage API Key.
        api_secret (str):   Vonage API Secret.

    Returns:
        list: List of incoming phone numbers.
    """
    try:
        print("YOOOOOBB")
        client              = Client(key=api_key, secret=api_secret)
        account             = Account(client=client)
        response            = account.numbers.get_account_numbers({"pattern": "", "search_pattern": ""})       # Get incoming numbers using the Vonage API
        # numbers             = response['_embedded']['numbers']                              # Extract the list of numbers from the response
        print(response)

        numbers = response["numbers"]                                                                           # Extract the list of numbers from the response
        return numbers
    except Exception as e:
        print(e)
        print("YOOOOOAAA")
        return []


def get_vonage_phonenumbers(api_key: str, api_secret: str):
    """
    Get a list of incoming phone numbers from a Vonage (Nexmo) account.

    Args:
        api_key (str):      Vonage API Key.
        api_secret (str):   Vonage API Secret.

    Returns:
        list: List of incoming phone numbers.
    """
    try:
        print("YOOOOOCC")
        client                = vonage.Client(key=api_key, secret=api_secret)
        print("YOOOOOCC22")
        response              = client.numbers.get_account_numbers({"pattern": "", "search_pattern": ""})

        print(response)

        numbers               = response["numbers"]

        return numbers
    except Exception as e:
        print(e)
        return []


def send_vonage_bulk_sms_with_phonenumbers(api_key, api_secret, sleeptime, letter, leads_list):
    """
    Send bulk SMS messages using the Vonage (Nexmo) API, cycling through a list of sender phone numbers.

    Args:
        api_key (str):              Vonage API Key.
        api_secret (str):           Vonage API Secret.
        sleeptime (int):            Time in seconds to sleep between sending messages.
        letter (str):               The message content.        
        leads_list (str):           List of String containing recipient phone numbers.
    Returns:
        None
    """
    try:
        i                       = 0
        # client = VonageClient(key=api_key, secret=api_secret)
        client                  = vonage.Client(key=api_key, secret=api_secret)            # Create Vonage client instance
        sms                     = vonage.Sms(client)
        phone_list_index        = 0                                                        # Initialize index to track phone numbers in phone_list

        print("WE MADE IT")
        # Get sender phone numbers using Vonage API
        # phone_list (list of str):   List of sender phone numbers.
        phone_list              = methods.to_str_phones_list(get_vonage_phonenumbers(api_key, api_secret))

        for number in leads_list:
            try:
                choice              = phone_list[phone_list_index]                      # Select sender phone number
                phone_list_index    = (phone_list_index + 1) % len(phone_list)          # Cycle through phone_list
                # Send SMS using Vonage API
                # =====================
                # response = client.send_message({
                #     'from': choice,
                #     'to': number.strip(),
                #     'text': letter
                # })
                # =====================
                responseData = sms.send_message(
                    {
                        "from": choice,
                        "to": number.strip(),
                        "text": letter,
                    }
                )
                status              = ""

                if responseData["messages"][0]["status"] == "0":
                    status          = "Success"
                else:
                    status          = "Failed\n""Message failed with error: {responseData['messages'][0]['error-text']}"


                i += 1                                                                  # Increment the counter
                # Print a report for the sent SMS
                print(f'Sending From  {choice}')
                print(f'Sending SMS to {number.strip()}')
                print(f'Status:   {status}')
                print(f'=== {i} SMS Sent ===  === from {leads_list}')
                print('---------------------')
                sleep(sleeptime)                                                        # Sleep before sending the next SMS
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
