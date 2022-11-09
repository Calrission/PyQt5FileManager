import os

#
#   Скрипт для быстрого подсчёта количество строк в .py файлах проекта (без учета строк самого скрипта)
#

lst = []
file = str(__file__).replace("/", "\\")
path = "\\".join(file.split("\\")[0:-1])
for i in os.listdir(os.path.realpath(path)):
    if i[0] == ".":
        continue
    path_i = path + "\\" + i
    if os.path.isfile(path_i):
        lst.append(path_i)
    else:
        for j in os.listdir(path_i):
            path_j = path_i + "\\" + j
            if os.path.isfile(path_j):
                lst.append(path_j)

lst = list(filter(lambda x: "count_lines.py" not in x and ".py" in x and ".pyc" not in x, lst))

count = 0
data = {}
for file in lst:
    with open(file, "r", encoding="utf-8") as f:
        count_file = len(f.read().split("\n"))
        count += count_file
        print(f"{f.name} - {count_file}")
        data[file] = count_file

print(f"Всего строчек: {count}")
print(f"Всего файлов .py: {len(lst)}")
