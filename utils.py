import os.path
import time
def join(path, fname):
    if path[-1] == '/':
        return path + fname
    return path + '/' + fname

def dirname(path):
    return os.path.dirname(path)

def fmttime(ftime):
    return time.strftime("%d-%b-%Y %H:%M", time.localtime(int(ftime)))

def fmtsize(fsize, bar = 4):
    if fsize == -1:
        return '-'
    res = '%d' % fsize
    if fsize >= 10**bar:
        fsize /= 1024
        res = '%dK' % fsize
        if fsize >= 10 ** (bar-1):
            fsize /= 1024
            res = '%dM' % fsize
            if fsize >= 10 ** (bar-1):
                fsize /= 1024
                res = '%dG' % fsiz
    return res
    
def fmttype(ftype):
    return 'folder' if ftype == 'F' else 'unknow'
