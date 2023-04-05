import json
import re

def reformat_json_data(data):
    # this only takes on
    question = data["question"]
    program = data["program"]
    answer = data["answer"]
    context = data["context"]

    # Extract answer value and unit
    answer_value, answer_unit = parse_answer_unit(answer)
    
    # Parse context
    context_items = re.findall(r"(F\d): (.+?)(?=(?:=F\d)|$)", context)
    context_dict = {k: v for k, v in context_items}

    # Parse program

    processed_program = process_program(program)

    # Create the final JSON object
    formatted_data = {
        "ID": "Q0",
        "question": question,
        "program": processed_program, # list of sub-questions
        "answer": answer_value,
        "unit": answer_unit,
        "context": context_dict
    }

    return formatted_data

def parse_answer_unit(answer_string):
    # doesn't work with E+10 but works with e+10
    if (answer_string != None):
        match_number = re.compile("([+-]?[\d.]+(?:[Ee][+-]?\d+)?)[ ]?([a-zA-Z]+(?:\*\*[0-9]+)?)?")
        match = re.findall(match_number, answer_string)
        answer_value = match[0][0]
        if (len(match) > 0):
            answer_unit = match[0][1]
        else:
            answer_unit = ""
    else:
        answer_value = ""
        answer_unit = ""
        print("The answer string is None.")

    #answer_unit = answer_string.pop(answer_value)    
    return answer_value, answer_unit

def process_program(program_str):
    question_pattern = r"([QP]\d+):[ ]?([^\=]+)"
    answer_pattern = r"(A\d+):[ ]?([^\=]+)"
    questions = re.findall(question_pattern, program_str)
    answers = re.findall(answer_pattern, program_str)
    question_list = []
    answer_dict = dict(answers)

    #print(dict(answers))

    for question_id, question_text in questions:
        question_dict = {
            "ID": question_id,
            "question":question_text.strip(),
            "answer": get_answer_value(answer_dict, question_id),
            "unit": get_answer_unit(answer_dict, question_id),
            "context": ""
        }
        question_list.append(question_dict)

    # get last line
    program_lines = program_str.split("=")[1:]
    execute = program_lines[-1] # the last line will be "P: xxx"
    question_list.append({"Execute": execute})

    return question_list

def get_answer_value(answer_dict, question_id):
    answer_id = question_id.replace("Q", "A")
    answer = answer_dict.get(answer_id, None)
    answer_value, _ = parse_answer_unit(answer)
    return answer_value

def get_answer_unit(answer_dict, question_id):
    answer_id = question_id.replace("Q", "A")
    answer = answer_dict.get(answer_id, None)
    _, answer_unit = parse_answer_unit(answer)
    return answer_unit



# save the newly formated data into another JSON file

if __name__ == '__main__':
    
    # Opening JSON file
    f = open('./realFP/train_realfp.json')
    
    # returns JSON object as a dictionary
    FP_data = json.load(f)
    
    # Iterating through the json list
    json_formatted_str = json.dumps(FP_data, indent=2)
    print("No. of Entries: " + str(len(FP_data)))
    #print(json_formatted_str)
    
    # Closing file
    f.close()

    # unit test
    test_data = FP_data[120]
    formated_data = reformat_json_data(test_data)
    print(json.dumps(test_data, indent=2))
    print(json.dumps(formated_data, indent=2))

    formated_data = []
    index = 0

    for entry in FP_data:
        formated_entry = reformat_json_data(entry)
        formated_data.append(formated_entry)
        index +=1
        print(index)
    
    formated_data_json = json.dumps(formated_data, indent=2)
    print(formated_data_json)

    with open('output.json', 'w', encoding='utf-8') as output:
        json.dump(formated_data, output, ensure_ascii=False, indent=4)
        output.close()
