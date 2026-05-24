import math
import os
import random
import re
import sys

#
# Complete the 'birthday' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_ARRAY s
#  2. INTEGER d
#  3. INTEGER m
#
def inorderTraversal(self, root):

    traversal = []
    node = root
    stack = []
    while node or stack:
        if node:
            stack.append(node)
            node = node.left
        else:
            node = stack.pop()
            traversal.append(node.val)
            node = node.right
                
    return traversal

def migratoryBirds(arr):
    # Write your code here
    dict = {}
    maxFrequencyOccured = 1
    mostFrequentNum = -1
    for i in range(0, len(arr)):
        if arr[i] in dict.keys():
            dict[arr[i]] += 1
            if maxFrequencyOccured < dict[arr[i]]:
                maxFrequencyOccured = dict[arr[i]]
                mostFrequentNum = arr[i]
            elif maxFrequencyOccured == dict[arr[i]]: #to keep the minimum number which occurred most if there is clash
                mostFrequentNum = min(mostFrequentNum, arr[i])
        else:
            dict[arr[i]] = 1
    
    return mostFrequentNum

def birthday(s, d, m):
    # Write your code here
    count = 0
    first_index = 0
    last_index = m
    bool = True
    
    while bool:
        if last_index > len(s):
            bool = False
        total = 0
        if m == 1:
            for val in s:
                if val == d:
                    count += 1
            bool = False       
        else:             
            for i in range(first_index, last_index):
                total = total + s[i]
        
            if total == d:
                count += 1    
            first_index +=  1
            last_index += 1
    return count
        
if __name__ == '__main__':
   # fptr = open(os.environ['OUTPUT_PATH'], 'w')

 #   n = 1

    s = [1,4]

  #  first_multiple_input = input().rstrip().split()

    d = 4

    m = 1

    result = birthday(s, d, m)
    print(result)