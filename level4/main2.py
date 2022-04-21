from os import makedirs
from os.path import join

import matplotlib.pyplot as plt


############  OUTPUT  ############
# test 1 matches reference 1 (distance : 156.03690120996666)
# test 2 matches reference 1 (distance : 168.4969984045333)
# test 3 matches reference 1 (distance : 108.55194333263334)
# test 4 matches reference 1 (distance : 101.04977772259997)
# test 5 matches reference 1 (distance : 114.12847424159999)
# test 6 matches reference 1 (distance : 124.05033675696664)
# test 7 matches reference 1 (distance : 127.24747436646668)
# test 8 matches reference 2 (distance : 103.34780980266667)
# test 9 matches reference 2 (distance : 355.6485093761999)
# test 10 matches reference 2 (distance : 120.54385064103333)
# test 11 matches reference 2 (distance : 98.52468910146666)
# test 12 matches reference 2 (distance : 135.72073271269994)
# test 13 matches reference 1 (distance : 448.08305648043347)
# test 14 matches reference 2 (distance : 138.85039261586667)
############  OUTPUT  ############

def calc_dis(A, B):
    d = 0.0
    for i in range(len(A)):
        d += (A[i] - B[i])**2
    return d

def my_min(v1, v2, v3):
    if v1[0] <= min(v2[0], v3[0]):
        return v1, 0
    elif v2[0] <= v3[0]:
        return v2, 1
    else:
        return v3, 2 

def calc_dtw(A, B):
    S = len(A)
    T = len(B)

    m = [[0 for j in range(T)] for i in range(S)]
    m[0][0] = (calc_dis(A[0], B[0]), (-1,-1))
    for i in range(1, S):
        m[i][0] = (m[i-1][0][0] + calc_dis(A[i], B[0]), (i - 1, 0))
    for j in range(1, T):
        m[0][j] = (m[0][j-1][0] + calc_dis(A[0], B[j]), (0, j - 1))

    for i in range(1, S):
        for j in range(1, T):
            minimum, index = my_min(m[i-1][j], m[i][j-1], m[i-1][j-1])
            indexes = [(i - 1, j), (i, j - 1), (i - 1, j - 1)]
            m[i][j] = (minimum[0] + calc_dis(A[i], B[j]), indexes[index])
    return m

reference_path_list = [join('..', 'time_series_dataset', 'level4', 'reference', '1', 'data1.dat'),
                       join('..', 'time_series_dataset', 'level4', 'reference', '2', 'data1.dat')]
references = [[], []]
for label in range(1, 3):
    for i in range(1, 4):
        with open(join('..', 'time_series_dataset', 'level4', 'reference', str(label), 'data' + str(i) + '.dat')) as f:
            time_data_str = f.read().split()
            time_data = []
            N = 64
            for i in range(0, len(time_data_str), N):
                time_data.append([float(t) for t in time_data_str[i:i+N]])
            references[label-1].append(time_data)
        
test_dir = join('..', 'time_series_dataset', 'level4', 'test')
tests = []
for label in range(1, 15):
    with open(join(test_dir, 'data' + str(label) + '.dat')) as f:
        time_data_str = f.read().split()
        time_data = []
        N = 64
        for i in range(0, len(time_data_str), N):
            time_data.append([float(t) for t in time_data_str[i:i+N]])
        tests.append(time_data)

for test_idx in range(14):
    ave_dis_list = [0, 0]
    for ref_idx in range(2):
        dis = [calc_dtw(tests[test_idx], references[ref_idx][i])[-1][-1][0] for i in range(3)]
        ave_dis_list[ref_idx] = sum(dis) / len(dis)

    min_ave_dis = min(ave_dis_list)
    pred = ave_dis_list.index(min_ave_dis)
    print("test {} matches reference {} (distance : {})".format(test_idx + 1, pred + 1, min_ave_dis))
