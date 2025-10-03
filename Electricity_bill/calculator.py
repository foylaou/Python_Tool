def calculate_bill(x: int, m: int) -> float:
    """
    計算住宅用電電費
    :param x: 每月用電度數
    :param m: 月份 (1~12)
    :return: 電費 (元)
    """
    # 判斷是否為夏月 (6~9 月)
    is_summer = 6 <= m <= 9

    # 夏月與非夏月的分段費率
    rates_summer = [
        (120, 1.68),
        (330, 2.45),
        (500, 3.70),
        (700, 5.04),
        (1000, 6.24),
        (float("inf"), 8.46)
    ]
    rates_non_summer = [
        (120, 1.68),
        (330, 2.16),
        (500, 3.03),
        (700, 4.14),
        (1000, 5.07),
        (float("inf"), 6.63)
    ]

    rates = rates_summer if is_summer else rates_non_summer

    remaining = x
    prev_limit = 0
    total = 0.0

    for limit, rate in rates:
        # 計算本區間度數
        block_usage = min(remaining, limit - prev_limit)
        if block_usage > 0:
            total += block_usage * rate
            remaining -= block_usage
        prev_limit = limit
        if remaining <= 0:
            break

    return round(total, 2)