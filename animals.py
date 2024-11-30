def view_animals(cursor):
    query = "SELECT id, name, species, gender, birth_date, arrival_date FROM Animals;"
    cursor.execute(query)
    animals = cursor.fetchall()
    print("\nСписок всех животных:")
    for animal in animals:
        print(f"ID: {animal[0]}, Имя: {animal[1]}, Вид: {animal[2]}, Пол: {animal[3]}, Дата рождения: {animal[4]}, Дата прибытия: {animal[5]}")


def add_animal(cursor, connection):
    name = input("Введите имя животного: ")
    species = input("Введите вид животного: ")
    gender = input("Введите пол животного (М/Ж): ")
    birth_date = input("Введите дату рождения животного (YYYY-MM-DD): ")
    arrival_date = input("Введите дату прибытия животного (YYYY-MM-DD): ")

    cursor.execute("SELECT id, name FROM Enclosures;")
    enclosures = cursor.fetchall()
    print("Список вольеров:")
    for enclosure in enclosures:
        print(f"{enclosure[0]}. {enclosure[1]}")

    enclosure_id = int(input("Выберите вольер для животного: "))

    query = """INSERT INTO Animals (name, species, gender, birth_date, arrival_date, enclosure_id) 
               VALUES (%s, %s, %s, %s, %s, %s);"""
    cursor.execute(query, (name, species, gender, birth_date, arrival_date, enclosure_id))
    connection.commit()
    print(f"Животное {name} успешно добавлено.")


def update_animal(cursor, connection):
    animal_id = int(input("Введите ID животного для изменения: "))
    print("Что вы хотите изменить?")
    print("1. Имя")
    print("2. Вид")
    print("3. Пол")
    print("4. Вольер")

    choice = input("Выберите действие: ")

    if choice == "1":
        new_name = input("Введите новое имя животного: ")
        query = "UPDATE Animals SET name = %s WHERE id = %s;"
        cursor.execute(query, (new_name, animal_id))
    elif choice == "2":
        new_species = input("Введите новый вид животного: ")
        query = "UPDATE Animals SET species = %s WHERE id = %s;"
        cursor.execute(query, (new_species, animal_id))
    elif choice == "3":
        new_gender = input("Введите новый пол животного (М/Ж): ")
        query = "UPDATE Animals SET gender = %s WHERE id = %s;"
        cursor.execute(query, (new_gender, animal_id))
    elif choice == "4":
        print("Список вольеров:")
        cursor.execute("SELECT id, name FROM Enclosures;")
        enclosures = cursor.fetchall()
        for enclosure in enclosures:
            print(f"{enclosure[0]}. {enclosure[1]}")

        new_enclosure_id = int(input("Выберите новый вольер для животного: "))

        cursor.execute("SELECT COUNT(*) FROM Enclosures WHERE id = %s;", (new_enclosure_id,))
        if cursor.fetchone()[0] == 0:
            print("Ошибка: выбранный вольер не существует.")
            return

        query = "UPDATE Animals SET enclosure_id = %s WHERE id = %s;"
        cursor.execute(query, (new_enclosure_id, animal_id))

    connection.commit()
    print("Данные животного обновлены.")


def delete_animal(cursor, connection):
    animal_id = int(input("Введите ID животного для удаления: "))
    query = "DELETE FROM Animals WHERE id = %s;"
    cursor.execute(query, (animal_id,))
    connection.commit()
    print("Животное удалено.")