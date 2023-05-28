from lib.input.load import load_sequences, load_labels
from lib.model import LSTM, protCNN

'''
My solution of the assignment follows the procedure described in 'Protein Sequence Classification
A case study on the Pfam dataset to classify protein families.' by Ronak Vijay available at
https://towardsdatascience.com/protein-sequence-classification-99c80d0ad2df.
'''

'''
The data files and label files in the correct format can be generated with the accompanying script "split_data.py".
'''
TRAIN_PATH = "data/train.fasta"
TEST_PATH = "data/test.fasta"
VALIDATE_PATH = "data/validate.fasta"

TRAIN_LABELS_PATH = "data/train_labels.txt"
TEST_LABELS_PATH = "data/test_labels.txt"
VALIDATE_LABELS_PATH = "data/validate_labels.txt"

'''
Experiment settings.
The individual NNs are configured in "lib/model/LTSM.py" and "lib/model/protCNN.py".
'''
MODEL = LSTM  # LTSM or protCNN
MAX_SEQUENCE_LENGTH = 100
TRAIN_EPOCHS = 33  # 33 for LSTM, 10 for protCNN
BATCH_SIZE = 256


if __name__ == '__main__':
    train = load_sequences(TRAIN_PATH, MAX_SEQUENCE_LENGTH,
                           categorical=MODEL == protCNN)
    train_labels = load_labels(TRAIN_LABELS_PATH)
    test = load_sequences(TEST_PATH, MAX_SEQUENCE_LENGTH,
                          categorical=MODEL == protCNN)
    test_labels = load_labels(TEST_LABELS_PATH)

    model = MODEL.init_model(MAX_SEQUENCE_LENGTH, train_labels.shape[1])
    model.summary()
    model.fit(x=train,
              y=train_labels,
              batch_size=BATCH_SIZE,
              epochs=TRAIN_EPOCHS,
              validation_data=(test, test_labels))
