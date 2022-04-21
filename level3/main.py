from os import makedirs
from os.path import join

import matplotlib.pyplot as plt


############  OUTPUT  ############
# test 1 matches reference 1 (distance : 0.30097106334199997)
# test 2 matches reference 2 (distance : 0.187151816543)
# test 3 matches reference 2 (distance : 0.11843070533600002)
# test 4 matches reference 2 (distance : 0.3426367051030001)
# test 5 matches reference 1 (distance : 0.550316684193)
# test 6 matches reference 1 (distance : 1.9284510030939999)
############  OUTPUT  ############

delta = lambda a,b: (a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2

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
    m[0][0] = (delta(A[0], B[0]), (-1,-1))
    for i in range(1, S):
        m[i][0] = (m[i-1][0][0] + delta(A[i], B[0]), (i - 1, 0))
    for j in range(1, T):
        m[0][j] = (m[0][j-1][0] + delta(A[0], B[j]), (0, j - 1))

    for i in range(1, S):
        for j in range(1, T):
            minimum, index = my_min(m[i-1][j], m[i][j-1], m[i-1][j-1])
            indexes = [(i - 1, j), (i, j - 1), (i - 1, j - 1)]
            m[i][j] = (minimum[0] + delta(A[i], B[j]), indexes[index])
    return m

def save_plot_img(references, test, save_path):
    fig, ax = plt.subplots(subplot_kw={'projection' : '3d'})
    
    x, y , z = [r[0] for r in references[0]], [r[1] for r in references[0]], [r[2] for r in references[0]]
    ax.plot(x, y, z, label="reference 1")
    
    x, y , z = [r[0] for r in references[1]], [r[1] for r in references[1]], [r[2] for r in references[1]]
    ax.plot(x, y, z, label="reference 2")
    
    x, y , z = [r[0] for r in test], [r[1] for r in test], [r[2] for r in test]
    ax.plot(x, y, z, label="test")
    
    ax.legend()
    fig.savefig(save_path)


reference_dir = join('..', 'time_series_dataset', 'level3', 'reference')
references = []
for label in range(1, 3):
    with open(join(reference_dir, str(label) + '.dat')) as f:
        time_data_str = f.read().split()
        time_data = []
        for i in range(0, len(time_data_str), 3):
            time_data.append([float(time_data_str[i]), float(time_data_str[i+1]), float(time_data_str[i+2])])
        references.append(time_data)
        
test_dir = join('..', 'time_series_dataset', 'level3', 'test')
tests = []
for label in range(1, 7):
    with open(join(test_dir, str(label) + '.dat')) as f:
        time_data_str = f.read().split()
        time_data = []
        for i in range(0, len(time_data_str), 3):
            time_data.append([float(time_data_str[i]), float(time_data_str[i+1]), float(time_data_str[i+2])])
        tests.append(time_data)

for test_idx in range(6):
    dis = [calc_dtw(tests[test_idx], references[i])[-1][-1][0] for i in range(2)]
    min_dis = min(dis)
    pred = dis.index(min_dis)
    print("test {} matches reference {} (distance : {})".format(test_idx + 1, pred + 1, min_dis))

    makedirs('imgs', exist_ok=True)
    save_path = join('imgs', 'test' + str(test_idx) + '.png')
    save_plot_img(references, tests[test_idx], save_path)
