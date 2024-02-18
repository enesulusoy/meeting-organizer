'''
Problem:
t and z are strings consist of lowercase English letters.

Find all substrings for t, and return the maximum value of [ len(substring) x [how many times the substring occurs in z] ]

Example:
t = acldm1labcdhsnd
z = shabcdacasklksjabcdfueuabcdfhsndsabcdmdabcdfa

Solution:
abcd is a substring of t, and it occurs 5 times in Z, len(abcd) x 5 = 20 is the solution

'''


def find_max(t,z):
    i = 0
    x = 1
    max = 0
    while i <= len(t):
        char = t[i: i + x]
        times = z.count(char)
        sum_ = len(char) * times
        if sum_ > max:
            max = sum_
        if i + x >= len(t):
            i = 0
            x += 1
        else:
            i += 1
        if x > len(t):
            break
        
    ## Farklı bir çözüm
    """
    max_value = 0
    for i in range(len(t)):
        for j in range(i + 1, len(t) + 1):
            substring = t[i:j]
            count = z.count(substring)
            value = len(substring) * count
            if value > max_value:
                max_value = value
    return max_value
    """
    print(max)
    return max


if __name__ == '__main__':
    find_max("acldm1labcdhsnd","shabcdacasklksjabcdfueuabcdfhsndsabcdmdabcdfa")
