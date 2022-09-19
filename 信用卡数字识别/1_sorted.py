import numpy as np
np.random.seed(0)

arr = np.random.permutation(9).reshape((3,3))
print(arr)

lst = arr.tolist()
print(lst)  # [[7, 2, 1], [4, 8, 6], [3, 0, 5]]

lst_sort = sorted(lst, key = lambda x: x[0]) # 以lst中的每个元素中的第0个为标准从小到大排序
print(lst_sort) # [[3, 0, 5], [4, 8, 6], [7, 2, 1]]