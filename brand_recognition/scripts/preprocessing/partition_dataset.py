import os
from glob import glob
import shutil
from sklearn.model_selection import train_test_split


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


def main():

    num_classes = 9
    path = os.getcwd() + "/workspace/data/"
    test_dir = os.getcwd() + "/workspace/training/images/test/"
    train_dir = os.getcwd() + "/workspace/training/images/train/"
    top_classes = os.listdir(path)

    for top_level_folder in top_classes[:num_classes]:
        for folder in os.listdir(os.path.join(path, top_level_folder)):
            # find image names
            image_files = glob(path + top_level_folder + "/" + folder + "/*.jpg")
            # remove extension
            image_names = [name.replace(".jpg", "") for name in image_files]
            # split into testing and training
            test_names, train_names = train_test_split(image_names, test_size=0.1)
            # move the files into testing and training directories
            batch_move_files(test_names, test_dir)
            batch_move_files(train_names, train_dir)


main()
