import os
import subprocess
import alive_progress as ap
import time

def find_files_with_user_comment(directory_path):
    files_with_user_comment = []

    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            user_comment = get_user_comment(file_path)
            if user_comment:
                files_with_user_comment.append(file_path)

    return files_with_user_comment

def get_user_comment(file_path):
    try:
        process = subprocess.Popen(['exiftool', '-UserComment', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, _ = process.communicate()
        if process.returncode == 0:
            return output.strip()
    except subprocess.CalledProcessError:
        pass

    return None

def set_screenshot_tag(file_path):
    try:
        subprocess.run(['xattr', '-w', 'com.apple.metadata:_kMDItemUserTags', '("Screenshot")', file_path], check=True)
        print(f"Проставлен тег 'Screenshot' для файла: {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Не удалось проставить тег 'Screenshot' для файла: {file_path}. Ошибка: {e}")

def main():
    directory_path = input("Введите путь к директории: ")

    if not os.path.isdir(directory_path):
        print("Указанная директория не существует.")
        return

    files_with_user_comment = find_files_with_user_comment(directory_path)

    if files_with_user_comment:
        with ap.alive_bar(len(files_with_user_comment), title='Проставление тегов') as bar:
            for file_path in files_with_user_comment:
                time.sleep(1)
                set_screenshot_tag(file_path)
                bar()

    else:
        print("В указанной директории нет файлов с метаданными 'User Comment'.")

if __name__ == "__main__":
    main()
