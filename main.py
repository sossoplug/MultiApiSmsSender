import sys

from termcolor import colored
import InfoB
import Pliv
import Twi
import Von
import methods
from dotenv import load_dotenv, find_dotenv
from os import getenv
import threading
import time
import urllib3

try:
    # Disable urllib3 warnings
    urllib3.disable_warnings()

    # Load environment variables
    load_dotenv(find_dotenv())

    # Initialize variables
    leads           = getenv("LEADS")
    bots            = int(getenv("BOTS"))
    leads_provider  = "cleaned_leads.txt"

    # Remove duplicates from leads and create leads provider file
    methods.remove_depulicate_line(leads, leads_provider)

    # Insert test number at specified intervals
    if getenv("INSERT_TEST_NUMBER"):
        methods.add_content_at_specified_intervals(leads_provider, getenv("TEST_NUMBER"), int(getenv("INTERVAL_BETWEEN_TEST_NUMBER")))

    # Get the total number of leads
    total = methods.get_total_leads(leads_provider)

    # Display banners
    time.sleep(1)
    methods.banner(string="❇️",                  font="doom", color="black")
    methods.banner(string="All In One",          font="doom", color="black")

    time.sleep(1)
    methods.banner(string="Exclusive Sender",   font="doom", color="black")

    time.sleep(1)
    methods.banner(string="Loading wait",       font="doom", color="blue")

    time.sleep(2)
    methods.banner(string=f"-------------\n"
                          f"{total} Recipients"
                          f"\n-------------",   font="doom", color="red")

    # Dispatch && DISPLAY leads to files for threading
    methods.dispatchleads(bots, total, leads_provider, getenv("TEST_NUMBER"))


    time.sleep(2)
    methods.decompte()

    # Initialize dictionaries and lists
    leads_dict: {}      = {}
    thread_name_dict    = {}
    thread_list         = []

    # Load leads from files and create thread names
    for x in range(1, bots + 1):
        leads_dict[f"bot_leads{x}"]     = methods.load_numbers(f"bots/numbers{x}.txt")
        thread_name_dict[f"bot_{x}"]    = f"bot_{x}"

    # API choice dictionary
    print(methods.banner(string=f"Select Your Sending Api\n"
                        " 1 )  : Twilio\n" \
                        " 2 )  : Plivo\n" \
                        " 3 )  : Vonage\n" \
                        " 4 )  : InfoBip\n",
    font="doom", color="black"))
    time.sleep(3)

    # User input for selecting API
    api_choice                          = None

    number_of_api                       = int(getenv("TOTAL_OF_SUPPORTED_APIS"))

    while type(api_choice) != int:
        try:
            api_choice = int(input(methods.banner(string=f"\nEnter the Corresponding Integer:\n", font="doom", color="green")))

        except:
            print(colored("================= ERROR ================\n"
                          f"YOU MUST ENTER AN INTEGER BETWEEN 1 AND {number_of_api}\n"
                          "================= ERROR ================\n"
                          "PRESS CTR + C TO QUIT\n"
                  , "red"))
            sys.exit()

    while int(api_choice) > number_of_api:
        try:
            print(colored("================= ERROR ================\n"
                          f"YOU MUST ENTER AN INTEGER BETWEEN [1 AND {number_of_api}]\n"
                          "================= ERROR ================\n"
                          "PRESS CTR + C TO QUIT\n"
                  , "red"))
            api_choice = int(input(f"Select Your SENDING API\n \n"
                                   f"\nEnter the Corresponding INTEGER:\n"))
        except:
            print(colored("================= ERROR ================\n"
                          f"YOU MUST ENTER AN INTEGER BETWEEN 1 AND {number_of_api}\n"
                          "================= ERROR ================\n"
                          "PRESS CTR + C TO QUIT\n"
                  , "red"))

    time.sleep(1)

    # Send using TWILIO API if selected
    if api_choice == 1:

        for x in range(1, bots + 1):
            thread = threading.Thread(target=Twi.SendBulk, args=(getenv("TWI_ACCOUNT_SID"),
                                                                 getenv("TWI_AUTH_TOKEN"),
                                                                 getenv("DELAY_IN_SECOND"),
                                                                 getenv("LETTER"),
                                                                 leads_dict[f"bot_leads{x}"])
                               )
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()


    # Send using PLIVO API if selected
    if api_choice == 2:  # Assuming 2 is the code for Plivo API

        thread_list = []

        for x in range(1, bots + 1):
            thread = threading.Thread(target=Pliv.SendPlivoBulk,  # Use the Plivo send function
                                      args=(getenv("PLIV_AUTH_ID"),
                                            getenv("PLIV_AUTH_TOKEN"),
                                            int(getenv("DELAY_IN_SECOND")),
                                            getenv("LETTER"),
                                            leads_dict[f"bot_leads{x}"])
                                      )
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()


    # Send using VONAGE API if selected
    if api_choice == 3:  # Assuming 3 is the code for Vonage API

        thread_list = []

        for x in range(1, bots + 1):
            thread = threading.Thread(target=Von.send_vonage_bulk_sms_with_phonenumbers,
                                      # Use the Vonage send function
                                      args=(getenv("VON_API_KEY"),
                                            getenv("VON_API_SECRET"),
                                            int(getenv("DELAY_IN_SECOND")),
                                            getenv("LETTER"),
                                            leads_dict[f"bot_leads{x}"])
                                      )
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

    # Send using INFOBIP API if selected
    if api_choice == 4:  # Code for InfoBip API

        thread_list = []

        for x in range(1, bots + 1):
            thread = threading.Thread(target=InfoB.send_infobip_bulk_sms_with_phonenumbers,
                                      # Use the InfoBip send function
                                      args=(getenv("INFOBIP_API_KEY"),
                                            getenv("INFOBIP_BASE_URL"),
                                            int(getenv("DELAY_IN_SECOND")),
                                            getenv("LETTER"),
                                            leads_dict[f"bot_leads{x}"])
                                      )
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()
except IndexError as e:
    print("DONE SENDING")
