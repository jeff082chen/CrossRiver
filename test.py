from CrossRiver import *
import time

results = []

total_price_A = 0
total_time_A = 0
total_count_t_A = 0
total_count_p_A = 0

total_price_U = 0
total_time_U = 0
total_count_t_U = 0
total_count_p_U = 0

for N in range(3, 11):
    for M in range(0, 3):
        for mode in [0, 1]:
            for alg in ['AS', 'UC']:
                start_time = time.time()
                Node = setParameter(N, M, mode = mode, alg = alg)
                start = Node()

                if alg == 'AS':
                    ans = start.AStartSearch()
                if alg == 'UC':
                    ans = start.uniformCost()
                end_time = time.time()

                last = ans['path'][-1]
                result = 'N:' + str(N) + ',M:' + str(M) + ',Mode:' + str(mode) + ',Alg:' + alg + ',Cost:' + str(last.total_cost) + ',Time:' + str(end_time - start_time) + 'count:' + str(ans['count'])
                results.append(result)

                if mode == 0 and alg == 'AS':
                    total_price_A += last.total_cost
                    total_count_p_A += ans['count']
                if mode == 1 and alg == 'AS':
                    total_time_A += last.total_cost
                    total_count_t_A += ans['count']
                if mode == 0 and alg == 'UC':
                    total_price_U += last.total_cost
                    total_count_p_U += ans['count']
                if mode == 1 and alg == 'UC':
                    total_time_U += last.total_cost
                    total_count_t_U += ans['count']

            results.append('\n')


avg_price_diff = (total_price_A - total_price_U) / 24
avg_time_diff = (total_time_A - total_time_U) / 24
avg_count_p_diff = (total_count_p_A - total_count_p_U) / 24
avg_count_t_diff = (total_count_t_A - total_count_t_U) / 24


with open('../results.txt', 'w') as f:
    for result in results:
        f.write(result + '\n')
    f.write('avg_count_t_diff:' + str(avg_count_t_diff) + '\n')
    f.write('avg_count_p_diff:' + str(avg_count_p_diff) + '\n')
    f.write('avg_price_diff:' + str(avg_price_diff) + '\n')
    f.write('avg_time_diff:' + str(avg_time_diff) + '\n')


