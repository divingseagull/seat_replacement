from random import choice


# random.choices 함수는 중복이 발생해 함수를 새로 만듬
def multiple_choice(lists: list, k: int) -> list:
    result = []
    if len(lists) < k:
        k = len(lists)
    if k == 0:
        return []
    for _ in range(k):
        chosen = choice(lists)
        lists.remove(chosen)
        result.append(chosen)
    return result


def _create_lists(total: int, divisor: int) -> list[int]:
    result = ([divisor] * (total // divisor))
    if (total % divisor) != 0:
        result.append(total % divisor)
    return result


class Member:  # 학생
    def __init__(self, student_id: int, applied: list[int]):
        self.id: int = student_id  # 학번
        self.applied: list[int] = applied  # 3의 길이를 가지는 리스트, 0: 1지망, 1: 2지망, 2: 3지망


class Seat:  # 좌석
    def __init__(self, seat_id: int):
        self.id: int = seat_id  # 좌석 ID
        self.owner: int | None = None  # 좌석 소유자


class SeatGroup:  # 구간
    def __init__(self, seats: list[Seat]):
        self.seats = seats
        self.applied: list[list[int]] = [[], [], []]  # 지원자 리스트, 0: 1지망, 1: 2지망, 2: 3지망
        self.owners: list[int] = []  # 구간 당첨자 리스트

    def available_seats(self) -> int:
        return len(self.seats) - len(self.owners)


class Class:  # 학급
    def __init__(self,
                 num_seats: int,
                 divisor: int,
                 member_datas: list[list[int, int | None, int | None, int | None, bool]],
                 start_num: int = 1,
                 /,
                 debug=False):
        self.groups: dict[int, SeatGroup] = dict()  # 학급의 구간 딕셔너리
        self.members: dict[int, list[int | None, int | None, int | None, bool]] = dict()  # 학급의 멤버 딕셔너리
        self.debug = debug

        # self.groups 초기화
        divided_num_seats = _create_lists(num_seats, divisor)
        for group_id, seats_num in enumerate(divided_num_seats, start=start_num):
            start = divisor * group_id + start_num
            end = start + seats_num
            d = {group_id: SeatGroup([Seat(seat_id) for seat_id in range(start, end)])}
            self.groups.update(d)

        # self.members 초기화
        for row in member_datas:  # row[0]: id, row[1]: first, row[2]: second, row[3]: third, True/False: has_group
            d = {row[0]: [row[1], row[2], row[3], False]}
            self.members.update(d)
            # 1, 2, 3지망에 지원
            for i in range(1, 4):
                if row[i] is None:
                    continue
                self.groups[row[i]].applied[i-1].append(row[0])

    def group_set_owners(self, group_id: int, owners: list[int]) -> None:  # 구간의 멤버 설정
        if self.debug:
            print(f"group_set_owners \n"
                  f"    group_id           : {group_id} \n"
                  f"    original_owners    : {self.groups[group_id].owners} \n"
                  f"    new_owners         : {owners} \n")
        self.groups[group_id].owners.extend(owners)
        for owner_id in owners:
            self.members[owner_id][3] = True
            print(f"    {owner_id}[3]: True")

        # remove_duplication
        for _group_id, group in list(self.groups.items()):
            if _group_id == group_id:
                continue
            else:
                for owner_id in owners:
                    for i in range(3):
                        try:
                            group.applied[i].remove(owner_id)
                        except ValueError:
                            continue
                        else:
                            before_removed = group.applied[i].copy()
                            before_removed.append(owner_id)
                            if self.debug:
                                print(f"    remove_duplication \n"
                                      f"        group_id       : {_group_id} \n"
                                      f"        applied        : {group.applied} \n"
                                      f"        index          : {i} \n"
                                      f"        owner_id       : {owner_id} \n"
                                      f"        before_removed : {before_removed} \n")
