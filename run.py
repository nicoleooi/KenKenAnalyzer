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

    '''Constraint: Every region must be satisifed'''
    for i in range(len(o)):
        E.add_constraint(o[i].sat)
    
    '''Constraint: Every region can only be satisfied if the operator results in the result'''

    return E

def add(region, N, E, x): 
    ''' @param: region of type Region
        @param: N is length of one side of grid, type int
        @param: E is Encoding object, to add constraints to
        @param: x is number of region, to keep Var names corresponding
        called to add constraint to the region if the op is addition
    '''
    if(region.operator != '+'):
        #wrong func was called, not an addition region
        return -1

    tgt = Var('region'+x+'_sum')

    #tgt is true iff the board's values add up to tgt
    #makeshift switch/case statement 
    sq = region.members  
    if(len(sq) == 1):
        E.add_constraint(iff(tgt, sq[0].value[region.rslt-1]))
    
    elif(len(sq == 2)):
        x = sq[0].value
        y = sq[1].value
        for i in range(N+1): #represents the number held sq[0]
            for j in range(N+1): #represents the number held in sq[1]
                if((i+j) == region.rslt):
                    #if they add up to the result, they're a valid combination for the constraint
                    E.add_constraint(iff(tgt, x[i-1] & y[j-1]))
    elif(len(sq == 3)):
        x = sq[0].value
        y = sq[1].value
        z = sq[2].value
        for i in range(N+1): #represents the number held sq[0]
            for j in range(N+1): #represents the number held in sq[1]
                for k in range(N+1): #represents the number held in sq[2]
                        if((i+j+k) == region.rslt):
                            #if they add up to the result, they're a valid combination for the constraint
                            E.add_constraint(iff(tgt, x[i-1] & y[j-1] & z[k-1]))

    #region can only be satisfied if the sum == rslt
    E.add_constraint(iff(region.sat,tgt))

'''
#this is wrong, summing must be integrated into the encoding
def plus(region, squares_valid, squares_values):
    #call if operator is a '+'
    tgt = region[1]
    members_idx = []
    members = region[0]
    for i in len(members):
        tmp = members[i] #a0 = squares_valid[0] == 0, b2 = squares_valid[5] == 5
        members_idx.append(squares_valid.index(tmp))

    for j in len(members):
        sum = 0
        val = squares_values[members_idx[j]]
        is_one = val[0]
        is_two = val[1]
        is_three = val[2]
        if(is_one):
            sum += 1
        elif(is_two):
            sum += 2
        elif(is_three):

    #members is a list of the member square's values

def mult(region, squares_valid, squares_values):
    #call if operator is a '*'
    tgt = region[1]
    members_idx = []
    members = region[0]
    for i in len(members):
        tmp = members[i] #a0 = squares_valid[0] == 0, b2 = squares_valid[5] == 5
        members_idx.append(squares_valid.index(tmp))
    
    for j in len(members):
        sum = 1
        val = squares_values[members_idx[j]]
        is_one = val[0]
        is_two = val[1]
        is_three = val[2]
        if(is_one):
            sum *= 1
        elif(is_two):
            sum *= 2
        elif(is_three):
            sum *= 3
'''

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