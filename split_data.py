from Bio import SeqIO
import numpy as np

'''
List two or more fasta files with protein sequences.
Each fasta file will be treated as a different protein family (i.e. a different class for the CNN to recognize).
'''
SEQUENCES_PATHS = ["CAFA3_training_data/phosphorylation.fasta",
                   "CAFA3_training_data/regulation.fasta"]

'''
The training sequences will be saved in "[SAVE_TO]/[TRAIN_FILENAME].fasta".
The labels of the training sequences will be saved in "[SAVE_TO]/[TRAIN_FILENAME]_labels.txt".
The test and validate sequences will be saved analogically.
'''
SAVE_TO = "data"
TRAIN_FILENAME = "train"
TEST_FILENAME = "test"
VALIDATE_FILENAME = "validate"

TRAIN_SPLIT = 0.8
TEST_SPLIT = 0.1
# validate split = 1 - TRAIN_SPLIT - TEST_SPLIT

RANDOM_SEED = 0


def save_labels(labels, save_to):
    with open(save_to, "w") as file:
        for label in labels:
            file.write("%d " % label)
        file.write("\n")


if __name__ == '__main__':
    assert(TRAIN_SPLIT > 0)
    assert(TEST_SPLIT > 0)
    assert(TRAIN_SPLIT + TEST_SPLIT <= 1)

    # load fasta files
    sequences = []
    for term in range(len(SEQUENCES_PATHS)):
        sequences.append([])
        for p in SeqIO.parse(SEQUENCES_PATHS[term], "fasta"):
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
            indexes, [int(TRAIN_SPLIT*len(indexes)), int((1-TEST_SPLIT)*len(indexes))])

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

    SeqIO.write(train, SAVE_TO + "/" + TRAIN_FILENAME + ".fasta", "fasta")
    SeqIO.write(test, SAVE_TO + "/" + TEST_FILENAME + ".fasta", "fasta")
    SeqIO.write(validate,
                SAVE_TO + "/" + VALIDATE_FILENAME + ".fasta", "fasta")
    save_labels(train_labels, SAVE_TO + "/" + TRAIN_FILENAME + "_labels.txt")
    save_labels(test_labels, SAVE_TO + "/" + TEST_FILENAME + "_labels.txt")
    save_labels(validate_labels,
                SAVE_TO + "/" + VALIDATE_FILENAME + "_labels.txt")
