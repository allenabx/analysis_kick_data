import matplotlib.pyplot as plt

BEGIN =725
END = -250
FILENAME = 'type2-2.csv'
CIRCLE_INTERVAL = 1
LIMIT = 0.
plot_joint =18
file = 'kick.skl'

def get_info(filename):
    with open(filename) as f:
        info = f.readlines()
        all_info = [i.strip('\n').split(',')[:][2:-1] for i in info[0:END]]
        all_info = all_info[0:1]+all_info[BEGIN:]


        return all_info


def plot(info, index):
    head = info[0]
    para = [float(k) for k in [_[:-1][index] for _ in info[1:]]]

    plt.plot(para, '.')
    plt.title(head[index])
    plt.xlabel('times')
    plt.ylabel('angle')

    plt.savefig('scores.png')
    plt.show()


def add_start(i):
    return "# STATE " + str(i) + "\n" \
                                 "STARTSTATE\n"


def add_mid(e, state):
    str1 = "settar "
    for i in range(len(e)):
        if (joint_check(e[i], state[i])):
            continue
        else:
            state[i] = e[i]

        if i < 4:
            str1 += ("EFF_LA" + str(i + 1) + " " + str(e[i]) + " ")
        elif i < 11:
            str1 += ("EFF_LL" + str(i - 3) + " " + str(e[i]) + " ")
        elif i < 18:
            str1 += ("EFF_RL" + str(i - 10) + " " + str(e[i]) + " ")
        elif i < 23:
            str1 += ("EFF_RA" + str(i - 17) + " " + str(e[i]) + " ")

    return str1


def add_end():
    return " end\n" \
           "wait " + str(CIRCLE_INTERVAL * 0.02) + " end\n" \
                                                   "ENDSTATE\n\n"


def joint_check(now, before):

    if abs(float(now) - float(before)) < LIMIT:
        return True
    else:
        return False


def add_state(i, e, last_state_value):
    strs = ""
    strs += add_start(i)
    strs += add_mid(e, last_state_value)
    strs += add_end()
    return strs

def str2float(strs):
    temp = []
    for i in strs:
        temp_line = []
        for j in i:
            temp_line.append(float(j))
        temp.append(temp_line)
    return temp

def generate_skill(all_info):
    skill_str = "STARTSKILL SKILL_KICK_LEFT_LEG\n" 
    all_info = str2float(all_info)
    last_state_value = len(all_info[0]) * [9999]


    for state_num, state_value in enumerate(all_info):
        skill_str += add_state(state_num, state_value, last_state_value)

    # print(temp_cnt)
    temp_str = "settar  end\n"
    skill_str = skill_str.replace(temp_str, '')
    skill_str += "\nENDSKILL\n" \
                 "REFLECTSKILL SKILL_KICK_LEFT_LEG SKILL_KICK_RIGHT_LEG\n"

    #print(skill_str)
    # print(temp_cnt)
    return skill_str

def write2file(filename,strs):
    file = open(filename, 'w+')
    file.write(strs)
    file.close()

if __name__ == '__main__':
    all_info = get_info(FILENAME)
    all_info = [all_info[i] for i in range(len(all_info)) if i % CIRCLE_INTERVAL == 0]
    plot(all_info, plot_joint)

    strs = generate_skill(all_info[1:])
    write2file(file,strs)