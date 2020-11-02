
from nnf import Var
from lib204 import Encoding
from string import ascii_lowercase

# Call your variables whatever you want
row = []
col = []
N = 5

# make row and column lists
# row i is true if the row has all the required numbers
# col i is true if the col has all the required numbers
for i in range(N):
    row.append(Var(f'row_{i}'))
    col.append(Var(f'col_{i}'))

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
            squares_valid.append(Var(f'{charOffset}{j}'))


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

print("\nInitial board configuration:")
for item in o:
    print(item)
print("* Note: ! indicates singular value in the specified box")

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


def iff(left, right):
    return (left.negate() | right) & (right.negate() | left)

def test_kenken():
    #row[i] << - >> (the row i contains the digits 1-5)
    #col[i] << - >> (the col i contains the digits 1-5)
    #o[i]   << - >> (when the the region i uses the operator in o[i][2] on the elements in o[i][0] to create an output equal to o[i][1])
    #squares_valid[i] << - >> (true if the corresponding value at squares_value[i] is the one hot encoding of 1 to 5. MSB corresponds to greatest index)
    #squares_value[i][0-4] <<->> (outputs of model, each i corresponds to a square on the kenken board and 0-4 correspond to the LSB to MSB of one hot encoding)
        # Idea for this -> we may need to apply binary arithmetic logic structures? If we can use operations rather than purely logic we would avoid this. I need to finish the video first.

        # To qualify as a "good" kenken board there should only be one solution to the puzzle.
    # Time taken or steps required to solve the board can be used in approximating the "difficulty"
    E = Encoding()

    #constraint for valid squares 
    for i in range(len(squares_values)):
        #at each square, access the list for squares_values
        #true if the square value is equal to the specified val
        is_one = (squares_values[i][0]& ~squares_values[i][1] & ~squares_values[i][2] & ~squares_values[i][3] & ~squares_values[i][4])
        is_two = (~squares_values[i][0]& squares_values[i][1] & ~squares_values[i][2] & ~squares_values[i][3] & ~squares_values[i][4])
        is_three = (~squares_values[i][0]& ~squares_values[i][1] & squares_values[i][2] & ~squares_values[i][3] & ~squares_values[i][4])
        is_four = (~squares_values[i][0]& ~squares_values[i][1] & ~squares_values[i][2] & squares_values[i][3] & ~squares_values[i][4])
        is_five = (~squares_values[i][0]& ~squares_values[i][1] & ~squares_values[i][2] & ~squares_values[i][3] & squares_values[i][4])

        #square is valid iff the square holds one of these values
        E.add_constraint(iff(squares_valid[i], ( is_one | is_two | is_three | is_four | is_five )) )
        
                    
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
        E.add_constraint(iff(row[int(i/5)], one_exists & two_exists & three_exists & four_exists & five_exists))

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

        E.add_constraint(iff(col[i], one_exists & two_exists & three_exists & four_exists & five_exists))

    return E

"""
For reference:
def example_theory():
    E = Encoding()
    E.add_constraint(a | b)
    E.add_constraint(~a | ~x)
    E.add_constraint(c | y | z)
    return E
"""

if __name__ == "__main__":

    T = test_kenken()
    # T = example_theory()
    # print("\nJust testing the example theory. Ignore below.")
    # print("Satisfiable: %s" % T.is_satisfiable())
    # print("# Solutions: %d" % T.count_solutions())
    # print("   Solution: %s" % T.solve())

    # print("\nVariable likelihoods:")
    # for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
    #     print(" %s: %.2f" % (vn, T.likelihood(v)))
    # print()
