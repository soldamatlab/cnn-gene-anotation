import os
from Bio import SeqIO
import numpy as np

'''
Settings for direct runs of split_data.py (as main).
These settings have no effect on calls of split_data() as a function (apart from RANDOM_SEED).

List two or more fasta files with protein sequences.
Each fasta file will be treated as a different protein family (i.e. a different class for the CNN to recognize).

The training sequences will be saved in "[SAVE_TO]/[TRAIN_FILENAME].fasta".
The labels of the training sequences will be saved in "[SAVE_TO]/[TRAIN_FILENAME]_labels.txt".
The test and validate sequences will be saved analogically.
'''
SEQUENCES_PATHS = ["CAFA3_training_data/apoptosis.fasta",
                   "CAFA3_training_data/damage.fasta"]

SAVE_TO = "apoptosis_damage"
TRAIN_FILENAME = "train"
TEST_FILENAME = "test"
VALIDATE_FILENAME = "validate"

TRAIN_SPLIT = 0.9
TEST_SPLIT = 0.1
# validate split = 1 - TRAIN_SPLIT - TEST_SPLIT

RANDOM_SEED = 0


def save_labels(labels, save_to):
    with open(save_to, "w") as file:
        for label in labels:
            file.write("%d " % label)
        file.write("\n")


def split_data(sequences_paths, train_split, test_split, save_to, train_filename, test_filename, validate_filename):
    assert(train_split > 0)
    assert(test_split > 0)
    assert(train_split + test_split <= 1)

    # load fasta files
    sequences = []
    for term in range(len(sequences_paths)):
        sequences.append([])
        for p in SeqIO.parse(sequences_paths[term], "fasta"):
            sequences[term].append(p)

    train = []
    test = []
    validate = []
    train_labels = []
    test_labels = []
    validate_labels = []
    for term in range(len(sequences)):
        # split indexes
        indexes = np.array([i for i in range(len(sequences[term]))])
        np.random.seed(0)
        np.random.shuffle(indexes)
        train_indexes, validate_indexes, test_indexes = np.split(
            indexes, [int(train_split*len(indexes)), int((1-test_split)*len(indexes))])

        # append sets
        for index in train_indexes:
            train.append(sequences[term][index])
            train_labels.append(term)
        for index in test_indexes:
            test.append(sequences[term][index])
            test_labels.append(term)
        for index in validate_indexes:
            validate.append(sequences[term][index])
            validate_labels.append(term)

    print("|train|    = %d" % len(train))
    print("|test|     = %d" % len(test))
    print("|validate| = %d" % len(validate))

    if not os.path.exists(SAVE_TO):
        os.makedirs(SAVE_TO)
    SeqIO.write(train, save_to + "/" + train_filename + ".fasta", "fasta")
    SeqIO.write(test, save_to + "/" + test_filename + ".fasta", "fasta")
    SeqIO.write(validate,
                save_to + "/" + validate_filename + ".fasta", "fasta")
    save_labels(train_labels, save_to + "/" + train_filename + "_labels.txt")
    save_labels(test_labels, save_to + "/" + test_filename + "_labels.txt")
    save_labels(validate_labels,
                save_to + "/" + validate_filename + "_labels.txt")


if __name__ == '__main__':
    split_data(SEQUENCES_PATHS, TRAIN_SPLIT, TEST_SPLIT, SAVE_TO, TRAIN_FILENAME, TEST_FILENAME, VALIDATE_FILENAME)
