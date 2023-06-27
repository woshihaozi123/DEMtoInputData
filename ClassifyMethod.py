import numpy as np

def UniformClassify(data, num_bins):
    # num of class
    print('Uniform num of class:', num_bins)

    # UniformClassify
    hist, bins = np.histogram(data, bins=num_bins, range=(min(data), max(data)))

    print("Histogram:", hist)
    print("Bins:", bins)
    return hist, bins


def EqualwidthClassify(data, num_bins):
    # num of class
    print('Num of equal width classes:', num_bins)
    data_range = max(data) - min(data)
    bin_width = data_range / num_bins

    # 计算分类的边界值
    bins = [min(data) + i * bin_width for i in range(num_bins + 1)]

    # 使用等宽法分类
    hist, _ = np.histogram(data, bins=bins)
    groups = np.digitize(data, bins)
    meanvalues=[];
    groupvalues=[];
    for i in range(1,num_bins+1):
        group_data = np.array(data)[groups == i]
        groupmean_value = np.nanmean(group_data)
        meanvalues.append(groupmean_value)
        groupvalues.append(group_data)

    print("Histogram:", hist)
    print("meanvalues:", meanvalues)
    print("Bins:", bins)
    print("groupvalues:", groupvalues)
    return hist, np.array(meanvalues),groupvalues,np.array(bins)


def EqualnumberClassify(sorted_data,num_bins):

    # 使用np.array_split函数对数据进行分类
    split_data = np.array_split(sorted_data, num_bins)

    # 计算每个分类的数量平均值
    hist = np.array([bin.shape[0] for bin in split_data])
    meanvalues = np.array([np.mean(bin) for bin in split_data])

    bins=np.array([bin[0] for bin in split_data])
    bins=np.append(bins, split_data[-1][-1])
    print("Histogram:", hist)
    print("meanvalues:", meanvalues)
    print("Bins:", bins)
    print("groupvalues:", split_data)

    return hist, np.array(meanvalues),split_data,np.array(bins)

