import numpy as np
from Bio import SeqIO

from lib.input.preprocess import preprocess


def load_sequences(path, max_sequence_length, categorical=False):
    sequences = []
    for s in SeqIO.parse(path, "fasta"):
        sequences.append(s)
    sequences = preprocess(sequences, max_sequence_length, categorical=categorical)
    return sequences


def load_labels(path):
    with open(path, "r") as file:
        labels_raw = [int(label) for label in file.read().split()]
    #return labels_raw
    unique = set(labels_raw)
    labels = np.zeros((len(labels_raw), len(unique)))
    for i in range(len(labels_raw)):
        labels[i][labels_raw[i]] = 1
    return labels
