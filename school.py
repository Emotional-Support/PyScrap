class main:
    def rand_num(amt):
        for i in range(amt):
            i += i
        print(i)

    def fibonacci(amt):
        x = 0
        y = 1
        for _ in range(amt):
            z = x + y
            print(z)
            x = y
            y = z


num_input = int(input())
main.fibonacci(num_input)
