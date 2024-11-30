def admin_menu(cursor, connection):
    while True:
        print("\n--- Меню администратора ---")
        print("1. Управление сотрудниками")
        print("2. Просмотр журнала действий сотрудников")
        print("3. Просмотр журнала действий посетителей")
        print("4. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            manage_employees(cursor, connection)
        elif choice == "2":
            view_actions_log(cursor)
        elif choice == "3":
            view_actions_log_visitors(cursor)
        elif choice == "4":
            break
        else:
            print("Неверный выбор, попробуйте еще раз.")


def authenticate_admin(cursor):
    name = input("Введите имя администратора: ")
    password = input("Введите пароль администратора: ")

    query = "SELECT id FROM Admins WHERE name = %s AND password = %s;"
    cursor.execute(query, (name, password))
    admin = cursor.fetchone()

    if admin:
        print(f"Добро пожаловать, {name}!")
        return admin[0]
    else:
        print("Неверное имя пользователя или пароль.")
        return None


def manage_employees(cursor, connection):
    while True:
        print("\n--- Управление сотрудниками ---")
        print("1. Добавить нового сотрудника")
        print("2. Удалить сотрудника")
        print("3. Изменить данные сотрудника")
        print("4. Просмотреть список сотрудников")
        print("5. Поиск сотрудника")
        print("6. Просмотр данных о животных")
        print("7. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            new_name = input("Введите имя нового сотрудника: ")
            new_password = input("Введите пароль нового сотрудника: ")
            new_position = input("Введите должность сотрудника: ")
            new_salary = input("Введите зарплату сотрудника: ")

            query = "INSERT INTO Employees (name, password, position, salary) VALUES (%s, %s, %s, %s);"
            cursor.execute(query, (new_name, new_password, new_position, new_salary))
            connection.commit()
            print(f"Сотрудник {new_name} добавлен.")

        elif choice == "2":
            employee_name = input("Введите имя сотрудника, которого хотите удалить: ")
            query = "DELETE FROM Employees WHERE name = %s;"
            cursor.execute(query, (employee_name,))
            connection.commit()
            print(f"Сотрудник {employee_name} удалён.")

        elif choice == "3":
            employee_name = input("Введите имя сотрудника для изменения данных: ")
            print("1. Изменить должность")
            print("2. Изменить зарплату")
            print("3. Изменить пароль")
            update_choice = input("Выберите действие: ")

            if update_choice == "1":
                new_position = input("Введите новую должность: ")
                query = "UPDATE Employees SET position = %s WHERE name = %s;"
                cursor.execute(query, (new_position, employee_name))
                connection.commit()
                print(f"Должность для сотрудника {employee_name} обновлена.")

            elif update_choice == "2":
                new_salary = input("Введите новую зарплату: ")
                query = "UPDATE Employees SET salary = %s WHERE name = %s;"
                cursor.execute(query, (new_salary, employee_name))
                connection.commit()
                print(f"Зарплата для сотрудника {employee_name} обновлена.")

            elif update_choice == "3":
                new_password = input("Введите новый пароль: ")
                query = "UPDATE Employees SET password = %s WHERE name = %s;"
                cursor.execute(query, (new_password, employee_name))
                connection.commit()
                print(f"Пароль для сотрудника {employee_name} обновлена.")
            else:
                print("Неверный выбор.")

        elif choice == "4":
            query = "SELECT name, password, position, salary FROM Employees;"
            cursor.execute(query)
            employees = cursor.fetchall()
            print("\nСписок сотрудников:")
            for employee in employees:
                print(f"Имя: {employee[0]}, Пароль: {employee[1]}, Должность: {employee[2]}, Зарплата: {employee[3]}")

        elif choice == "5":
            search = input("Введите имя сотрудника для поиска: ")
            query = "SELECT name, password, position, salary FROM Employees WHERE name = %s;"
            cursor.execute(query, (search,))
            employees = cursor.fetchall()
            if employees:
                print("\nРезультаты поиска:")
                for employee in employees:
                    print(f"Имя: {employee[0]}, Пароль: {employee[1]}, Должность: {employee[2]}, Зарплата: {employee[3]}")
            else:
                print("Сотрудники не найдены.")

        elif choice == "6":
            query = "SELECT name, species, birth_date FROM Animals;"
            cursor.execute(query)
            animals = cursor.fetchall()
            print("\nСписок животных:")
            for animal in animals:
                print(f"Имя: {animal[0]}, Вид: {animal[1]}, Дата рождения: {animal[2]}")

        elif choice == "7":
            print("Выход из управления сотрудниками.")
            break

        else:
            print("Неверный выбор, попробуйте еще раз.")


def view_actions_log(cursor):
    while True:
        print("\n--- Журнал действий ---")
        print("1. Просмотреть последние записи")
        print("2. Поиск по типу действия")
        print("3. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            query = "SELECT timestamp, action_type, details FROM ActionsLog ORDER BY timestamp DESC LIMIT 10;"
            cursor.execute(query)
            logs = cursor.fetchall()
            print("\nПоследние 10 записей:")
            for log in logs:
                print(f"Время: {log[0]}, Действие: {log[1]}, Подробности: {log[2]}")

        elif choice == "2":
            action_type = input("Введите тип действия: ")
            query = "SELECT timestamp, action_type, details FROM ActionsLog WHERE action_type = %s ORDER BY timestamp DESC;"
            cursor.execute(query, (action_type,))
            logs = cursor.fetchall()
            if logs:
                print(f"\nЗаписи для действия '{action_type}':")
                for log in logs:
                    print(f"Время: {log[0]}, Подробности: {log[1]}")
            else:
                print(f"Записей для действия '{action_type}' не найдено.")

        elif choice == "3":
            print("Выход из просмотра журнала действий.")
            break

        else:
            print("Неверный выбор, попробуйте еще раз.")


def view_actions_log_visitors(cursor):
    query = """SELECT al.id, al.visitor_id, v.name AS visitor_name, al.action_time, al.action_description
               FROM actionsLogVisitors al
               JOIN Visitors v ON al.visitor_id = v.id
               ORDER BY al.action_time DESC;"""
    cursor.execute(query)
    actions = cursor.fetchall()

    if actions:
        print("\nЛог действий посетителей:")
        for action in actions:
            print(f"ID: {action[0]}, Посетитель ID: {action[1]}, Имя: {action[2]}, "
                  f"Время: {action[3]}, Действие: {action[4]}")
    else:
        print("Лог действий пуст.")
