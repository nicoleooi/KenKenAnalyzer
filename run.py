from nnf import Var
from nnf.operators import xor, implies
from lib204 import Encoding
from string import ascii_lowercase
import time

'''Each individual grid in the board is represented by a Square. ie. a 3x3 kenken board will have 9 Squares'''
class Square:
    def __init__(self, is_valid, value):
        #proposition for whether the square contains a number from 1 - N
        self.is_valid = is_valid 
        #proposition for value of the square (list of N nnf variables)
        self.value = value

'''Each region in the board is represented by bolded borders around its grid members, an operator and result. 
    For further clarification, refer to the final report.'''
class Region:
    def __init__(self, members, rslt, operator):
        #list of Square objects
        self.members = members
        #char of operator corresponding to region
        self.operator = operator
        #int of result required for region
        self.rslt = rslt

    def get_len(self):
        return len(self.members)
    
    def get_members(self):
        return self.members

def getSquareVal(atom):
    """
    Helper function used to retrieve the value of the number represented from the nnf Var passed in as a parameter
    Used in displaying board solution after calling SAT solver
    """
    for x in atom:
        if x.isdigit():
            num = x
    return int(num)

def iff(left, right):
    return ((left & right) | (left.negate() & right.negate()))

def getTrueAtoms(solution):
    """
    Helper function to return list of only the atoms labeled "True" and in alphabetical order (useful for examining proposed solution for board)
    """
    true_in_sol = [k for k in sol if solution[k] == True]
    true_in_sol = sorted(true_in_sol)
    return true_in_sol

def displayBoard(solution, dim):
    """
    Helper function to visually display the solution for the board
    """
    true_sol = getTrueAtoms(solution)
    board = []
    print("\nExample solved solution shown in board view:")
    for i in range(dim):
        print("    "+str(i), end='')
      
    for atom in true_sol:
        if len(atom) == 4:
            board.append(getSquareVal(atom))
    for i in range(dim*dim):
        if i%dim == 0:
            charOffset = chr(ord('a')+int(i/dim))
            print("\n")
            print(f'{charOffset} '+'|',end='')
        print(" %d | " % board[i],end='')
    print("\n")


def printConfig(boardConfig):
    print("\nInitial board configuration:")
    for reg in boardConfig:
        for m in reg.members:
            print(m.is_valid)
    print("* Note: ! indicates singular value in the specified box")

