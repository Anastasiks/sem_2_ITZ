import pandas as pd

# читаем файлы
osen = pd.read_excel("Список 15вар - осень.xls")
vesna = pd.read_excel("Список 15вар - весна.xls")
# добавляем столбец с семестром
osen["Семестр"] = "Осень"
vesna["Семестр"] = "Весна"
# объединяем две таблицы
itog = pd.concat([osen, vesna], ignore_index=True)
# сохраняем новый сводный файл
itog.to_excel("Сводный файл текущего года.xlsx", index=False)
print("Файл создан")