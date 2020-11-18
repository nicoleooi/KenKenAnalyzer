
from nnf import Var
from lib204 import Encoding
from string import ascii_lowercase

# Call your variables whatever you want


def getSquareVal(atom):
    """
    Helper function used to retrieve the value of the number represented from the nnf Var passed in as a parameter
    Will be used in the cage arithmetic section - not implemented yet

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
    print("\nSolved solution of board:")
    for atom in true_sol:
        if len(atom) == 4:
            board.append(getSquareVal(atom))
    for i in range(dim*dim):
        if i%dim == 0:
            print("\n|",end='')       
        print(" %d | " % board[i],end='')
    print("\n")


def printConfig(boardConfig):
    """

    """
    print("\nInitial board configuration:")
    for region in boardConfig:
        print(region)
    print("* Note: ! indicates singular value in the specified box")

def test_kenken3x3():
    E = Encoding()
    N = 3
    row = []
    col = []
    for i in range(N):
        row.append(Var(f'row_{i}'))
        col.append(Var(f'col_{i}'))

    squares_valid = []
    for i in range(N): 
        for j in range(N): 
                charOffset = chr(ord('a')+i)
                squares_valid.append(Var(f'{charOffset}{j}'))


    squares_values = []
    for i in range(N): #Columns
        for j in range(N): #Rows
            # Create a list for each square
            vals_list = []
            for x in range(1,N+1):
                charOffset = chr(ord('a')+i)

                # Create booleans in each list corresponding to if the square is 1,2,3
                vals_list.append(Var(f'{charOffset}{j}'+'_'+f'{x}'))
            squares_values.append(vals_list)
    print(squares_values)
    '''
    o is a list representing the board
    each item in the list is a region, each region is a list
    each region is a list of 3 items: the squares in the region, the number it must evaluate to, operator
    '''
    o = []
    o.append([[squares_valid[0],squares_valid[3]],3,'+'])
    o.append([[squares_valid[1],squares_valid[4]],5,'+'])
    o.append([[squares_valid[2]],1,'!'])
    o.append([[squares_valid[5],squares_valid[8]],5,'+'])
    o.append([[squares_valid[6],squares_valid[7]],4,'+'])
    printConfig(o)

    for i in range(len(squares_values)):
        #at each square, access the list for squares_values
        #true if the square value is equal to the specified val
        is_one = (squares_values[i][0]& ~squares_values[i][1] & ~squares_values[i][2])
        is_two = (~squares_values[i][0]& squares_values[i][1] & ~squares_values[i][2])
        is_three = (~squares_values[i][0]& ~squares_values[i][1] & squares_values[i][2])

        #square is valid iff the square holds one of these values
        E.add_constraint(iff(squares_valid[i],( is_one | is_two | is_three)))
        E.add_constraint(squares_valid[i])

    for i in range(0,len(squares_values), N): #increment by 3
        # a row is valid iff it contains the numbers 1-5
        # Check combinations of squares_values[square of index 0-24][value]
        one_exists = ((squares_values[i][0]& ~squares_values[i][1] & ~squares_values[i][2]) | 
                    (squares_values[i+1][0]& ~squares_values[i+1][1] & ~squares_values[i+1][2]) | 
                    (squares_values[i+2][0]& ~squares_values[i+2][1] & ~squares_values[i+2][2]))
        two_exists = ((~squares_values[i][0]& squares_values[i][1] & ~squares_values[i][2]) |
                    (~squares_values[i+1][0]& squares_values[i+1][1] & ~squares_values[i+1][2]) |
                    (~squares_values[i+2][0]& squares_values[i+2][1] & ~squares_values[i+2][2]))
        three_exists = ((~squares_values[i][0]& ~squares_values[i][1] & squares_values[i][2]) |
                    (~squares_values[i+1][0]& ~squares_values[i+1][1] & squares_values[i+1][2]) |
                    (~squares_values[i+2][0]& ~squares_values[i+2][1] & squares_values[i+2][2]))
        
        E.add_constraint(iff(row[int(i/N)], one_exists & two_exists & three_exists))
        E.add_constraint(row[int(i/N)])


    for i in range(N):
        # A column is valid iff it contains the numbers 1-5
        one_exists = ((squares_values[i][0]& ~squares_values[i][1] & ~squares_values[i][2]) |
                    (squares_values[i+N][0]& ~squares_values[i+N][1] & ~squares_values[i+N][2]) |
                    (squares_values[i+N*2][0]& ~squares_values[i+N*2][1] & ~squares_values[i+N*2][2]))
        two_exists = ((~squares_values[i][0]& squares_values[i][1] & ~squares_values[i][2]) |
                    (~squares_values[i+N][0]& squares_values[i+N][1] & ~squares_values[i+N][2]) |
                    (~squares_values[i+N*2][0]& squares_values[i+N*2][1] & ~squares_values[i+N*2][2]))
        three_exists = ((~squares_values[i][0]& ~squares_values[i][1] & squares_values[i][2]) |
                    (~squares_values[i+N][0]& ~squares_values[i+N][1] & squares_values[i+N][2]) |
                    (~squares_values[i+N*2][0]& ~squares_values[i+N*2][1] & squares_values[i+N*2][2]))

        E.add_constraint(iff(col[i], one_exists & two_exists & three_exists))
        E.add_constraint(col[i])



    operationList = []
    #operationDict = {}

    #if (f'region[0][0]_{i}')


    # Logic for checking arithmetic of regions - Not complete yet!!
    for idx, region in enumerate(o):
        print(region[0])
        if len(region[0]) == 1:
            operationList.append(Var(f'{region[0][0]}_{region[1]}'))
            E.add_constraint(operationList[idx])
        elif len(region[0]) == 2:
            varList = []
            for i in range(1,4):
                for j in range(1,4):
                    if (i+j == region[1]):
                        varList.append(Var(f'{region[0][0]}_{i}'))
                        varList.append(Var(f'{region[0][1]}_{j}'))

                        #E.add_constraint((Var(f'{region[0][0]}_{i}') & Var(f'{region[0][1]}_{j}')).negate() | Var(f'group{idx}result_{i+j}'))
                        #E.add_constraint(Var(f'group{idx}result_{i+j}').negate() | (Var(f'{region[0][0]}_{i}') & Var(f'{region[0][1]}_{j}')))
            operationList.append(Var(f'group{idx}result_{region[1]}'))
            #E.add_constraint(operationList[idx].negate() | (varList[0] & varList[1]) | (varList[2] & varList[3]))

            #operationList.append("Hi")
            E.add_constraint(operationList[idx])
        elif len(region[0]) == 3:
            operationList.append("5")
            pass
        elif len(region[0]) == 4:
            operationList.append("5")
            pass  
    return E

'''
def plus(region, squares_valid, squares_values):
    #call if operator is a '+'
    tgt = region[1]
    members_idx = []
    members = region[0]
    for i in len(members):
        tmp = members[i] #a0 = squares_valid[0] == 0, b2 = squares_valid[5] == 5
        members_idx.append(squares_valid.index(tmp))
    
    for j in len(members_idx):
        sum = 0
        val = squares_values[members_idx[j]]
        is_one = val[0]
        is_two = val[1]
        is_three = val[2]
        if(is_one):
            sum += 1
        elif(is_two):
            sum += 2
        else:
            sum += 3

def mult(region, squares_valid, squares_values):
    #call if operator is a '*'
    tgt = region[1]
    members_idx = []
    members = region[0]
    for i in len(members):
        tmp = members[i] #a0 = squares_valid[0] == 0, b2 = squares_valid[5] == 5
        members_idx.append(squares_valid.index(tmp))
    
    for j in len(members_idx):
        sum = 1
        val = squares_values[members_idx[j]]
        is_one = val[0]
        is_two = val[1]
        is_three = val[2]
        if(is_one):
            sum *= 1
        elif(is_two):
            sum *= 2
        else:
            sum *= 3
'''


def test_kenken5x5():
    #row[i] << - >> (the row i contains the digits 1-5)
    #col[i] << - >> (the col i contains the digits 1-5)
    #o[i]   << - >> (when the the region i uses the operator in o[i][2] on the elements in o[i][0] to create an output equal to o[i][1])
    #squares_valid[i] << - >> (true if the corresponding value at squares_value[i] is the one hot encoding of 1 to 5. MSB corresponds to greatest index)
    #squares_value[i][0-4] <<->> (outputs of model, each i corresponds to a square on the kenken board and 0-4 correspond to the LSB to MSB of one hot encoding)
    # Idea for this -> we may need to apply binary arithmetic logic structures? If we can use operations rather than purely logic we would avoid this. I need to finish the video first.

    # To qualify as a "good" kenken board there should only be one solution to the puzzle.
    # Time taken or steps required to solve the board can be used in approximating the "difficulty"

    E = Encoding()
    row = []
    col = []
    N = 5

    # make row and column lists
    # row i is true if the row has all the required numbers
    # col i is true if the col has all the required numbers
    """
    for i in range(N):
        row.append(Var(f'row_{i}')) # removed this as aux variables temporarily to attempt to speed up solving time
        col.append(Var(f'col_{i}'))
    """
    for i in range(N):
        row.append(f'row_{i}')
        col.append(f'col_{i}')


    print(row)
    print(col)

    # create squares a0-e4 as nnf Variables
    # each row is from a to e
    # each col is from 0 to 4
    # each variable in squares_valid is a variable indicating if it represents an acceptable number (1-5)
    squares_valid = []
    for i in range(N): 
        for j in range(N): 
                charOffset = chr(ord('a')+i)
                squares_valid.append(f'{charOffset}{j}') #removed valid square aux variable temporarily


    # should find a way to categorize the squares into regions automatically given a config text file ... 
    # in the meantime we will do it manually
    o = []
    o.append([[squares_valid[0],squares_valid[1],squares_valid[5],squares_valid[6]],14,'+'])
    o.append([[squares_valid[2],squares_valid[7]],3,'-'])
    o.append([[squares_valid[3], squares_valid[4]],4,'/'])
    o.append([[squares_valid[8],squares_valid[9]],2,'-'])
    o.append([[squares_valid[10],squares_valid[11]],2,'-'])
    o.append([[squares_valid[12],squares_valid[17],squares_valid[18],squares_valid[23]],40,'*'])
    o.append([[squares_valid[13],squares_valid[14],squares_valid[19]],9,'+'])
    o.append([[squares_valid[15],squares_valid[20]],2,'/'])
    o.append([[squares_valid[16],squares_valid[21],squares_valid[22]],12,"*"])
    o.append([[squares_valid[24]],5,'!'])
    printConfig(o)

    squares_values = []
    for i in range(N): #Columns
        for j in range(N): #Rows
            # Create a list for each square
            vals_list = []
            for x in range(1,N+1):
                charOffset = chr(ord('a')+i)

                # Create booleans in each list corresponding to if the square is 1,2,3,4, or 5
                vals_list.append(Var(f'{charOffset}{j}'+'_'+f'{x}'))
            squares_values.append(vals_list)
    print(squares_values)

    #constraint for valid squares 
    for i in range(len(squares_values)):
        #at each square, access the list for squares_values
        #true if the square value is equal to the specified val
        is_one = (squares_values[i][0]& ~squares_values[i][1] & ~squares_values[i][2] & ~squares_values[i][3] & ~squares_values[i][4])
        is_two = (~squares_values[i][0]& squares_values[i][1] & ~squares_values[i][2] & ~squares_values[i][3] & ~squares_values[i][4])
        is_three = (~squares_values[i][0]& ~squares_values[i][1] & squares_values[i][2] & ~squares_values[i][3] & ~squares_values[i][4])
        is_four = (~squares_values[i][0]& ~squares_values[i][1] & ~squares_values[i][2] & squares_values[i][3] & ~squares_values[i][4])
        is_five = (~squares_values[i][0]& ~squares_values[i][1] & ~squares_values[i][2] & ~squares_values[i][3] & squares_values[i][4])

        # Square is valid iff the square holds one of these values
        #E.add_constraint(iff(squares_valid[i], ( is_one | is_two | is_three | is_four | is_five )) )
        #E.add_constraint(squares_valid[i])
        E.add_constraint(( is_one | is_two | is_three | is_four | is_five )) #Temporarily removed auxiliary variables in attempt to reduce solving time
        
                    
    # Constraint for valid rows
    for i in range(0,len(squares_values), 5): #increment by 5
        # a row is valid iff it contains the numbers 1-5
        # Check combinations of squares_values[square of index 0-24][value]
        one_exists = ((squares_values[i][0]& ~squares_values[i][1] & ~squares_values[i][2] & ~squares_values[i][3] & ~squares_values[i][4]) |
                    (squares_values[i+1][0]& ~squares_values[i+1][1] & ~squares_values[i+1][2] & ~squares_values[i+1][3] & ~squares_values[i+1][4]) |
                    (squares_values[i+2][0]& ~squares_values[i+2][1] & ~squares_values[i+2][2] & ~squares_values[i+2][3] & ~squares_values[i+2][4]) |
                    (squares_values[i+3][0]& ~squares_values[i+3][1] & ~squares_values[i+3][2] & ~squares_values[i+3][3] & ~squares_values[i+3][4]) |
                    (squares_values[i+4][0]& ~squares_values[i+4][1] & ~squares_values[i+4][2] & ~squares_values[i+4][3] & ~squares_values[i+4][4]))
        two_exists = ((~squares_values[i][0]& squares_values[i][1] & ~squares_values[i][2] & ~squares_values[i][3] & ~squares_values[i][4]) |
                    (~squares_values[i+1][0]& squares_values[i+1][1] & ~squares_values[i+1][2] & ~squares_values[i+1][3] & ~squares_values[i+1][4]) |
                    (~squares_values[i+2][0]& squares_values[i+2][1] & ~squares_values[i+2][2] & ~squares_values[i+2][3] & ~squares_values[i+2][4]) |
                    (~squares_values[i+3][0]& squares_values[i+3][1] & ~squares_values[i+3][2] & ~squares_values[i+3][3] & ~squares_values[i+3][4]) |
                    (~squares_values[i+4][0]& squares_values[i+4][1] & ~squares_values[i+4][2] & ~squares_values[i+4][3] & ~squares_values[i+4][4]))
        three_exists = ((~squares_values[i][0]& ~squares_values[i][1] & squares_values[i][2] & ~squares_values[i][3] & ~squares_values[i][4]) |
                    (~squares_values[i+1][0]& ~squares_values[i+1][1] & squares_values[i+1][2] & ~squares_values[i+1][3] & ~squares_values[i+1][4]) |
                    (~squares_values[i+2][0]& ~squares_values[i+2][1] & squares_values[i+2][2] & ~squares_values[i+2][3] & ~squares_values[i+2][4]) |
                    (~squares_values[i+3][0]& ~squares_values[i+3][1] & squares_values[i+3][2] & ~squares_values[i+3][3] & ~squares_values[i+3][4]) |
                    (~squares_values[i+4][0]& ~squares_values[i+4][1] & squares_values[i+4][2] & ~squares_values[i+4][3] & ~squares_values[i+4][4]))
        four_exists = ((~squares_values[i][0]& ~squares_values[i][1] & ~squares_values[i][2] & squares_values[i][3] & ~squares_values[i][4]) |
                    (~squares_values[i+1][0]& ~squares_values[i+1][1] & ~squares_values[i+1][2] & squares_values[i+1][3] & ~squares_values[i+1][4]) |
                    (~squares_values[i+2][0]& ~squares_values[i+2][1] & ~squares_values[i+2][2] & squares_values[i+2][3] & ~squares_values[i+2][4]) |
                    (~squares_values[i+3][0]& ~squares_values[i+3][1] & ~squares_values[i+3][2] & squares_values[i+3][3] & ~squares_values[i+3][4]) |
                    (~squares_values[i+4][0]& ~squares_values[i+4][1] & ~squares_values[i+4][2] & squares_values[i+4][3] & ~squares_values[i+4][4]))
        five_exists = ((~squares_values[i][0]& ~squares_values[i][1] & ~squares_values[i][2] & ~squares_values[i][3] & squares_values[i][4]) |
                    (~squares_values[i+1][0]& ~squares_values[i+1][1] & ~squares_values[i+1][2] & ~squares_values[i+1][3] & squares_values[i+1][4]) |
                    (~squares_values[i+2][0]& ~squares_values[i+2][1] & ~squares_values[i+2][2] & ~squares_values[i+2][3] & squares_values[i+2][4]) |
                    (~squares_values[i+3][0]& ~squares_values[i+3][1] & ~squares_values[i+3][2] & ~squares_values[i+3][3] & squares_values[i+3][4]) |
                    (~squares_values[i+4][0]& ~squares_values[i+4][1] & ~squares_values[i+4][2] & ~squares_values[i+4][3] & squares_values[i+4][4]))
        
        # Add constraint to to row[0-4] auxilliary variables to check validity of rows
        #E.add_constraint(iff(row[int(i/5)], one_exists & two_exists & three_exists & four_exists & five_exists))
        #E.add_constraint(row[int(i/5)])
        E.add_constraint(one_exists & two_exists & three_exists & four_exists & five_exists)

    # Constraint for valid cols
    for i in range(5):
        # A column is valid iff it contains the numbers 1-5
        one_exists = ((squares_values[i][0]& ~squares_values[i][1] & ~squares_values[i][2] & ~squares_values[i][3] & ~squares_values[i][4]) |
                    (squares_values[i+5][0]& ~squares_values[i+5][1] & ~squares_values[i+5][2] & ~squares_values[i+5][3] & ~squares_values[i+5][4]) |
                    (squares_values[i+10][0]& ~squares_values[i+10][1] & ~squares_values[i+10][2] & ~squares_values[i+10][3] & ~squares_values[i+10][4]) |
                    (squares_values[i+15][0]& ~squares_values[i+15][1] & ~squares_values[i+15][2] & ~squares_values[i+15][3] & ~squares_values[i+15][4]) |
                    (squares_values[i+20][0]& ~squares_values[i+20][1] & ~squares_values[i+20][2] & ~squares_values[i+20][3] & ~squares_values[i+20][4]))
        two_exists = ((~squares_values[i][0]& squares_values[i][1] & ~squares_values[i][2] & ~squares_values[i][3] & ~squares_values[i][4]) |
                    (~squares_values[i+5][0]& squares_values[i+5][1] & ~squares_values[i+5][2] & ~squares_values[i+5][3] & ~squares_values[i+5][4]) |
                    (~squares_values[i+10][0]& squares_values[i+10][1] & ~squares_values[i+10][2] & ~squares_values[i+10][3] & ~squares_values[i+10][4]) |
                    (~squares_values[i+15][0]& squares_values[i+15][1] & ~squares_values[i+15][2] & ~squares_values[i+15][3] & ~squares_values[i+15][4]) |
                    (~squares_values[i+20][0]& squares_values[i+20][1] & ~squares_values[i+20][2] & ~squares_values[i+20][3] & ~squares_values[i+20][4]))
        three_exists = ((~squares_values[i][0]& ~squares_values[i][1] & squares_values[i][2] & ~squares_values[i][3] & ~squares_values[i][4]) |
                    (~squares_values[i+5][0]& ~squares_values[i+5][1] & squares_values[i+5][2] & ~squares_values[i+5][3] & ~squares_values[i+5][4]) |
                    (~squares_values[i+10][0]& ~squares_values[i+10][1] & squares_values[i+10][2] & ~squares_values[i+10][3] & ~squares_values[i+10][4]) |
                    (~squares_values[i+15][0]& ~squares_values[i+15][1] & squares_values[i+15][2] & ~squares_values[i+15][3] & ~squares_values[i+15][4]) |
                    (~squares_values[i+20][0]& ~squares_values[i+20][1] & squares_values[i+20][2] & ~squares_values[i+20][3] & ~squares_values[i+20][4]))
        four_exists = ((~squares_values[i][0]& ~squares_values[i][1] & ~squares_values[i][2] & squares_values[i][3] & ~squares_values[i][4]) |
                    (~squares_values[i+5][0]& ~squares_values[i+5][1] & ~squares_values[i+5][2] & squares_values[i+5][3] & ~squares_values[i+5][4]) |
                    (~squares_values[i+10][0]& ~squares_values[i+10][1] & ~squares_values[i+10][2] & squares_values[i+10][3] & ~squares_values[i+10][4]) |
                    (~squares_values[i+15][0]& ~squares_values[i+15][1] & ~squares_values[i+15][2] & squares_values[i+15][3] & ~squares_values[i+15][4]) |
                    (~squares_values[i+20][0]& ~squares_values[i+20][1] & ~squares_values[i+20][2] & squares_values[i+20][3] & ~squares_values[i+20][4]))
        five_exists = ((~squares_values[i][0]& ~squares_values[i][1] & ~squares_values[i][2] & ~squares_values[i][3] & squares_values[i][4]) |
                    (~squares_values[i+5][0]& ~squares_values[i+5][1] & ~squares_values[i+5][2] & ~squares_values[i+5][3] & squares_values[i+5][4]) |
                    (~squares_values[i+10][0]& ~squares_values[i+10][1] & ~squares_values[i+10][2] & ~squares_values[i+10][3] & squares_values[i+10][4]) |
                    (~squares_values[i+15][0]& ~squares_values[i+15][1] & ~squares_values[i+15][2] & ~squares_values[i+15][3] & squares_values[i+15][4]) |
                    (~squares_values[i+20][0]& ~squares_values[i+20][1] & ~squares_values[i+20][2] & ~squares_values[i+20][3] & squares_values[i+20][4]))

        #E.add_constraint(iff(col[i], one_exists & two_exists & three_exists & four_exists & five_exists))
        #E.add_constraint(col[i])
        E.add_constraint(one_exists & two_exists & three_exists & four_exists & five_exists)


    return E


if __name__ == "__main__":

    T = test_kenken3x3()
    print("\n------Begin Tests------")
    print(T.vars())
    print("\nSatisfiable: %s" % T.is_satisfiable())
    print("# Solutions: %d" % T.count_solutions()) # commented out because it hangs when testing kenken5x5
    sol = T.solve()
    sorted_sol = getTrueAtoms(sol)
    print("   Solution: %s" % sol)
    print("   \nSorted solution: %s" % sorted_sol)
    displayBoard(sol, 3)
    print("\nVariable likelihoods (work in progress):")
    #for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
    #    print(" %s: %.2f" % (vn, T.likelihood(v)))
    print()



"""
Extra notes:
Can call getTrueAtoms(T.solve()) in main if you want to print out only the true atoms in the model.

