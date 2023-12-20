import csv
from src import sql

csv_path = input("CSV 파일의 경로\n > ")
_field_names = ["first", "second", "third"]
field_names = []
num_students = int(input("학생의 수\n > "))
field_name_id = input("학생의 번호가 될 열의 이름\n > ")

for f_name in _field_names:
    _n = input(f"{f_name}가 될 열의 이름\n > ")
    field_names.append(_n)

group_input = input("각 구간의 이름(쉼표로 구분)\n > ")
group_names: list[str] = []

for e in group_input.split(','):
    group_names.append(e.strip())


def extract_data(file):
    reader = csv.DictReader(file)
    result = []
    keys = [field_name_id]
    keys.extend(field_names)

    for row in reader:
        student_data = dict()
        for _name in keys:
            student_data[_name] = row[_name]
        result.append(student_data)

    return result


with open(csv_path, 'r', encoding="UTF-8") as csvfile:
    dict_datas = extract_data(csvfile)
    values = []
    students_ids = set()
    group_ids = dict()
    for g_id, g_name in enumerate(group_names, start=1):
        group_ids.update({g_name: g_id})

    for data in dict_datas:
        v = []
        students_ids.add(int(data[field_name_id]))
        used_values: set[int] = set()
        v.append(int(data[field_name_id]))

        for key in field_names:
            if data[key] != '':
                if group_ids[data[key]] in used_values:
                    value = None
                else:
                    value = group_ids[data[key]]
                    used_values.add(value)
            else:
                value = None
            v.append(value)
        values.append(v)

    sym_diff = students_ids.symmetric_difference({i for i in range(1, num_students + 1)})

    if sym_diff:
        for n in sym_diff:
            values.append([n, None, None, None])

    # FIXME: id 키 중복
    for value in values:
        sql.query("INSERT INTO students VALUES (%s, %s, %s, %s)", value)

print("데이터가 DB에 저장되었습니다.")
