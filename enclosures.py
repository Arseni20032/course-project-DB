
def add_enclosure(cursor, connection):
    name = input("Введите название вольера: ")

    location = input("Введите расположение вольера: ")

    query = """
    INSERT INTO Enclosures (name, location)
    VALUES (%s, %s);
    """
    cursor.execute(query, (name, location))
    connection.commit()
    print(f"Вольер {name} успешно добавлен.")


def update_enclosure(cursor, connection):
    enclosure_id = int(input("Введите ID вольера для изменения: "))
    print("Что вы хотите изменить?")
    print("1. Название")
    print("2. Расположение")

    choice = input("Выберите действие: ")

    if choice == "1":
        new_name = input("Введите новое название вольера: ")
        query = "UPDATE Enclosures SET name = %s WHERE id = %s;"
        cursor.execute(query, (new_name, enclosure_id))
    elif choice == "2":
        new_location = input("Введите новое расположение вольера: ")
        query = "UPDATE Enclosures SET location = %s WHERE id = %s;"
        cursor.execute(query, (new_location, enclosure_id))
    else:
        print("Неверный выбор.")
        return

    connection.commit()
    print("Данные вольера успешно обновлены.")


def delete_enclosure(cursor, connection):
    enclosure_id = int(input("Введите ID вольера для удаления: "))

    # Проверить, есть ли животные в вольере
    query_check = "SELECT COUNT(*) FROM Animals WHERE enclosure_id = %s;"
    cursor.execute(query_check, (enclosure_id,))
    count = cursor.fetchone()[0]

    if count > 0:
        print("Ошибка: В вольере находятся животные. Удаление невозможно.")
        return

    query_delete = "DELETE FROM Enclosures WHERE id = %s;"
    cursor.execute(query_delete, (enclosure_id,))
    connection.commit()
    print("Вольер успешно удален.")