Rough notes for modelling arithmetic - couldn't create them completely because we have not defined a 3x3 board yet
    General process:
    1) Configure board under o like we did in run.py but replacing the 5x5 config with a 3x3 config
        o = []
        o.append([[squares_valid[0],squares_valid[1],squares_valid[5],squares_valid[6]],14,'+'])
        o.append([[squares_valid[2],squares_valid[7]],3,'-'])
        o.append([[squares_valid[3], squares_valid[4]],4,'/'])
        o.append([[squares_valid[8],squares_valid[9]],2,'-'])
        o.append([[squares_valid[10],squares_valid[11]],2,'-'])
        o.append([[squares_valid[12],squares_valid[17],squares_valid[18],squares_valid[23]],40,'*'])
        o.append([[squares_valid[13],squares_valid[14],squares_valid[19]],9,'+'])
        o.append([[squares_valid[15],squares_valid[20]],2,'/'])
        o.append([[squares_valid[16],squares_valid[21],squares_valid[22]],12,"*"])
        o.append([[squares_valid[24]],5,'!'])

    2) Starting with first element of o, get the operator.
    3) Will finish this later, but use a process combining line 115 and 117-120

    groupis4 = Var('groupis4')
    E.add_constraint(groupis4)
    print(getSquareVal(squares_values[0][1]))
    print(getSquareVal(squares_values[1][1]))

    E.add_constraint(iff(Var(f'groupis{getSquareVal(squares_values[0][1])+getSquareVal(squares_values[1][1])}'), squares_values[0][1] & squares_values[1][1]))
    
    for i in range(5):
        for j in range(5):

            E.add_constraint(iff(Var(f'x_is_{i+j}'), Var(f'y_is_{i}') & Var(f'z_is_{j}')))

"""