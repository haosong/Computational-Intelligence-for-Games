import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras import optimizers
import sys
from yahtzee import YahtzeeScoresheet, YahtzeeRoll

category = ["1", "2", "3", "4", "5", "6", "3K", "4K", "FH", "SS", "LS", "C", "Y", "Y+"]  # Y/Y+, UP

label_dict = {
    "1": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "2": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "3": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    "4": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    "5": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    "6": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    "NK": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    "3K": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    "4K": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    "Y": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    "Y+": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    "FH": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    "S": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    "SS": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    "LS": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    "C": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    "RE": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
}


def process(line, has_label):
    line = line.strip()
    # print(line)
    line_split = line.split(',')
    # print(line_split)
    cur_fill = line_split[0].split(' ')
    roll = YahtzeeRoll.parse(line_split[1])
    reroll = int(line_split[2])
    vector = []

    index = 0
    sheet = YahtzeeScoresheet()
    for i in range(len(category)):
        if cur_fill[index] == category[i]:
            vector.append(1)
            if category[i] == "Y+":
                sheet.scores[12] = 1
            else:
                sheet.scores[i] = 1
            index += 1
        else:
            vector.append(0)
    # print(sheet.scores)

    up_score = int(cur_fill[index][2:])
    if up_score > 63:
        up_score = 1
    else:
        up_score /= 63
    vector.append(up_score)

    roll_list = roll.as_list()
    vector.extend([(x - 1) / 5 for x in roll_list])
    vector.append(reroll / 2)

    if has_label:
        label = ""
        result = line_split[3]
        if not result.startswith("["):
            # print("1-label = " + result)
            label = label_dict[result]
        else:
            not_found = True
            result = result[1:-1]
            result_roll = YahtzeeRoll.parse(result)
            if result == "":
                label = "RE"
                not_found = False
            for i in range(1, 7):
                select = ''.join(str(n) for n in roll.select_all([i]).as_list())
                if select != '' and select == result and vector[i - 1] == 0:
                    label = str(i)
                    not_found = False
                    break
            if not_found:
                select = ''.join(str(n) for n in roll.select_for_full_house().as_list())
                if select != '' and select == result and vector[8] == 0:
                    label = "FH"
                    not_found = False
            if not_found:
                is_3k = False
                for i in range(1, 7):
                    if result_roll.count(i) >= 3:
                        is_3k = True
                select = ''.join(str(n) for n in roll.select_for_n_kind(sheet, reroll).as_list())
                if (select != '' and select == result) or len(set(result)) == 1 or is_3k:
                    label = "NK"
                    not_found = False
            if not_found:
                select = ''.join(str(n) for n in roll.select_for_straight(sheet).as_list())
                if (select != '' and select == result or len(set(result)) == 4) and (vector[9] == 0 or vector[10] == 0):
                    label = "S"
                    not_found = False
            if not_found:
                select = ''.join(str(n) for n in roll.select_for_chance(reroll).as_list())
                if select != '' and select == result and vector[11] == 0:
                    label = "C"
                    not_found = False
            if not_found and sum(vector[:13]) == 12:
                not_found = False
                for i in range(0, 13):
                    if vector[i] == 0:
                        label = category[i]
            if not_found:
                is_single = True
                # if len(set(result)) == len(result):
                for i in range(1, 7):
                    if result_roll.count(i) > 1:
                        is_single = False
                        break
                if is_single and (vector[9] == 0 or vector[10] == 0):
                    label = "S"
                    not_found = False
            if not_found:
                not_found = False
                if vector[6] == 1 and vector[7] == 1 and vector[8] == 1 and vector[11] == 0:
                    label = "C"
                elif vector[6] == 1 and vector[7] == 1 and vector[8] == 0:
                    label = "FH"
                elif vector[6] == 0 or vector[7] == 0:
                    label = "NK"
                elif len(result) == 2 and len(set(result)) == 2 and vector[int(result[0]) - 1] == 0 \
                        and vector[int(result[1]) - 1] == 0:
                    label = result[1]
                else:
                    not_found = True
            if not_found:
                print("not_found")
                pass
            else:
                # print("2-label = " + label)
                label = label_dict[label]
        one_vector = vector + label
        # print(one_vector)
        print(*one_vector, sep=',')
        # return one_vector
    else:
        # return [vector]
        pass


def train():
    x_all = []
    y_all = []
    # read from stdin
    for line in sys.stdin:
        data = list(map(float, line.split(',')))
        x_all.append(data[0:21])
        y_all.append(data[21:])

    test_size = int(len(x_all) / 5)
    train_size = len(x_all) - test_size

    x_train = np.matrix(x_all[:train_size])
    y_train = np.matrix(y_all[:train_size])

    x_test = np.matrix(x_all[train_size:])
    y_test = y_all[train_size:]

    # define a full-connected network structure with 3 layers
    model = Sequential()
    model.add(Dense(300, activation='relu', input_dim=x_train.shape[1]))
    model.add(Dropout(0.1))
    model.add(Dense(y_train.shape[1], activation='softmax'))

    # compile the model
    sgd = optimizers.SGD(lr=0.1, decay=1e-6, momentum=0.8, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    # fit the model
    model.fit(x_train, y_train, epochs=100, batch_size=5)

    y_predict = [max(enumerate(y), key=lambda x: x[1])[0] for y in model.predict(x_test)]
    y_correct = [max(enumerate(y), key=lambda x: x[1])[0] for y in y_test]
    print(sum((1 if y[0] == y[1] else 0) for y in zip(y_predict, y_correct)) / len(y_predict))

    # evaluate the model
    # training accuracy
    # res = model.evaluate(X, Y)
    # print("\n%s: %.2f%%" % (model.metrics_names[1], res[1] * 100))


'''
def train():
    # define a full-connected network structure with 3 layers
    model = Sequential()
    model.add(Dense(300, input_dim=X.shape[1], activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(Y.shape[1], activation='sigmoid'))

    # compile the model
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.8, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd)

    # fit the model
    model.fit(X, Y, epochs=100, batch_size=5)

    # evaluate the model
    # training accuracy
    res = model.evaluate(X, Y)
    print("\n%s: %.2f%%" % (model.metrics_names[1], res[1] * 100))

    model = Sequential()
    model.add(Dense(32, activation='relu', input_dim=100))
    model.add(Dense(10, activation='softmax'))
    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    pass
'''


class NNStrategy:
    def __init__(self, model):
        self.model = model
        pass

    def choose_dice(self):
        prediction = self.model.predict()  # np.array(tk.texts_to_sequences(text))
        print(prediction)
        pass

    def choose_category(self):
        pass


# nninput = self.encode()
# nn_out = self.model.predict()
# cat = max(zip(range(())))
if __name__ == "__main__":
    # Train
    train()

    # Generate train set
    # for line in sys.stdin:
    #     process(line, True)
    #     print("\n")
