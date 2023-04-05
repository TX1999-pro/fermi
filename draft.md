```json
{
  "ID": "Q0",
  "question": "If I were to take an English penny, melt it down, then somehow stretch it out into a perfect hollow sphere 1 atom thick, how large would 
this sphere be?",
  "program": [
    "PROGRAM:",
    "Q1: What is the volume of a single penny?",
    "Q2: What is the thickness of the penny which is in the form of a hollow sphere now?",
    "A1: 0.93 in**3",
    "A2: 3.9e-9 in",
    "Q2 -> A2 | F2",
    "Q1 -> A1 | F1",
    "P: Div (Q1, Q2)"
  ],
  "answer": "2.3e+8",
  "unit": "in",
  "context": {
    "F1": "The volume of the penny is 
0.93 in**3",
    "F2": "The thickness of the penny 
is 3.9e-9 in"
  }
}
```