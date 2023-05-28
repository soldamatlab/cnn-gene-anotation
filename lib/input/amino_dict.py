# https://dmnfarrell.github.io/bioinformatics/mhclearning
# http://www.cryst.bbk.ac.uk/education/AminoAcid/the_twenty.html
# 1 letter code for 20 natural amino acids
import numpy as np

CODES = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
         'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']


def create_dict():
    char_dict = {}
    for index, val in enumerate(CODES):
        char_dict[val] = index+1
    return char_dict


def integer_encode(data, char_dict):
    """
    - Encodes code sequence to integer values.
    - 20 common amino acids are taken into consideration
      and rest 4 are categorized as 0.
    """
    encoded_data = []
    for sequence in data:
        encoded_sequence = []
        for code in sequence:
            encoded_sequence.append(char_dict.get(code, 0))
        encoded_data.append(np.array(encoded_sequence))
    return encoded_data
