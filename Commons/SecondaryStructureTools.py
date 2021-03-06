#!/usr/bin/python
import os


def find_matching_parenthesis(text, opening_position):
    closing_position = opening_position
    counter = 1
    while counter > 0:
        closing_position += 1
        char = text[closing_position]
        if char == "(":
            counter += 1
        if char == ")":
            counter -= 1
    return closing_position

def find_matching_char(char, text, initial_position):
    openList = ["[","{","<","A","B","C","D","E"]
    closeList = ["]","}",">","a","b","c","d","e"]
    if char in openList:
        openChar = char
        closeChar = closeList[openList.index(openChar)]
        char_position = initial_position
        counter = 1
        while counter > 0:
            char_position += 1
            char = text[char_position]
            if char == openChar:
                counter += 1
            if char == closeChar:
                counter -= 1
    elif char in closeList:
        closeChar = char
        openChar = openList[closeList.index(closeChar)]
        char_position = initial_position
        counter = 1
        while counter > 0:
            char_position -= 1
            char = text[char_position]
            if char == closeChar:
                counter += 1
            if char == openChar:
                counter -= 1
    else:
        char_position = initial_position

    return char_position

def fill_secondary(conectors, text):
    connectors_ss = []
    chars = ['.','(',')']
    for connector in conectors:
        for nucl_no in range(connector[0],connector[1]):
            if text[nucl_no] not in chars:
                paired_bracket_loc = find_matching_char(text[nucl_no], text, nucl_no)
                if all(paired_bracket_loc not in range(pair[0],pair[1]) for pair in conectors):
                    text = text[:nucl_no] + '.' + text[nucl_no+1:]
                    text = text[:paired_bracket_loc] + '.' + text[paired_bracket_loc+1:]
        connectors_ss.append(text[connector[0]:connector[1]])
    return connectors_ss, text


def find_junction(db_sequence, junction_start, common_stem_length_calc = True):
    stems_identified = 0
    list_of_pairs = []
    if db_sequence[junction_start] == "(":
        last = find_matching_parenthesis(db_sequence, junction_start)
        list_of_pairs.append([junction_start+1, last+1])
        junction_start += 1
        stems_identified += 1

        while junction_start < last:
            if db_sequence[junction_start] == "(":
                end = find_matching_parenthesis(db_sequence, junction_start)
                list_of_pairs.append([junction_start+1, end+1])

                junction_start = end + 1
                stems_identified += 1

            else:
                junction_start += 1
    else:
        junction_start += 1
    if stems_identified > 2:
        if common_stem_length_calc:
            return True, stems_identified, list_of_pairs, common_stem_length(db_sequence, list_of_pairs)
        else:
            return True, stems_identified, list_of_pairs
    else:
        return False, stems_identified, list_of_pairs


def common_stem_length(db_sequence, list_of_pairs):
    length_table = []
    pair_length_table = []
    for i,pair in enumerate(list_of_pairs):
        start = pair[0]-1
        open_count = 0
        end = pair[1]-1
        end_count = 0
        if i == 0:
            while db_sequence[start] == '(' and start >= 0:
                start -=1
                open_count += 1
        else:
            while db_sequence[start] == '(':
                start +=1
                open_count += 1
        length_table.append(open_count)
        if i == 0:
            while db_sequence[end] == ')' and end < len(db_sequence)-1:
                end +=1
                end_count += 1
        else:
            while db_sequence[end] == ')':
                end -=1
                end_count += 1
        length_table.append(end_count)
        pair_length_table.append([open_count, end_count])
    pair_common_length_table = [min(pair) for pair in pair_length_table]
    return pair_common_length_table

