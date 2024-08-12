def number_game(numbers):
    n = len(numbers)
    dp = [[0] * n for _ in range(n)]

    # 初始化单元素情况
    for i in range(n):
        dp[i][i] = numbers[i] if numbers[i] % 2 == 0 else -numbers[i]

    # 填充DP表
    for length in range(2, n + 1):  # 子数组长度
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(
                [
                    (numbers[k] if numbers[k] % 2 == 0 else -numbers[k])
                    + (0 if k == i else -dp[i][k - 1])
                    + (0 if k == j else -dp[k + 1][j])
                    for k in range(i, j + 1)
                ]
            )

    alice_score = (sum(numbers) + dp[0][n - 1]) // 2
    bob_score = sum(numbers) - alice_score
    if alice_score > bob_score:
        return ("Alice", alice_score)
    elif alice_score < bob_score:
        return ("Bob", bob_score)
    else:
        return ("Tie", alice_score)


# 测试用例
print("number_game([5, 2, 7, 3])", number_game([5, 2, 7, 3]))
print("number_game([3, 2, 1, 0])", number_game([3, 2, 1, 0]))
print("number_game([2, 2, 2, 2])", number_game([2, 2, 2, 2]))
