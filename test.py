def number_game(numbers: list[int]) -> tuple[str, int]:
    """
    @numbers@ is an unordered array of integers. The array is guaranteed to be of even length.
    Return a tuple consisting of the winner's name and the winner's score assuming that both play optimally.
    "Optimally" means that each player makes moves that maximise their chance of winning
    and minimise opponent's chance of winning.
    You are ALLOWED to use a tuple in your return here, like: return (x, y)
    Possible string values are "Alice", "Bob", and "Tie"
    Limitations:
            @numbers@ may contain up to 300'000 elements.
            Each element is in range 0 <= numbers[i] <= 10^16

    Examples:
    number_game([5, 2, 7, 3]) == ("Bob", 5)
    number_game([3, 2, 1, 0]) == ("Tie", 0)
    number_game([2, 2, 2, 2]) == ("Alice", 4)
    """

    # Separate even and odd numbers
    evens = [num for num in numbers if num % 2 == 0]
    odds = [num for num in numbers if num % 2 != 0]

    # Sort both lists in descending order
    evens.sort(reverse=True)
    odds.sort(reverse=True)

    alice_score = 0
    bob_score = 0

    # Alice starts first
    turn = 0

    while evens or odds:
        if turn % 2 == 0:  # Alice's turn
            if evens and (not odds or evens[0] >= odds[0]):
                alice_score += evens.pop(0)
            elif odds:
                odds.pop(0)
        else:  # Bob's turn
            if odds and (not evens or odds[0] >= evens[0]):
                bob_score += odds.pop(0)
            elif evens:
                evens.pop(0)
        turn += 1

    if alice_score > bob_score:
        return ("Alice", alice_score)
    elif bob_score > alice_score:
        return ("Bob", bob_score)
    else:
        return ("Tie", alice_score)


# Example usage
print(number_game([5, 2, 7, 3]))  # Output: ("Bob", 5)
print(number_game([3, 2, 1, 0]))  # Output: ("Tie", 0)
print(number_game([2, 2, 2, 2]))  # Output: ("Alice", 4)
print(number_game([3, 1, 6, 2, 4, 7, 1, 1]))  # Output: ("Alice", 6)


print(number_game([5, 2, 7, 3]))
assert number_game([5, 2, 7, 3]) == ("Bob", 5)
assert number_game([3, 2, 1, 0]) == ("Tie", 0)
assert number_game([2, 2, 2, 2]) == ("Alice", 4)
assert number_game([3, 1, 6, 2, 4, 7, 1, 1]) == ("Alice", 6)
