import os
import json
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

with open('./FermiQuestionTree.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    f.close()


# example = {
#   "content": "{\n    \"question\": \"What is the area of Madagascar, in square angstroms?\",\n    \"answer\": \"32\",\n    \"unit\": \"square angstroms\",\n    \"context\": \"\"\n}",        
#   "role": "assistant"
# }

# obj = json.loads(example["content"]) 
response_list = []
output_list = [] 
a = len(data)

# MAIN LOOP
for i in range(a):
    # set my message
    entry = json.dumps(data[i], indent=0)
    
    # BEST prompt
    content = "You will update the unit field of the following json object based on question field:\n{entry}. If the question suggest no unit for the answer, return null. Only reply json object and nothing else".format(
        entry = entry
    )

    # BAD prompt
    # content = "Create python to update the unit attribute of the following json object, based on it's question attribute: \n{entry}. Return the original json object if no unit can be provided. Only respond with a single json object. Never return null.".format(
    #     entry = entry
    # )

    # initialise list of returned output


    # customise my message
    my_messages = [
        {"role": "user", "content": content}
    ]

    try:
        # create chat completion
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=my_messages,
            max_tokens = 150
        )
    except Exception as e:
        print(e)

    # always cache response immediately
    with open('cache.json', 'a', encoding='utf-8') as output:
        try:
            json.dump(response, output, ensure_ascii=False, indent=4)
        except Exception as e:
            print("Cache Error for index: " + str(i))
            print(e)

        output.close()
    
    # store completed prompt
    response_content = response['choices'][0]['message']['content']
    try:
        response_obj = json.loads(response_content)
        # console output
        print(i)
        print(response_obj)
    except Exception as e:
        print("Convert Error for index:" + str(i))
        print(e)
        # cache error response, append to the file
        with open('exception.txt', 'a', encoding='utf-8') as exception_file:
            exception_file.write("\n") # add new line
            exception_file.write(response_content)
            exception_file.close()
        response_obj = data[i] # write in original object
    
    
    output_list.append(response_obj)
    
    # write into file immediately to prevent data loss
    with open('PopFQT.json', 'w', encoding='utf-8') as output:
        json.dump(output_list, output, ensure_ascii=False, indent=4)
        output.close()
    

print(output_list)
with open('PopFQT.json', 'w', encoding='utf-8') as output:
    json.dump(output_list, output, ensure_ascii=False, indent=4)
    output.close()


# failure example
#'{\n    "question": "What is 7<sup>43</sup>?",\n    
# "answer": "36",\n    
# "unit": "",\n    
# "context": ""\n} 
# \n\n
# There is no unit associated with a mathematical calculation, so the "unit" field should remain empty. No updates are necessary.'

# crashed at index 133 because an empty string is returned
# only rescued 14 -> need to cache response!!
