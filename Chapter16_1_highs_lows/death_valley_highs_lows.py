import csv
from datetime import datetime
from matplotlib import pyplot as plt

filename = 'death_valley_2014.csv' #文件名
with open(filename) as f: #将结果文件对象存储在f中
    reader = csv.reader(f)
    header_row = next(reader) #返回文件的下一行，由于只调用一次，因此返回第一行

    dates,highs,lows = [],[],[]

    for row in reader:
        try:
            current_date = datetime.strptime(row[0],"%Y-%m-%d")
            high = int(row[1])
            low = int(row[3])
        except ValueError:
            print(current_date,'missing data')
        else:
            dates.append(current_date)
            highs.append(high)
            lows.append(low)

    fig = plt.figure(dpi=128,figsize=(10,6))
    plt.plot(dates,highs,c='red')
    plt.plot(dates,lows,c='blue')
    plt.fill_between(dates,highs,lows,facecolor='green',alpha=0.1)

    plt.title('',fontsize=24)
    plt.xlabel('',fontsize=16)
    #绘制斜的日期标签
    fig.autofmt_xdate()
    plt.ylabel('',fontsize=16)

    #设置每个坐标轴的取值范围
    #plt.axis([1,31,0,100])
    #设置刻度标记的大小
    plt.tick_params(axis='both',which='major',labelsize=16)

    plt.show()