import os


def main():

    num_classes = 9
    path = os.getcwd() + "/workspace/data/"
    top_classes = os.listdir(path)

    for top_level_folder in top_classes[:num_classes]:
        for folder in os.listdir(os.path.join(path, top_level_folder)):
            src_path = os.path.join(path, top_level_folder) + "/" + folder
            brand_lower = folder.lower()

            for file in os.listdir(src_path):
                name, ext = os.path.splitext(file)
                new_name = f'{name}_{brand_lower}'
                os.rename(src_path + "/" + file, src_path + "/" + new_name + ext)


main()
