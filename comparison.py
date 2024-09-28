
import pandas as pd
import numpy as np
from fonetika.soundex import RussianSoundex
import json
from fonetika.distance import PhoneticsInnerLanguageDistance
soundex = RussianSoundex(delete_first_letter=True)


def compar(csv_row,json_row,base):
    flag = 0
    weights = {'jaro_winkler': 0.5, 'levenshtein': 0.5, 'soundex': 0.0}
    if combined_similarity(sort_words(csv_row['full_name']), sort_words(json_row['full_name'])) > 0.75:
        flag += 1
    if combined_similarity(csv_row['email'], json_row['email']) > 0.75:
        flag += 1
    if combined_similarity(csv_row['birthdate'], json_row['birthdate'], weights) > 0.75:
        flag += 1
    if base ==1:
        if combined_similarity(csv_row['address'],json_row['address'])>0.75:
            flag+=1
        if combined_similarity(csv_row['phone'], json_row['phone'],weights) > 0.75:
            flag += 1
        if csv_row['sex']==json_row['sex']:
            flag+=1
        return 1 if flag>=4 else 0
    elif base ==2:
        if combined_similarity(csv_row['address'], json_row['address']) > 0.75:
            flag += 1
        if combined_similarity(csv_row['phone'], json_row['phone'], weights) > 0.75:
            flag += 1
        return 1 if flag >= 4 else 0
    else:
        if csv_row['sex']==json_row['sex']:
            flag+=1
        return 1 if flag >= 3 else 0

def sort_words(string):
    words = string.split()
    sorted_words = sorted(words)

    return " ".join(sorted_words)

def combined_similarity(string1, string2, weights=None):
    # Определение весов, если они не указаны
    if weights is None:
        weights = {'jaro_winkler': 0.5, 'levenshtein': 0.3, 'soundex': 0.2}

    def levenshtein_distance(str1, str2):
        row_length = len(str1) + 1
        col_length = len(str2) + 1
        distance = np.zeros((row_length, col_length), dtype=int)

        for i in range(1, row_length):
            for k in range(1, col_length):
                distance[i][0] = i
                distance[0][k] = k

        for col in range(1, col_length):
            for row in range(1, row_length):
                if str1[row - 1] == str2[col - 1]:
                    cost = 0
                else:
                    cost = 1

                distance[row][col] = min(distance[row - 1][col] + 1,
                                         distance[row][col - 1] + 1,
                                         distance[row - 1][col - 1] + cost)

        distance = distance[row][col]

        return distance

    def jaro_distance1(s1, s2):
        if s1 == s2:
            return 1.0

        len_s1 = len(s1)
        len_s2 = len(s2)

        max_dist = int(max(len_s1, len_s2) / 2) - 1

        matches = 0
        s1_matches = [False] * len_s1
        s2_matches = [False] * len_s2

        for i in range(len_s1):
            start = max(0, i - max_dist)
            end = min(i + max_dist + 1, len_s2)
            for j in range(start, end):
                if s2_matches[j]:
                    continue
                if s1[i] == s2[j]:
                    s1_matches[i] = True
                    s2_matches[j] = True
                    matches += 1
                    break

        if matches == 0:
            return 0.0

        transpositions = 0
        k = 0
        for i in range(len_s1):
            if not s1_matches[i]:
                continue
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1

        transpositions /= 2

        return (matches / len_s1 + matches / len_s2 + (matches - transpositions) / matches) / 3

    def jaro_winkler_similarity1(s1, s2, scaling=0.1):

        jaro_dist = jaro_distance1(s1, s2)

        prefix = 0
        max_prefix = 4
        for i in range(min(len(s1), len(s2))):
            if s1[i] == s2[i]:
                prefix += 1
            else:
                break
            if prefix == max_prefix:
                break

        return jaro_dist + (prefix * scaling * (1 - jaro_dist))

    def prcnt(str1:str, str2:str) -> (float,float):
        dist = PhoneticsInnerLanguageDistance(soundex)
        mx_len = max(len(str1),len(str2))
        res_soundex = float(1-dist.distance(str1,str2)/mx_len)
        res_levinshtein = float(1-levenshtein_distance(str1,str2)/mx_len)
        return res_soundex, res_levinshtein

    sound_res, levin_res = prcnt(string1, string2)
    jaro_winkler = jaro_winkler_similarity1(string1, string2)

    combined_score = (weights['jaro_winkler'] * jaro_winkler +
                      weights['levenshtein'] * levin_res +
                      weights['soundex'] * sound_res)

    return combined_score

