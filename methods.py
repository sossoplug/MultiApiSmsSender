import random
import os
import sys
import time
import hashlib
import dotenv
import pyfiglet
from termcolor import colored


def get_total_leads(filename: str):
    """
    Get the total number of leads from a file.

    Args:
        filename (str): The name of the file containing leads.

    Returns:
        int: Total number of leads.
    """
    counter = 0
    try:
        file = open(filename, "r")
        numbers = file.readlines()
        for number in numbers:
            counter += 1

    except Exception as e:
        print(e)

    return counter


def set_dotenv_var(string_value: str, key_string: str):
    """
    Set an environment variable temporarily and update it in the .env file.

    Args:
        string_value (str): The value to set for the environment variable.
        key_string (str):   The key of the environment variable in the .env file.
    """
    dotenv_file             = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    os.environ["temp"]      = string_value
    # Write changes to .env file.
    dotenv.set_key(dotenv_file, key_string, os.environ["temp"])



def set_phones(phone_list: list, counter_init):
    """
    Set incoming phone numbers as environment variables in the .env file.

    Args:
        phone_list (list):  List of incoming phone number records.
        counter_init:       Initial counter value for numbering the environment variables.
    """
    dotenv_file                     = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    counter                         = counter_init

    for record in phone_list:
        phone                       = record.phone_number
        os.environ["temp"]          = phone
        dotenv.set_key(dotenv_file, f"FROM_NUM{counter}", os.environ["temp"])
        counter                     += 1


def load_numbers(file_name: str):
    """
    Load a list of numbers from a file.

    Args:
        file_name (str):    Path to the file containing numbers.

    Returns:
        list:               List of numbers loaded from the file.
    """
    leads = []  # List to store loaded numbers

    try:
        # Open the file for reading
        with open(file_name, "r") as file:
            numbers = file.readlines()

            # Iterate through each line and append to the leads list
            for number in numbers:
                leads.append(number.replace("\n", ''))

            # Check if the leads list is empty
            if not leads:
                print("INSERT A LIST OF NUMBERS TO VERIFY")
                sys.exit()
    except Exception as e:
        print(e)

    return leads



def banner(string: str, font: str, color: str):
    """
    Print a banner text with a specified font and color.

    Args:
        string (str): The text to be converted to banner.
        font (str): The font to be used for the banner.
        color (str): The color of the banner text.

    Returns:
        None
    """
    __banner__ = pyfiglet.figlet_format(string, font=font, justify="center")
    print(colored(__banner__, color))

def decompte():
    """
    Print a countdown sequence with colored numbers.

    Args:
        None

    Returns:
        None
    """

    print(banner(string="GET READY:",               font="doom", color="black"))
    print(banner(string="\t\t------ 3",             font="doom", color="black"))
    time.sleep(1)

    print(banner(string="\t--- 2",                  font="doom", color="black"))
    time.sleep(1)

    print(banner(string="- 1",                      font="doom", color="black"))
    time.sleep(1)

    print(banner(string="-- Let's Go --\n",   font="doom",     color="black"))
    time.sleep(1)



def remove_depulicate_line(input_file_path, output_file_path):
    """
    Remove duplicate lines from an input file and write unique lines to an output file.

    Args:
        input_file_path (str): Path to the input file containing duplicate lines.
        output_file_path (str): Path to the output file to write unique lines.

    Returns:
        None
    """
    try:
        # Set to store hash values of completed lines
        completed_lines_hash = set()

        # Open the output file for writing
        with open(output_file_path, "w") as output_file:
            # Iterate through lines in the input file
            for line in open(input_file_path, "r"):
                try:
                    hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()          # Calculate the hash value of the line

                    # Check if the hash value is not already in the set
                    if hashValue not in completed_lines_hash:
                        output_file.write(line)                                                 # Write the line to the output file
                        completed_lines_hash.add(hashValue)                                     # Add the hash value to the set

                except Exception as inner_exception:
                    print(f"Error processing line: {inner_exception}")

    except Exception as outer_exception:
        print(f"An error occurred During Initial Leads Cleaning: {outer_exception}")



def add_content_at_specified_intervals(filename, new_content, lines_per_chunk):
    """
    Add new content at specified intervals in an existing file.

    Args:
        filename (str):         Path to the file where content will be added.
        new_content (str):      Content to be added at intervals.
        lines_per_chunk (int):  Number of lines between each insertion.

    Returns:
        None
    """
    try:
        # Open the file for reading and writing
        with open(filename, "r+") as file:
            # Read existing lines from the file
            lines = file.readlines()
            num_lines = len(lines)

            # Iterate through the file lines in chunks
            for i in range(lines_per_chunk, num_lines, lines_per_chunk):
                lines.insert(i, new_content + "\n")  # Insert new content at specified intervals

            # Rewind the file pointer to the beginning
            file.seek(0)

            # Write modified lines back to the file
            file.writelines(lines)
    except IOError as e:
        print(e)


def dispatchleads(splitter: int, total: int, leads_filename, test_number: str):
    """
    Dispatch leads from a source file into multiple output files.

    Args:
        splitter (int):         Number of output files to split leads into.
        total (int):            Total number of leads.
        leads_filename (str):   The name of the file containing leads.
        test_number (str):      The test number to include in the output files.
    """
    try:
        remainder               = total % splitter
        integer                 = total // splitter
        files                   = []

        print(banner(string=f" Splitting {total} leads within {splitter} files\n" ,             font="doom",        color="black"))
        time.sleep(2)
        print(banner(string=f" Between {splitter}  Bots\n" ,                                    font="doom",        color="black"))
        time.sleep(2)
        print(banner(string=f" Leads Per File : {integer}\n" ,                                  font="doom",        color="black"))
        time.sleep(2)
        print(banner(string=f" One file randomly get {remainder} additional numbers \n" ,       font="doom",        color="black"))
        time.sleep(2)

        # Clean files
        for digit in range(1, (splitter + 1)):
            open(f'bots/numbers{digit}.txt', 'w').close()
            files.append(f'bots/numbers{digit}.txt')

        file                    = open(leads_filename, "r")
        lines                   = file.readlines()
        first_num               = file.readline()

        # Write UPPER Test num
        for digit in range(1, (splitter + 1)):
            with open(f"bots/numbers{digit}.txt", "a") as momo:
                momo.write(f"{test_number}\n")

        # Handle remainder
        if 0 < remainder < 2:
            with open(random.choice(files), "a") as mymy:
                mymy.write(first_num)
        elif remainder > 1:
            for digit in range(1, (remainder + 1)):
                with open(random.choice(files), "a") as mimi:
                    mimi.write(lines[0])
                    lines.pop(0)

        # Equally split leads within files
        for digit in range(1, (splitter + 1)):
            with open(f"bots/numbers{digit}.txt", "a") as myfile:
                for x in range(1, (integer + 1)):
                    if len(lines) == 1:
                        myfile.write(f"{lines[0]}\n")
                    else:
                        myfile.write(f"{lines[0]}")
                    lines.pop(0)

        # Write LOWER Test num
        for digit in range(1, (splitter + 1)):
            with open(f"bots/numbers{digit}.txt", "a") as momo:
                momo.write(f"{test_number}\n")

    except Exception as e:
        print(e.with_traceback())


def to_str_phones_list(phone_list: []):
    """
    Convert a list of phone numbers represented as strings to a list of strings.

    Args:
        phone_list ([]):    List of phone number records.

    Returns:
        [str]:              List of phone numbers converted to string.
    """
    int_phones              = []
    for record in phone_list:
        phone               = record.phone_number
        int_phones.append(str(phone))
    return int_phones
