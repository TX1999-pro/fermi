from eval_utils import compile_fp

# test
p = "PROGRAM:=Q1: How long does it take to pluck a single strand of hair?=Q2: How many hairs do we have on our body?=A1: 5 s=A2: 5e+6=Q2 -> A2 | F2=Q1 -> A1 | F1=P: Mul (Q1, Q2)"
context = "CONTEXT:=F1: It takes around 5 seconds to pluck a single strand of hair.=F2: The entire human body has 5e+6 hair follicles."    

print(compile_fp(context,p))