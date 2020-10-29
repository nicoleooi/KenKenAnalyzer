
from nnf import Var
from lib204 import Encoding
from string import ascii_lowercase

# Call your variables whatever you want
a = Var('a')
b = Var('b')
c = Var('c')
x = Var('x')
y = Var('y')
z = Var('z')

row = []
col = []


# make row and column lists
for i in range(5):
    row.append(Var(f'row_{i}'))

for i in range(5):
    col.append(Var(f'col_{i}'))
print(row)
print(col)


# create squares a0-e5 as nnf Variables
squares = []
for i in range(5):
    for j in range(5):
        charOffset = chr(ord('a')+i)
        squares.append(Var(f'{charOffset}{j}'))

# should find a way to categorize the squares into regions automatically given a config text file ... in the meantime we will do it manually
o = []
o.append([[squares[0],squares[1],squares[5],squares[6]],14,'+'])
o.append([[squares[2],squares[7]],3,'-'])
o.append([[squares[3], squares[4]],4,'/'])
o.append([[squares[8],squares[9]],2,'-'])
o.append([[squares[10],squares[11]],2,'-'])
o.append([[squares[12],squares[17],squares[18],squares[23]],40,'*'])
o.append([[squares[13],squares[14],squares[19]],9,'+'])
o.append([[squares[15],squares[20]],2,'/'])
o.append([[squares[16],squares[21],squares[22]],12,"*"])
o.append([[squares[24]],5,'!'])

print("\nInitial board configuration:")
for item in o:
    print(item)
print("* Note: ! indicates singular value in the specified box")



#
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    E = Encoding()
    E.add_constraint(a | b)
    E.add_constraint(~a | ~x)
    E.add_constraint(c | y | z)
    return E

def test_kenken():
    #row[i] << - >> (the row i contains the digits 1-5)
    #col[i] << - >> (the col i contains the digits 1-5)
    #o[i]   << - >> (when the the region i uses the operator in o[i][2] on the elements in o[i][0] to create an output equal to o[i][1])
    #squareValue << - >> (true if one of these values: 001, 010, 011, 100, 101)
        # Idea for this -> we may need to apply binary arithmetic logic structures? If we can use operations rather than purely logic we would avoid this. I need to finish the video first.


    # To qualify as a "good" kenken board there should only be one solution to the puzzle.
    # Time taken or steps required to solve the board can be used in approximating the "difficulty"


    # Are we going to go through all of the potential values for each square? Is that how it is going to solve?
    # In this case we model each square with having the values between 1-5 inclusive.
    # In binary, we can represent this as 001, 010, 011, 100, 101



    return



if __name__ == "__main__":

    T = example_theory()
    print("\nJust testing the example theory. Ignore below.")
    print("Satisfiable: %s" % T.is_satisfiable())
    print("# Solutions: %d" % T.count_solutions())
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        print(" %s: %.2f" % (vn, T.likelihood(v)))
    print()
