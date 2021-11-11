import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--data_dir')
parser.add_argument('--out_path')
args = parser.parse_args()


def convert_classes(classes, start=1):
    msg = ''
    for id, name in enumerate(classes, start=start):
        msg = msg + 'item {\n'
        msg = msg + ' name: "' + name + '"\n'
        msg = msg + ' id: ' + str(id) + '\n}\n\n'
    return msg[:-1]


def main(data_dir, out_path):
    top_classes = os.listdir(data_dir)
    classes = [os.listdir(data_dir + '/' + x + "/") for x in top_classes]

    final = []
    for x in classes:
        final += x
    final = [x.lower() for x in final]

    label_map = convert_classes(final)

    with open(out_path + '/' + "label_map.pbtxt", "w") as f:
        f.write(label_map)
        f.close()


main(args.data_dir, args.out_path)
