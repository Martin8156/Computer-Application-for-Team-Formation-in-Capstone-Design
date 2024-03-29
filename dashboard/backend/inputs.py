

# By default, weights are initialized to the following values.
weights = [0, 0.5, 1, 1.5, 2]

# Input: Specific number to change weight of
def input_weight(index, weight):
    weights[index] = weight

# Input: New List of weights
def input_all_weights(new_weight_list):
    for i in range(5):
        weights[i] = new_weight_list[i]


def apply_weight(value):
    product = value * weights[value - 1]
    return product