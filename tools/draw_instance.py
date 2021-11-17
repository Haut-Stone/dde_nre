# encoding=utf-8
import matplotlib.pyplot as plt
from pylab import *                                 # 支持中文
mpl.rcParams['font.sans-serif'] = ['SimHei']

names = ['0', '200', '400', '600', '800', '1000', '1200', '1400', '1600', '1800', '2000', '2200', '2400', '2600', '2800']
x = range(len(names))
y = [0.28, 0.42, 0.48, 0.523, 0.622, 0.571, 0.616, 0.6, 0.581, 0.584, 0.629, 0.617, 0.651, 0.641, 0.624]
y1 = [0.21, 0.306, 0.31, 0.336, 0.375, 0.365, 0.417, 0.396, 0.421, 0.400, 0.436, 0.444, 0.381, 0.449, 0.43]
f1 = [0.17, 0.346, 0.46, 0.436, 0.495, 0.475, 0.534, 0.554, 0.605, 0.674, 0.687, 0.725, 0.711, 0.739, 0.734]
# for i in range(len(y)):
#     solo = 2*y[i]*y1[i]/(y[i]+y1[i])
#     f1.append(solo)
loss = [19.1, 15.2, 13.46, 12.65, 11.20, 12.1, 11.4, 10.4, 10.5, 9.2, 8.3, 7.9, 8.2, 7.9, 7.8]
loss2 = [17.1, 11.2, 8.86, 7.9, 8.31, 8.52, 7.53, 6.8, 6.9, 6.7, 6.8, 6.3, 7.6, 6.3, 6.4]
plt.ylim(0, 20)  # 限定纵轴的范围
# plt.plot(x, y, marker='o', mec='r', mfc='w',label=u'准确率曲线')
# plt.plot(x, f1, marker='o', ms=10, label=u'命名实体识别f1值', mfc='w', mec='r')
# plt.plot(x, y1, marker='*', ms=10, label=u'关系抽取f1值', mfc='w', mec='g')
plt.plot(x, loss, marker='o', ms=10, mec='r', mfc='w', label=u'命名实体识别 loss 曲线')
plt.plot(x, loss2, marker='o', ms=10, mec='g', mfc='w', label=u'关系抽取 loss 曲线')
plt.legend()  # 让图例生效
plt.xticks(x, names, rotation=45)
plt.margins(0)
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"训练次数")  # X轴标签
plt.ylabel("数值")  # Y轴标签
plt.title("loss 曲线图表")  # 标题

plt.show()