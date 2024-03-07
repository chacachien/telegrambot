user_inputs =[]
with open("/Users/phatnguyen/Document/work/dan/test/question/question1.txt", "r") as f:
    lines = f.readlines()
    user_inputs+= [line.strip() for line in lines]

print(user_inputs)