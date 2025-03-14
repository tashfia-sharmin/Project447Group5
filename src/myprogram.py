#!/usr/bin/env python
import os
import string
import random
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import csv
from collections import defaultdict, Counter
import pickle
import json


class MyModel:
    """
    This is a starter model to get you started. Feel free to modify this file.
    """
    def __init__(self, n, alpha=1):
        self.n = n  # Size of n-grams
        self.alpha = alpha  # Laplace smoothing factor
        self.model = defaultdict(Counter)
        self.vocab = set()  # Track unique characters
        self.most_common_chars = None

    @classmethod
    def load_training_data(cls, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            data = []
            for row in reader:
                unicode_seq, frequency, language_id = row  # Ignore the Word column
                unicode_seq = eval(unicode_seq)
                frequency = int(frequency)
                language_id = int(language_id)
                data.append((unicode_seq, frequency, language_id))
            return data

    @classmethod
    def load_test_data(cls, file_path):
        # going out one file for predict.sh
        if not os.path.exists(file_path):
            work_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'example'))
            file_path = os.path.join(work_dir, 'input.txt')

        with open(file_path, "r", encoding="utf-8") as file:
            data = []
            for line in file:
                unicode_seq = tuple(ord(c) for c in line.strip())  # Convert characters to Unicode
                data.append(unicode_seq)
            return data

    @classmethod
    def write_pred(cls, preds, fname):
        with open(fname, 'wt') as f:
            for p in preds:
                # print(p)
                f.write('{}\n'.format(p))

    def run_train(self, data, batch_size):
        # Build raw frequency counts
        # for unicode_seq, frequency, _ in data:
        #     for i in range(len(unicode_seq) - self.n + 1):
        #         prefix = tuple(unicode_seq[i:i + self.n - 1])
        #         next_char = unicode_seq[i + self.n - 1]
        #         self.model[prefix][next_char] += frequency
        #         self.vocab.add(next_char)

        # vocab_size = len(self.vocab)

        # # Convert counts to probabilities with Laplace smoothing
        # for prefix, counts in self.model.items():
        #     total = sum(counts.values()) + self.alpha * vocab_size
        #     for char in self.vocab:
        #         counts[char] = (counts.get(char, 0) + self.alpha) / total

        temp_model = defaultdict(Counter)  # temp model + vocab for batching
        temp_vocab = set()

        for batch_start in range(0, len(data), batch_size):
            batch = data[batch_start:batch_start + batch_size]

            for unicode_seq, frequency, _ in batch:
                for i in range(len(unicode_seq) - self.n + 1):
                    prefix = tuple(unicode_seq[i:i + self.n - 1])
                    next_char = unicode_seq[i + self.n - 1]
                    temp_model[prefix][next_char] += frequency
                    temp_vocab.add(next_char)

            for prefix, counts in temp_model.items():
                for char, count in counts.items():
                    self.model[prefix][char] += count

            self.vocab.update(temp_vocab)
            temp_model.clear()
            temp_vocab.clear()

        vocab_size = len(self.vocab)

        for prefix, counts in self.model.items():
            total = sum(counts.values()) + self.alpha * vocab_size
            for char in self.vocab:
                counts[char] = (counts.get(char, 0) + self.alpha) / total

    def compute_most_common_chars(self):
        most_common_chars = Counter()
        for counts in self.model.values():
            most_common_chars.update(counts)
        return most_common_chars.most_common(3)

    def run_pred(self, sequence_unicode, top_k=3):
        sequence_unicode = tuple(sequence_unicode[-(self.n - 1):])  # Ensure correct prefix length

        # Backoff approach: Try shorter prefixes if necessary
        while sequence_unicode:
            if sequence_unicode in self.model:
                predictions = sorted(
                    self.model[sequence_unicode].items(), key=lambda x: x[1], reverse=True
                )
                return [char for char, _ in predictions[:top_k]]
            sequence_unicode = sequence_unicode[1:]  # Shorten prefix (backoff)

        # # If no match found, return cached most common characters
        return [char for char, _ in self.most_common_chars]


    def save(self, work_dir):
        with open(os.path.join(work_dir, 'model.pkl'), 'wb') as f:
            pickle.dump((self.n, self.alpha, self.model, self.vocab), f)

    @classmethod
    def load(cls, work_dir):
        work_dir = os.path.abspath('work')
        file_path = os.path.join(work_dir, 'model.pkl')

        # going out one file for predict.sh
        if not os.path.exists(file_path):
            work_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'work'))
            file_path = os.path.join(work_dir, 'model.pkl')

        with open(file_path, 'rb') as f:
            n, alpha, model, vocab = pickle.load(f)
        loaded_model = cls(n, alpha)
        loaded_model.model = model
        loaded_model.vocab = vocab
        loaded_model.most_common_chars = loaded_model.compute_most_common_chars()
        return loaded_model

# Quick method to return the character from Unicode
def unicode_to_char(unicode):
    return chr(unicode)

# Quick method to return the Unicode from character
def convert_to_uni(word):
    return tuple(ord(char) for char in word)

# Small TEST
# model = MyModel(n=4)
# data = model.load_training_data("train_split_en.csv")  # Load data
# model.run_train(data, batch_size=20)

# # using example input.txt
# test_data = model.load_test_data("example/input.txt")

# predictions = []
# for sequence in test_data:
#     pred = model.run_pred(sequence)  # Predict for the current sequence
#     predictions.append(''.join([chr(c) for c in pred]))  # Convert Unicode to characters

# # Write predictions to a file
# model.write_pred(predictions, 'pred.txt')

# OLD
# Predict next Unicode characters for the sequence "hel"
# predictions = model.run_pred((104, 101, 108))
# predictions = [unicode_to_char(p) for p in predictions]
# print(predictions)
# model.write_pred(predictions, 'output.txt')

# Will work once we update to handle larger dataset -> think we need to update run_pred
# i think we need to make sure this works tho
if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('mode', choices=('train', 'test'), help='what to run')
    parser.add_argument('--work_dir', help='where to save', default='work')
    parser.add_argument('--test_data', help='path to test data', default='example/input.txt')
    parser.add_argument('--test_output', help='path to write test predictions', default='pred.txt')
    args = parser.parse_args()

    random.seed(0)

    if args.mode == 'train':
        if not os.path.isdir(args.work_dir):
            print('Making working directory {}'.format(args.work_dir))
            os.makedirs(args.work_dir)

        print('Instatiating model')
        model = MyModel(n=4)

        print('Loading training data')
        train_data = MyModel.load_training_data('data/train_split.csv')

        print('Training')
        model.run_train(train_data, batch_size=64)

        print('Saving model')
        model.save(args.work_dir)

    elif args.mode == 'test':
        print('Loading model')
        model = MyModel.load('work')

        print('Loading test data from {}'.format(args.test_data))
        test_data = MyModel.load_test_data(args.test_data)

        print('Making predictions')
        predictions = []
        for sequence in test_data:
            pred = model.run_pred(sequence)  # Predict for the current sequence
            predictions.append(''.join([chr(c) for c in pred]))
        # pred = model.run_pred(test_data)

        print('Writing predictions to {}'.format(args.test_output))
        # assert len(pred) == len(test_data), 'Expected {} predictions but got {}'.format(len(test_data), len(pred))
        model.write_pred(predictions, args.test_output)
    else:
        raise NotImplementedError('Unknown mode {}'.format(args.mode))
