import itertools

import numpy as np


class LabelCodec:
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ0123456789- "

    # Translation of characters to unique numerical classes
    @staticmethod
    def encode_number(number):
        return list(map(lambda c: LabelCodec.ALPHABET.index(c), number))

    # Reverse translation of numerical classes back to characters
    @staticmethod
    def decode_number(labels):
        ret = []
        for c in labels:
            if c == len(LabelCodec.ALPHABET):  # CTC Blank
                ret.append("")
            else:
                ret.append(LabelCodec.ALPHABET[c])
        return "".join(ret)

    @staticmethod
    def get_alphabet_len():
        return len(LabelCodec.ALPHABET)

    @staticmethod
    def decode_number_from_output(out):
        for j in range(out.shape[0]):
            out_best = list(np.argmax(out[j, 2:], 1))
            out_best = [k for k, g in itertools.groupby(out_best)]
            outstr = ''
            for c in out_best:
                if c < len(LabelCodec.ALPHABET):
                    outstr += LabelCodec.ALPHABET[c]
            return outstr
