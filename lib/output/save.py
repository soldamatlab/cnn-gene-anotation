import pickle


def save_history(history, path):
    with open(path, 'wb') as file_pi:
        pickle.dump(history.history, file_pi)


def load_history(path):
    with open(path, "rb") as file_pi:
        history = pickle.load(file_pi)
    return history
