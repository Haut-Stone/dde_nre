# encoding=utf-8
import matplotlib.pyplot as plt
from pylab import *                                 # 支持中文
mpl.rcParams['font.sans-serif'] = ['SimHei']

names = ['0', '20', '40', '60', '80', '100', '200', '300']
x = range(len(names))
y = [0.134, 0.259, 0.293, 0.373, 0.381, 0.498, 0.696, 0.674]
y1 = [0.21, 0.24, 0.27, 0.36, 0.33, 0.393, 0.37, 0.33]
# f1 = []
# for i in range(len(y)):
#     solo = 2*y[i]*y1[i]/(y[i]+y1[i])
#     f1.append(solo)
# loss = [2.21, 1.89, 1.78, 1.69, 1.61, 1.43, 0.967, 1.02]

plt.ylim(0, 1)  # 限定纵轴的范围
plt.plot(x, y, marker='o', mec='r', mfc='w',label=u'训练集上的准确率曲线')
plt.plot(x, y1, marker='*', ms=10, label=u'测试集上的准确率曲线')
# plt.plot(x, f1, marker='*', ms=10, label=u'f1值曲线', color='green')
# plt.plot(x, loss, marker='o', ms=10, mec='r', mfc='w', label=u'loss 曲线')
plt.legend()  # 让图例生效
plt.xticks(x, names, rotation=45)
plt.margins(0)
plt.subplots_adjust(bottom=0.15)
plt.xlabel(u"训练次数")  # X轴标签
plt.ylabel("数值")  # Y轴标签
plt.title("准确率图表")  # 标题

plt.show()