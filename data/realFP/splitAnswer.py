import re
import math
import json


def reformat_json_data(index, data):
    # @param: index: <int>
    # data: <json object>
    question = data["question"]
    program = data["program"]
    answer = data["answer"]
    context = data["context"]
    #fact = data["fact_transform"]

    # Extract answer value and unit
    answerValue, answerUnit = parse_answer_unit(answer)

    # convert answer to order of magnitude value (log base 10)
    OOM_string = convertStringToOOM(answerValue)
    
    # Parse context into an object
    context_object = parse_context(context)

    # Create the final JSON object
    formatted_data = {
        "ID": str(index),
        "question": question,
        "answer": answerValue,
        "OOM": OOM_string,
        "unit": answerUnit,
        "context": context_object
    }
    return formatted_data


def parse_answer_unit(answerString):
    if (answerString == None): # NoneType exception
        return "", ""
    
    # define pattern
    pattern = re.compile("([+-]?[\d.]+(?:[Ee][+-]?\d+)?)[ ]?([a-zA-Z]+(?:\*\*[0-9]+)?)?")
    match = pattern.match(answerString)
    if match:
        answerValue = match.group(1)
        answerUnit = match.group(2) if match.group(2) else ""
        #print(f"Value: {captured_value}, Unit: {captured_unit}")
    else:
        return "", ""
   
    return answerValue, answerUnit

def parse_context(context):
    pattern = re.compile("=(F\d+):([^=]+)")
    matches = pattern.findall(context)
    context_object = {}

    for match in matches:
        key = match[0]
        value = match[1].strip()
        context_object[key] = value
    return context_object

def convertStringToOOM(m_string):
    # assuming m_string is non-negative
    if (m_string == None or m_string == ""):
        return 0
    exponent = math.log10(float(m_string))
    multiplier = 10 ** (exponent % 1)
    if (multiplier > math.sqrt(10)):
        # round up
        return math.floor(exponent+1)
    else:
        return math.floor(exponent)


