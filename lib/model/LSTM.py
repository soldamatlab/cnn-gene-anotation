from keras import layers, regularizers, Model
from lib.input.amino_dict import CODES


def init_model(max_sequence_length, n_classes):
    x_input = layers.Input(shape=(max_sequence_length,))
    emb = layers.Embedding(len(CODES)+1, 128, input_length=max_sequence_length)(x_input)
    # CuDNNLSTM can replace LSTM (CuDNNLSTM is trained using GPU)
    bi_rnn = layers.Bidirectional(layers.LSTM(
        64,
        kernel_regularizer=regularizers.l2(0.01),
        recurrent_regularizer=regularizers.l2(0.01),
        bias_regularizer=regularizers.l2(0.01)
    ))(emb)
    x = layers.Dropout(0.3)(bi_rnn)

    # softmax classifier
    x_output = layers.Dense(n_classes, activation='softmax')(x)

    model_LSTM = Model(inputs=x_input, outputs=x_output)
    model_LSTM.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model_LSTM