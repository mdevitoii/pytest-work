# Michael DeVito II
# test_program.py
# Using pytest to test student submissions for rgb_to_cmyk.py

import pytest # idk why this line shows up yellow for me
import importlib.util
import os, sys 
import re
import inspect

folder = "submissions" # folder name of where student files are located
sys.path.append(os.path.join(os.getcwd(),folder)) # includes the folder where student files are into the current working directory


liststudents = ['student1'] # list of all student filenames


# loads student's main() method
def load_student_module(filepath): 
    module = importlib.import_module(filepath)
    return module

# find the student's primary function if it isn't main()
def find_conversion_function(module): 
    functions = inspect.getmembers(module, inspect.isfunction) # uses inspect library to find functions
    if len(functions) == 1: 
        return functions[0][1]
    elif len(functions) > 1: # throws an error if more than one function is present
        pytest.skip(f"There's more than one function! Sketchy File Present: {file}")
        return None
    return None

for file in liststudents: # for each student file, run a pytest

    module = load_student_module(file) # initialize the module using the load_student_module function

    conversion_function = find_conversion_function(module) #  finds main() if it isn't called main

    def extract_cmyk_values(output):
        # Regex pattern to find numbers (C, M, Y, K values)
        # Not gonna lie, this was entirely ChatGPT. I'm a little confused on how exactly this works, but it does
        pattern = r"[C|c][=:]\s*(\d+).*?[M|m][=:]\s*(\d+).*?[Y|y][=:]\s*(\d+).*?[K|k][=:]\s*(\d+)"
        
        match = re.search(pattern, output, re.DOTALL) # searches output for a match to what we are expecting

        if match:
            return tuple(map(int, match.groups()))  # Converts output to integers
        return None # if no match, fails the pytest


    def test_program_case1(monkeypatch, capsys):
        if not module or not conversion_function: # throws error if no method is found
            pytest.skip(f"Skipping non-Python file or no conversion function found: {file}")
        
        inputs = iter(["255","255","0"]) # the inputs we are testing
        monkeypatch.setattr("builtins.input", lambda *args: next(inputs)) # mocks the inputs for us

        try:
            conversion_function('255','255','0') # runs main() with parameters
        except:
            conversion_function() # runs main()

        captured = capsys.readouterr() # gets the output after we put in our inputs

        expected_cmyk = (0,0,100,0) # Expected output values
        extracted_cmyk = extract_cmyk_values(captured.out) # the outputs we get after using regex

        # finally, test that the values we received are equal to the ones we expected
        # if this fails, then student code did not work as expected
        assert extracted_cmyk == expected_cmyk, f"Expected {expected_cmyk}, but got {extracted_cmyk}" 

    def test_program_case2(monkeypatch, capsys):
        if not module: # makes sure module is imported
            pytest.skip(f"Skipping non-Python file: {file}")
        
        inputs = iter(["120","93","20"]) # inputs we are testing
        monkeypatch.setattr("builtins.input", lambda *args: next(inputs)) # mocks the inputs

        try:
            conversion_function('120','93','20') # runs main() with parameters
        except:
            conversion_function() # runs main()

        captured = capsys.readouterr() # gets output from main() after our inputs are placed

        expected_cmyk = (0,23,83,53) # Expected output values
        extracted_cmyk = extract_cmyk_values(captured.out) # the outputs we get after regex

        # finally, test that the values we received are equal to the ones we expected
        # if this fails, then student code did not work as expected
        assert extracted_cmyk == expected_cmyk, f"Expected {expected_cmyk}, but got {extracted_cmyk}"