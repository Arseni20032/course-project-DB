from validations import validate_gender, validate_date


def view_animals(cursor):
    query = "SELECT id, name, species, gender, birth_date, arrival_date FROM Animals;"
    cursor.execute(query)
    animals = cursor.fetchall()
    print("\nСписок всех животных:")
    for animal in animals:
        print(f"ID: {animal[0]}, Имя: {animal[1]}, Вид: {animal[2]}, Пол: {animal[3]}, Дата рождения: {animal[4]}, Дата прибытия: {animal[5]}")


def add_animal(cursor, connection):

    name = input("Введите имя животного: ").strip()
    while not name:
        print("Имя не может быть пустым. Попробуйте снова.")
        name = input("Введите имя животного: ").strip()

    species = input("Введите вид животного: ").strip()
    while not species:
        print("Вид не может быть пустым. Попробуйте снова.")
        species = input("Введите вид животного: ").strip()

    gender = input("Введите пол животного (М/Ж): ").strip()
    while not validate_gender(gender):
        print("Пол должен быть указан как 'М' (мужской) или 'Ж' (женский). Попробуйте снова.")
        gender = input("Введите пол животного (М/Ж): ").strip()
    gender = gender.upper()

    birth_date = input("Введите дату рождения животного (YYYY-MM-DD): ").strip()
    while not validate_date(birth_date):
        print("Неверный формат даты. Убедитесь, что дата соответствует формату или дата не указана в будущем.")
        birth_date = input("Введите дату рождения животного (YYYY-MM-DD): ").strip()

    arrival_date = input("Введите дату прибытия животного (YYYY-MM-DD): ").strip()
    while not validate_date(arrival_date):
        print("Неверный формат даты. Убедитесь, что дата соответствует формату YYYY-MM-DD.")
        arrival_date = input("Введите дату прибытия животного (YYYY-MM-DD): ").strip()

    cursor.execute("SELECT id, name FROM Enclosures;")
    enclosures = cursor.fetchall()
    if not enclosures:
        print("Нет доступных вольеров. Добавьте вольеры перед добавлением животного.")
        return

    print("Список вольеров:")
    for enclosure in enclosures:
        print(f"{enclosure[0]}. {enclosure[1]}")

    enclosure_id = input("Выберите ID вольера для животного: ").strip()
    while not enclosure_id.isdigit() or int(enclosure_id) not in [e[0] for e in enclosures]:
        print("Введите корректный ID вольера из предложенного списка.")
        enclosure_id = input("Выберите ID вольера для животного: ").strip()
    enclosure_id = int(enclosure_id)

    query = """INSERT INTO Animals (name, species, gender, birth_date, arrival_date, enclosure_id) 
               VALUES (%s, %s, %s, %s, %s, %s);"""
    cursor.execute(query, (name, species, gender, birth_date, arrival_date, enclosure_id))
    connection.commit()
    print(f"Животное {name} успешно добавлено.")


def validate_name_or_species(value):
    return bool(value.strip())


def update_animal(cursor, connection):
    # Проверка существования животного
    animal_id = input("Введите ID животного для изменения: ").strip()
    while not animal_id.isdigit():
        print("Ошибка: ID должен быть числом.")
        animal_id = input("Введите ID животного для изменения: ").strip()
    animal_id = int(animal_id)

    cursor.execute("SELECT COUNT(*) FROM Animals WHERE id = %s;", (animal_id,))
    if cursor.fetchone()[0] == 0:
        print("Ошибка: животное с таким ID не найдено.")
        return

    print("Что вы хотите изменить?")
    print("1. Имя")
    print("2. Вид")
    print("3. Пол")
    print("4. Вольер")

    choice = input("Выберите действие: ").strip()
    while choice not in ["1", "2", "3", "4"]:
        print("Ошибка: введите корректный номер действия.")
        choice = input("Выберите действие: ").strip()

    if choice == "1":
        new_name = input("Введите новое имя животного: ").strip()
        while not validate_name_or_species(new_name):
            print("Ошибка: имя не может быть пустым.")
            new_name = input("Введите новое имя животного: ").strip()

        query = "UPDATE Animals SET name = %s WHERE id = %s;"
        cursor.execute(query, (new_name, animal_id))

    elif choice == "2":
        new_species = input("Введите новый вид животного: ").strip()
        while not validate_name_or_species(new_species):
            print("Ошибка: вид не может быть пустым.")
            new_species = input("Введите новый вид животного: ").strip()

        query = "UPDATE Animals SET species = %s WHERE id = %s;"
        cursor.execute(query, (new_species, animal_id))

    elif choice == "3":
        new_gender = input("Введите новый пол животного (М/Ж): ").strip()
        while not validate_gender(new_gender):
            print("Ошибка: пол должен быть указан как 'М' (мужской) или 'Ж' (женский).")
            new_gender = input("Введите новый пол животного (М/Ж): ").strip()
        new_gender = new_gender.upper()

        query = "UPDATE Animals SET gender = %s WHERE id = %s;"
        cursor.execute(query, (new_gender, animal_id))

    elif choice == "4":
        print("Список вольеров:")
        cursor.execute("SELECT id, name FROM Enclosures;")
        enclosures = cursor.fetchall()
        if not enclosures:
            print("Нет доступных вольеров. Добавьте вольеры перед изменением.")
            return

        for enclosure in enclosures:
            print(f"{enclosure[0]}. {enclosure[1]}")

        new_enclosure_id = input("Выберите новый ID вольера для животного: ").strip()
        while not new_enclosure_id.isdigit() or int(new_enclosure_id) not in [e[0] for e in enclosures]:
            print("Ошибка: введите корректный ID вольера из предложенного списка.")
            new_enclosure_id = input("Выберите новый ID вольера для животного: ").strip()
        new_enclosure_id = int(new_enclosure_id)

        query = "UPDATE Animals SET enclosure_id = %s WHERE id = %s;"
        cursor.execute(query, (new_enclosure_id, animal_id))

    connection.commit()
    print("Данные животного успешно обновлены.")


def delete_animal(cursor, connection):
    animal_id = int(input("Введите ID животного для удаления: "))
    query = "DELETE FROM Animals WHERE id = %s;"
    cursor.execute(query, (animal_id,))
    connection.commit()
    print("Животное удалено.")
