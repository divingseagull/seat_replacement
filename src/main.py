import os

import classes
import sql

seats_per_group = int(input("구간당 좌석 수: "))
start_num = 1
debug = True
member_datas = sql.query("SELECT * FROM students")
member_num = len(member_datas)
cls = classes.Class(len(member_datas), seats_per_group, member_datas, start_num, debug=debug)


# 1차 추첨
if debug:
    print("-----------\n"
          "-- FIRST --\n"
          "-----------\n")
for i in range(start_num, 3 + start_num):
    for group_id, group in list(cls.groups.items()):
        available_nums = group.available_seats()
        chosen_member_ids = classes.multiple_choice(group.applied[i-1], available_nums)
        cls.group_set_owners(group_id, chosen_member_ids)
        if available_nums == 0:
            group.applied = [[], [], []]

no_seats = []
for member_id, applied in list(cls.members.items()):
    if not cls.members[member_id][3]:
        no_seats.append(member_id)

if debug:
    print(f"no_seats: {no_seats} \n")

if debug:
    print("------------\n"
          "-- SECOND --\n"
          "------------\n")
# 2차 추첨
for group_id, group in list(cls.groups.items()):
    if group.available_seats() > 0:
        available_nums = group.available_seats()
        chosen_member_ids = classes.multiple_choice(no_seats, available_nums)
        cls.group_set_owners(group_id, chosen_member_ids)

print("------------\n"
      "-- RESULT --\n"
      "------------\n")
for group_id, group in list(cls.groups.items()):
    group.owners.sort()
    print(f"{group_id}: ", end='')
    [print(f"{number:2}", end=' ') for number in group.owners]
    print()

if debug:
    print("-----------------\n"
          "-- MEMBER DATA --\n"
          "-----------------\n")
    for member_id, member_data in list(cls.members.items()):
        print(f"ID: {member_id:2} | {member_data}")

os.system("pause")
