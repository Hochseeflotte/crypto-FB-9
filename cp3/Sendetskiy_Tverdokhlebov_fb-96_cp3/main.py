import itertools
from collections import Counter
import pandas as pd


# Alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
#             'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь', 'э', 'ю', 'я']
Alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
Alphabet = list(Alphabet)
with open("01.txt", 'r') as f1:
    text = f1.read().lower().replace("ъ", "ь").replace("ё", "е").replace("\n", "")
top_ru_birgams = ['ст', 'но', 'то', 'на', 'ен']
top_text_bigrams = ['рн', 'ыч', 'нк', 'цз', 'иа']
lenght = len(Alphabet)


# bigrams
def bigram(text):
    arr2 = []
    i = 0
    while i < len(text) - 1:
        arr2.append(text[i]+text[i+1])
        i += 2
    return arr2


bigram1 = Counter(bigram(text))


def bigram_frequancy(bigram):
    bigramfreq=[]
    for i in bigram:
        bigramfreq.append(bigram[i]/sum(bigram.values()))
        # print(bigramfreq)
    return bigramfreq


# таблиця із топ5 біграм
def PrintBigramTop(bigram):
    dic=dict(list(zip(bigram, bigram_frequancy(bigram))))
    sorted_keys= sorted(dic, key=dic.get, reverse=True)[:5]
    sorted_dict = {}
    for i in sorted_keys:
        sorted_dict[i] = dic[i]

    #print(sorted_dict)
    #print(tabulate(data, headers='keys', tablefmt='grid'))
    return sorted_dict

# print(PrintBigramTop(bigram1).keys())


# gcd
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


# обернений елемент
def rev_elem(elem, mod):
    if gcd(elem, mod) == 1:
        for x in range(0, mod - 1):
            ans = (elem * x) % mod
            if ans == 1:
                return x
    else:
        return -1


# rivnyannya
def linear_equation(a, b, n):
    d = gcd(a, n)
    rev_a = rev_elem(a, n)
    x = []
    if d == 1:
        x.append((rev_a * b) % n)

    else:
        if (b % d) == 0:
            a1 = a/d
            b1 = b/d
            n1 = n/d
            res = (rev_elem(a1 * b1, n1)) % n1
            for i in range(d):
                x.append(res + i * n1)
        else:
            x.append(-1)
    return x


def bigram_num(bgrm):
    return 31 * Alphabet.index(bgrm[0]) + Alphabet.index(bgrm[1])


def bigram_txt(num):
    return Alphabet[num // 31] + Alphabet[num % 31]


def decrypt(a, b, text):
    decrypted_text = ""
    rev_a = rev_elem(a, len(Alphabet)**2)
    for i in range(0, len(text), 2):
        y = bigram_num(text[i] + text[i+1])
        x = ((y-b)*rev_a) % len(Alphabet)**2
        decrypted_text += bigram_txt(x)
    return decrypted_text


# test
# def check(text):
#     d = dict.fromkeys(text, 0)
#     for key in d:
#         d[key] /= len(text)
#     if d['а'] < 0.05:
#         return 0
#     if d['е'] < 0.05:
#         return 0
#     if d['о'] < 0.07:
#         return 0
#     if d['ф'] > 0.03 or d['щ'] > 0.03 or d['ь'] > 0.05:
#         return 0
#
#     return 1


def possible_keys():
    possible_keys = []
    for i in range(0,5):
        for j in range(0,5):
            for n in range(0,5):
                for m in range(0,5):
                    if n==m or i==j:
                        continue
                    X1 = Alphabet.index(top_ru_birgams[i][0])*31+Alphabet.index(top_ru_birgams[i][1])
                    X2 = Alphabet.index(top_ru_birgams[j][0])*31+Alphabet.index(top_ru_birgams[j][1])
                    Y1 = Alphabet.index(top_text_bigrams[n][0])*31+Alphabet.index(top_text_bigrams[n][1])
                    Y2 = Alphabet.index(top_text_bigrams[m][0])*31+Alphabet.index(top_text_bigrams[m][1])

                    a = linear_equation((X1-X2), (Y1-Y2), 31*31)
                    for num in a:
                        b = (Y1-num*X1)%(31*31)
                        if a!=-1:
                            ans = (num, b)
                            possible_keys.append(ans)
    return possible_keys


for i in range(0,len(possible_keys())):
    print(possible_keys()[i], decrypt(possible_keys()[i][0], possible_keys()[i][1], text))
    print('\n')



