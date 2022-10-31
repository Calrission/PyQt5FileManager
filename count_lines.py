import os

#
#   Скрипт для быстрого подсчёта количсетво строк в .py файлах проекта
#

lst = [i for i in os.listdir(os.path.realpath("/".join(str(__file__).split("/")[0:-1])))
       if os.path.isfile(i) and i != "count_lines.py" and ".py" in i]
count = 0
for file in lst:
    with open(file, "r") as f:
        count += len(f.read().split("\n"))

print(count)