test_data = [
    {
        "question": "If I were to take an English penny, melt it down, then somehow stretch it out into a perfect hollow sphere 1 atom thick, how large would this sphere be?",
        "program": "PROGRAM:=Q1: What is the volume of a single penny?=Q2: What is the thickness of the penny which is in the form of a hollow sphere now?=A1: 0.93 in**3=A2: 3.9e-9 in=Q2 -> A2 | F2=Q1 -> A1 | F1=P: Div (Q1, Q2)",
        "answer": "2.3e+8 in**2",
        "context": "CONTEXT:=F1: The volume of the penny is 0.93 in**3=F2: The thickness of the penny is 3.9e-9 in"
    },
    {
        "question": "How long would it take to pluck each hair out of your body one at a time?",
        "program": "PROGRAM:=Q1: How long does it take to pluck a single strand of hair?=Q2: How many hairs do we have on our body?=A1: 5 s=A2: 5e+6=Q2 -> A2 | F2=Q1 -> A1 | F1=P: Mul (Q1, Q2)",
        "answer": "2.5e+7 s",
        "context": "CONTEXT:=F1: It takes around 5 seconds to pluck a single strand of hair.=F2: The entire human body has 5e+6 hair follicles."
    },
    {
        "question": "How many air molecules are in this lecture hall?",
        "program": "PROGRAM:=Q1: What is the volume of the lecture hall?=Q2: What is the volume of a single air molecule?=A1: 24000 m**3=A2: 3e-24 m**3=Q2 -> A2 | F2=Q1 -> A1 | F1=P: Div (Q1, Q2)",
        "answer": "8.00E+27",
        "context": "CONTEXT:=F1: The volume of the lecture hall is 24000 metre cube=F2: The volume of a single air molecule is 3e-24 cubic meter"
    },
    {
        "question": "A cure for all cancers would increase the average American lifespan by how many years?",
        "program": "PROGRAM:=Q1: What is the average american lifespan?=Q2: Cancer cuts down the average lifespan by how many years?=A1: 78=A2: 5=Q2 -> A2 | F2=Q1 -> A1 | F1=P: Add (Q1, Q2)",
        "answer": "83",
        "context": "CONTEXT:=F1: The average american lifespan is 78 years.=F2: Cancer cuts down the average lifespan of a person by 5 years."
    },
    {
        "question": "What is the number of queen-size mattresses it would take to fill the star Betelgeuse which has 18 times the mass of the Sun?",
        "program": "PROGRAM:=Q1: What is the mass of the star Betelgeuse?=Q2: What is the mass of a queen size mattress?=Q3: What is the mass of the sun?=Q4: What is the ratio of the mass of Betelgeuse to mass of sun?=A1: 140 lb=A2: 4.3e+30 lb=A3: 18=Q4 -> A3 | F3=Q3 -> A2 | F2=Q1 -> Mul (Q4, Q3)=Q2 -> A1 | F1=P: Div (Q1, Q2)",
        "answer": "5.50E+29",
        "context": "CONTEXT:=F1: The mass of a queen size mattress is 140 pounds=F2: The mass of the sun is 4.3e+30 pounds.=F3: The ratio of mass of Betelgeuse to mass of sun is 18"
    },
    {
        "question": "If a human was 0.07324219 millimeters large, how long would it take it to walk a mile?",
        "program": "PROGRAM:=Q1: How long does it take for a human of normal height to walk a mile?=Q2: What is the ratio of the height of the normal human to that of the given human?=Q3: What is the height of a normal human?=Q4: What is the height of the given human?=A1: 20 min=A2: 1730 mm=A3: 0.07324219 mm=Q4 -> A3 | F3=Q3 -> A2 | F2=Q2 -> Div (Q3, Q4)=Q1 -> A1 | F1=P: Mul (Q1, Q2)",
        "answer": "472405.3 min",
        "context": "CONTEXT:=F1: An average human takes around 20 minutes to walk a mile. Length of stride is directly proportional to the height of the person.=F2: The height of the average human i s 1730 mm.=F3: The height of the given human is 0.07324219 mm."
    },
    {
        "question": "The grass on the lawn grows 10 cm in height during the week between mowings. Estimate the mass, g, of the grass clippings collected each week.",
        "program": "PROGRAM:=Q1: What is the total number of blades collected in the week after cutting them?=Q2: What is the average mass of a single blade of grass?=Q3: What is the average size of a lawn?=Q4: How many blades of grass are there on a single ft**2 of a lawn?=A1: 0.01 g=A2: 200 ft**2=A3: 3000 ft**-2=Q4 -> A3 | F3=Q3 -> A2 | F2=Q1 -> Mul (Q3, Q4)=Q2 -> A1 | F1=P: Mul (Q1, Q2)",
        "answer": "6000 g",
        "context": "CONTEXT:=F1: The weight of a blade of grass is 0.01 g=F2: The average size of a freshly mowed lawn is 200 ft**2=F3: There are 3000 blades of grass in a single ft**2 of a lawn."
    },
    {
        "question": "How much force is required to move a planet with a punch?",
        "program": "PROGRAM:=Q1: What is the force required to move the object from its position?=Q2: What is the average gravitational force of a planet?=A1: 1 N=A2: 3e+22 N=Q2 -> A2 | F2=Q1 -> A1 | F1=P: Add (Q1, Q2)",
        "answer": "3e+22 N",
        "context": "CONTEXT:=F1: The force required to move an object from its position could be any force that is greater than the force that the object is exerting opposite to us (in this case, it is the gravitational force) (e.g. 1 N).=F2: The average gravitational force of a planet is 3e+22 N"
    },
    {
        "question": "What is the average pressure, atm, at the bottom of the Earth's oceans?",
        "program": "PROGRAM:=Q1: What is the force acting on the bottom of the oceans?=Q2: What is the surface area of the oceans?=Q3: What is the mass of the ocean cover?=Q4: What is the acceleration due to gravity?=Q5: The pressure acting on bottom of the oceans in Pascals=Q6: How many pascals are in an atm?=A1: 5.10082e+20 m**2=A2: 1.3e+21 kg=A3: 10 m*s**-2=A4: 9.8e-6 atm*kg**-1*m**1*s**2=Q4 -> A3 | F3=Q3 -> A2 | F2=Q1 -> Mul (Q3, Q4)=Q2 -> A1 | F1=Q5 -> Div(Q1, Q2)=Q6 -> A4 | F4=P: Mul (Q5, Q6)",
        "answer": "2.4e-4 atm",
        "context": "CONTEXT:=F1: The surface area of the oceans is 5.10082e+20 m**2=F2: The total mass of ocean cover is 1.3e+21 kg=F3: The acceleration due to gravity is 10 m/sec**2=F4: One atm in 101325 pascals"
    },
    {
        "question": "How many port-a-potties should be planned for the next million-man-march?",
        "program": "PROGRAM:=Q1: How many people participate in a million march?=Q2: How many people can one port-a-potty service?=A1: 1000000=A2: 50=Q2 -> A2 | F2=Q1 -> A1 | F1=P: Div (Q1, Q2)",
        "answer": "20000",
        "context": "CONTEXT:=F1: A total of 1000000 people participate in a million march=F2: A single port-a-potty can service 50 people."
    },
    {
        "question": "What is the energy needed to evaporate the oceans?",
        "program": "PROGRAM:=Q1: What is the volume of the oceans?=Q2: What is the energy required to evaporate 1 cc of water?=A1: 1.3e+24=A2: 540 cal=Q2 -> A2 | F2=Q1 -> A1 | F1=P: Mul (Q1, Q2)",
        "answer": "7e+26 cal",
        "context": "CONTEXT:=F1: The volume of the oceans is 1.3e+24 cc=F2: The energy required to evaporate 1cc of water is 540 calories"
    }
]

# CHECK: some answer doesn't make any sense...

# print("No. of Entries: " + str(len(test_data)))

# formatted_data = []
# index = 0

# for entry in test_data:
#     formatted_entry = reformat_json_data(index, entry)
#     formatted_data.append(formatted_entry)
#     index +=1

# formatted_data_json = json.dumps(formatted_data, indent=2)
# print(formatted_data_json)


if __name__ == '__main__':
    # load dataset
    f = open('./data/realFP/test_realfp.json',"r", encoding="utf-8")
    FP_data = json.load(f)
    print("No. of Entries: " + str(len(FP_data)))

    # reformat dataset
    formatted_data = []
    index = 0

    for entry in FP_data:
        formatted_entry = reformat_json_data(index, entry)
        formatted_data.append(formatted_entry)
        index +=1

    # print the formated object
    formatted_data_json = json.dumps(formatted_data, indent=2)
    print(formatted_data_json)

    # write into a new file
    with open('formatted_combined_realfp.json', 'w', encoding='utf-8') as output:
        json.dump(formatted_data, output, ensure_ascii=False, indent=4)
        output.close()