import multiprocessing
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
def search_in_file_mp(file_path, keywords, queue):
    try:
        result = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for word in keywords:
                count = content.count(word)  # Підраховуємо кількість входжень слова
                if count > 0:
                    if word not in result:
                        result[word] = []
                    result[word].append((file_path, count))  # Додаємо кількість входжень у кожному файлі
        queue.put(result)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Функція для обробки файлів у процесах
def process_files_multiprocessing(file_paths, keywords):
    processes = []
    queue = multiprocessing.Queue()

    for file_path in file_paths:
        process = multiprocessing.Process(target=search_in_file_mp, args=(file_path, keywords, queue))
        processes.append(process)
        process.start()

    results = {}
    for process in processes:
        process.join()

    while not queue.empty():
        result = queue.get()
        for word, data in result.items():
            if word not in results:
                results[word] = []
            results[word].extend(data)

    return results

# Основна програма для багатопроцесорного підходу
def main_multiprocessing(file_paths, keywords):
    start_time = time.time()
    results = process_files_multiprocessing(file_paths, keywords)
    end_time = time.time()
    
    print(f"Multiprocessing execution time: {end_time - start_time:.2f} seconds")
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
    keywords = ["k", "e", "y"]  # Ключові слова (змінити під потрібні)
    multiprocessing_results = main_multiprocessing(file_paths, keywords)

    # Виведення результатів пошуку
    if multiprocessing_results:
        for word, occurrences in multiprocessing_results.items():
            print(f"\nWord '{word}' found in:")
            for file_path, count in occurrences:
                print(f"  - {file_path}: {count} time(s)")
    else:
        print("No matches found.")
