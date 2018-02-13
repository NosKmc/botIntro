def stair(n):
    string = ""
    for i in range(n + 1):
        string += str(i)
        print(string)

def stairr(n):
    string = ""
    for i in range(n + 1):
        string += str(i)
    for i in range(n + 1):
        print(string[0:n + 1 - i])

x = int(input("Please enter an integer: "))

for i in range(x + 1):
    stair(i)
    stairr(i-1)
