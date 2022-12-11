import os
import re
import shutil
import sys
from pathlib import Path

file_extension = {"images": ['.jpeg', '.png', '.jpg', '.svg'],
                  "documents": ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
                  "archives": ['.zip', '.gz', '.tar'],
                  "music": ['.mp3', '.ogg', '.wav', '.amr'],
                  "video": ['.avi', '.mp4', '.mov', '.mkv'],
                  "other": None
                  }


def normalize(name):
    """ The function changes the transliteration of files from Cyrillic to Latin
     and replaces characters with "_" """
    cyrillic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    translation = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
        "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    trans = {}

    for c, l in zip(cyrillic_symbols, translation):
        trans[ord(c)] = l
        trans[ord(c.upper())] = l.upper()
    trans_name = name.translate(trans)
    trans_name = re.sub(r'\W', '_', trans_name)

    return trans_name


def sorting_files(files):
    """" File sorting function according to their extensions"""
    chars = {
        "images": [],
        "documents": [],
        "archives": [],
        "music": [],
        "video": [],
        "other": [],
    }
    for file in files:
        suffix_name = file[file.rfind("."):]

        if suffix_name in file_extension["images"]:
            chars["images"].append(file)
        elif suffix_name in file_extension["documents"]:
            chars["documents"].append(file)
        elif suffix_name in file_extension["archives"]:
            chars["archives"].append(file)
        elif suffix_name in file_extension["music"]:
            chars["music"].append(file)
        elif suffix_name in file_extension["video"]:
            chars["video"].append(file)
        else:
            chars["other"].append(file)

    return chars


def delete_folders(path_dir):
    """ Function to delete empty folders """
    for d in os.listdir(path_dir):
        a = os.path.join(path_dir, d)
        if os.path.isdir(a):
            delete_folders(a)
            if not os.listdir(a):
                os.rmdir(a)


def main():
    """Main Function"""
    try:
        path_dir = sys.argv[1]
    except IndexError:
        return f"No folder, pass the path to sort folder"
    if path_dir:
        path_to_file = path_dir
        norm_names_list = []
        all_suffix_names = []
        count_files = 0
        for root, dirs, files in os.walk(path_dir):

            for file in files:
                suffix_name = file[file.rfind("."):]
                if suffix_name not in all_suffix_names:
                    all_suffix_names.append(suffix_name)

                os.replace(Path(root) / file, Path(path_to_file, file))
                norm_name = normalize(file[:file.rfind(".")]) + file[file.rfind("."):]
                os.replace(Path(path_to_file, file), Path(path_to_file, norm_name))

                if norm_name not in norm_names_list:
                    norm_names_list.append(norm_name)
                    count_files += 1

        dict_files = sorting_files(norm_names_list)
        list_new_folders = []

        for file_types, files in dict_files.items():
            list_new_folders.append(file_types)

            for file in files:
                if not Path(path_to_file, file_types).exists():
                    Path(path_to_file, file_types).mkdir()
                if not Path(path_to_file, file_types, file_types).exists():
                    Path(path_to_file, file_types, file_types).mkdir()
                if file_types == "archives":
                    shutil.unpack_archive(Path(path_to_file, file), Path(path_to_file, file_types, file_types, file))
                    os.replace(Path(path_to_file, file), Path(path_to_file, file_types, file))
                else:
                    os.replace(Path(path_to_file, file), Path(path_to_file, file_types, file))

        delete_folders(path_to_file)
    else:
        return f"Your folder Your folder does not exist"


    print("All folders: ", list_new_folders)
    print("All extension files: ", all_suffix_names)
    print("Names all files in folder: ", dict_files)
    print("Count files: ", count_files)

    print()
    print("Sorted!")


if __name__ == "__main__":
    main()
