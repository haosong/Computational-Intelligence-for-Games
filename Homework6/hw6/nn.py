import numpy as np
import datetime
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout
from keras import optimizers
import sys
from yahtzee import YahtzeeScoresheet, YahtzeeRoll

category = ["1", "2", "3", "4", "5", "6", "3K", "4K", "FH", "SS", "LS", "C", "Y", "Y+"]  # Y/Y+, UP

output_label = ["1", "2", "3", "4", "5", "6", "K", "FH", "S", "C", "RE"]

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

    # for i in range(1, 7):
    #     vector.append(roll.count(i) / 5)

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
        return one_vector
    else:
        return vector


def train():
    np.random.seed(7)

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
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # fit the model
    model.fit(x_train, y_train, epochs=100, batch_size=50)

    y_predict = [max(enumerate(y), key=lambda x: x[1])[0] for y in model.predict(x_test)]
    y_correct = [max(enumerate(y), key=lambda x: x[1])[0] for y in y_test]

    test_set_accu = sum((1 if y[0] == y[1] else 0) for y in zip(y_predict, y_correct)) / len(y_predict)
    print(test_set_accu)

    model.save('my_model.h5')
    # model_json = model.to_json()
    # print(model_json)
    # with open("model.json" + datetime.datetime.now().isoformat() + str(test_set_accu), "w") as json_file:
    #     json_file.write(model_json)
    return model


class NNStrategy:
    def __init__(self):
        self.model = load_model('my_model_230.h5')
        # self.model = model
        pass

    def choose_dice(self, sheet, roll, rerolls):
        line = sheet.as_state_string() + "," + "".join(str(x) for x in roll.as_list()) + "," + str(rerolls)
        # print(line)
        x = [process(line, False)]
        predict = self.model.predict(np.matrix(x))[0]
        # print("c_d_predict")
        # print(predict)
        # y_predict = [max(enumerate(y), key=lambda x: x[1])[0] for y in predict]
        label_order = sorted(range(len(predict)), key=lambda i: predict[i], reverse=True)
        # print(label_order)
        label = label_order[0]
        # output_label = ["1", "2", "3", "4", "5", "6", "K", "FH", "S", "C", "RE"]
        # category = ["1", "2", "3", "4", "5", "6", "3K", "4K", "FH", "SS", "LS", "C", "Y", "Y+"]  # Y/Y+, UP
        # label_index = output_label.index(category[label])
        if label < 6:
            keep = roll.select_all([label + 1])  # select 1 ~ 6
        elif output_label[label] == "K":
            keep = roll.select_for_n_kind(sheet, rerolls)
        elif output_label[label] == "FH":
            keep = roll.select_for_full_house()
        elif output_label[label] == "C":
            keep = roll.select_for_chance(rerolls)
        elif output_label[label] == "S":
            keep = roll.select_for_straight(sheet)
        elif output_label[label] == "RE":
            keep = YahtzeeRoll.parse("")
        else:
            pass
            # print("no found!!!!!!!!!!!!!")
            # print(output_label[label])
        return keep

    def choose_category(self, sheet, roll):
        line = sheet.as_state_string() + "," + "".join(str(x) for x in roll.as_list()) + "," + str(0)
        # print(line)
        x = [process(line, False)]
        predict = self.model.predict(np.matrix(x))[0]
        # print("c_c_predict")
        # print(predict)
        label_order = sorted(range(len(predict)), key=lambda i: predict[i], reverse=True)
        # print(label_order)
        for index in range(0, len(label_order)):
            label = output_label[label_order[index]]
            # print(label)
            if label == "RE":
                continue
            if label in category:
                if sheet.is_marked(category.index(label)):
                    continue
                else:
                    return category.index(label)
            elif label == "K":
                if sheet.is_marked(category.index("3K")) \
                        and sheet.is_marked(category.index("4K")) \
                        and sheet.is_marked(category.index("Y")):
                    continue
                else:
                    if roll.is_n_kind(5) and not sheet.is_marked(category.index("Y")):
                        return category.index("Y")
                    elif roll.is_n_kind(4) and not sheet.is_marked(category.index("4K")):
                        return category.index("4K")
                    elif roll.is_n_kind(3) and not sheet.is_marked(category.index("3K")):
                        return category.index("3K")
                    else:
                        continue
            elif label == "S":
                if sheet.is_marked(category.index("SS")) \
                        and sheet.is_marked(category.index("LS")):
                    continue
                else:
                    if roll.is_straight(5) and not sheet.is_marked(category.index("LS")):
                        return category.index("LS")
                    elif roll.is_straight(4) and not sheet.is_marked(category.index("SS")):
                        return category.index("SS")
                    else:
                        continue
        for i in range(13):
            if not sheet.is_marked(i):
                return i


# nninput = self.encode()
# nn_out = self.model.predict()
# cat = max(zip(range(())))
if __name__ == "__main__":
    # Train
    train()

    # Generate train set
    # for line in sys.stdin:
    #     process(line, True)
        # print("\n")
