"""
電梯控制系統 (Elevator Control System)
最佳路徑演算法實作
"""

from typing import List, Tuple
from enum import IntEnum


class Direction(IntEnum):
    """電梯方向"""
    UP = 11
    DOWN = 12


class ElevatorController:
    """電梯控制器 - 實現最佳路徑停靠演算法"""

    def __init__(self, initial_floor: int = 1, max_floor: int = 10):
        """
        初始化電梯控制器

        Args:
            initial_floor: 電梯初始樓層
            max_floor: 最高樓層
        """
        self.current_floor = initial_floor
        self.max_floor = max_floor
        self.direction = None  # 當前運行方向
        self.stops = []  # 停靠記錄

    def process_commands(self, commands: List[Tuple[int, int]]) -> List[int]:
        """
        處理命令並返回最佳停靠順序

        Args:
            commands: 命令列表 [(location, command), ...]
                     location: 1-10 樓層號, 11 表示電梯內
                     command: 1-10 目標樓層, 11 上樓, 12 下樓

        Returns:
            停靠樓層順序列表
        """
        # 解析命令
        requests = self._parse_commands(commands)

        # 執行最佳路徑演算法
        route = self._calculate_optimal_route(requests)

        return route

    def _parse_commands(self, commands: List[Tuple[int, int]]) -> dict:
        """
        解析命令，分類為上行請求和下行請求

        Returns:
            {
                'up_requests': {樓層: 目標樓層},
                'down_requests': {樓層: 目標樓層},
                'internal_requests': [目標樓層列表]
            }
        """
        up_requests = {}
        down_requests = {}
        internal_requests = []

        for location, command in commands:
            if location == 11:  # 電梯內的指令
                internal_requests.append(command)
            elif command == Direction.UP:  # 上樓請求
                up_requests[location] = None
            elif command == Direction.DOWN:  # 下樓請求
                down_requests[location] = None
            else:  # 指定樓層
                # 判斷是上行還是下行
                if command > location:
                    up_requests[location] = command
                else:
                    down_requests[location] = command

        return {
            'up_requests': up_requests,
            'down_requests': down_requests,
            'internal_requests': internal_requests
        }

    def _calculate_optimal_route(self, requests: dict) -> List[int]:
        """
        計算最佳路徑 - 使用 SCAN 演算法（電梯演算法）

        策略：
        1. 繼續當前方向直到沒有請求
        2. 改變方向處理反向請求
        3. 優先處理同方向的請求
        """
        route = []
        up_floors = sorted(requests['up_requests'].keys())
        down_floors = sorted(requests['down_requests'].keys(), reverse=True)
        internal_floors = sorted(set(requests['internal_requests']))

        # 決定初始方向
        if not self.direction:
            self.direction = self._determine_initial_direction(
                up_floors, down_floors, internal_floors
            )

        current = self.current_floor

        # 合併所有需要停靠的樓層
        all_stops = set()

        # 處理上行請求
        for floor in up_floors:
            all_stops.add(floor)
            target = requests['up_requests'][floor]
            if target:
                all_stops.add(target)

        # 處理下行請求
        for floor in down_floors:
            all_stops.add(floor)
            target = requests['down_requests'][floor]
            if target:
                all_stops.add(target)

        # 處理電梯內請求
        all_stops.update(internal_floors)

        # 移除當前樓層
        all_stops.discard(current)

        # SCAN 演算法實作
        if self.direction == Direction.UP or (
                self.direction is None and
                any(f > current for f in all_stops)
        ):
            # 先往上
            up_stops = sorted([f for f in all_stops if f > current])
            down_stops = sorted([f for f in all_stops if f < current], reverse=True)
            route = up_stops + down_stops
        else:
            # 先往下
            down_stops = sorted([f for f in all_stops if f < current], reverse=True)
            up_stops = sorted([f for f in all_stops if f > current])
            route = down_stops + up_stops

        return route

    def _determine_initial_direction(self, up_floors, down_floors, internal_floors):
        """決定初始運行方向"""
        up_count = len([f for f in up_floors if f >= self.current_floor])
        down_count = len([f for f in down_floors if f <= self.current_floor])

        # 統計電梯內的請求方向
        internal_up = len([f for f in internal_floors if f > self.current_floor])
        internal_down = len([f for f in internal_floors if f < self.current_floor])

        total_up = up_count + internal_up
        total_down = down_count + internal_down

        return Direction.UP if total_up >= total_down else Direction.DOWN

    def simulate(self, commands: List[Tuple[int, int]]) -> None:
        """
        模擬電梯運行並輸出詳細過程

        Args:
            commands: 命令列表
        """
        print(f"📍 電梯初始位置: {self.current_floor}F")
        print(f"📥 收到命令: {commands}")
        print("-" * 60)

        route = self.process_commands(commands)

        print(f"🎯 最佳停靠順序: {route}")
        print("-" * 60)
        print("🚀 開始運行:")

        for i, floor in enumerate(route, 1):
            direction_symbol = "⬆️" if floor > self.current_floor else "⬇️"
            print(f"  {i}. 從 {self.current_floor}F {direction_symbol} 到 {floor}F")
            self.current_floor = floor

        print(f"✅ 完成！最終位置: {self.current_floor}F")
        print("=" * 60)


def run_test(test_num: int, initial_floor: int, commands: List[Tuple[int, int]]):
    """執行單個測試案例"""
    print(f"\n{'=' * 60}")
    print(f"測試 4.{test_num}")
    print(f"{'=' * 60}")

    controller = ElevatorController(initial_floor)
    controller.simulate(commands)


def main():
    """主程式 - 執行所有測試"""
    print("🏢 電梯控制系統 - 最佳路徑演算法測試")

    # 測試資料 4.3
    run_test(3, 1, [(5, 12), (10, 12), (3, 12), (7, 11)])

    # 測試資料 4.4
    run_test(4, 10, [(5, 12), (10, 12), (3, 11), (7, 11)])

    # 測試資料 4.5
    run_test(5, 4, [(5, 12), (10, 12), (3, 12), (7, 11)])

    # 測試資料 4.6
    run_test(6, 1, [(5, 12), (10, 12), (8, 12), (7, 11)])


if __name__ == "__main__":
    main()