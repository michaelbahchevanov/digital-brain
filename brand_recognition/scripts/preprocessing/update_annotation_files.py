from xml.etree import ElementTree as et
import os
from glob import glob


def main():

    num_classes = 9
    path = os.getcwd() + "/workspace/data/"
    top_classes = os.listdir(path)

    for top_level_folder in top_classes[:num_classes]:
        for folder in os.listdir(os.path.join(path, top_level_folder)):
            src_path = os.path.join(path, top_level_folder) + "/" + folder
            xml_files = glob(path + top_level_folder + "/" + folder + "/*.xml")
            brand_lower = folder.lower()

            for file in xml_files:
                tree = et.parse(file)
                entry = tree.find('.//filename').text
                head, tail = entry.split(".")
                hist = tree.find('.//filename').text = f"{head}_{brand_lower}.{tail}"
                tree.write(file)
                print(hist)


main()
