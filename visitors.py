from animals import view_animals
from events import view_events, register_for_event


def visitor_menu(cursor, connection, visitor_id):
    while True:
        print("\n--- Меню посетителя ---")
        print("1. Просмотреть список животных")
        print("2. Оставить отзыв")
        print("3. Просмотреть предстоящие мероприятия")
        print("4. Купить билет")
        print("5. Зарегистрироваться на мероприятие")
        print("6. Просмотреть отзывы")
        print("7. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            view_animals(cursor)
        elif choice == "2":
            leave_review(cursor, connection, visitor_id)
        elif choice == "3":
            view_events(cursor)
        elif choice == "4":
            buy_ticket(cursor, connection, visitor_id)
        elif choice == "5":
            register_for_event(cursor, visitor_id, connection)
        elif choice == "6":
            view_reviews(cursor)
        elif choice == "7":
            break
        else:
            print("Неверный выбор, попробуйте снова.")


def register_visitor(cursor, connection):
    name = input("Введите ваше имя: ")
    password = input("Введите пароль: ")

    query = "SELECT id FROM Visitors WHERE name = %s;"
    cursor.execute(query, (name,))
    visitor = cursor.fetchone()

    if visitor:
        print("Посетитель с таким именем уже существует.")
        return

    query = "INSERT INTO Visitors (name, password) VALUES (%s, %s);"
    cursor.execute(query, (name, password))
    connection.commit()
    print(f"Посетитель '{name}' успешно зарегистрирован.")


def authenticate_visitor(cursor):
    name = input("Введите ваше имя: ")
    password = input("Введите пароль: ")

    query = "SELECT id FROM Visitors WHERE name = %s AND password = %s;"
    cursor.execute(query, (name, password))
    visitor = cursor.fetchone()

    if visitor:
        print(f"Добро пожаловать, {name}!")
        return visitor[0]
    else:
        print("Неверное имя или пароль.")
        return None


def leave_review(cursor, connection, visitor_id):
    query = "SELECT id FROM VisitorReviews WHERE visitor_id = %s;"
    cursor.execute(query, (visitor_id,))
    existing_review = cursor.fetchone()

    if existing_review:
        print("Вы уже оставили отзыв.")
        return

    while True:
        try:
            rating = int(input("Оцените зоопарк (1-5): "))
            if 1 <= rating <= 5:
                break
            else:
                print("Оценка должна быть от 1 до 5.")
        except ValueError:
            print("Введите корректное значение оценки.")

    comment = input("Введите ваш комментарий: ")

    query = """INSERT INTO VisitorReviews (visitor_id, rating, comment)
               VALUES (%s, %s, %s);"""
    cursor.execute(query, (visitor_id, rating, comment))
    connection.commit()
    print("Ваш отзыв успешно добавлен.")


def buy_ticket(cursor, connection, visitor_id):
    query = "SELECT id, name, date FROM Events WHERE date >= CURRENT_DATE ORDER BY date ASC;"
    cursor.execute(query)
    events = cursor.fetchall()

    if not events:
        print("На данный момент нет доступных мероприятий для покупки билетов.")
        return

    print("\nДоступные мероприятия:")
    for event in events:
        print(f"ID: {event[0]}, Название: {event[1]}, Дата: {event[2]}")

    while True:
        try:
            event_id = int(input("Введите ID мероприятия, на которое хотите купить билет: "))
            query = "SELECT id FROM Events WHERE id = %s AND date >= CURRENT_DATE;"
            cursor.execute(query, (event_id,))
            event = cursor.fetchone()

            if not event:
                print("Мероприятие с указанным ID не найдено или уже прошло. Попробуйте снова.")
            else:
                break
        except ValueError:
            print("Введите корректный ID мероприятия.")

    query = """INSERT INTO Tickets (visitor_id, event_id) 
               VALUES (%s, %s);"""
    cursor.execute(query, (visitor_id, event_id))
    connection.commit()

    print(f"Билет успешно куплен на мероприятие ID {event_id}.")


def view_reviews(cursor):
    query = """SELECT vr.rating, vr.comment, v.name 
               FROM VisitorReviews vr 
               JOIN Visitors v ON vr.visitor_id = v.id 
               ORDER BY vr.id DESC;"""
    cursor.execute(query)
    reviews = cursor.fetchall()

    if not reviews:
        print("На данный момент нет отзывов.")
        return

    print("\n--- Отзывы посетителей ---")
    for review in reviews:
        print(f"Посетитель: {review[2]}")
        print(f"Оценка: {review[0]} / 5")
        print(f"Комментарий: {review[1]}")
        print("-" * 40)


