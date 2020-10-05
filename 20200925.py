import os
import pandas as pd
import matplotlib.pyplot as plt
import time

attribution = ['workclass', 'education', 'matrital_status', 'occupation',
               'relationship', 'race', 'sex', 'native_country']


class train(object):

    def __init__(self, workclass, education, matrital_status, occupation,
                 relationship, race, sex, native_country, salary):
        self.workclass = workclass
        self.education = education
        self.matrital_status = matrital_status
        self.occupation = occupation
        self.relationship = relationship
        self.race = race
        self.sex = sex
        self.native_country = native_country
        self.salary = salary


os.chdir('C://Users/CookiePie/Desktop/todo/test')


# 加载训练集
def load_data(name):
    with open(name, 'r', encoding='gbk') as x:

        # 储存训练数据
        adults = []
        # 逐行读取
        for i in x:

            # 逗号分割
            m = i.split(',')

            # 删掉字符串中的前后空格和
            for n in range(len(m)):
                m[n] = m[n].strip(' ')
                m[n] = m[n].strip('\n')
                m[n] = m[n].strip('.')

            # 将单行数据变成train类
            people = train(m[1], m[3], m[5], m[6], m[7], m[8], m[9], m[13], m[14])
            adults.append(people)

        return adults


# 似然函数表格
def likelihood(data, typ):
    y = pd.DataFrame(columns=attribution)
    test = []
    z = 0  # 计数

    for xx in attribution:

        for x in data:
            if x.salary == typ:
                m = getattr(x, xx)  # 获得属性值

                if m != '?':
                    if m in test:
                        y.loc[m, xx] += 1
                    elif not (m in test):
                        test.append(m)
                        row = [0 for i in range(8)]
                        row[z] = 1
                        row = dict(zip(attribution, row))
                        row = pd.DataFrame(row, index=[m])
                        y = y.append(row)

        z += 1
    return y


# data_1是大于50的似然，data_2是小于等于50的似然
def probability(data, data_1, data_2, t, above, below):
    def score(data_m, pre):
        score_list = []
        data_index = data_m.index.tolist()
        for x in data:
            score_m = 1
            for xx in attribution:
                m = getattr(x, xx)
                if m in data_index:
                    score_m *= data_m.loc[m, xx] / data_m[xx].sum()
                else:
                    score_m *= 1 / (data_m[xx].sum() + len(data_m[data_m[xx] != 0]))
            score_m *= pre
            score_list.append(score_m)
        return score_list

    score_above50 = score(data_1, 7841 / 32561)
    score_below50 = score(data_2, 24720 / 32561)
    TP = 0
    FP = 0
    for i in range(len(score_above50)):
        a = '<=50K'
        if score_above50[i] / score_below50[i] >= t:
            a = '>50K'

        # a是我判断出的最后结果
        if a == '>50K' and data[i].salary == '>50K':
            TP += 1
        elif a == '>50K' and data[i].salary == '<=50K':
            FP += 1

    return TP / above, FP / below


'''data_train = load_data('adult.data')
a = 0
b = 0
for i in data_train:
    if i.salary == '>50K':
        a += 1
    else:
        b += 1
print(a)
print(b)'''
data_test = load_data('adult.test')
aa = 0
b = 0
for q in data_test:
    if q.salary == '>50K':
        aa += 1
    else:
        b += 1
data_above = pd.read_excel('test1.xlsx', index_col=0)
data_below = pd.read_excel('test2.xlsx', index_col=0)
x_row = []
y_row = []
count = 0
test_1 = [0.000001, 0.01, 0.03, 0.05, 0.07, 0.09,
          0.1, 0.3, 0.5, 0.7, 0.9]
test_2 = range(1, 100, 20)
test_1.extend(test_2)
for k in test_1:
    start = time.perf_counter()
    re_1, re_2 = probability(data_test, data_above, data_below, k, above=aa, below=b)
    x_row.append(re_1)
    y_row.append(re_2)
    end = time.perf_counter()
    count += 1
    print(str(count) + '次完成' + '，用时' + str(end - start) + '秒')
print(y_row)
print(x_row)
plt.plot(y_row, x_row)
plt.axis([0, 1, 0, 1])
plt.show()