#dynamic test of kenken, pass in the dimension of the grid
def test_kenken(N): 
    #scope of project constrained to 3x3 and 4x4 boards
    if((N > 4) | (N < 3)):
        return -1

    E = Encoding()
    '''Create row and column propositions'''
    row = []
    col = []
    for i in range(N):
        row.append(Var(f'row_{i}'))
        col.append(Var(f'col_{i}'))

    '''Create board squares'''
    board = []
    for i in range(N):
         for j in range(N): 
             # Create boolean corresponding to if the value at the square is valid or not
            charOffset = chr(ord('a')+i)
            is_valid = Var(f'{charOffset}{j}')
            values = []
            for x in range(1,N+1):
                charOffset = chr(ord('a')+i)
                # Create booleans in each list corresponding to if the square is 1,2,3
                values.append(Var(f'{charOffset}{j}_{x}'))
            board.append(Square(is_valid, values))       


    try:

        '''
        Create Regions, o is a list of Regions
        Uncomment the desired configuration, DO NOT uncomment more than one configuration or else it will just solve the most recent one.
        Board configurations are also listed along with the number of solutions they have and their classified difficulty.
        If you are switching between a 3x3 and 4x4 configuration, set the kenken_size variable to the proper dimensions at the top of the main function.
        '''

    
        """
        # 3x3 ADDITION ONLY BOARD (1 solution - easy)
        o = []
        o.append(Region([board[0],board[3]],3,'+'))
        o.append(Region([board[1],board[4]],5,'+'))
        o.append(Region([board[2]],1,'!'))
        o.append(Region([board[5],board[8]],5,'+'))
        o.append(Region([board[6],board[7]],4,'+'))
        """

        """
        # 3x3 BOARD WITH MULTIPLICATION, ADDITION, SUBTRACTION (2 solutions - easy)
        o = []
        o.append(Region([board[0]],3,'!'))
        o.append(Region([board[1],board[2]],1,'-'))
        o.append(Region([board[3],board[4]],3,'+'))
        o.append(Region([board[5]],3,'!'))
        o.append(Region([board[6], board[7],board[8]],6,'*'))
        """

        
        # 3x3 BOARD WITH DIVISION, ADDITION, SUBTRACTION (2 solutions - medium)
        o = []
        o.append(Region([board[0],board[3]],3,'/'))
        o.append(Region([board[1],board[2],board[4],board[5]],8,'+'))
        o.append(Region([board[6],board[7]],1,'-'))
        o.append(Region([board[8]],1,'!'))
        
        

        
        """
        # 4x4 BOARD WITH ADDITION, SUBTRACTION, DIVISION, MULTIPLICATION (3 solutions - very hard)
        o = []
        o.append(Region([board[0],board[1],board[4],board[8]],12,'*'))
        o.append(Region([board[2],board[3]],2,'/'))
        o.append(Region([board[5],board[9]],1,'-'))
        o.append(Region([board[6],board[7],board[10]],8,'+'))
        o.append(Region([board[11],board[14],board[15]],6,'+'))
        o.append(Region([board[12],board[13]],2,'-'))
        """

        """
        # 4x4 BOARD WITH ADDITION, MULTIPLICATION, SUBTRACTION (3 solutions - easy/medium)
        o = []
        o.append(Region([board[0],board[1],board[4]],8,'*'))
        o.append(Region([board[2],board[3],board[7]],8,'+'))
        o.append(Region([board[5],board[6]],6,'*'))
        o.append(Region([board[8],board[12]],4,'+'))
        o.append(Region([board[9],board[10],board[13]],9,'+'))
        o.append(Region([board[14]],1,'!'))
        o.append(Region([board[11],board[15]],2,'-'))
        """
    
    except:
        print("Incorrect specified board size or invalid board configuration! Please the kenken_size paramter at the top of the main function.")
        quit()

    print("Board layout defined:")
    

    ''' Constraint: Numbers on board must be from 1-N, sets the constraint for the proposition is_valid in each Square'''
    for i in range(len(board)):
        # At each square, access the list for squares_values
        # True if the square value is equal to the specified val
        sq = board[i]
        
        if N==3:
            is_one = (sq.value[0]& ~sq.value[1] & ~sq.value[2])
            is_two = (~sq.value[0]& sq.value[1] & ~sq.value[2])
            is_three = (~sq.value[0]& ~sq.value[1] & sq.value[2])
            E.add_constraint(iff(sq.is_valid,( is_one | is_two | is_three)))
        elif N==4:
            is_one = (sq.value[0]& ~sq.value[1] & ~sq.value[2]& ~sq.value[3])
            is_two = (~sq.value[0]& sq.value[1] & ~sq.value[2]& ~sq.value[3])
            is_three = (~sq.value[0]& ~sq.value[1] & sq.value[2]& ~sq.value[3])
            is_four = (~sq.value[0]& ~sq.value[1] & ~sq.value[2]& sq.value[3])
            E.add_constraint(iff(sq.is_valid,( is_one | is_two | is_three | is_four)))

        # Square is valid iff the square holds one of these values
        E.add_constraint(sq.is_valid)
    print("Valid square constraints added.")

    ''' Constraint: Row must contain EVERY number from 1-N, with no repeats'''
    for i in range(0,len(board), N): 
        if N == 3:
            one_exists = ((board[i].value[0]& ~board[i].value[1] & ~board[i].value[2]) | 
                        (board[i+1].value[0]& ~board[i+1].value[1] & ~board[i+1].value[2]) | 
                        (board[i+2].value[0]& ~board[i+2].value[1] & ~board[i+2].value[2]))
            two_exists = ((~board[i].value[0]& board[i].value[1] & ~board[i].value[2]) |
                        (~board[i+1].value[0]& board[i+1].value[1] & ~board[i+1].value[2]) |
                        (~board[i+2].value[0]& board[i+2].value[1] & ~board[i+2].value[2]))
            three_exists = ((~board[i].value[0]& ~board[i].value[1] & board[i].value[2]) |
                        (~board[i+1].value[0]& ~board[i+1].value[1] & board[i+1].value[2]) |
                        (~board[i+2].value[0]& ~board[i+2].value[1] & board[i+2].value[2]))
            
            E.add_constraint(iff(row[int(i/N)], one_exists & two_exists & three_exists))

        elif N == 4:
            one_exists = ((board[i].value[0]& ~board[i].value[1] & ~board[i].value[2] & ~board[i].value[3]) | 
                        (board[i+1].value[0]& ~board[i+1].value[1] & ~board[i+1].value[2] & ~board[i+1].value[3]) | 
                        (board[i+2].value[0]& ~board[i+2].value[1] & ~board[i+2].value[2] & ~board[i+2].value[3]) |
                        (board[i+3].value[0]& ~board[i+3].value[1] & ~board[i+3].value[2] & ~board[i+3].value[3]))

            two_exists = ((~board[i].value[0]& board[i].value[1] & ~board[i].value[2] & ~board[i].value[3]) |
                        (~board[i+1].value[0]& board[i+1].value[1] & ~board[i+1].value[2] & ~board[i+1].value[3]) |
                        (~board[i+2].value[0]& board[i+2].value[1] & ~board[i+2].value[2] & ~board[i+2].value[3]) |
                        (~board[i+3].value[0]& board[i+3].value[1] & ~board[i+3].value[2] & ~board[i+3].value[3]))

            three_exists = ((~board[i].value[0]& ~board[i].value[1] & board[i].value[2] & ~board[i].value[3]) |
                        (~board[i+1].value[0]& ~board[i+1].value[1] & board[i+1].value[2] & ~board[i+1].value[3]) |
                        (~board[i+2].value[0]& ~board[i+2].value[1] & board[i+2].value[2] & ~board[i+2].value[3]) |
                        (~board[i+3].value[0]& ~board[i+3].value[1] & board[i+3].value[2] & ~board[i+3].value[3]))

            four_exists = ((~board[i].value[0]& ~board[i].value[1] & ~board[i].value[2] & board[i].value[3]) |
                        (~board[i+1].value[0]& ~board[i+1].value[1] & ~board[i+1].value[2] & board[i+1].value[3]) |
                        (~board[i+2].value[0]& ~board[i+2].value[1] & ~board[i+2].value[2] & board[i+2].value[3]) |
                        (~board[i+3].value[0]& ~board[i+3].value[1] & ~board[i+3].value[2] & board[i+3].value[3]))
            
            E.add_constraint(iff(row[int(i/N)], one_exists & two_exists & three_exists & four_exists))


        E.add_constraint(row[int(i/N)])
    print("Row constraints added.")

    ''' Constraint: Col must contain EVERY number from 1-N, with no repeats'''
    for i in range(N):
        if N == 3:
            one_exists = ((board[i].value[0]& ~board[i].value[1] & ~board[i].value[2]) |
                        (board[i+N].value[0]& ~board[i+N].value[1] & ~board[i+N].value[2]) |
                        (board[i+N*2].value[0]& ~board[i+N*2].value[1] & ~board[i+N*2].value[2]))
            two_exists = ((~board[i].value[0]& board[i].value[1] & ~board[i].value[2]) |
                        (~board[i+N].value[0]& board[i+N].value[1] & ~board[i+N].value[2]) |
                        (~board[i+N*2].value[0]& board[i+N*2].value[1] & ~board[i+N*2].value[2]))
            three_exists = ((~board[i].value[0]& ~board[i].value[1] & board[i].value[2]) |
                        (~board[i+N].value[0]& ~board[i+N].value[1] & board[i+N].value[2]) |
                        (~board[i+N*2].value[0]& ~board[i+N*2].value[1] & board[i+N*2].value[2]))

            E.add_constraint(iff(col[i], one_exists & two_exists & three_exists))

        elif N == 4:
            one_exists = ((board[i].value[0]& ~board[i].value[1] & ~board[i].value[2] & ~board[i].value[3]) |
                        (board[i+N].value[0]& ~board[i+N].value[1] & ~board[i+N].value[2] & ~board[i+N].value[3]) |
                        (board[i+N*2].value[0]& ~board[i+N*2].value[1] & ~board[i+N*2].value[2] & ~board[i+N*2].value[3]) |
                        (board[i+N*3].value[0]& ~board[i+N*3].value[1] & ~board[i+N*3].value[2] & ~board[i+N*3].value[3]))

            two_exists = ((~board[i].value[0]& board[i].value[1] & ~board[i].value[2] & ~board[i].value[3]) |
                        (~board[i+N].value[0]& board[i+N].value[1] & ~board[i+N].value[2] & ~board[i+N].value[3]) |
                        (~board[i+N*2].value[0]& board[i+N*2].value[1] & ~board[i+N*2].value[2] & ~board[i+N*2].value[3]) |
                        (~board[i+N*3].value[0]& board[i+N*3].value[1] & ~board[i+N*3].value[2] & ~board[i+N*3].value[3]))

            three_exists = ((~board[i].value[0]& ~board[i].value[1] & board[i].value[2] & ~board[i].value[3]) |
                        (~board[i+N].value[0]& ~board[i+N].value[1] & board[i+N].value[2] & ~board[i+N].value[3]) |
                        (~board[i+N*2].value[0]& ~board[i+N*2].value[1] & board[i+N*2].value[2] & ~board[i+N*2].value[3]) |
                        (~board[i+N*3].value[0]& ~board[i+N*3].value[1] & board[i+N*3].value[2] & ~board[i+N*3].value[3]))
            
            four_exists = ((~board[i].value[0]& ~board[i].value[1] & ~board[i].value[2] & board[i].value[3]) |
                        (~board[i+N].value[0]& ~board[i+N].value[1] & ~board[i+N].value[2] & board[i+N].value[3]) |
                        (~board[i+N*2].value[0]& ~board[i+N*2].value[1] & ~board[i+N*2].value[2] & board[i+N*2].value[3]) |
                        (~board[i+N*3].value[0]& ~board[i+N*3].value[1] & ~board[i+N*3].value[2] & board[i+N*3].value[3]))

            E.add_constraint(iff(col[i], one_exists & two_exists & three_exists & four_exists))

    
        E.add_constraint(col[i])
    print("Column constraints added.")
    
    ''' Constraint: Each region must have squares that provide an arithmetic result as defined by the region's result and operator,
        accessed as region.rslt and region.operator'''
    operationList = []
    for idx, region in enumerate(o):
        varList = []
        sq = region.get_members()
        if region.get_len() == 1:
            varList.append(Var(f'{sq[0].is_valid}_{region.rslt}'))

        elif region.get_len() == 2:
            for i in range(1,N+1):
                for j in range(1,N+1):
                    if region.operator != "/":
                        condition = f'{i}{region.operator}{j}'                      
                        if (abs(eval(condition)) == region.rslt): # this line supports subtraction, multiplication, addition
                            # AND the two squares that make up the sum/difference/product
                            varList.append(Var(f'{sq[0].is_valid}_{i}')&Var(f'{sq[1].is_valid}_{j}'))
                    
                    elif region.operator == "/":
                        # support for division is different: order matters
                        if i%j == 0:
                            # j divides i
                            condition = f'{i}{region.operator}{j}'  
                            if (abs(eval(condition)) == region.rslt): 
                                # AND the two squares that make up the sum/difference/product
                                varList.append(Var(f'{sq[0].is_valid}_{i}')&Var(f'{sq[1].is_valid}_{j}'))
                        
                        elif j%i == 0:
                            # i divides j
                            condition = f'{j}{region.operator}{i}'  
                            if (abs(eval(condition)) == region.rslt): 
                                # AND the two squares that make up the sum/difference/product
                                varList.append(Var(f'{sq[0].is_valid}_{i}')&Var(f'{sq[1].is_valid}_{j}'))

        elif region.get_len() == 3:
            for i in range(1,N+1):
                for j in range(1,N+1):
                    for k in range(1,N+1):
                        if region.operator != "/":
                            condition = f'{i}{region.operator}{j}{region.operator}{k}'                      
                            if (abs(eval(condition)) == region.rslt): # this line supports subtraction, multiplication, addition (no division requried for regions of 3+ squares)
                                # AND the two squares that make up the sum/difference/product
                                
                                varList.append(Var(f'{sq[0].is_valid}_{i}')&Var(f'{sq[1].is_valid}_{j}')&Var(f'{sq[2].is_valid}_{k}'))
                                #print(len(varList))

        elif region.get_len() == 4:
            for i in range(1,N+1):
                for j in range(1,N+1):
                    for k in range(1,N+1):
                        for l in range(1,N+1):
                            if region.operator != "/":
                                condition = f'{i}{region.operator}{j}{region.operator}{k}{region.operator}{l}'                      
                                if (abs(eval(condition)) == region.rslt): # this line supports subtraction, multiplication, addition (no division requried for regions of 3+ squares)
                                    # AND the two squares that make up the sum/difference/product
                                    varList.append(Var(f'{sq[0].is_valid}_{i}')&Var(f'{sq[1].is_valid}_{j}')&Var(f'{sq[2].is_valid}_{k}')&Var(f'{sq[3].is_valid}_{l}'))

        operationList.append(Var(f'group{idx}result_{region.rslt}'))
    
        # Add constraint of the group's result
        E.add_constraint(operationList[idx])

        if len(varList) == 1: # Only one possible option for the region's configuration
            previous = varList[0]
        else:
            # Create combined XOR statement (for all the possible square combinations)
            for jdx in range(1,len(varList)):
                previous = xor(varList[jdx-1],varList[jdx])
                varList[jdx] = previous

        # Add constraint that the group's result implies ONE OF the combinations of squares
        E.add_constraint(implies(operationList[idx],previous))
    
    print("Arithmetic constraints added. Finished definition.")

    return E

