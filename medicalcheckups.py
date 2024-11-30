from datetime import datetime


def view_medical_checkups(cursor, employee_id):
    query = """SELECT mc.id, a.id AS animal_id, a.name AS animal_name, mc.checkup_date, mc.observations, mc.prescribed_treatment
               FROM MedicalCheckups mc
               JOIN Animals a ON mc.animal_id = a.id
               WHERE mc.employee_id = %s
               ORDER BY mc.checkup_date DESC;"""
    cursor.execute(query, (employee_id,))
    checkups = cursor.fetchall()

    if checkups:
        print("\nМедицинские осмотры:")
        for checkup in checkups:
            print(f"ID осмотра: {checkup[0]}, Животное ID: {checkup[1]}, Название животного: {checkup[2]}, "
                  f"Дата осмотра: {checkup[3]}, Наблюдения: {checkup[4]}, Назначенное лечение: {checkup[5]}")
    else:
        print("Нет записей о медицинских осмотрах.")


def add_medical_checkup(cursor, connection, employee_id):
    query = "SELECT id, name FROM Animals;"
    cursor.execute(query)
    animals = cursor.fetchall()

    if not animals:
        print("Нет животных в базе данных.")
        return

    print("\nСписок животных:")
    for animal in animals:
        print(f"ID: {animal[0]}, Название: {animal[1]}")

    animal_id = int(input("Введите ID животного для осмотра: "))

    query = "SELECT id FROM Animals WHERE id = %s;"
    cursor.execute(query, (animal_id,))
    animal = cursor.fetchone()

    if not animal:
        print("Животное с таким ID не найдено.")
        return

    checkup_date = datetime.now().strftime('%Y-%m-%d')

    observations = input("Введите наблюдения: ")
    prescribed_treatment = input("Введите назначенное лечение: ")

    query = """INSERT INTO MedicalCheckups (animal_id, employee_id, checkup_date, observations, prescribed_treatment)
               VALUES (%s, %s, %s, %s, %s);"""
    cursor.execute(query, (animal_id, employee_id, checkup_date, observations, prescribed_treatment))
    connection.commit()

    print(f"Медицинский осмотр для животного ID {animal_id} успешно добавлен.")


def update_medical_checkup(cursor, connection, employee_id):
    query = """SELECT id, animal_id, checkup_date, observations, prescribed_treatment 
               FROM MedicalCheckups 
               WHERE employee_id = %s;"""
    cursor.execute(query, (employee_id,))
    checkups = cursor.fetchall()

    if not checkups:
        print("Нет записей о медицинских осмотрах.")
        return

    print("\nСписок медицинских осмотров:")
    for checkup in checkups:
        print(f"ID: {checkup[0]}, Животное ID: {checkup[1]}, Дата: {checkup[2]}, "
              f"Наблюдения: {checkup[3]}, Лечение: {checkup[4]}")

    checkup_id = int(input("Введите ID осмотра для изменения: "))

    query = "SELECT id FROM MedicalCheckups WHERE id = %s AND employee_id = %s;"
    cursor.execute(query, (checkup_id, employee_id))
    checkup = cursor.fetchone()

    if not checkup:
        print("Осмотр с таким ID не найден.")
        return

    observations = input("Введите новые наблюдения (оставьте пустым для пропуска): ")
    prescribed_treatment = input("Введите новое назначенное лечение (оставьте пустым для пропуска): ")

    query = """UPDATE MedicalCheckups 
               SET observations = COALESCE(%s, observations), 
                   prescribed_treatment = COALESCE(%s, prescribed_treatment)
               WHERE id = %s AND employee_id = %s;"""
    cursor.execute(query, (observations or None, prescribed_treatment or None, checkup_id, employee_id))
    connection.commit()

    print(f"Медицинский осмотр ID {checkup_id} успешно обновлён.")


def delete_medical_checkup(cursor, connection, employee_id):
    checkup_id = int(input("Введите ID осмотра для удаления: "))

    query = "SELECT id FROM MedicalCheckups WHERE id = %s AND employee_id = %s;"
    cursor.execute(query, (checkup_id, employee_id))
    checkup = cursor.fetchone()

    if not checkup:
        print("Осмотр с таким ID не найден.")
        return

    query = "DELETE FROM MedicalCheckups WHERE id = %s AND employee_id = %s;"
    cursor.execute(query, (checkup_id, employee_id))
    connection.commit()

    print(f"Медицинский осмотр ID {checkup_id} успешно удалён.")
