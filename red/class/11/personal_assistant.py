import json
import csv
import sys
import re
from datetime import datetime


class DataModel:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_data(self):
        with open(self.file_name, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def find_by_id(self, item_id):
        return next((item for item in self.data if item['id'] == item_id), None)


class NoteModel(DataModel):
    def __init__(self, file_name="notes.json"):
        super().__init__(file_name)

    def add(self, title, content):
        note_id = len(self.data) + 1
        timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        self.data.append({"id": note_id, "title": title, "content": content, "timestamp": timestamp})
        self.save_data()

    def edit(self, note_id, title=None, content=None):
        note = self.find_by_id(note_id)
        if note:
            note['title'] = title or note['title']
            note['content'] = content or note['content']
            note['timestamp'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.save_data()

    def delete(self, note_id):
        self.data = [note for note in self.data if note['id'] != note_id]
        self.save_data()

    def export_to_csv(self, file_name):
        with open(file_name, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["id", "title", "content", "timestamp"])
            writer.writeheader()
            writer.writerows(self.data)

    def import_from_csv(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.data.append(row)
            self.save_data()
        except FileNotFoundError:
            print("Файл не найден.")


class PersonalAssistant:
    def __init__(self):
        self.notes = NoteModel()

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, '%d-%m-%Y')
            return True
        except ValueError:
            return False

    def validate_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def manage_notes(self):
        while True:
            print("\nУправление заметками:")
            print("1. Добавить новую заметку")
            print("2. Просмотреть список заметок")
            print("3. Просмотреть заметку")
            print("4. Редактировать заметку")
            print("5. Удалить заметку")
            print("6. Экспорт заметок в CSV")
            print("7. Импорт заметок из CSV")
            print("8. Назад")
            choice = input("Выберите действие: ")

            if choice == "1":
                title = input("Введите заголовок заметки: ")
                content = input("Введите содержимое заметки: ")
                self.notes.add(title, content)
                print("Заметка успешно добавлена!")
            elif choice == "2":
                for note in self.notes.data:
                    print(f"ID: {note['id']}, Заголовок: {note['title']}, Дата: {note['timestamp']}")
            elif choice == "3":
                note_id = int(input("Введите ID заметки: "))
                note = self.notes.find_by_id(note_id)
                if note:
                    print(f"Заголовок: {note['title']}\nСодержимое: {note['content']}\nДата: {note['timestamp']}")
                else:
                    print("Заметка не найдена.")
            elif choice == "4":
                note_id = int(input("Введите ID заметки: "))
                title = input("Введите новый заголовок (или оставьте пустым): ")
                content = input("Введите новое содержимое (или оставьте пустым): ")
                self.notes.edit(note_id, title or None, content or None)
                print("Заметка успешно обновлена!")
            elif choice == "5":
                note_id = int(input("Введите ID заметки: "))
                self.notes.delete(note_id)
                print("Заметка успешно удалена!")
            elif choice == "6":
                file_name = input("Введите имя файла для экспорта: ")
                self.notes.export_to_csv(file_name)
                print(f"Заметки экспортированы в {file_name}")
            elif choice == "7":
                file_name = input("Введите имя CSV-файла для импорта: ")
                self.notes.import_from_csv(file_name)
                print("Заметки успешно импортированы!")
            elif choice == "8":
                break
            else:
                print("Неверный ввод, попробуйте снова.")

    def main_menu(self):
        while True:
            print("\nДобро пожаловать в Персональный помощник!")
            print("Выберите действие:")
            print("1. Управление заметками")
            print("2. Выход")
            choice = input("Введите номер действия: ")

            if choice == "1":
                self.manage_notes()
            elif choice == "2":
                print("Выход из программы. До свидания!")
                sys.exit()
            else:
                print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    app = PersonalAssistant()
    app.main_menu()
