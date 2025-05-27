import math
with open('words.txt') as f:
    wordfile = f.read().strip().split('\n')
    print(wordfile[:9])

def count_permutations(length):
    if length == 1:
        return 1
    else:
        return length * count_permutations(length-1)

def find_permutations(word, remaining):
    perms = []
    if len(remaining) == 0:
        perms.append(word)
    else:
        wordlist=remaining[:]
        for i in wordlist:
            remaining = wordlist[:]
            remaining.remove(i) 
            perms += find_permutations(word + i, remaining)
    return perms

def find_permutations_choose(word, remaining, lenword):
    perms = []
    if len(remaining) == lenword:
        perms.append(word)
    else:
        wordlist=remaining[:]
        for i in wordlist:
            remaining = wordlist[:]
            remaining.remove(i) 
            perms += find_permutations_choose(word + i, remaining, lenword)
    return perms


def find_anagrams(word):
    perms = find_permutations('', list(word))
    anas = []
    for i in perms:
        if i in wordfile:
            anas.append(i)
    anas = list(set(anas))
    return anas

def main():
    word = input('enter a word: ')
    # permutations = find_anagrams(word)
    permutations = find_permutations('', list(word))
    # permutations = find_permutations_choose('', list(word), 4)
    print(permutations)
    print(len(permutations))
    print(count_permutations(len(word)))
    print(math.factorial(len(word)))

if __name__ =='__main__':
    main()