# https://www.reddit.com/r/Python/comments/bxfgos/python_discords_fifth_code_jam_will_run_0628_0707/

# TODO create my own Unit tests, include numbers, and what happens when we only have one char, but want symbls AND caps, UserWarning
# TODO refactor and cleanup
# TODO lose these double variables via refactoring

# The generator should support password_length < 1 000 000 characters.
# The generator should not take more than 5 seconds to finish. 
# Do NOT allow both lists to be passed at the same time. 

# Must return a string. 
# Must generate a random password. 
# The password must be exactly password_length characters long.
# If has_symbols is True, the password must contain at least one symbol, such as #, !, or @. 
# If has_uppercase is True, the password must contain at least one uppercase letter. 
# additional param ignored_chars as a list
# additional param allowed_chars as a user supplied list
# only use given list at a time if both raise a UserWarning explaining that only one may be passed. 

# qualifier.py contains the actual task, and this is where you will write all of your code. 
# tests.py contains tests that will verify whether or not you've completed the qualifier.
# You will need to run this file and copy-paste its output into the Code Jam Signup after you've written your code.
# code in qualifier.py and tests in tests.py run from the same folder. 
# TODO We will need you to copy the output that tests.py generates as well as all the code you wrote in qualifier.py into your code jam application.

import warnings
import string
import random
import logging
import sys
# To clear the clutter when running in a debugger change the level to one above INFO
# which is DEBUG and you will not see any of the breadcurmbs from INFO that are being logged to the console
# logging removed during cleanup, leave this import for when clean logging details are added back
logging.basicConfig(level=logging.INFO)  


def generate_password(
    password_length: int = 8,
    has_symbols: bool = False,
    has_uppercase: bool = False, 
    allowed_chars = None, 
    ignored_chars = None) -> str:


    """Generates a random password.
    The password will be exactly `password_length` characters. Max 1 Million.
    If `has_symbols` is True, the password will contain at least one symbol, such as #, !, or @.
    If `has_uppercase` is True, the password will contain at least one upper
    case letter.
    If allowed_chars are given as a list these will be the only chars used.
    If ignored_chars are given as a list these chars will be ignored.
    Only one list can be passed at a time, either ignored_chars or allowed_chars.
    """  

    if allowed_chars != None and ignored_chars != None:
        raise UserWarning('Warning...........This password generator can only accept one list at a time. You may pass either an ignored_char list, or an allowed_char list; but not both at the same time.')    
    
    if password_length > 1000000:
        warnings.warn("Warning.....password too long, try below a million characters")
        #sys.exit()
    

    #TODO refactor these vars, no need to double them 
    has_symbols1 = has_symbols
    password_length1 = password_length 
    has_uppercase1 = has_uppercase
    allowed_chars1 = allowed_chars
    ignored_chars1 = ignored_chars

    def check_for_allowed_chars(allowed_chars1):
        if allowed_chars1 != None:
            allowed_chars2 = allowed_chars1
            return allowed_chars2
        else:
            password_pool = string.printable
            # lose the chars in the printable generator that are not really letters 
            # such as tabs, new lines, spaces, carriage returns, and x0b/xoc's 
            password_pool_reduced = password_pool.translate({ord(i): None for i in ' \n\t\r\x0b\x0c'})
            return password_pool_reduced

    password_allowed_choices = check_for_allowed_chars(allowed_chars1)

    def check_for_ignored_chars(ignored_chars1, password_allowed_choices):
        if ignored_chars1 != None:
            ignored_chars2 = ignored_chars1
            ignored_chars_string = ''
            ignored_chars_string = ''.join(ignored_chars2)
            #The generator of printable chars need to be a list for translate({ord(i)}) below
            password_choices_string = ''
            password_choices_string = ''.join(password_allowed_choices)
            password_choices_with_removed_chars = password_choices_string.translate({ord(i): None for i in ignored_chars_string})
            return password_choices_with_removed_chars
        else:
            password_ignored_choices = password_allowed_choices
            return password_ignored_choices

    password_choices = check_for_ignored_chars(ignored_chars1, password_allowed_choices)

    def actual_generation(password_length1, password_choices):
        count = 0
        password_list = []
        while count < password_length1:
            letter = random.choice(password_choices)
            password_list.append(letter)
            count += 1
        password_string = ''.join(password_list)
        return password_string

    generated_password = actual_generation(password_length1, password_choices)

    def capitalize_at_least_one(generated_password, password_choices, has_uppercase1 = True):
            cap_password = ''
            count = 0
            symbol_count = 0
            if has_uppercase1 == True:
                if generated_password[0].islower() == True or (generated_password.isalpha() != True and generated_password.isnumeric() != True):
                    ignored_char_list = (string.ascii_lowercase + string.digits + string.punctuation)
                    ignored_char_string = ''
                    ignored_char_string = ''.join(ignored_char_list)
                    password_choices_string = ''
                    password_choices_string = ''.join(password_choices)
                    clean_alphas_only = password_choices_string.translate({ord(i): None for i in ignored_char_string})
                    uppercase_random = random.choice(clean_alphas_only)
                    first_char = generated_password[:1]
                    rest_of_password = generated_password[1:]
                    cap_password = uppercase_random + rest_of_password
                else:
                    cap_password = generated_password
            return cap_password

    capped_password = capitalize_at_least_one(generated_password, password_choices)

    def symbol_addition(capped_password):
        symb_password = ''
        if has_symbols1 != False:
            punct_chars = set(string.punctuation)
            if any(char in punct_chars for char in capped_password):
                #any function will return True if at least one of the characters is in punct_chars.
                symb_password = capped_password
            else:
                random_punct = random.choice(string.punctuation)
                symb_password = capped_password[:-1] + random_punct

        else:
            symb_password = capped_password
        return symb_password
    
    tweaked_final_password = symbol_addition(capped_password)
    
    return str(tweaked_final_password)