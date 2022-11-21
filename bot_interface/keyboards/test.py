
x = 100
sum_num = 0
while x >= 1:
    num = 1 / x
    sum_num += num

    print(f'\t{x=}: {num=}: {sum_num=}')
    x -= 1
print(sum_num)