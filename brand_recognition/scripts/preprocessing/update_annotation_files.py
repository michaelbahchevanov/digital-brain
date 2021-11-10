from xml.etree import ElementTree as et
import os
from glob import glob
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--data_dir')
args = parser.parse_args()


def main(data_dir):

    num_classes = 9
    top_classes = os.listdir(data_dir)

    for top_level_folder in top_classes[:num_classes]:
        for folder in os.listdir(os.path.join(data_dir, top_level_folder)):
            xml_files = glob(data_dir + '/' + top_level_folder + "/" + folder + "/*.xml")
            # brand_lower = folder.lower()

            for file in xml_files:
                tree = et.parse(file)
                # entry = tree.find('.//filename').text
                try:
                    head, tail = os.path.basename(file).split(".")
                except:
                    continue
                # print(head)
                # hist = tree.find('.//filename').text = f""
                hist = tree.find('.//filename').text = f"{head}.jpg"
                tree.write(file)
                print(hist)


main(args.data_dir)
