import os


def convert_classes(classes, start=1):
    msg = ''
    for id, name in enumerate(classes, start=start):
        msg = msg + 'item {\n'
        msg = msg + ' name: "' + name + '"\n'
        msg = msg + ' id: ' + str(id) + '\n}\n\n'
    return msg[:-1]


def main():
    path = os.getcwd() + "/workspace/data/"
    top_classes = os.listdir(path)
    classes = [os.listdir(path + x + "/") for x in top_classes]

    final = []
    for x in classes:
        final += x
    final = [x.lower() for x in final]

    label_map = convert_classes(final)

    with open(path + "label_map.pbtxt", "w") as f:
        f.write(label_map)
        f.close()


main()
