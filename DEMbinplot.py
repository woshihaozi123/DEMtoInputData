import numpy as np
import matplotlib.pyplot as plt

def Elevationgroupbarplot(categories,hist,meanvalue,bins,titlestr):
    # Set the width of the bars
    bar_width = 0.5

    # Create x-axis coordinates
    x = np.arange(len(categories))
    colors = ['red', 'green', 'blue', 'orange']
    # Plot the bar chart
    for m, n in zip(x, hist):
        plt.bar(m, n, width=bar_width,color =colors[m])

    plt.text(-0.7,  hist[0]+ 0.1, 'mean:', ha='center', va='bottom')
    plt.text(-0.7, hist[0] + 0.05, 'range:', ha='center', va='bottom')
    for m, n, i in zip(x, hist, meanvalue):

        plt.text(m + 0.1, n + 0.1, str(i)+'m', ha='center', va='bottom')

    for m, n, i in zip(x, hist, bins):
        plt.text(m + 0.1, n + 0.05, str(bins[m])+'-'+str(bins[m+1])+'m', ha='center', va='bottom')

    # Add axis labels and legend
    plt.ylim(0, 0.6)
    plt.xlim(-1, 3.8)
    plt.xlabel('Categories')
    plt.ylabel('Frequency')
    plt.xticks(x, categories)
    #plt.legend()
    plt.title(titlestr)
    # Display the chart

    # 保存图像为 JPEG 格式，设置 DPI 值为 300
    plt.savefig(titlestr.replace(" ", "_")+'.png',  bbox_inches= 'tight',dpi=300)
    plt.show()


def EqualwidthbarPlot(data, ttbins, bin_width,fraction,meanvalue,titlestr):
    # elevation class bins
    print('ttbins:', ttbins)
    # bin width
    print('binbarwidth:', bin_width)
    data_range = max(data) - min(data)
    num_bins=int(data_range/bin_width)+1


    # 计算分类的边界值
    bins = [int(min(data)) + i * bin_width for i in range(num_bins + 1)]

    # 使用等宽法分类
    hist, _ = np.histogram(data, bins=bins)

    # Set the width of the bars
    bar_width = bin_width/2

    # Create x-axis coordinates
    x = np.arange(int(min(data)),int(min(data))+num_bins*bin_width,bin_width)
    print('bins:', bins)
    print('x:', x)
    print('x length:', x.shape[0])
    print('hist length:', hist.shape[0])
    colors = ['red', 'green', 'blue', 'orange']
    categories = ['elevation1', 'elevation2', 'elevation3', 'elevation4']
    #plt.text(140, 600, 'Mean:', ha='center', va='bottom')
    #plt.text(140, 500, 'Range:', ha='center', va='bottom')
    for i in range(len(colors)):

        x1 = x[np.logical_and((x >= ttbins[i]), (x <= ttbins[i+1]))]
        hist1 =hist [np.logical_and((x>= ttbins[i]) , (x <= ttbins[i + 1]))]
        print('x1',x1)
        # Plot the bar chart
        for m, n in zip(x1, hist1):
                 plt.bar(m + bar_width, n, width=bar_width, color=colors[i])

        #plt.text(meanvalue[i] , 600, str(meanvalue[i]) + 'm', ha='center', va='bottom')
        #plt.text(meanvalue[i], 500, str(ttbins[i]) + '-' + str(ttbins[i + 1]) + 'm', ha='center', va='bottom')


    plt.xlim(int(min(data)),int(min(data))+num_bins)
    plt.xlabel('DEM(m)')
    plt.ylabel('Frequency')

    xticks= np.array([min(data) + i * 40 for i in range(int(data_range / 40) + 1)])
    xticks= np.append(xticks, max(data))

    handles1 = plt.bar([0], [0], color='red')
    handles2 = plt.bar([0], [0], color='green')
    handles3 = plt.bar([0], [0], color='blue')
    handles4 = plt.bar([0], [0], color='orange')
    labels = categories
    plt.legend([handles1, handles2,handles3, handles4], labels)

    plt.xticks(xticks)
    # plt.legend()
    plt.title(titlestr)

    plt.savefig(titlestr.replace(" ", "_") + '.png',  bbox_inches= 'tight',dpi=300)
    plt.show()


