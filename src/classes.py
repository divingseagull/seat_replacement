from random import choice


# 중복 없는 choices
def choices(lists: list, k: int) -> list:
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


def create_lists(total: int, divisor: int) -> list[int]:
    result = ([divisor] * (total // divisor))
    if (total % divisor) != 0:
        result.append(total % divisor)
    return result


class Member:  # 학생
    def __init__(self, student_id: int, applied: list[int, int, int]):
        self.id: int = student_id  # 학번
        self.applied: list[int, int, int] = applied  # 3의 길이를 가지는 리스트, 0: 1지망, 1: 2지망, 2: 3지망


class Seat:  # 좌석
    def __init__(self, seat_id: int):
        self.id: int = seat_id  # 좌석 ID
        self.owner: int | None = None  # 좌석 소유자


class SeatGroup:  # 구간
    def __init__(self, seats: list[Seat]):
        self.seats = seats
        # 지원자 리스트, 0: 1지망, 1: 2지망, 2: 3지망
        self.applied: list[list[int]] = [[], [], []]
        self.owners: list[int] = []  # 구간 당첨자 리스트

    def available_seats(self) -> int:
        return len(self.seats) - len(self.owners)


class Class:
    def __init__(self,
                 num_seats: int,
                 divisor: int,
                 member_datas: list[list[int, int | None, int | None, int | None, bool]]):
        """
        :param num_seats: 자리의 수
        :param divisor: 한 그룹의 최대 자리의 수
        :param member_datas: 각 멤버의 데이터
        """
        start_num = 1
        self.groups: dict[int, SeatGroup] = dict()
        self.members: dict[int, list[int | None, int | None, int | None, bool]] = dict()


        # self.groups 초기화
        divided_num_seats = create_lists(num_seats, divisor)
        for group_id, seats_num in enumerate(divided_num_seats):
            start = divisor * group_id + start_num
            end = start + seats_num
            seat_list = [Seat(seat_id) for seat_id in range(start, end)]
            group_data = {group_id: SeatGroup(seat_list)}

            self.groups.update(group_data)


        # self.members 초기화
        for row in member_datas:
            member_id = row[0]
            first = row[1]
            second = row[2]
            third = row[3]
            member_data = {member_id: [first, second, third, False]}

            self.members.update(member_data)
            # 1, 2, 3지망에 지원
            for i in range(1, 4):
                if row[i] is None:
                    continue
                group_nth_applied = self.groups[row[i]].applied[i-1]
                group_nth_applied.append(member_id)


    # 중복 제거
    def remove_duplications(self, target_group_id: int, owners_list: list[int]) -> None:
        for group_id, group in list(self.groups.items()):
            if group_id == target_group_id:
                continue
            else:
                for owner_id in owners_list:
                    for i in range(3):
                        try:
                            group.applied[i].remove(owner_id)
                        except ValueError:
                            continue
                        else:
                            before_removed = group.applied[i].copy()
                            before_removed.append(owner_id)


    # 구간의 멤버 설정
    def group_set_owners(self, target_group_id: int, owners_list: list[int]) -> None:
        self.groups[target_group_id].owners.extend(owners_list)
        for owner_id in owners_list:
            member_data = self.members[owner_id]
            member_data[3] = True

        self.remove_duplications(target_group_id, owners_list)
