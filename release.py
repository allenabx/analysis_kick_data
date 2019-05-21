import matplotlib.pyplot as plt


def get_info(filename):
    with open(filename) as f:
        info = f.readlines()
        head = info[0].strip('\n').split(',')
        all_info = [i.strip('\n').split(',') for i in info[1:-1]]
        return head, all_info

def plot(head,info,index):
    para = [float(k) for k in [_[:-1][index] for _ in info]]
    plt.plot(para, '.')
    plt.title(head[index])
    plt.xlabel('times')
    plt.ylabel('angle')

    plt.savefig('scores.png')
    plt.show()
if __name__ == '__main__':
    head, all_info = get_info('11goal.csv')
    plot(head,all_info,20)



