"""
學生成績管理系統
提供學生資料輸入、排序、統計分析等功能
"""

from typing import List, Dict
import os


class Student:
    """學生類別"""

    def __init__(self, student_id: str, name: str, chinese: int,
                 english: int, math: int, science: int):
        self.student_id = student_id
        self.name = name
        self.chinese = chinese
        self.english = english
        self.math = math
        self.science = science
        self.total = chinese + english + math + science
        self.average = self.total / 4
        self.rank = 0

    def __repr__(self):
        return f"Student({self.student_id}, {self.name}, 總分:{self.total})"


class GradeManagementSystem:
    """成績管理系統"""

    def __init__(self):
        self.students: List[Student] = []

    def clear_screen(self):
        """清除螢幕"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        """顯示主選單"""
        print("\n" + "=" * 60)
        print("📚 學生成績管理系統".center(60))
        print("=" * 60)
        print("\n請選擇功能：")
        print("  (1) 輸入學生資料")
        print("  (2) 計算總分排序並顯示成績總表")
        print("  (3) 計算各科平均並列印不及格名單")
        print("  (4) 結束程式")
        print("-" * 60)

    def input_student_data(self):
        """功能1: 輸入學生資料"""
        print("\n" + "=" * 60)
        print("📝 輸入學生資料".center(60))
        print("=" * 60)

        try:
            student_id = input("\n請輸入學號 (輸入 'q' 返回主選單): ").strip()
            if student_id.lower() == 'q':
                return

            name = input("請輸入姓名: ").strip()

            print("\n請輸入各科成績 (0-100):")
            chinese = int(input("  國文: "))
            english = int(input("  英文: "))
            math = int(input("  數學: "))
            science = int(input("  自然: "))

            # 驗證成績範圍
            scores = [chinese, english, math, science]
            if any(score < 0 or score > 100 for score in scores):
                print("\n❌ 錯誤：成績必須在 0-100 之間！")
                input("\n按 Enter 繼續...")
                return

            # 建立學生物件
            student = Student(student_id, name, chinese, english, math, science)
            self.students.append(student)

            print("\n✅ 學生資料已成功新增！")
            print(f"\n學號: {student_id}")
            print(f"姓名: {name}")
            print(f"總分: {student.total}")
            print(f"平均: {student.average:.2f}")

        except ValueError:
            print("\n❌ 錯誤：請輸入有效的數字！")
        except Exception as e:
            print(f"\n❌ 發生錯誤：{e}")

        input("\n按 Enter 繼續...")

    def calculate_and_display_rankings(self):
        """功能2: 計算排序並顯示成績總表"""
        if not self.students:
            print("\n⚠️  目前沒有學生資料！")
            input("\n按 Enter 繼續...")
            return

        # 依總分排序（由高到低）
        sorted_students = sorted(self.students, key=lambda s: s.total, reverse=True)

        # 設定排名
        for rank, student in enumerate(sorted_students, 1):
            student.rank = rank

        print("\n" + "=" * 100)
        print("🏆 學生成績總表（依排名排序）".center(100))
        print("=" * 100)

        # 表頭
        print(f"\n{'排名':<6}{'學號':<12}{'姓名':<10}{'國文':<8}{'英文':<8}"
              f"{'數學':<8}{'自然':<8}{'總分':<8}{'平均':<8}")
        print("-" * 100)

        # 顯示每位學生資料
        for student in sorted_students:
            rank_display = f"🥇 {student.rank}" if student.rank == 1 else \
                f"🥈 {student.rank}" if student.rank == 2 else \
                    f"🥉 {student.rank}" if student.rank == 3 else \
                        f"   {student.rank}"

            print(f"{rank_display:<8}{student.student_id:<12}{student.name:<10}"
                  f"{student.chinese:<8}{student.english:<8}{student.math:<8}"
                  f"{student.science:<8}{student.total:<8}{student.average:<8.2f}")

        print("-" * 100)
        print(f"\n📊 統計資訊：共 {len(self.students)} 位學生")

        # 計算全班平均
        class_total_avg = sum(s.total for s in self.students) / len(self.students)
        print(f"📈 全班總分平均：{class_total_avg:.2f}")

        input("\n按 Enter 繼續...")

    def calculate_subject_average_and_failing(self):
        """功能3: 計算各科平均並列印不及格名單"""
        if not self.students:
            print("\n⚠️  目前沒有學生資料！")
            input("\n按 Enter 繼續...")
            return

        print("\n" + "=" * 80)
        print("📊 各科平均成績與不及格名單".center(80))
        print("=" * 80)

        # 計算各科平均
        subjects = {
            '國文': 'chinese',
            '英文': 'english',
            '數學': 'math',
            '自然': 'science'
        }

        print("\n📈 各科平均成績：")
        print("-" * 80)

        for subject_name, subject_attr in subjects.items():
            scores = [getattr(s, subject_attr) for s in self.students]
            average = sum(scores) / len(scores)
            max_score = max(scores)
            min_score = min(scores)

            print(f"\n{subject_name}：")
            print(f"  平均分數：{average:.2f}")
            print(f"  最高分數：{max_score}")
            print(f"  最低分數：{min_score}")

        # 列印不及格名單
        print("\n" + "=" * 80)
        print("❌ 不及格名單（成績 < 60）".center(80))
        print("=" * 80)

        has_failing = False

        for subject_name, subject_attr in subjects.items():
            failing_students = [
                s for s in self.students
                if getattr(s, subject_attr) < 60
            ]

            if failing_students:
                has_failing = True
                print(f"\n📌 {subject_name} 不及格：")
                print(f"{'學號':<12}{'姓名':<10}{'成績':<8}")
                print("-" * 40)

                for student in failing_students:
                    score = getattr(student, subject_attr)
                    print(f"{student.student_id:<12}{student.name:<10}{score:<8}")

        if not has_failing:
            print("\n✨ 太棒了！所有學生所有科目都及格！")

        print("\n" + "=" * 80)
        input("\n按 Enter 繼續...")

    def run(self):
        """執行系統主程式"""
        while True:
            self.clear_screen()
            self.display_menu()

            try:
                choice = input("\n請輸入選項 (1-4): ").strip()

                if choice == '1':
                    self.clear_screen()
                    self.input_student_data()

                elif choice == '2':
                    self.clear_screen()
                    self.calculate_and_display_rankings()

                elif choice == '3':
                    self.clear_screen()
                    self.calculate_subject_average_and_failing()

                elif choice == '4':
                    self.clear_screen()
                    print("\n" + "=" * 60)
                    print("👋 感謝使用學生成績管理系統！".center(60))
                    print("=" * 60)
                    print()
                    break

                else:
                    print("\n❌ 無效的選項，請輸入 1-4！")
                    input("\n按 Enter 繼續...")

            except KeyboardInterrupt:
                print("\n\n程式已中斷。")
                break
            except Exception as e:
                print(f"\n❌ 發生錯誤：{e}")
                input("\n按 Enter 繼續...")
