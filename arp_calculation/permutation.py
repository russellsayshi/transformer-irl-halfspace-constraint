for first_index in range(3):
    remaining_indices = list(range(3))
    remaining_indices = remaining_indices[0:first_index] + remaining_indices[first_index+1:]
    for second_index in remaining_indices:
        third_index = 3 - first_index - second_index
        print(first_index, second_index, third_index)
