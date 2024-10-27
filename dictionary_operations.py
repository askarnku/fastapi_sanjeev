my_dict = {}

my_list = []

for i in range(4):
    my_dict[str(i)] = "hello" + str(i)
    my_list.append(my_dict)
    print(i, my_dict)
    print("------------")
