import os
from pathlib import Path
import shutil
import sys

# список расширений для каждой категории
# image_extensions = ('JPEG', 'PNG', 'JPG', 'SVG')
# video_extensions = ('AVI', 'MP4', 'MOV', 'MKV')
# document_extensions = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
# music_extensions = ('MP3', 'OGG', 'WAV', 'AMR')
# archive_extensions = ('ZIP', 'GZ', 'TAR')

# список всех расширений в папке
known_extensions = set()

# список неизвестных расширений
unknown_extensions = set()

def normalize(filename):
    """Приводит имя файла к нормализованному виду"""
    mapping = {
        ord('а'): 'a', ord('б'): 'b', ord('в'): 'v', ord('г'): 'g',
        ord('д'): 'd', ord('е'): 'e', ord('ё'): 'e', ord('ж'): 'zh',
        ord('з'): 'z', ord('и'): 'i', ord('й'): 'y', ord('к'): 'k',
        ord('л'): 'l', ord('м'): 'm', ord('н'): 'n', ord('о'): 'o',
        ord('п'): 'p', ord('р'): 'r', ord('с'): 's', ord('т'): 't',
        ord('у'): 'u', ord('ф'): 'f', ord('х'): 'h', ord('ц'): 'ts',
        ord('ч'): 'ch', ord('ш'): 'sh', ord('щ'): 'sch', ord('ъ'): '',
        ord('ы'): 'y', ord('ь'): '', ord('э'): 'e', ord('ю'): 'yu',
        ord('я'): 'ya', ord('А'): 'A', ord('Б'): 'B', ord('В'): 'V',
        ord('Г'): 'G', ord('Д'): 'D', ord('Е'): 'E', ord('Ё'): 'E',
        ord('Ж'): 'Zh', ord('З'): 'Z', ord('И'): 'I', ord('Й'): 'Y',
        ord('К'): 'K', ord('Л'): 'L', ord('М'): 'M', ord('Н'): 'N',
        ord('О'): 'O', ord('П'): 'P', ord('Р'): 'R', ord('С'): 'S',
        ord('Т'): 'T', ord('У'): 'U', ord('Ф'): 'F', ord('Х'): 'H',
        ord('Ц'): 'Ts', ord('Ч'): 'Ch', ord('Ш'): 'Sh', ord('Щ'): 'Sch',
        ord('Ъ'): '', ord('Ы'): 'Y', ord('Ь'): '', ord('Э'): 'E',
        ord('Ю'): 'Yu', ord('Я'): 'Ya',
    }
    return filename.translate(mapping)
    # О
# # Задаем путь к папке
# folder_path = r'D:\testfolder'

# # Получаем список файлов в папке
# files = os.listdir(folder_path)

# Анализируем файлы и создаем списки для каждого типа файлов
# image_files = []
# document_files = []
# other_files = []

categories = {'documents': ['.doc', '.xlsx', '.pdf'],
              'audios': ['.mp3', '.aiff', '.wav'],
              'videos': ['.mp4', '.mkv'],
              'archives': ['.zip', '.tar', '.rar'],
              'other': []}

# for file in files:
#     file_path = os.path.join(folder_path, file)
#     if file.endswith('.jpg') or file.endswith('.png'):
#         image_files.append(file_path)
#     elif file.endswith('.doc') or file.endswith('.pdf'):
#         document_files.append(file_path)
#     else:
#         other_files.append(file_path)

# Создаем папки для каждого типа файлов
# image_folder_path = os.path.join(folder_path, 'Images')
# document_folder_path = os.path.join(folder_path, 'Documents')
# other_folder_path = os.path.join(folder_path, 'Other')

# os.makedirs(image_folder_path, exist_ok=True)
# os.makedirs(document_folder_path, exist_ok=True)
# os.makedirs(other_folder_path, exist_ok=True)

# Перемещаем файлы в соответствующие папки
# for file in image_files:
#     shutil.move(file, image_folder_path)

# for file in document_files:
#     shutil.move(file, document_folder_path)

# for file in other_files:
#     shutil.move(file, other_folder_path)

def create_and_unpack_archive(folder_path:str, archive_name: str, extraction_path: str):
    shutil.make_archive('backup', 'zip', 'some_folder/inner')
    shutil.unpack_archive(archive_name, 'new_folder_for_data')

def get_category(item: Path):
    ext = item.suffix.lower()
    for category, extensions in categories.items():
        if ext in extensions:
            known_extensions.add(ext)
            return category
    unknown_extensions.add(ext)
    return 'other'


def move_file(item:Path, root_dir:Path):
    category = get_category(item)
    target_folder = root_dir / category

    if not target_folder.exists():
        target_folder.mkdir()

    item.replace(target_folder / f'{normalize(item.stem)}{item.suffix}')


def sort_dir(item:Path, root_dir: Path):
    for i in item.glob('*'):
        if i.is_dir():
            sort_dir(i, root_dir)
            i.rmdir()
        else:
            move_file(i, root_dir)


def sort_root(path:Path):
    for item in [item for item in path.glob('*') if item.name not in categories]:
        if item.is_dir():
            sort_dir(item, path)
            item.rmdir()
        else:
            move_file(item, path)


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "Send path to folder as parameter on call"

    if not path.exists():
        return f"Path {path} dos't exists. Check the path and try again."

    sort_root(path)

    return 'All Ok'


if __name__ == '__main__':
    print(main())