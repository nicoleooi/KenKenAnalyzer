from nnf import Var
from lib204 import Encoding
from string import ascii_lowercase

'''
Finished constraints:
    - row and column
    - must be a valid number from 1-N
TO DO constraints:
    - must evaluate to the region's constraints
'''

class Square:
    def _init_(self,is_valid, value):
        self.is_valid = is_valid
        self.value = value

    def get_val(self):
        if(self.value.isnull()): #no values created yet
            return -1
        else:
            return (self.value.index(True) + 1)

class Region:
    def _init_(self, members, rslt, operator, sat):
        self.members = members
        self.operator = operator
        self.rslt = rslt
        self.sat = sat

    def get_len(self):
        return len(self.members)

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

#dynamic test of kenken, pass in the dimension of the grid
def test_kenken(N): 
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
                values.append(Var(f'{charOffset}{j}'+'_'+f'{x}'))
            board.append(Square(is_valid, values))       

    '''
    Create Regions, o is a list of Regions
    '''
    o = []
    o.append(Region([board[0],board[3]],3,'+', Var('region1')))
    o.append(Region([board[1],board[4]],5,'+', Var('region2')))
    o.append(Region([board[2]],1,'!', Var('region3')))
    o.append(Region([board[5],board[8]],5,'+',Var('region4')))
    o.append(Region([board[6],board[7]],4,'+',Var('region5')))
    printConfig(o)

    ''' Constraint: Numbers on board must be from 1-N'''
    for i in range(len(board)):
        #at each square, access the list for squares_values
        #true if the square value is equal to the specified val
        sq = board[i]
        is_one = (sq.value[0]& ~sq.value[1] & ~sq.value[2])
        is_two = (~sq.value[0]& sq.value[1] & ~sq.value[2])
        is_three = (~sq.value[0]& ~sq.value[1] & sq.value[2])

        #square is valid iff the square holds one of these values
        E.add_constraint(iff(sq.is_valid,( is_one | is_two | is_three)))
        E.add_constraint(sq.is_valid)

    ''' Constraint: Row must contain EVERY number from 1-N, with no repeats'''
    for i in range(0,len(board), N): 
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
        E.add_constraint(row[int(i/N)])

    ''' Constraint: Col must contain EVERY number from 1-N, with no repeats'''
    for i in range(N):
        # A column is valid iff it contains the numbers 1-5
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
        E.add_constraint(col[i])

    '''
    Defining functions for each operator
    Constraint: Every region can only be satisfied if the operator results in the result
    '''

    def add(region): 
        ''' 
        @param: region of type Region
        called to add constraint to the region if the op is addition
        '''
        #everything in the string must be relative to the region
        statements = []
        sq = region.members  
        if(len(sq) == 1):
            #E.add_constraint(iff(region.sat, sq[0].value[region.rslt-1]))
            statements.append('sq[0].value[region.rslt-1]')
        
        elif(len(sq) == 2):
            x = sq[0].value
            y = sq[1].value
            for i in range(N+1): #represents the number held sq[0]
                for j in range(N+1): #represents the number held in sq[1]
                    if((i+j) == region.rslt):
                        #if they add up to the result, they're a valid combination for the constraint
                        #E.add_constraint(iff(region.sat, x[i-1] & y[j-1]))
                        statements.append('(sq[0].value['+i+'-1] & sq[1].value['+j+'-1])')

        elif(len(sq) == 3):
            x = sq[0].value
            y = sq[1].value
            z = sq[2].value
            for i in range(N+1): #represents the number held sq[0]
                for j in range(N+1): #represents the number held in sq[1]
                    for k in range(N+1): #represents the number held in sq[2]
                            if((i+j+k) == region.rslt):
                                #if they add up to the result, they're a valid combination for the constraint
                                #E.add_constraint(iff(region.sat, x[i-1] & y[j-1] & z[k-1]))
                                statements.append('(sq[0].value['+i+'-1] & sq[1].value['+j+'-1] & sq[2].value['+k+'-1])')

        elif(len(sq) == 4):
            w = sq[0].value
            x = sq[1].value
            y = sq[2].value
            z = sq[3].value
            for i in range(N+1): #represents the number held sq[0]
                for j in range(N+1): #represents the number held in sq[1]
                    for k in range(N+1): #represents the number held in sq[2]
                        for m in range(N+1): #represents the number held in sq[3]
                            if((i+j+k+m) == region.rslt):
                                #if they add up to the result, they're a valid combination for the constraint
                                #E.add_constraint(iff(region.sat, w[i-1] & x[j-1] & y[k-1] & z[m-1]))
                                statements.append('(sq[0].value['+i+'-1] & sq[1].value['+j+'-1] & sq[2].value['+k+'-1] & sq[3].value['+m+'-1])')

        eval_statement = ''
        i = 0
        #skip the last element
        while(i < len(statements)):
            if(i == 0):
                eval_statement = '(' + statements[i]
                i += 1
                continue
            else:
                eval_statement += (' | ' + statements[i])

        eval_statement += ')'

        #evaluate code below
        E.add_constraint(iff(region.sat, eval(eval_statement)))

    def mult(region): 
        ''' 
        @param: region of type Region
        called to add constraint to the region if the op is addition
        '''
        #everything in the string must be relative to the region
        statements = []
        sq = region.members  
        if(len(sq) == 1):
            #E.add_constraint(iff(region.sat, sq[0].value[region.rslt-1]))
            statements.append('sq[0].value[region.rslt-1]')
        
        elif(len(sq) == 2):
            x = sq[0].value
            y = sq[1].value
            for i in range(N+1): #represents the number held sq[0]
                for j in range(N+1): #represents the number held in sq[1]
                    if((i*j) == region.rslt):
                        #if they add up to the result, they're a valid combination for the constraint
                        #E.add_constraint(iff(region.sat, x[i-1] & y[j-1]))
                        statements.append('(sq[0].value['+i+'-1] & sq[1].value['+j+'-1])')

        elif(len(sq) == 3):
            x = sq[0].value
            y = sq[1].value
            z = sq[2].value
            for i in range(N+1): #represents the number held sq[0]
                for j in range(N+1): #represents the number held in sq[1]
                    for k in range(N+1): #represents the number held in sq[2]
                            if((i*j*k) == region.rslt):
                                #if they add up to the result, they're a valid combination for the constraint
                                #E.add_constraint(iff(region.sat, x[i-1] & y[j-1] & z[k-1]))
                                statements.append('(sq[0].value['+i+'-1] & sq[1].value['+j+'-1] & sq[2].value['+k+'-1])')

        elif(len(sq) == 4):
            w = sq[0].value
            x = sq[1].value
            y = sq[2].value
            z = sq[3].value
            for i in range(N+1): #represents the number held sq[0]
                for j in range(N+1): #represents the number held in sq[1]
                    for k in range(N+1): #represents the number held in sq[2]
                        for m in range(N+1): #represents the number held in sq[3]
                            if((i*j*k*m) == region.rslt):
                                #if they add up to the result, they're a valid combination for the constraint
                                #E.add_constraint(iff(region.sat, w[i-1] & x[j-1] & y[k-1] & z[m-1]))
                                statements.append('(sq[0].value['+i+'-1] & sq[1].value['+j+'-1] & sq[2].value['+k+'-1] & sq[3].value['+m+'-1])')

        eval_statement = ''
        i = 0
        #skip the last element
        while(i < len(statements)):
            if(i == 0):
                eval_statement = '('+statements[i]
                i += 1
                continue
            else:
                eval_statement += (' | ' + statements[i])

        eval_statement += ')'

        #evaluate code below
        E.add_constraint(iff(region.sat, eval(eval_statement)))

    '''Constraint: Every region must be satisifed'''
    for i in range(len(o)):
        if(o[i].operator == '+'):
            add(o[i])
        elif(o[i].operator == 'x'):
            mult(o[i])
        E.add_constraint(o[i].sat)
    
    return E

if __name__ == "__main__":

    T = test_kenken(3)
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