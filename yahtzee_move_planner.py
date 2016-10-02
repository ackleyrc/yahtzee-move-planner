"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper scorecard options
"""

import random

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for _ in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def gen_all_perms(outcomes, length):
    """
    Iterative function that generates the set of all permutations
    of outcomes of given length
    """

    answer_set = set([()])
    for _ in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                if item not in partial_sequence:
                    new_sequence = list(partial_sequence)
                    new_sequence.append(item)
                    temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def gen_all_combos(outcomes, length):
    """
    Iterative function that generates the set of all combinations
    of outcomes of given length
    """

    perms = list(gen_all_perms(outcomes, length))
    combos = set([tuple(sorted(list(item))) for item in perms])

    return combos


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """

    max_score = 0
    for die_val in hand:
        count = hand.count(die_val)
        current_score = count * die_val
        if current_score > max_score:
            max_score = current_score

    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """

    poss_die_vals = range(1,num_die_sides+1)
    seqs = gen_all_sequences(poss_die_vals, num_free_dice)
    total = 0.0
    for seq in seqs:
        total += score(held_dice + seq)
    expected_val = total / len(seqs)

    return expected_val


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """

    all_holds = set([])

    length = len(hand)
    for num_held in range(length+1):
        combos = gen_all_combos(range(length),num_held)
        for indices in combos:
            hold = []
            for index in indices:
                hold.append(hand[index])
            all_holds.add(tuple(hold))

    return all_holds


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """

    potential_holds = gen_all_holds(hand)
    max_score = 0.0
    best_hold = ()
    for hold in potential_holds:
        current_score = expected_value(hold, num_die_sides, len(hand)-len(hold))
        if current_score > max_score:
            max_score = current_score
            best_hold = hold

    return (max_score, best_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print("Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score)


#run_example()

NUM_DIE_SIDES = 6
hand = tuple(sorted([random.randint(1,6) for die in range(5)]))
print("You rolled:", hand)
hand_score, hold = strategy(hand, NUM_DIE_SIDES)
print("Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score)
