import pandas as pd
from typing import List
from model import State, StepResponse

easy_data = []
medium_data = []
hard_data = []

df = pd.read_csv('dataset.csv')
rows_list = df.to_dict(orient='records')

for row in rows_list:
    if row['difficulty'] == "easy":
        easy_data.append(row)
    elif row['difficulty'] == "medium":
        medium_data.append(row)
    elif row['difficulty'] == "hard":
        hard_data.append(row)


class DNSenv:

    def __init__(self, data):
        self.action_map = {
            0: 'allow',
            1: 'investigate',
            2: 'block'
        }
        self.query_map = {"A": 0, "TXT": 1, "MX": 2}
        self.data = data
        self.index = 0
        self.done = False
        self.correct_count = 0
        self.partial_count = 0
        self.total_steps = 0
        self.last_actions: List[int] = []

    def row_to_features(self, row):
        return [
            float(row["domain_length"]) / 100,
            float(row["request_frequency"]) / 1000,
            float(row["entropy"]) / 8,
            float(self.query_map.get(row["query_type"], 0))
        ]

    def reset(self):
        self.index = 0
        self.done = False
        self.correct_count = 0
        self.partial_count = 0
        self.total_steps = 0
        self.last_actions = []
        return State(features=self.row_to_features(self.data[self.index]))

    def step(self, action: int):

        action_str = self.action_map[action]
        self.last_actions.append(action)

        curr = self.data[self.index]
        label = curr.get("label", "unknown")

        self.total_steps += 1
        reward = -1

        if label == "normal":
            if action_str == 'allow':
                reward = 1
                self.correct_count += 1
            elif action_str == 'investigate':
                reward = 0.5
                self.partial_count += 1
            elif action_str == 'block':
                reward = -1

        elif label == "suspicious":
            if action_str == 'investigate':
                reward = 1
                self.correct_count += 1
            elif action_str in ['allow', 'block']:
                reward = -1

        elif label == "tunneling":
            if action_str == 'block':
                reward = 1
                self.correct_count += 1
            elif action_str == 'investigate':
                reward = 0.3
                self.partial_count += 1
            elif action_str == 'allow':
                reward = -1

        else:
            reward = -1

        reward = (reward + 1) / 2

        self.index += 1

        if self.index >= len(self.data):
            self.done = True
            next_features = [0.0, 0.0, 0.0, 0.0]
        else:
            next_features = self.row_to_features(self.data[self.index])

        return StepResponse(
            state=State(features=next_features),
            reward=float(reward),
            done=self.done
        )

    def state(self):
        if self.done:
            return None
        return State(features=self.row_to_features(self.data[self.index]))

    def grader_easy(self):
        return self.correct_count / max(1, self.total_steps)

    def grader_medium(self):
        return (self.correct_count + 0.5 * self.partial_count) / max(1, self.total_steps)

    def grader_hard(self):
        correct = 0
        total = self.total_steps

        for i in range(total):
            row = self.data[i]
            label = row["label"]
            action = self.action_map[self.last_actions[i]]

            if label == "normal" and action == 'allow':
                correct += 1
            elif label == "suspicious" and action == 'investigate':
                correct += 1
            elif label == "tunneling" and action == 'block':
                correct += 1

        return correct / max(1, total)