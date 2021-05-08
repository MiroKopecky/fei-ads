def b_calc_recursion(n: int) -> int:
    if n <= 1:
        return 1

    results = 0
    for k in range(n):
        results += b_calc_recursion(k) * b_calc_recursion(n - 1 - k)

    return results


def b_calc_dynamic_programming(n: int) -> int:
    if n <= 1:
        return 1

    results = [1] * 2 + [0] * (n - 1)

    for i in range(2, n + 1):
        for k in range(i):
            results[i] += results[k] * results[i - 1 - k]

    return results[n]


def v_calc_recursion(n: int) -> int:
    if n <= 1:
        return 1

    res = 0
    for k in range(n):
        if k > 3:
            break
        else:
            res += v_calc_recursion(k) * v_calc_recursion(n - 1 - k)

    return res


def v_calc_dynamic_programming(n: int) -> int:
    if n <= 1:
        return 1

    results = [1] * 2 + [0] * (n - 1)

    for i in range(2, n + 1):
        for k in range(min(3, i - 1) + 1):
            results[i] += results[k] * results[i - 1 - k]

    return results[n]


def main():
    for n in range(1, 21):
        print(f'Nodes [{n:02d}] -> b{n} = [{b_calc_dynamic_programming(n)}], '
              f'v{n} = [{v_calc_dynamic_programming(n)}]')

        # print(f'Nodes [{n:02d}] -> b{n} = [{b_calc_recursion(n)}], '
        #      f'v{n} = [{v_calc_recursion(n)}]')


if __name__ == '__main__':
    main()
