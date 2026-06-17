def find_min_max(arr: list) -> tuple:
    if len(arr) == 1:
        return arr[0], arr[0]
    if len(arr) == 2:
        return (min(arr[0], arr[1]), max(arr[0], arr[1]))
    mid = len(arr) // 2
    left_min, left_max = find_min_max(arr[:mid])
    right_min, right_max = find_min_max(arr[mid:])
    return min(left_min, right_min), max(left_max, right_max)


if __name__ == "__main__":
    assert find_min_max([3]) == (3, 3)
    assert find_min_max([5, 2]) == (2, 5)
    assert find_min_max([3, 1, 4, 1, 5, 9, 2, 6]) == (1, 9)
    assert find_min_max([-7, 0, 3, -1]) == (-7, 3)
    print("All assertions passed.")

    sample = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    print(f"Array: {sample}")
    print(f"Min, Max: {find_min_max(sample)}")