if __name__ == "__main__":
    kenken_size = 3
    T = test_kenken(kenken_size)
    print("\n------Begin Tests------")
    print("\nSatisfiable: %s" % T.is_satisfiable())
    numSolutions = T.count_solutions()
    if numSolutions != 0: # Board config has at least one solution
        print("# Solutions: %d" % numSolutions) 
        startTime = time.perf_counter()
        sol = T.solve()
        endTime = time.perf_counter()
        sorted_sol = getTrueAtoms(sol)
        print("   Solution: %s" % sol)
        print("   \nSorted solution: %s" % sorted_sol)
        displayBoard(sol, kenken_size)
        
        print("\nUser results:\n")
        if numSolutions != 1:
            print(f'There are {numSolutions} solutions to this KenKen configuration. Since there is more than 1 solution, it would technically not be a valid configuration (but it is still solvable).')
        else:
            print("There is only 1 solution to this KenKen configuration. This would be considered a valid configuration.")

        # The time taken and therefore difficulty is very affected by regions with higher number of squares (3,4 size regions)
        timeTaken = endTime-startTime

        # Difficulty level thresholds determined by testing solving time for configurations from each difficulty category from an online source of randomly-generated KenKen puzzles.
        if timeTaken < 1.5:
            difficulty = "easy"
        elif timeTaken<3:
            difficulty = "medium" 
        elif timeTaken<30:
            difficulty = "hard"
        else:
            difficulty = "VERY hard"
        print(f'Based on the time taken for the computer to solve this configuration ({timeTaken:.2f}s), it would be considered {difficulty} difficulty.\nPLEASE NOTE: this difficulty value is only an approximation and is very affected by regions with >3 squares.\n')
    else: # Board config has no solutions
        print("The provided board configuration has no solutions. It is invalid and its difficulty cannot be classified.\n")
