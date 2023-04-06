import json

def count_JSON_length(json_file:str):
    # counts the number of objects in the given object
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            f.close()
            return len(data)
    except Exception as e:
        print (e)


# Open the JSON file containing the Fermi questions
with open('./questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    f.close()

# Get the questions object from the data dictionary
questions = data['questions']

# Create a list to hold the question-answer pairs
question_answer_pairs = []

# Iterate over each question in the questions object and create a dictionary for each question-answer pair
for question, answer in questions.items():
    q_dict = {}
    q_dict['question'] = question
    q_dict['answer'] = str(answer)
    q_dict['unit'] = ''
    question_answer_pairs.append(q_dict)

# Print the list of question-answer pairs
print(question_answer_pairs)

with open('FermiQuestionTree.json', 'w', encoding='utf-8') as output:
    json.dump(question_answer_pairs, output, ensure_ascii=False, indent=4)
    output.close()