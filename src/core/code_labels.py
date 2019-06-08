
class Code_labels:
    def __init__(self):
        self._labels_counter = {}
       
    def get_label_name(self, label_name):
        if label_name not in self._labels_counter:
            self._labels_counter[label_name] = 0
            return "{}_{:02d}".format(label_name, self._labels_counter[label_name])

        self._labels_counter[label_name] += 1
        return "{}_{:02d}".format(label_name, self._labels_counter[label_name])