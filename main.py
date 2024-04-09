import os

from lib.input.load import load_sequences, load_labels
from lib.model import LSTM, protCNN
from lib.output.save import save_history
from lib.output.plot import plot_history

'''
My solution of the assignment follows the procedure described in 'Protein Sequence Classification.
A case study on the Pfam dataset to classify protein families.' by Ronak Vijay available at
https://towardsdatascience.com/protein-sequence-classification-99c80d0ad2df.
'''

'''
The data files and label files in the correct format can be generated with the accompanying script "split_data.py".
'''
DATA_FOLDER = "population_damage"

TRAIN_PATH = DATA_FOLDER + "/train.fasta"
TEST_PATH = DATA_FOLDER + "/test.fasta"
VALIDATE_PATH = DATA_FOLDER + "/validate.fasta"

TRAIN_LABELS_PATH = DATA_FOLDER + "/train_labels.txt"
TEST_LABELS_PATH = DATA_FOLDER + "/test_labels.txt"
VALIDATE_LABELS_PATH = DATA_FOLDER + "/validate_labels.txt"

'''
Experiment settings.
The individual NNs are configured in "lib/model/LTSM.py" and "lib/model/protCNN.py".
'''
MODEL = LSTM # LSTM or protCNN
MAX_SEQUENCE_LENGTH = 100
TRAIN_EPOCHS = 33 # 33 for LSTM, 15 for ProtCNN
BATCH_SIZE = 256

SAVE_HISTORY = True
SHOW_PLOTS = False

RUN_NAME = DATA_FOLDER + "_" + \
    ("LSTM" if MODEL == LSTM else "protCNN") + \
    "_l" + str(MAX_SEQUENCE_LENGTH) + \
    "_e" + str(TRAIN_EPOCHS) +\
    "_b" + str(BATCH_SIZE)
HISTORY_PATH = "./results/" + RUN_NAME + "_trainHistoryDict"

if __name__ == '__main__':
    train = load_sequences(TRAIN_PATH, MAX_SEQUENCE_LENGTH,
                           categorical=MODEL == protCNN)
    train_labels = load_labels(TRAIN_LABELS_PATH)
    test = load_sequences(TEST_PATH, MAX_SEQUENCE_LENGTH,
                          categorical=MODEL == protCNN)
    test_labels = load_labels(TEST_LABELS_PATH)

    model = MODEL.init_model(MAX_SEQUENCE_LENGTH, train_labels.shape[1])
    model.summary()
    history = model.fit(x=train,
                        y=train_labels,
                        batch_size=BATCH_SIZE,
                        epochs=TRAIN_EPOCHS,
                        validation_data=(test, test_labels))

    if SAVE_HISTORY:
        if not os.path.exists("results"):
            os.makedirs("results")
        save_history(history, HISTORY_PATH)
    plot_history(history, show=SHOW_PLOTS, save_as="./results/" + RUN_NAME)
