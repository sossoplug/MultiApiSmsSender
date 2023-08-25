from infobip_channels.sms.channel import SMSChannel
from time import sleep
import methods
import http.client
import json


def get_infobip_phonenumbers(api_key, base_url):
    '''
    Get a list of incoming phone numbers from an InfoBip account.

    Args:
        api_key (str):  InfoBip API Key.
        base_url (str): InfoBip Base URL.

    Returns:
        list: List of incoming phone numbers.
    '''
    try:
        base_url        = base_url.replace("https://", "")
        conn            = http.client.HTTPSConnection(base_url)
        headers         = {
            'Authorization': f"App {api_key}",
            'Accept': 'application/json'
        }
        conn.request("GET", "/numbers/1/numbers", '', headers)
        res             = conn.getresponse()
        data            = res.read().decode("utf-8")
        # print(f"API Response: {data}")                                              # Print the actual API response
        numbers_data    = json.loads(data)

        phone_numbers   = [entry['number'] for entry in numbers_data['numbers']]    # Extracting just the phone numbers from the response data
        # print(phone_numbers)

        return phone_numbers

    except Exception as e:
        print(f"Error fetching InfoBip phone numbers: {e}")
        return []


def to_str_phones_list(phone_list: []):
    """
    Convert a list of phone numbers represented as strings to a list of strings.

    Args:
        phone_list ([]):    List of phone number records.

    Returns:
        [str]:              List of phone numbers converted to string.
    """
    return [str(phone) for phone in phone_list]


def send_infobip_bulk_sms_with_phonenumbers(api_key, base_url, sleeptime, letter, leads_list):
    '''
    Send bulk SMS messages using the InfoBip API, cycling through a list of sender phone numbers.

    Args:
        api_key (str):              InfoBip API Key.
        base_url (str):             InfoBip Base URL.
        sleeptime (int):            Time in seconds to sleep between sending messages.
        letter (str):               The message content.
        leads_list ([str]):         List of String containing recipient phone numbers.


    Returns:
        None
    '''

    try:
        # Initialize the SMS channel with InfoBip credentials.
        channel = SMSChannel.from_auth_params(
            {
                "base_url": base_url,
                "api_key": api_key,
            }
        )

        # Get sender phone numbers using InfoBip API
        phone_list = to_str_phones_list(get_infobip_phonenumbers(api_key, base_url))

        for number in leads_list:
            try:
                for choice in phone_list:
                    # Send SMS using InfoBip API
                    sms_response = channel.send_sms_message(
                        {
                            "messages": [
                                {
                                    "destinations": [{"to": number.strip()}],
                                    "text": letter,
                                }
                            ]
                        }
                    )

                    # Check response for success or failure
                    if sms_response["messages"][0]["status"]["groupName"] == "PENDING":
                        status = "Success"
                    else:
                        status = "Failed: " + sms_response["messages"][0]["status"]["description"]

                    # Print a report for the sent SMS
                    print(f'Sending From  {choice}')
                    print(f'Sending SMS to {number.strip()}')
                    print(f'Status:   {status}')
                    sleep(sleeptime)  # Sleep before sending the next SMS

            except Exception as e:
                print(f"Error sending SMS to {number.strip()}. Error: {e}")

    except Exception as e:
        print(f"Error in send_infobip_bulk_sms_with_phonenumbers: {e}")
    else:
        print("DONE SENDING.")