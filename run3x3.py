
from nnf import Var
from lib204 import Encoding
from string import ascii_lowercase

N = 3


def iff(left, right):
    return ((left & right) | (left.negate() & right.negate()))

def getSquareVal(squareVar):
    for x in squareVar.name:
        if x.isdigit():
            num = x
    return int(num)

def test_kenken3():
    E = Encoding()
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
    for i in range(3): #Columns
        for j in range(3): #Rows
            # Create a list for each square
            vals_list = []
            for x in range(1,N+1):
                charOffset = chr(ord('a')+i)

                # Create booleans in each list corresponding to if the square is 1,2,3,4, or 5
                vals_list.append(Var(f'{charOffset}{j}'+'_'+f'{x}'))
            squares_values.append(vals_list)
    print(squares_values)

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


    """
    Rough notes for arithmetic - couldn't create them completely because we have not defined a 3x3 board yet

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
    return E


if __name__ == "__main__":
    T = test_kenken3()
    print("\nJust testing the example theory. Ignore below.")
    print("Satisfiable: %s" % T.is_satisfiable())
    print("# Solutions: %d" % T.count_solutions())
    sol = T.solve()
    true_in_sol = [k for k in sol if sol[k] == True]
    true_in_sol = sorted(true_in_sol)
    print(type(true_in_sol))
    print("   Solution: %s" % true_in_sol)

    print("\nVariable likelihoods:")
    #for v,vn in zip([x,y,z], 'xyz'):
    #    print(" %s: %.2f" % (vn, T.likelihood(v)))
    print()