from keras.utils import pad_sequences, to_categorical

from lib.input.amino_dict import *


def preprocess(data, max_sequence_length, categorical=False):
    char_dict = create_dict()
    data_prepro = integer_encode(data, char_dict)
    data_prepro = pad_sequences(data_prepro, maxlen=max_sequence_length, padding='post', truncating='post')
    if categorical:
        data_prepro = to_categorical(data_prepro)
    return data_prepro
