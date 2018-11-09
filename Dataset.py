import numpy as np


def find_candidates(items1, items2):
    result = []
    for i in range(len(items1)):
        if items1[i] in items2:
            result.append(i)
    return result


def one_hot(labels, label_num):
    result = []
    for i in range(len(labels)):
        one_hot_vec = [0] * label_num
        one_hot_vec[labels[i][0]] = 1
        result.append(one_hot_vec)
    return result


class Dataset:
    def __init__(self,
                 data_path='',
                 batch_size=5,
                 max_sequence_length=20,
                 windows=3,
                 eval_num=50):

        self.windows = windows
        self.batch_size = batch_size
        self.max_sequence_length = max_sequence_length
        self.eval_num = eval_num

        self.all_words = list()
        self.all_pos_taggings = list()
        self.all_marks = list()
        self.all_labels = list()
        self.instances = list()

        self.word_id = dict()
        self.pos_taggings_id = dict()
        self.mark_id = dict()

        self.read_dataset()
        self.eval_instances = self.instances[-eval_num:]
        self.train_instances = self.instances[0:-eval_num]
        self.batch_nums = len(self.train_instances) // self.batch_size
        self.index = np.arange(len(self.train_instances))
        self.point = 0

    def read_dataset(self):
        all_words, all_pos_taggings, all_labels, all_marks = [set() for _ in range(4)]

        def read_one_sentence(words, marks, labels):
            pos_taggings = []
            for word in words: all_words.add(word)
            for mark in marks: all_marks.add(mark)
            for label in labels: all_labels.add(label)

            self.instances.append({
                'words': words,
                'pos_taggings': pos_taggings,
                'marks': marks,
                'labels': labels,
            })

        read_one_sentence(
            words=['It', 'could', 'swell', 'to', 'as', 'much', 'as', '$500 billion', 'if', 'we', 'go', 'to', 'war', 'in', 'Iraq'],
            marks=['A',  'A',     'A',     'A',  'A',  'A',    'A',  'B',            'A',  'B',  'A',  'A',  'T',   'A',  'B'],
            labels=['',  '',      '',      '',   '',   '',     '',   '',           '', 'Attacker','',  '', 'Conflict/Attack', '', 'Place'],
        )

        all_words.add('<eos>')
        all_pos_taggings.add('*')

        self.word_id = dict(zip(all_words, range(len(all_words))))
        self.pos_taggings_id = dict(zip(all_pos_taggings, range(len(all_pos_taggings))))
        self.mark_id = dict(zip(all_marks, range(len(all_marks))))

        self.all_words = list(all_words)
        self.all_pos_taggings = list(all_pos_taggings)
        self.all_labels = list(all_labels)
        self.all_marks = list(all_marks)

    def shuffle(self):
        np.random.shuffle(self.index)
        self.point = 0

    def next_batch(self):
        start = self.point
        self.point = self.point + self.batch_size
        if self.point > len(self.train_instances):
            self.shuffle()
            start = 0
            self.point = self.point + self.batch_size
        end = self.point
        batch_instances = map(lambda x: self.train_instances[x], self.index[start:end])
        return batch_instances

    def next_train_data(self):
        batch_instances = self.next_batch()
        pos_tag, y, x, t, c, pos_c, pos_t = [list() for _ in range(7)]

        for instance in batch_instances:
            words = instance.words
            pos_taggings = instance.pos_taggings
            marks = instance.marks
            label = instance.label

            index_candidates = find_candidates(marks, ['B'])
            assert (len(index_candidates)) == 1
            index_triggers = find_candidates(marks, ['T'])
            assert (len(index_triggers)) == 1
            y.append(label)
            marks = marks + ['A'] * (self.max_sequence_length - len(marks))
            words = words + ['<eos>'] * (self.max_sequence_length - len(words))
            pos_taggings = pos_taggings + ['*'] * (self.max_sequence_length - len(pos_taggings))
            pos_taggings = map(lambda x: self.pos_taggings_id[x], pos_taggings)
            pos_tag.append(pos_taggings)
            index_words = map(lambda x: self.word_id[x], words)
            x.append(index_words)

            pos_candidate = range(-index_candidates[0], 0) + range(0, self.max_sequence_length - index_candidates[0])
            pos_c.append(pos_candidate)
            pos_trigger = range(-index_triggers[0], 0) + range(0, self.max_sequence_length - index_triggers[0])
            pos_t.append(pos_trigger)

            t.append([index_words[index_triggers[0]]] * self.max_sequence_length)
            c.append([index_words[index_candidates[0]]] * self.max_sequence_length)

            assert len(words) == len(marks) == len(pos_taggings) == len(index_words) == len(pos_candidate) == len(pos_trigger)

        assert len(y) == len(x) == len(t) == len(c) == len(pos_c) == len(pos_t) == len(
            pos_tag)

        return x, t, c, one_hot(y, len(self.all_labels)), pos_c, pos_t, pos_tag

    def eval_data(self):
        pass