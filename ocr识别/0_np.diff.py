import numpy as np

arr =np.array([[1,2],[3,5]])
diff = np.diff(arr, axis=1)
sum_ = np.sum(arr, axis=1)
print(diff, sum_) # [[1],[2]]
print(np.argmin(sum_))