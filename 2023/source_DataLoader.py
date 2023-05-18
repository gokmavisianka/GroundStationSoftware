from datetime import datetime
import pandas as pd

names = ("temperature", "pressure", "altitude")


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def pump(output: list):
    length = len(output)
    sub_dictionary = {}
    for index in range(length):
        key = names[index]
        value = output[index]
        condition = is_float(value)
        if condition is False:
            value = data_loader.data_frame[key].mean()
        else:
            value = float(value)
        sub_dictionary[key] = value
    data_loader.update(sub_dictionary)


def filter(input: str):
    output = input.split(":")
    length = len(output)
    target_length = len(names)
    if length == target_length:
        pump(output)
    elif length < target_length:
        difference = target_length - length
        for number in range(difference):
            input += ":"
        filter(input)
    else:
        input = ":".join(output[:3])
        filter(input)


class DataLoader:
    def __init__(self):
        self.time_data = [self.get_time()]
        self.dictionary = {"temperature": [0.0], "pressure": [0.0], "altitude": [0.0]}
        self.data_frame = pd.DataFrame(data=self.dictionary)
        self.LineGraphs = {}

    def update(self, sub_dictionary):
        self.time_data.append(self.get_time())
        for key in sub_dictionary:
            self.dictionary[key].append(sub_dictionary[key])
            try:
                self.LineGraphs[key].variables["Roket"]["value"] = self.dictionary[key]
                self.LineGraphs[key].variables["Faydalı Yük"]["value"] = self.dictionary[key]
                self.LineGraphs[key].draw()
            except KeyError:
                print(f"LineGraphs['{key}'] bulunamadı.")

        sub_data_frame = pd.DataFrame(index=[self.get_time()], data=sub_dictionary)
        self.data_frame = self.data_frame.add(sub_data_frame, fill_value=0)

        print(self.data_frame)

    def define(self, LineGraphs):
        self.LineGraphs = LineGraphs

    @staticmethod
    def get_time() -> str:
        time = datetime.now()
        return f"{time.hour:02}:{time.minute:02}:{time.second:02}"

data_loader = DataLoader()
