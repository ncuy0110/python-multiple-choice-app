import json
from random import randint

data = {
    'questions': [],
    'answers': []
}

for i in range(10):
    data['questions'].append({
        "question": f"Question {i + 1}",
        "options": ["1", "2", "3", "4"]
    })

for i in range(10):
    data['answers'].append(randint(0, 3))

json_object = json.dumps(data, indent=2)

with open("data.json", "w") as outfile:
    outfile.write(json_object)
