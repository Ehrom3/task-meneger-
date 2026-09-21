from connector import get_connection, create_table

def add_task():
    title = input("Название: ")
    description = input("Описание: ")
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "insert into tasks(title, description) values(%s, %s)",
                    (title, description)
                )
        conn.close()
        print("Задание добавлено")
    except Exception as r:
        print("Ошибка:", r)

def show_tasks():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("select * from tasks order by id")
                tasks = cursor.fetchall()
                for task in tasks:
                    print(task)
        conn.close()
    except Exception as r:
        print("Ошибка:", r)

def update_task():
    task_id = input("ID задания: ")
    title = input("Новое название: ")
    description = input("Новое описание: ")
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """update tasks
                    set title=%s, description=%s
                    where id=%s""",
                    (title, description, task_id)
                )
        conn.close()
        print("Задание обновлено")
    except Exception as r:
        print("Ошибка:", r)

def delete_task():
    task_id = input("ID задания: ")

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "delete from tasks where id=%s",
                    (task_id,)
                )
        conn.close()
        print("Задание удалено")
    except Exception as r:
        print("Ошибка:", r)

create_table()

while True:
    print("""
1. Добавить задание
2. Посмотреть задания
3. Обновить задание
4. Удалить задание
0. Выход
""")

    choice = input("Выберите: ")

    if choice == "1":
        add_task()
    elif choice == "2":
        show_tasks()
    elif choice == "3":
        update_task()
    elif choice == "4":
        delete_task()
    elif choice == "0":
        break
    else:
        print("Неверный выбор")