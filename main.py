def get_sequence(n):
    """ Выводит n первых элементов последовательности (например, 122333444455555)"""
    if n == 0:
        return 0
    sequence = ''.join(str(num) * num for num in range(1, n + 1))
    return sequence


while True:
    try:
        num = input("Введите число: ")
        if num in ('exit', 'quit', 'stop', 'q', 'стоп', 'выход'):
            break
        if not num.isdigit():
            raise ValueError
    except ValueError:
        print('Введите положительное число!')
    else:
        print(get_sequence(int(num)))
