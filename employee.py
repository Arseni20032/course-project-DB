from animals import view_animals, add_animal, update_animal, delete_animal
from enclosures import add_enclosure, update_enclosure, delete_enclosure
from events import view_events, add_event, update_event, delete_event
from feeding import view_feeding_schedules, add_feeding_schedule, update_feeding_schedule, delete_feeding_schedule
from medicalcheckups import view_medical_checkups, add_medical_checkup, update_medical_checkup, delete_medical_checkup


def employee_menu(cursor, connection, employee_id):
    while True:
        print("\n--- Меню сотрудника ---")
        print("1. Управление животными")
        print("2. Управление вольерами")
        print("3. Управление событиями")
        print("4. Управление кормлением животных")
        print("5. Управление медицинскими осмотрами")
        print("6. Выход")
        choice = input("Выберите категорию: ")

        if choice == "1":
            while True:
                print("\n--- Управление животными ---")
                print("1. Просмотр данных о животных")
                print("2. Добавление нового животного")
                print("3. Изменение данных животного")
                print("4. Удаление животного")
                print("5. Назад")
                sub_choice = input("Выберите действие: ")

                if sub_choice == "1":
                    view_animals(cursor)
                elif sub_choice == "2":
                    add_animal(cursor, connection)
                elif sub_choice == "3":
                    update_animal(cursor, connection)
                elif sub_choice == "4":
                    delete_animal(cursor, connection)
                elif sub_choice == "5":
                    break
                else:
                    print("Неверный выбор, попробуйте еще раз.")

        elif choice == "2":
            while True:
                print("\n--- Управление вольерами ---")
                print("1. Добавление нового вольера")
                print("2. Изменение данных вольера")
                print("3. Удаление вольера")
                print("4. Назад")
                sub_choice = input("Выберите действие: ")

                if sub_choice == "1":
                    add_enclosure(cursor, connection)
                elif sub_choice == "2":
                    update_enclosure(cursor, connection)
                elif sub_choice == "3":
                    delete_enclosure(cursor, connection)
                elif sub_choice == "4":
                    break
                else:
                    print("Неверный выбор, попробуйте еще раз.")
        elif choice == "3":
            while True:
                print("\n--- Управление событиями ---")
                print("1. Просмотр событий")
                print("2. Добавление нового события")
                print("3. Изменение события")
                print("4. Удаление события")
                print("5. Назад")
                sub_choice = input("Выберите действие: ")
                if sub_choice == "1":
                    view_events(cursor)
                elif sub_choice == "2":
                    add_event(cursor, connection, employee_id)
                elif sub_choice == "3":
                    update_event(cursor, connection)
                elif sub_choice == "4":
                    delete_event(cursor, connection)
                elif sub_choice == "5":
                    break
                else:
                    print("Неверный выбор, попробуйте еще раз.")
        elif choice == "4":
            while True:
                print("\n--- Управление кормлением животных ---")
                print("1. Посмотреть расписание кормления")
                print("2. Добавить расписание кормления")
                print("3. Изменить расписание кормления")
                print("4. Удалить расписание кормления")
                print("5. Назад")
                sub_choice = input("Выберите действие: ")
                if sub_choice == "1":
                    view_feeding_schedules(cursor)
                elif sub_choice == "2":
                    add_feeding_schedule(cursor, connection, employee_id)
                elif sub_choice == "3":
                    update_feeding_schedule(cursor, connection, employee_id)
                elif sub_choice == "4":
                    feeding_id = int(input("Введите ID расписания кормления для удаления: "))
                    delete_feeding_schedule(cursor, connection, feeding_id)
                elif sub_choice == "5":
                    break
                else:
                    print("Неверный выбор, попробуйте еще раз.")
        elif choice == "5":
            while True:
                print("\n--- Управление медицинскими осмотрами ---")
                print("1. Посмотреть мед. осмотр")
                print("2. Добавить мед. осмотр")
                print("3. Изменить мед. осмотр")
                print("4. Удалить мед. осмотр")
                print("5. Назад")
                sub_choice = input("Выберите действие: ")
                if sub_choice == "1":
                    view_medical_checkups(cursor, employee_id)
                elif sub_choice == "2":
                    add_medical_checkup(cursor, connection, employee_id)
                elif sub_choice == "3":
                    update_medical_checkup(cursor, connection, employee_id)
                elif sub_choice == "4":
                    delete_medical_checkup(cursor, connection, employee_id)
                elif sub_choice == "5":
                    break
                else:
                    print("Неверный выбор, попробуйте еще раз.")
        elif choice == "6":
            print("Выход из меню сотрудника.")
            break
        else:
            print("Неверный выбор, попробуйте еще раз.")


def authenticate_employee(cursor):
    name = input("Введите имя сотрудника: ")
    password = input("Введите пароль: ")

    query = """
    SELECT id, position 
    FROM Employees 
    WHERE name = %s AND password = %s;
    """
    cursor.execute(query, (name, password))
    result = cursor.fetchone()

    if result:
        employee_id = result[0]
        print(f"Добро пожаловать, {name}!")
        return employee_id
    else:
        print("Неверные учетные данные сотрудника.")
        return None



