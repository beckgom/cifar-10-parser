# -*- coding: utf-8 -*-

# Objective: get the image file from the pickled CIFAR-10 for making the DB in DIGITS
# get pickled CIFAR-10 first at http://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
# then extract tar file
# Run this script

import os
import Image

def unpickle(file):
    import cPickle
    fo = open(file, 'rb')
    dict = cPickle.load(fo)
    fo.close()
    return dict


def convert_image_from_pack(filename, path, meta, logfile):
    raw_data = unpickle(filename)

    def get_image_format(data):
        return [(data[i], data[i + 1024], data[i + 2048]) for i in xrange(1024)]

    def saveImage(img, mode, size, filename):
        new_img = Image.new(mode, size)
        new_img.putdata(img)
        new_img.save(filename)

    for i in xrange(len(raw_data['data'])):
        image_format = get_image_format(raw_data['data'][i])
        label = raw_data['labels'][i]
        filepath = path + "/" + str(label) + "/" + raw_data['filenames'][i]
        saveImage(image_format, "RGB", (32, 32), filepath)
        logfile.write(filepath + "\t" + str(label) + "\n")


def save_label_file(filename):
    meta = unpickle(filename)
    list_label = meta['label_names']
    with open("labels.txt", 'w') as f:
        for label in list_label:
            f.write(label + '\n')
        f.close()
    return meta

def make_dir(meta, db_type):
    os.system("mkdir " + db_type)
    os.chdir(db_type)
    for i in xrange(len(meta['label_names'])):
        command = "mkdir " + str(i)
        os.system(command)
    os.chdir("..")


def convert_DB(meta, db_type):
    train_file_list = ['data_batch_1', 'data_batch_2', 'data_batch_3', 'data_batch_4', 'data_batch_5']
    test_file_list = ['test_batch']
    file_list = {"train": train_file_list, "test":test_file_list}
    db_log = db_type + ".txt"
    f = open(db_log, "w")
    for filename in file_list[db_type]:
        convert_image_from_pack(filename, db_type, meta, f)
    f.close()
    print "Done for " + db_type

def main():
    meta = save_label_file("batches.meta")

    make_dir(meta, "train")
    make_dir(meta, "test")

    convert_DB(meta, "train")
    convert_DB(meta, "test")


if __name__ == '__main__':
    main()
