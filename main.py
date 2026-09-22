from connector import get_connection, create_tables


def registration():
    username = input("Логин: ").strip()

    if not username:
        print("Логин не может быть пустым")
        return

    password = input("Пароль из 8 цифр: ").strip()

    if len(password) != 8 or not password.isdigit():
        print("Пароль должен состоять из 8 цифр")
        return
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    "select id from users where username = %s",
                    (username,)
                )

                if cursor.fetchone():
                    print("Такой пользователь уже существует")
                    return

                cursor.execute(
                    "insert into users(username, password) values(%s, %s)",
                    (username, password)
                )

        print("Регистрация успешна")

    except Exception as e:
        print("Ошибка:", e)


def login():
    username = input("Логин: ").strip()
    password = input("Пароль: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    select id
                    from users
                    where username = %s and password = %s
                    """,
                    (username, password)
                )

                user = cursor.fetchone()

                if user:
                    print("Вход выполнен")
                    return user[0]

                print("Неверный логин или пароль")
                return None

    except Exception as e:
        print("Ошибка:", e)
        return None


def add_task(user_id):
    title = input("Название задания: ").strip()

    if not title:
        print("Название не может быть пустым")
        return

    description = input("Описание: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    insert into tasks(title, description, user_id)
                    values(%s, %s, %s)
                    """,
                    (title, description, user_id)
                )

        print("Задание добавлено")

    except Exception as e:
        print("Ошибка:", e)


def show_tasks(user_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    select id, title, description
                    from tasks
                    where user_id = %s
                    order by id
                    """,
                    (user_id,)
                )

                tasks = cursor.fetchall()

                if not tasks:
                    print("У вас пока нет заданий")
                    return

                for task in tasks:
                    print(task)

    except Exception as e:
        print("Ошибка:", e)


def update_task(user_id):
    task_id = input("ID задания: ").strip()

    if not task_id.isdigit():
        print("ID должен быть числом")
        return

    title = input("Новое название: ").strip()

    if not title:
        print("Название не может быть пустым")
        return

    description = input("Новое описание: ").strip()

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    update tasks
                    set title = %s, description = %s
                    where id = %s and user_id = %s
                    """,
                    (title, description, task_id, user_id)
                )

                if cursor.rowcount == 0:
                    print("Задание не найдено")
                    return

        print("Задание обновлено")

    except Exception as e:
        print("Ошибка:", e)


def delete_task(user_id):
    task_id = input("ID задания: ").strip()

    if not task_id.isdigit():
        print("ID должен быть числом")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    delete from tasks
                    where id = %s and user_id = %s
                    """,
                    (task_id, user_id)
                )

                if cursor.rowcount == 0:
                    print("Задание не найдено")
                    return

        print("Задание удалено")

    except Exception as e:
        print("Ошибка:", e)


def task_menu(user_id):
    while True:
        print("""
1. Добавить задание
2. Посмотреть задания
3. Обновить задание
4. Удалить задание
0. Выйти из аккаунта
""")

        choice = input("Выберите: ").strip()

        if choice == "1":
            add_task(user_id)

        elif choice == "2":
            show_tasks(user_id)

        elif choice == "3":
            update_task(user_id)

        elif choice == "4":
            delete_task(user_id)

        elif choice == "0":
            break

        else:
            print("Выберите правильный пункт")


create_tables()

while True:
    print("""
1. Регистрация
2. Вход
0. Выход
""")

    choice = input("Выберите: ").strip()

    if choice == "1":
        registration()

    elif choice == "2":
        user_id = login()

        if user_id:
            task_menu(user_id)

    elif choice == "0":
        print("Программа завершена")
        break

    else:
        print("Выберите правильный пункт")
