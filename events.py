def view_events(cursor):
    query = "SELECT id, name, date, description FROM Events WHERE date >= CURRENT_DATE ORDER BY date ASC;"
    cursor.execute(query)
    events = cursor.fetchall()
    if events:
        print("\nПредстоящие мероприятия:")
        for event in events:
            print(f"ID: {event[0]}, Название: {event[1]}, Дата: {event[2]}, Описание: {event[3]}")
    else:
        print("Нет предстоящих мероприятий.")


def add_event(cursor, connection, employee_id):
    name = input("Введите название события: ")
    date = input("Введите дату события (YYYY-MM-DD): ")
    description = input("Введите описание события: ")

    query = """
    INSERT INTO Events (name, date, description, employee_in_charge) 
    VALUES (%s, %s, %s, %s);
    """
    cursor.execute(query, (name, date, description, employee_id))
    connection.commit()
    print(f"Событие '{name}' успешно добавлено.")


def update_event(cursor, connection):
    event_id = int(input("Введите ID события для изменения: "))
    print("Что вы хотите изменить?")
    print("1. Название")
    print("2. Дата")
    print("3. Описание")
    choice = input("Выберите действие: ")

    if choice == "1":
        new_name = input("Введите новое название: ")
        query = "UPDATE Events SET name = %s WHERE id = %s;"
        cursor.execute(query, (new_name, event_id))
    elif choice == "2":
        new_date = input("Введите новую дату (YYYY-MM-DD): ")
        query = "UPDATE Events SET date = %s WHERE id = %s;"
        cursor.execute(query, (new_date, event_id))
    elif choice == "3":
        new_description = input("Введите новое описание: ")
        query = "UPDATE Events SET description = %s WHERE id = %s;"
        cursor.execute(query, (new_description, event_id))
    else:
        print("Неверный выбор.")
        return

    connection.commit()
    print("Событие обновлено.")


def delete_event(cursor, connection):
    event_id = int(input("Введите ID события для удаления: "))
    query = "DELETE FROM Events WHERE id = %s;"
    cursor.execute(query, (event_id,))
    connection.commit()
    print("Событие удалено.")


def register_for_event(cursor, visitor_id, connection):
    query = "SELECT id, name, date FROM Events WHERE date >= CURRENT_DATE ORDER BY date ASC;"
    cursor.execute(query)
    events = cursor.fetchall()

    if not events:
        print("Нет доступных мероприятий для регистрации.")
        return

    print("\nДоступные мероприятия:")
    for event in events:
        print(f"ID: {event[0]}, Название: {event[1]}, Дата: {event[2]}")

    event_id = int(input("Введите ID мероприятия для регистрации: "))

    query = "SELECT id FROM Events WHERE id = %s AND date >= CURRENT_DATE;"
    cursor.execute(query, (event_id,))
    event = cursor.fetchone()

    if not event:
        print("Мероприятие с указанным ID не найдено или уже прошло.")
        return

    query = "SELECT id FROM Tickets WHERE visitor_id = %s AND event_id = %s;"
    cursor.execute(query, (visitor_id, event_id))
    ticket = cursor.fetchone()

    if not ticket:
        print("Вы не купили билет на это мероприятие. Сначала купите билет.")
        return

    query = "SELECT id FROM EventRegistrations WHERE visitor_id = %s AND event_id = %s;"
    cursor.execute(query, (visitor_id, event_id))
    registration = cursor.fetchone()

    if registration:
        print("Вы уже зарегистрированы на это мероприятие.")
        return

    query = "INSERT INTO EventRegistrations (visitor_id, event_id) VALUES (%s, %s);"
    cursor.execute(query, (visitor_id, event_id))
    connection.commit()
    print(f"Вы успешно зарегистрировались на мероприятие ID {event_id}.")
