import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--data_dir')
args = parser.parse_args()


def main(data_dir):

    num_classes = 9
    top_classes = os.listdir(data_dir)

    for top_level_folder in top_classes[:num_classes]:
        for folder in os.listdir(os.path.join(data_dir, top_level_folder)):
            src_path = os.path.join(data_dir, top_level_folder) + "/" + folder
            brand_lower = folder.lower()

            for file in os.listdir(src_path):
                name, ext = os.path.splitext(file)
                new_name = f'{name}_{brand_lower}'
                # os.rename(src_path + "/" + file, src_path + "/" + new_name.split('_')[0] + ext)
                os.rename(src_path + "/" + file, src_path + "/" + new_name + ext)
                print(f'Created at: {src_path + "/" + file, src_path + "/" + new_name + ext}')


main(args.data_dir)
