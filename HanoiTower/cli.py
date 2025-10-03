import argparse
from .core import move_counts

def main():
    parser = argparse.ArgumentParser(
        description="河內塔盤子移動次數：輸入總盤數 n 與上限 k（k<=n），輸出盤號 1..k 各自移動次數。"
    )
    parser.add_argument("n", type=int, help="總盤數 (n >= 1)")
    parser.add_argument("k", type=int, help="計算上限盤號 (1 <= k <= n)")
    args = parser.parse_args()

    result = move_counts(args.n, args.k)
    for disk, cnt in result.items():
        print(f"盤 {disk}: {cnt} 次")

if __name__ == "__main__":
    main()