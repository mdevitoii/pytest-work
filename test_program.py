# Michael DeVito II
# test_program.py
# Using pytest to test student submissions for rgb_to_cmyk.py

import pytest                               # used to test student code
import importlib.util                       # used to import student modules
from os import path,getcwd                  # used to get directory of student files
from sys import path as sysPath             # used also to get directory of student files
from re import search,DOTALL                # used to match student output to expected output
from inspect import getmembers,isfunction   # used to find student's method if it isn't main()


# folder name of where student files are located
folder = "submissions"

# is true when a student's file is sketchy
sketchy_file = False

# includes the folder where student files are into the current working directory
sysPath.append(path.join(getcwd(),folder)) 

# load students that have not been graded yet, and ones that have been graded already
with open("tograde.txt",'r') as file:
    toGrade = file.readlines()
with open("graded.txt",'r') as file:
    graded = file.readlines()

# replaces \n character for all items in lists
for f in toGrade:
    toGrade[toGrade.index(f)]= f.replace("\n", "")   
for f in graded:
        graded[graded.index(f)]= f.replace("\n", "")   

# loads student's main() method
def load_student_module(filepath): 
    module = importlib.import_module(filepath)
    return module

# find the student's primary function if it isn't main()
def find_conversion_function(module): 
    functions = getmembers(module,isfunction) # uses inspect library to find functions
    if len(functions) == 1: 
        return functions[0][1]
    elif len(functions) > 1: # throws an error if more than one function is present
        print(f"There's more than one function! Sketchy File Present: {file}")
        sketchy_file = True
        return functions[0][1]
    print(f"No module found for file: {file}")
    return None

# get the cmyk output from student's program and return it if found
def extract_cmyk_values(output):
    # Regex pattern to find numbers (C, M, Y, K values)
    # Not gonna lie, this was entirely ChatGPT. I'm a little confused on how exactly this works, but it does
    pattern = r"[C|c][=:]\s*(\d+).*?[M|m][=:]\s*(\d+).*?[Y|y][=:]\s*(\d+).*?[K|k][=:]\s*(\d+)"
    
    match = search(pattern, output, DOTALL) # searches output for a match to what we are expecting

    if match:
        return tuple(map(int, match.groups()))  # Converts output to integers
    return None # if no match, fails the pytest

for file in toGrade: # for each student file, run a pytest

    # Troubleshooting:
    # print(f'To Grade: \n{toGrade}\n\n')
    # print(f'Graded: \n{graded}\n\n')

    if file not in graded:
        print(f'\n----------------------------------\nFile Being Graded: {file}\n')
        # initialize the module using the load_student_module function
        module = load_student_module(file)

        # mark student as graded
        graded.append(file + '\n')
        with open("graded.txt",'w') as f:
            f.writelines(graded)
            

        # finds main() if it isn't called main
        conversion_function = find_conversion_function(module)
        def test_program_case1(monkeypatch, capsys):
                
            if not module or not conversion_function: # throws error if no method is found
                print(f"Skipping non-Python file or no conversion function found: {file}")

            try:    
                inputs = iter(["255","255","0"]) # the inputs we are testing
                monkeypatch.setattr("builtins.input", lambda *args: next(inputs)) # mocks the inputs for us

                try:
                    conversion_function('255','255','0') # runs main() with parameters
                except:
                    conversion_function() # runs main() with no parameters

                captured = capsys.readouterr() # gets the output after we put in our inputs

                expected_cmyk = (0,0,100,0) # Expected output values
                extracted_cmyk = extract_cmyk_values(captured.out) # the outputs we get after using regex

                # finally, test that the values we received are equal to the ones we expected
                # if this fails, then student code did not work as expected
                assert extracted_cmyk == expected_cmyk, f"Expected {expected_cmyk}, but got {extracted_cmyk}" 
            except:
                print(f"TestCase 1: Manual Review required for error found in file: {file}")


        ''' 
        Commented out to make things simple. When I have first test working, I will update this.


        def test_program_case2(monkeypatch, capsys):
            if not module: # makes sure module is imported
                pytest.skip(f"Skipping non-Python file: {file}")
            
            try:
                inputs = iter(["120","93","20"]) # inputs we are testing
                monkeypatch.setattr("builtins.input", lambda *args: next(inputs)) # mocks the inputs

                try:
                    conversion_function('120','93','20') # runs main() with parameters
                except:
                    conversion_function() # runs main() with no parameters

                captured = capsys.readouterr() # gets output from main() after our inputs are placed

                expected_cmyk = (0,23,83,53) # Expected output values
                extracted_cmyk = extract_cmyk_values(captured.out) # the outputs we get after regex

                # finally, test that the values we received are equal to the ones we expected
                # if this fails, then student code did not work as expected
                assert extracted_cmyk == expected_cmyk, f"Expected {expected_cmyk}, but got {extracted_cmyk}"
            except:
                print(f"TestCase 2: Manual Review required for error found in file: {file}")
        '''