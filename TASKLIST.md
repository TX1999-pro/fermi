# Task List

## 1. Improve readability
The json file may not be very human-accessible (i.e. train_realfp.json)

-[x] write a helper program to load and output json data in a more readable way => printFP.py

```python
import json
  
# Opening JSON file
f = open('./realFP/train_realfp.json')
  
# returns JSON object as a dictionary
data = json.load(f)
  
# Iterating through the json list
json_formatted_str = json.dumps(data, indent=2)
print(json_formatted_str)
  
# Closing file
f.close()
```

## 2. Understand how the PROGRAM is represented and executed

!!!  What does this mean?
```json
{
    "question": "How many air molecules are in this lecture hall?",  
    "program": "PROGRAM:=Q1: What is the volume of the lecture hall?=Q2: What is the volume of a single air molecule?=A1: 24000 m**3=A2: 3e-24 m**3=Q2 -> A2 | F2=Q1 -> A1 | F1=P: Div (Q1, Q2)"
};
{
    "question": "What is the number of queen-size mattresses it would take to fill the star Betelgeuse which has 18 times the mass of the Sun?",    
    "program": "PROGRAM:=Q1: What is the mass of the star Betelgeuse?=Q2: What is the mass of a queen size mattress?=Q3: What is the mass of the sun?=Q4: What is the ratio of the mass of Betelgeuse to mass of sun?=A1: 140 lb=A2: 4.3e+30 lb=A3: 18=Q4 -> A3 | F3=Q3 -> A2 | F2=Q1 -> Mul (Q4, Q3)=Q2 -> A1 | F1=P: Div (Q1, Q2)"
};
```
### What do these symbols mean?

`=`: separation of statements.

`->`: evaluation.

`|`: because of.
```json
"PROGRAM:
=Q1: How long does it take to pluck a single strand of hair?
=Q2: How many hairs do we have on our body?
=A1: 5 s
=A2: 5e+6
=Q2 -> A2 | F2
=Q1 -> A1 | F1
=P: Mul (Q1, Q2)"
// separated by line for readability, as the orginal data does not contain \n
```
Looks like the program use FILO, or a stack model for execution.
Q0 -> in
Q1 -> in
Q2 -> in

Q2 -> F2 is relevant -> A2 -> out
Q1 -> F1 is relevant -> A1 -> out
Q0 -> results based on A1 and A2 -> out


## 3. Format dataset into a more organised data structure
The database is US-centric, where units used are not in SI.
Also, the author used string-based symbolic expression to separate the contents, and parse using his self-defined python codes.

For example, the PROGRAM, and CONTEXT use “=” as an indicator:

```json
{
    "question": "How long would it take to pluck each hair out of your body one at a time?",
    "program": "PROGRAM:=Q1: How long does it take to pluck a single strand of hair?=Q2: How many hairs do we have on our body?=A1: 5 s=A2: 5e+6=Q2 -> A2 | F2=Q1 -> A1 | F1=P: Mul (Q1, Q2)",
    "answer": "2.5e+7 s",
    "context": "CONTEXT:=F1: It takes around 5 seconds to pluck a single strand of hair.=F2: The entire human body has 5e+6 hair follicles."    
}
```
A better representation of input data for training could be:

!!! This is just my first intuition, on simple decomposition tree (n=3)
```json
{
    "ID": "Q0",
    "question": "How long would it take to pluck each hair out of your body one at a time?",
    "program": 
    [
        {
            "ID": "Q1",
            "question": "How long does it take to pluck a single strand of hair?",
            "answer": "5",
            "unit": "s",  
            "context": "F1"
        },
        {
            "ID": "Q2",
            "question": "How many hairs do we have on our body?",
            "answer": "5e+6",
            "unit": "",
            "context": "F2"
        },
        {
            "context": ["F1", "F2"],
            "operation": ["Q1", "x", "Q2"]
        }
    ],    
    "answer": "2.5e+7",
    "unit": "s",
    "context": 
        {
            "F1": "It takes around 5 seconds to pluck a single strand of hair.", 
            "F2": "The entire human body has 5e+6 hair follicles."
        }    
}

```
Let's first find out questions that have more than 2 sub-questions

!!! How do we format every object in the array into such a structure?
1. Do we hardcode this using python or javascript?
2. Do we give the LLM some example and use LLM to perform the computation?

- [x] parse answer unit
- [x] parse context into key-value pairs
- [ ] parse program into sub-questions

- [ ] execute the program
    - [ ] retrieve the question id, question text, and answer
    - [ ] ~~match the context~~

- [ ] program syntax / grammar

!!! NOTE: Some of the answers do not contain units...
- [ ] I can ignore the units in answer for now, and do a manual check later (if the missing unit case is not prevalent)

## 4. Train a model to predict answer A and program P, from question Q

### 4.1 start with simpler case, one level decomposition 

Decompose one question into 2 sub-questions. Since the fermi problem is recursive in nature, just like the tree structure, we can then perform the same operation on the sub-questions.



### 



## Complexity
We may define the complexity of the answer based on the number of nodes (total number of questions answered, including the original one).

## Chain of reasoning
From the [paper](https://arxiv.org/abs/2110.14207), it says most entries contains typically 2 subquestions (n=3), with 176 questions in REALFP contain deeper chain of reasoning (up to 10 subquestions).

!!! How do we rank questions by complexity?
