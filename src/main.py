import os

import classes
import sql

seats_per_group = int(input("구간당 좌석 수: "))
start_num = 1
member_datas = sql.query("SELECT * FROM students")
member_num = len(member_datas)
cls = classes.Class(len(member_datas), seats_per_group, member_datas)
no_seats = []


# 1차 추첨
def first():
    for i in range(start_num, 3 + start_num):
        for group_id, group in list(cls.groups.items()):
            available_nums = group.available_seats()
            chosen_member_ids = classes.choices(group.applied[i - 1], available_nums)
            cls.group_set_owners(group_id, chosen_member_ids)
            if available_nums == 0:
                group.applied = [[], [], []]


# 배정받지 못한 사람 선택
def select_no_seats():
    for member_id, applied in list(cls.members.items()):
        if not cls.members[member_id][3]:
            no_seats.append(member_id)


# 2차 추첨
def second():
    for group_id, group in list(cls.groups.items()):
        if group.available_seats() > 0:
            available_nums = group.available_seats()
            chosen_member_ids = classes.choices(no_seats, available_nums)
            cls.group_set_owners(group_id, chosen_member_ids)


# 결과 출력
def print_result():
    for group_id, group in list(cls.groups.items()):
        group.owners.sort()
        print(f"{group_id}: ", end='')
        [print(f"{number:2}", end=' ') for number in group.owners]
        print()


if __name__ == "__main__":
    first()
    select_no_seats()
    second()
    print_result()

    os.system("pause")
