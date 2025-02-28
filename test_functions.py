# Michael DeVito II
# test_functions.py
# Using pytest to test student submissions for functions assignment

import pytest                               # used to test student code
import importlib.util                       # used to import student modules
from os import path,getcwd                  # used to get directory of student files
from sys import path as sysPath             # used also to get directory of student files

'''
Ants.py:
pytest -m ants_test

era.py:
pytest -m era_test

'''


folder = "submissions" # folder name of where student files are located
sysPath.append(path.join(getcwd(),folder)) # includes the folder where student files are into the current working directory


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


for file in toGrade: # for each student file, run a pytest


    if file not in graded:
        print(f'\n----------------------------------\nFile Being Graded: {file}\n')
        # initialize the module using the load_student_module function
        module = load_student_module(file)

        # mark student as graded
        graded.append(file + '\n')
        with open("graded.txt",'w') as f:
            f.writelines(graded)
            
        @pytest.mark.ants_test
        def test_ants(capsys):
            if "ants" in file:    
                if not module: # throws error if no method is found
                    print(f"Skipping non-Python file: {file}")

                try:    
                    # runs the main() function
                    file.main()

                    captured = capsys.readouterr() # gets the output after we put in our inputs

                    assert captured
                except:
                    print(f"TestCase ANTS: Manual Review required for error found in file: {file}")

        @pytest.mark.era_test
        def test_era(capsys):
            
            if "era" in file:
                if not module: # throws error if no method is found
                    print(f"Skipping non-Python file: {file}")

                try:    
                    # runs the era() function
                    file.era(91,25)

                    captured = capsys.readouterr() # gets the output after we put in our inputs

                    assert captured == 2.47
                except:
                    print(f"TestCase ERA: Manual Review required for error found in file: {file}")