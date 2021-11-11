import os
from glob import glob
import shutil
from sklearn.model_selection import train_test_split
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--data_dir')
parser.add_argument('--out_path')
args = parser.parse_args()


def batch_move_files(file_list, dest_path):
    for file in file_list:
        image = file + ".jpg"
        head_image, tail_image = os.path.split(image)
        xml = file + ".xml"
        head_xml, tail_xml = os.path.split(xml)

        print(os.path.join(dest_path, tail_image))
        print(os.path.join(dest_path, tail_xml))

        shutil.copy(image,
                    os.path.join(dest_path, tail_image))
        shutil.copy(xml,
                    os.path.join(dest_path, tail_xml))
    return


def main(data_dir, out_path):

    num_classes = 9
    test_dir = os.path.join(out_path, 'validation')
    train_dir = os.path.join(out_path, 'train')
    top_classes = os.listdir(data_dir)

    for top_level_folder in top_classes[:num_classes]:
        for folder in os.listdir(os.path.join(data_dir, top_level_folder)):
            # find image names
            image_files = glob(data_dir + '/' + top_level_folder + "/" + folder + "/*.jpg")
            # remove extension
            image_names = [name.replace(".jpg", "") for name in image_files]
            # split into testing and training
            train_names, test_names = train_test_split(image_names, test_size=0.1)
            # move the files into testing and training directories
            batch_move_files(test_names, test_dir)
            batch_move_files(train_names, train_dir)


main(args.data_dir, args.out_path)
