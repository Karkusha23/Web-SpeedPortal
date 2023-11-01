# ТЗ по БД
## Описание
### Общее описание
SpeedPortal - веб-платформа для расмещения и просмотра спидранов пользователей в разных играх и категориях. Авторизованный пользователь может оставить заявку на размещение его рана в общей таблице, модератор должен будет его проверить на валидность и принять решение - публиковать его или нет
### Предметная область
Предметная область включает следующие сущности:
* Пользователь
* Игра
* Категория спидрана
* Ран (забег)
* Комментарий к рану
## Данные
### Пользователь
Должны храниться следующие данные о пользователе
* Уникальный идентификатор
* Имя пользователя (уникальное)
* Адрес электронной почты (уникальный)
* Пароль
* Изображение профиля (аватар)
* Количество набранных очков
* Биография ("о себе")
* Является ли пользователь модератором, если да, то какие имеет полномочия, например, повышать до модераторов других пользователей, одобраять или отклонять раны, банить пользователей
Модераторы имеют полномочия только в рамках своей "компетенции", то есть перечня игр, в которых они могут объективно оценивать валидность рана
* Забанен ли пользователь, если да, то причина бана
### Игра
Должны храниться следующие данные об игре
* Название (уникальное)
* Ссылка на игру в Steam (уникальная)
* Иконка
* Банер
* Описание
* Доступные категории спидранов
Для категорий в свою очередь требуется хранить их уникальное название и описание
### Раны
Должна храниться следующая информация о ране
* Игра
* Категория
* Время пробега
* Ссылка на видео с раном
* Статус рана - на рассмотрении, принят, отклонен, идентификатор модератора, проверявшего ран, если отклонен, то причина отказа
### Для каждого элемента данных - ограничения
### Общие ограничения целостности
## Пользовательские роли
### Для каждой роли - наименование, ответственность, количество пользователей в этой роли?
## UI / API 
Django
## Технологии разработки
### Язык программирования
* Python
* JS
### СУБД
PostgreSQL
## Тестирование