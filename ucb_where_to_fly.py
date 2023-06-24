import math

d = 8
numbers_of_selections = [0] * d
sums_of_rewards = [0] * d
dict_of_commands = {0: "w", 1: "s", 2: "a", 3: "d", 4: "q", 5: "e", 6: "i", 7: "k"}


def ucb_where_to_fly(square, n=0):
    ad = 0
    max_upper_bound = 0
    for i in range(0, d):
        if numbers_of_selections[i] > 0:
            average_reward = sums_of_rewards[i] / numbers_of_selections[i]
            delta_i = math.sqrt(3 / 2 * math.log(n + 1) / numbers_of_selections[i])
            upper_bound = average_reward + delta_i
        else:
            upper_bound = 1e400
        if upper_bound > max_upper_bound:
            max_upper_bound = upper_bound
            ad = i
    numbers_of_selections[ad] = numbers_of_selections[ad] + 1
    reward = square
    sums_of_rewards[ad] = sums_of_rewards[ad] + reward
    n += 1
    return dict_of_commands[ad]
