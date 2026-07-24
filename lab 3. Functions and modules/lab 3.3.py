def time_series_cv(n_samples, window_type, train_size, test_size, step):
    start = 0
    while True:
        if window_type == 'expanding':
            train_start = 0
            train_stop = train_size + start
        else:
            train_start = start
            train_stop = train_size + start
        test_start = train_stop
        test_stop = test_start + test_size
        if test_stop > n_samples:
            break
        yield slice(train_start, train_stop), slice(test_start, test_stop)
        start += step
params = input().split()
n_samples = int(params[0])
window_type = params[1]
train_size = int(params[2])
test_size = int(params[3])
step = int(params[4])
cv = time_series_cv(n_samples, window_type, train_size, test_size, step)
for train_slice, test_slice in cv:
    print(f"{train_slice.start} {train_slice.stop} {test_slice.start} {test_slice.stop}")