import os

#
#   Скрипт для быстрого подсчёта количество строк в .py файлах проекта (без учета строк самого скрипта)
#

lst = [i for i in os.listdir(os.path.realpath("/".join(str(__file__).split("/")[0:-1])))
       if os.path.isfile(i) and i != "count_lines.py" and ".py" in i]
count = 0
for file in lst:
    with open(file, "r") as f:
        count_file = len(f.read().split("\n"))
        count += count_file
        print(f"{f.name} - {count_file}")

print(count)