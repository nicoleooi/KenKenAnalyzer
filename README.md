[![Work in Repl.it](https://classroom.github.com/assets/work-in-replit-14baed9a392b3a25080506f3b7b6d57f295ec2978f6f33ec97e36a161684cbe9.svg)](https://classroom.github.com/online_ide?assignment_repo_id=310135&assignment_repo_type=GroupAssignmentRepo)

# CISC/CMPE 204 Modelling Project - Kenken Board Analyzer

The purpose of this project is to read a 5x5 Kenken board configuration and provide the user information on:
1. If it is a valid Kenken board configuration. 
    * For the board to be considered valid there must be **one and only one** viable solution. For a solution to be viable the rows and columns all must contain the numbers 1-5 without repeats, and the numbers in the "cages" must produce the arithmetic result using the operator specified for the cage. For the full rules to Kenken you can read more [here](https://www.puzzazz.com/how-to/kenken).
2. The suggested difficulty for the board configuration.

As of this version, all the developed code for the project can be found in run.py. One-hot encoding is used with booleans to represent the possible inputs of 1-5 in each of the kenken squares. The row and column constraints have been coded, and the team is currently working on incorperating the constraints for checking the arithmetic of each "cage" using logic. 
*Note: the T.count_solutions() method was found to hang on the 5x5 board configuration, so we have also implemented a function that scales it back and checks on a 3x3 board configuration.

The board configuration must be manually inputted, however the team is considering creating the ability to read the configuration from a txt file. The current board configuration inputted is shown below.

![Image of kenken board configuration](https://raw.githubusercontent.com/CISC-204/modelling-project-107/master/images/Kenken_Board.png?token=AHC3LHG43YIACQTE67INB7K7VF4IE)


## Structure

* `documents`: Contains folders for both of your draft and final submissions. README.md files are included in both.
* `run.py`: General wrapper script that executes the test_kenken function. Runs auto-checks using the model produced by test_kenken.
* `test.py`: Run this file to confirm that your submission has everything required. This essentially just means it will check for the right files and sufficient theory size.
