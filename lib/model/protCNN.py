from keras import layers, regularizers, Model
from lib.input.amino_dict import CODES


def residual_block(data, filters, d_rate):
    """
    _data: input
    _filters: convolution filters
    _d_rate: dilation rate
    """

    shortcut = data

    bn1 = layers.BatchNormalization()(data)
    act1 = layers.Activation('relu')(bn1)
    conv1 = layers.Conv1D(filters, 1,
                          dilation_rate=d_rate,
                          padding='same',
                          kernel_regularizer=regularizers.l2(0.001))(act1)

    # bottleneck convolution
    bn2 = layers.BatchNormalization()(conv1)
    act2 = layers.Activation('relu')(bn2)
    conv2 = layers.Conv1D(filters, 3,
                          padding='same',
                          kernel_regularizer=regularizers.l2(0.001))(act2)

    # skip connection
    x = layers.Add()([conv2, shortcut])

    return x


def init_model(max_sequence_length, n_classes):
    x_input = layers.Input(shape=(max_sequence_length, len(CODES)+1))

    # initial conv
    conv = layers.Conv1D(128, 1, padding='same')(x_input)

    # per-residue representation
    res1 = residual_block(conv, 128, 2)
    res2 = residual_block(res1, 128, 3)

    x = layers.MaxPooling1D(3)(res2)
    x = layers.Dropout(0.5)(x)

    # softmax classifier
    x = layers.Flatten()(x)
    x_output = layers.Dense(n_classes,
                            activation='softmax',
                            kernel_regularizer=regularizers.l2(0.0001))(x)

    model_protCNN = Model(inputs=x_input, outputs=x_output)
    model_protCNN.compile(optimizer='adam',
                        loss='categorical_crossentropy',
                        metrics=['accuracy'])

    model_protCNN.summary()
    return model_protCNN
