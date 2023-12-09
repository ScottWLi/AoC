import re
from collections import Counter
import math

PATTERN = r"\s+(\d+)"
FACES_JOKER = {'T':10, 'J':1, 'Q':12, 'K':13, 'A':14}
FACES = {'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
HAND_STRENGTH = {"five_of_a_kind":7,
                 "four_of_a_kind":6,
                 "full_house":5,
                 "three_of_a_kind":4,
                 "two_pair":3,
                 "one_pair":2,
                 "high_card":1}

def card_strength(card):

    if card.isalpha():
        return FACES[card]

    return int(card)

def card_strength_joker(card):

    if card.isalpha():
        return FACES_JOKER[card]

    return int(card)

def hand_strength(hand):

    card_count = Counter()

    for card in hand:
        card_count[card] += 1

    totals = Counter(card_count.values())

    if 5 in totals:
        return HAND_STRENGTH["five_of_a_kind"]
    elif 4 in totals:
        return HAND_STRENGTH["four_of_a_kind"]
    elif 3 in totals and 2 in totals:
        return HAND_STRENGTH["full_house"]
    elif 3 in totals:
        return HAND_STRENGTH["three_of_a_kind"]
    elif 2 in totals and totals[2] == 2:
        return HAND_STRENGTH["two_pair"]
    elif 2 in totals:
        return HAND_STRENGTH["one_pair"]
    else:
        return HAND_STRENGTH["high_card"]

def hand_strength_joker(hand):

    card_count = Counter()

    for card in hand:
        card_count[card] += 1

    if 'J' in card_count and card_count['J'] != 5:
        N_J = card_count['J']
        del card_count['J']
        card_count[max(card_count, key=card_count.get)] += N_J

    totals = Counter(card_count.values())


    if 5 in totals:
        return HAND_STRENGTH["five_of_a_kind"]
    elif 4 in totals:
        return HAND_STRENGTH["four_of_a_kind"]
    elif 3 in totals and 2 in totals:
        return HAND_STRENGTH["full_house"]
    elif 3 in totals:
        return HAND_STRENGTH["three_of_a_kind"]
    elif 2 in totals and totals[2] == 2:
        return HAND_STRENGTH["two_pair"]
    elif 2 in totals:
        return HAND_STRENGTH["one_pair"]
    else:
        return HAND_STRENGTH["high_card"]


def maina(file):
    # Read in all lines of the file as tuples
    # Sort based on the hand strength
    # then multiply rank by bid

    hand_bid_list = []

    with open(file, 'r') as f:

        for line in f:

            hand, bid = line.split(' ')
            hand_bid_list.append((hand, bid))

    hand_bid_list.sort(key=lambda x: (hand_strength(x[0]),
                                      card_strength(x[0][0]),
                                      card_strength(x[0][1]),
                                      card_strength(x[0][2]),
                                      card_strength(x[0][3]),
                                      card_strength(x[0][4]),))


    total_winnings = 0
    for i, (_, bid) in enumerate(hand_bid_list):
        total_winnings += (i + 1) * int(bid)

    return total_winnings

def mainb(file):
    # Read in all lines of the file as tuples
    # Sort based on the hand strength
    # then multiply rank by bid

    hand_bid_list = []

    with open(file, 'r') as f:

        for line in f:

            hand, bid = line.split(' ')
            hand_bid_list.append((hand, bid))

    hand_bid_list.sort(key=lambda x: (hand_strength_joker(x[0]),
                                      card_strength_joker(x[0][0]),
                                      card_strength_joker(x[0][1]),
                                      card_strength_joker(x[0][2]),
                                      card_strength_joker(x[0][3]),
                                      card_strength_joker(x[0][4]),))

    total_winnings = 0

    for i, (hand, bid) in enumerate(hand_bid_list):
        print(hand)
        total_winnings += (i + 1) * int(bid)

    return total_winnings


if __name__ == '__main__':

    file = './data.txt'
    print(mainb(file))