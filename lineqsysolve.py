from typing import List


def solve(matrix: List[List[float]]) -> List[float]:
    # check size of matrix
    n: int = len(matrix)
    assert n >= 1
    assert all(len(row) == n + 1 for row in matrix)

    # Gaussian elimination
    for i in range(n - 1):
        # avoid zeros on diagonal
        j: int = i
        while j < n and matrix[j][i] == 0:
            j += 1
        matrix[i], matrix[j] = matrix[j], matrix[i]

        for j in range(i + 1, n):
            if matrix[j][i] == 0:
                continue
            a: float = matrix[i][i] / matrix[j][i]
            for k in range(n + 1):
                matrix[j][k]: float = matrix[i][k] - a * matrix[j][k]

    for i in range(n)[::-1]:
        for j in range(i + 1, n):
            matrix[i][n] -= matrix[i][j] * matrix[j][n]
            matrix[i][j]: float = 0
        matrix[i][n] /= matrix[i][i]
        matrix[i][i]: float = 1

    return [row[n] for row in matrix]
