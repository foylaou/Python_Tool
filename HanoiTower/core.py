from typing import Dict

def move_counts(n: int, k: int) -> Dict[int, int]:
    """
    計算河內塔中，盤號 1..k 各自的移動次數（給定總盤數 n，k <= n）。

    數學性質：第 i 號盤（1 = 最小盤，頂部）會移動 2^(n - i) 次。

    :param n: 總盤數 (n >= 1)
    :param k: 計算範圍上限 (1 <= k <= n)
    :return: {盤號: 移動次數}
    """
    if not isinstance(n, int) or not isinstance(k, int):
        raise TypeError("n 與 k 需為整數")
    if n < 1:
        raise ValueError("n 必須 >= 1")
    if k < 1 or k > n:
        raise ValueError("k 必須介於 1..n 之間")

    return {i: 2 ** (n - i) for i in range(1, k + 1)}