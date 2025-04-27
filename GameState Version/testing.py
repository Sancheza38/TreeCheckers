import random
rad = 30
num = (random.randint(0,4294967295))%960
print(num)
floor=num-(num%(rad*2))
print(floor)
y_axis = floor+rad
print(y_axis)
y2_axis = 960-1-y_axis
print(y2_axis)
