from operator import le


def getCharOccurence(stringy):
    visited = {}
    for first in range(0, len(stringy)):
        if stringy[first] in visited :
            visited[stringy[first]] = visited[stringy[first]] + 1
        else:
            visited[stringy[first]] = 1   
        
    return visited        

string = "greatundoings"
print("The input string is " + string)
length = getCharOccurence(string)
print("The number of occurance of a char is :")
print(length)   