from solution.algorithm import solve_by_dp
from solution.files import FileEngine, TEST_RANGE


def main():
    for i in range(*TEST_RANGE):
        fe = FileEngine(i)
        segments = fe.read()
        result = solve_by_dp(segments)
        fe.write(result)
        print('Completed #{i}: {result}'.format(i=i, result=result))

        # # to verify the result using brute force
        # print('Verifying #{i} by brute force...'.format(i=i))
        # result = solve_by_brute_force(segments)
        # print('Verified #{i}: {result}'.format(i=i, result=result))


if __name__ == '__main__':
    main()
