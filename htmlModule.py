
#
def get_oddeven(filelist):
    filelist0, filelist1 = [], []
    for i in range(filelist):
        if i % 2 == 0:
            filelist0.append(filelist[i])
        elif i % 2 == 1:
            filelist1.append(filelist[i])
        else:
            Exception('Something went wrong while executing get_oddeven')
    return filelist0, filelist1

