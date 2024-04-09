from matplotlib import pyplot as plt


'''
Code by Rahul Verma at https://stackoverflow.com/questions/41908379/keras-plot-training-validation-and-test-set-accuracy.
'''
def plot_history(history, show=True, save_as=None):
    plt.figure()
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    if save_as is not None:
        plt.savefig(save_as + "_accuracy.png")
    if show:
        plt.show()

    plt.figure()
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    if save_as is not None:
        plt.savefig(save_as + "_loss.png")
    if show:
        plt.show()
