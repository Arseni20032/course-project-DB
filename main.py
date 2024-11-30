import psycopg2
from admin import admin_menu, authenticate_admin
from employee import employee_menu, authenticate_employee
from visitors import visitor_menu, authenticate_visitor, register_visitor


def connect():
    try:
        connection = psycopg2.connect(
            database="zoo_management",
            user="zoo_user",
            password="yourpassword",
            host="127.0.0.1",
            port="5432"
        )
        cursor = connection.cursor()
        print("Подключение к базе данных установлено.")

        while True:
            print("\n--- Главное меню ---")
            print("1. Вход")
            print("2. Регистрация")
            print("3. Выход")
            choice = input("Выберите действие: ")

            if choice == "1":
                print("\nКто вы?")
                print("1. Администратор")
                print("2. Сотрудник")
                print("3. Посетитель")
                role_choice = input("Выберите роль: ")

                if role_choice == "1":  # Администратор
                    admin_id = authenticate_admin(cursor)
                    if admin_id:
                        admin_menu(cursor, connection)
                    else:
                        print("Вы не админ!")

                elif role_choice == "2":  # Сотрудник
                    employee_id = authenticate_employee(cursor)
                    if employee_id:
                        employee_menu(cursor, connection, employee_id)

                elif role_choice == "3":  # Посетитель

                    visitor_id = authenticate_visitor(cursor)
                    if visitor_id:
                        visitor_menu(cursor, connection, visitor_id)
                        break
                    else:
                        print("Ошибка авторизации. Попробуйте снова.")
                else:
                    print("Некорректный выбор. Попробуйте снова.")

            elif choice == "2":
                register_visitor(cursor, connection)

            elif choice == "3":
                print("Завершение работы.")
                break

            else:
                print("Неверный выбор, попробуйте снова.")

        cursor.close()
        connection.close()
        print("Подключение к базе данных закрыто.")

    except Exception as e:
        print(f"Ошибка подключения: {e}")


connect()
