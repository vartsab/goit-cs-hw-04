import threading
import time
import os
from faker import Faker

# Генерація файлів з випадковим текстом
def generate_files():
    fake = Faker()
    for i in range(1, 4):
        file_name = f"file{i}.txt"
        content = fake.text()
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated {file_name}:")
        print(content)

# Перевірка наявності файлів
def check_existing_files():
    existing_files = []
    for i in range(1, 4):
        file_name = f"file{i}.txt"
        if os.path.exists(file_name):
            existing_files.append(file_name)
    return existing_files

# Функція для пошуку ключових слів у файлі
def search_in_file(file_path, keywords, results):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for word in keywords:
                count = content.count(word)  # Підраховуємо кількість входжень слова
                if count > 0:
                    if word not in results:
                        results[word] = []
                    results[word].append((file_path, count))  # Додаємо кількість входжень у кожному файлі
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Функція для обробки файлів у потоках
def process_files_threading(file_paths, keywords):
    threads = []
    results = {}

    for file_path in file_paths:
        thread = threading.Thread(target=search_in_file, args=(file_path, keywords, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results

# Основна програма для багатопотокового підходу
def main_threading(file_paths, keywords):
    start_time = time.time()
    results = process_files_threading(file_paths, keywords)
    end_time = time.time()
    
    print(f"Threading execution time: {end_time - start_time:.2f} seconds")
    return results

if __name__ == "__main__":
    # Перевірка наявності файлів
    existing_files = check_existing_files()

    if existing_files:
        print(f"Existing files found: {', '.join(existing_files)}")
        user_input = input("Do you want to generate new files? (y/n): ").strip().lower()
        if user_input == 'y':
            generate_files()
        else:
            print("Using existing files.")
    else:
        print("No existing files found. Generating new files.")
        generate_files()

    # Приклад використання
    file_paths = ["file1.txt", "file2.txt", "file3.txt"]  # Список файлів
    keywords = ["k", "e", "y"]  # Ключові слова
    threading_results = main_threading(file_paths, keywords)

    # Виведення результатів пошуку
    if threading_results:
        for word, occurrences in threading_results.items():
            print(f"\nWord '{word}' found in:")
            for file_path, count in occurrences:
                print(f"  - {file_path}: {count} time(s)")
    else:
        print("No matches found.")
