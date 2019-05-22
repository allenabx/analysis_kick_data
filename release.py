import matplotlib.pyplot as plt

BEGIN = 300
END = -1
FILENAME = '3.csv'
LIMIT = 0.5
0

def get_info(filename):
    with open(filename) as f:
        info = f.readlines()
        head = info[0].strip('\n').split(',')
        all_info = [i.strip('\n').split(',') for i in info[BEGIN:END]]
        head = head[2:-1]

        all_info = [i[2:] for i in all_info]

        return head, all_info


def plot(head, info, index):
    para = [float(k) for k in [_[:-1][index] for _ in info]]
    plt.plot(para, '.')

    plt.title(head[index])
    plt.xlabel('times')
    plt.ylabel('angle')

    plt.savefig('scores.png')
    plt.show()


def init_skill(first_info):
    str1 = "STARTSKILL SKILL_KICK_LEFT_LEG\n" \
           "# STATE 0\n" \
           "STARTSTATE\n"
    str1 += "settar "
    for i in range(len(first_info)):
        if i < 4:
            str1 += ("EFF_LA" + str(i + 1) + " " + first_info[i] + " ")
        elif i < 10:
            str1 += ("EFF_LL" + str(i - 3) + " " + first_info[i] + " ")
        elif i < 14:
            str1 += ("EFF_RA" + str(i - 9) + " " + first_info[i] + " ")
        elif i < 20:
            str1 += ("EFF_RL" + str(i - 13) + " " + first_info[i] + " ")
    str1 += " end\n" \
            "wait 0.02 end\n" \
            "ENDSTATE\n"
    return str1


def add_skill(i, e, state):
    str1 = "# STATE " + str(i) + "\n" \
                                 "STARTSTATE\n"
    str1 += "settar "
    for i in range(len(e)):
        if abs(float(e[i]) - float(state[i])) < 0.5:
            continue

        if i < 4:
            str1 += ("EFF_LA" + str(i + 1) + " " + e[i] + " ")
        elif i < 10:
            str1 += ("EFF_LL" + str(i - 3) + " " + e[i] + " ")
        elif i < 14:
            str1 += ("EFF_RA" + str(i - 9) + " " + e[i] + " ")
        elif i < 20:
            str1 += ("EFF_RL" + str(i - 13) + " " + e[i] + " ")

    str1 += " end\n" \
            "wait 0.02 end\n" \
            "ENDSTATE\n\n"
    return str1


def refresh_state(now, befor,cnt):
    now = [float(i) for i in now]
    befor = [float(i) for i in befor]

    for i in range(len(now)):
        if abs(now[i] - befor[i]) < LIMIT: pass#now[i] = befor[i]
        else :cnt=cnt +1
    print(cnt)
    return now,cnt


def generate_skill(all_info):
    now_state = all_info[0]
    skill_str = init_skill(now_state)
    temp_cnt = 0
    for i, e in enumerate(all_info):
        skill_str += add_skill(i, e, now_state)
        now_state ,temp_cnt= refresh_state(e, now_state,temp_cnt)
    #print(temp_cnt)
    temp_str = "settar  end\n"
    skill_str = skill_str.replace(temp_str, '')
    print(skill_str)
    print(temp_cnt)

if __name__ == '__main__':

    head, all_info = get_info(FILENAME)
    plot(head,all_info,9)
    generate_skill(all_info)
