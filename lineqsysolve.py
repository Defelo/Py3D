from typing import List


def solve(matrix: List[List[float]]) -> List[float]:
    # check size of matrix
    n: int = len(matrix)
    assert n >= 1
    assert all(len(row) == n + 1 for row in matrix)

    # order matrix to avoid zeros on diagonal
    ordered_matrix: List[List[float]] = [None for _ in matrix]
    while matrix:
        best_index: int = 0
        best_zero_cnt: int = 0
        for i, row in enumerate(matrix):
            zero_cnt: int = sum(row[j] == 0 or ordered_matrix[j] is not None for j in range(n))
            assert zero_cnt < n
            if zero_cnt > best_zero_cnt:
                best_zero_cnt: int = zero_cnt
                best_index: int = i
            if zero_cnt + 1 == n:
                break
        row: List[int] = matrix[best_index]
        pos: int = 0
        while row[pos] == 0 or ordered_matrix[pos] is not None:
            pos += 1
        ordered_matrix[pos] = row
        del matrix[best_index]
    matrix: List[List[float]] = ordered_matrix

    # Gaussian elimination
    for i in range(n - 1):
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
