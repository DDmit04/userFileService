# WEB Файловое хранилище.

---

Приложение взаимодействует с базой данных, в которой находится информация о всех файлах хранилища.

В качестве хранилища выступает файловая система компьютера.

---

### Функции:
- Получение списка файлов хранилища
- Получение списка файлов хранилища
- Загрузка/удаление файлов в хранилище
- Поиск всех файлов, находящихся по определённой части пути
- Скачивание файлов из хранилища
- Изменение информации о файле (имя, путь, комментарий к файлу)
- Синхронизация файлов хранилища с БД

---

### Используемые технологии и библиотеки
- Flask
- Postgresql
- SQLAlchemy

### Запуск приложения.

- Создать файл **./src/.env** с переменной DB_URL
```
DB_URL=<URL вышей БД>
```
- Запустить приложение
```
pip install -r ./src/requirements.txt
python ./src/app.py 
```