def longestUniqueSubsttr(stringy):
    last_visited = {}
    window = 0
    result = 0
    for first in range(0, len(stringy)):
        if stringy[first] in last_visited :
            window = max(window, last_visited[stringy[first]] + 1)
        result = max(result, first - window + 1)
        last_visited[stringy[first]] = first
    return result        

string = "okmama"
print("The input string is " + string)
length = longestUniqueSubsttr(string)
print("The length of the longest non-repeating character" +
      " substring is " + str(length))   