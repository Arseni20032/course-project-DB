def view_feeding_schedules(cursor):
    query = """SELECT fs.id, a.id AS animal_id, a.name AS animal_name, fs.feeding_time, fs.food_type, fs.food_quantity, e.name AS staff_member_name
               FROM FeedingSchedules fs
               JOIN Animals a ON fs.animal_id = a.id
               JOIN Employees e ON fs.staff_member_id = e.id
               ORDER BY fs.feeding_time;"""
    cursor.execute(query)
    schedules = cursor.fetchall()

    if schedules:
        print("\nВсе расписания кормления:")
        for schedule in schedules:
            print(f"ID расписания: {schedule[0]}, Животное ID: {schedule[1]}, Название животного: {schedule[2]}, "
                  f"Время: {schedule[3]}, Корм: {schedule[4]}, Количество: {schedule[5]} кг, Кормит: {schedule[6]}")
    else:
        print("Нет расписаний кормлений в базе данных.")


def add_feeding_schedule(cursor, connection, employee_id):
    query = "SELECT id, name FROM Animals;"
    cursor.execute(query)
    animals = cursor.fetchall()

    if not animals:
        print("Нет животных в базе данных.")
        return

    print("\nСписок животных:")
    for animal in animals:
        print(f"ID: {animal[0]}, Название: {animal[1]}")

    animal_id = int(input("Введите ID животного для добавления кормления: "))

    query = "SELECT id FROM Animals WHERE id = %s;"
    cursor.execute(query, (animal_id,))
    animal = cursor.fetchone()

    if not animal:
        print("Животное с таким ID не найдено.")
        return

    feeding_time_str = input("Введите время кормления (HH:MM): ")

    try:
        feeding_time = f'{feeding_time_str}:00'
    except ValueError:
        print("Некорректный формат времени. Используйте HH:MM.")
        return

    # Проверяем, существует ли уже расписание кормления для этого животного в интервале ±3 часа
    query = """SELECT id FROM FeedingSchedules 
               WHERE animal_id = %s 
               AND feeding_time BETWEEN (TIME %s - INTERVAL '3 HOURS') AND (TIME %s + INTERVAL '3 HOURS');"""
    cursor.execute(query, (animal_id, feeding_time_str, feeding_time_str))
    existing_schedule = cursor.fetchone()

    if existing_schedule:
        print(f"Расписание кормления для животного ID {animal_id} уже существует в интервале ±3 часа от {feeding_time_str}.")
        return

    food_type = input("Введите тип корма: ")
    food_quantity = float(input("Введите количество корма (кг): "))

    query = """INSERT INTO FeedingSchedules (animal_id, feeding_time, food_type, food_quantity, staff_member_id)
               VALUES (%s, %s, %s, %s, %s);"""
    cursor.execute(query, (animal_id, feeding_time, food_type, food_quantity, employee_id))
    connection.commit()

    print(f"Расписание кормления для животного ID {animal_id} успешно добавлено.")


def update_feeding_schedule(cursor, connection, employee_id):
    query = "SELECT id, animal_id, feeding_time, food_type, food_quantity FROM FeedingSchedules;"
    cursor.execute(query)
    feeding_schedules = cursor.fetchall()

    if not feeding_schedules:
        print("Нет расписаний кормлений в базе данных.")
        return

    print("\nСписок расписаний кормлений:")
    for schedule in feeding_schedules:
        print(f"ID: {schedule[0]}, Животное ID: {schedule[1]}, Время: {schedule[2]}, Корм: {schedule[3]}, Количество: {schedule[4]}")

    feeding_id = int(input("Введите ID расписания кормления для изменения: "))

    query = "SELECT id, animal_id, feeding_time FROM FeedingSchedules WHERE id = %s;"
    cursor.execute(query, (feeding_id,))
    schedule = cursor.fetchone()

    if not schedule:
        print("Расписание с таким ID не найдено.")
        return

    animal_id = schedule[1]

    feeding_time_str = input("Введите новое время кормления (HH:MM): ")

    try:
        feeding_time = f'{feeding_time_str}:00'  # Преобразуем время в формат для SQL
    except ValueError:
        print("Некорректный формат времени. Используйте HH:MM.")
        return

    # Проверяем, существует ли уже расписание кормления для этого животного в интервале ±3 часа от нового времени
    query = """SELECT id FROM FeedingSchedules 
               WHERE animal_id = %s 
               AND feeding_time BETWEEN (TIME %s - INTERVAL '3 HOURS') AND (TIME %s + INTERVAL '3 HOURS')
               AND id != %s;"""  # Исключаем текущее расписание
    cursor.execute(query, (animal_id, feeding_time_str, feeding_time_str, feeding_id))
    existing_schedule = cursor.fetchone()

    if existing_schedule:
        print(f"Расписание кормления для животного ID {animal_id} уже существует в интервале ±3 часа от {feeding_time_str}.")
        return

    food_type = input("Введите новый тип корма: ")
    food_quantity = float(input("Введите новое количество корма (кг): "))

    query = """UPDATE FeedingSchedules 
               SET feeding_time = %s, food_type = %s, food_quantity = %s, staff_member_id = %s
               WHERE id = %s;"""
    cursor.execute(query, (feeding_time, food_type, food_quantity, employee_id, feeding_id))
    connection.commit()

    print(f"Расписание кормления ID {feeding_id} успешно обновлено.")


def delete_feeding_schedule(cursor, connection, feeding_id):
    query = """DELETE FROM FeedingSchedules WHERE id = %s;"""
    cursor.execute(query, (feeding_id,))
    connection.commit()

    print(f"Расписание кормления с ID {feeding_id} успешно удалено.")
