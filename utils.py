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
    
def fmttype(ftype, filename):
    TEXT_TYPE = ['doc', 'docx', 'txt', 'rtf', 'odf', 'text', 'nfo']
    AUDIO_TYPE = ['aac', 'mp3', 'wav', 'wma', 'm4p', 'flac']
    IMAGE_TYPE = ['bmp', 'gif', 'jpg', 'jpeg', 'png','svg']
    IMAGESOURCE_TYPE = ['eps', 'ico', 'psd', 'psp', 'raw', 'tga', 'tif', 'tiff', 'svg']
    VIDEO_TYPE = [
        'mv4', 'bup', 'mkv', 'ifo', 'flv', 'vob', '3g2', 'bik', 'xvid', 'divx',
        'wmv', 'avi', '3gp', 'mp4', 'mov', '3gpp', '3gp2', 'swf', 'mpg', 'mpeg'
    ]
    ARCHIVE_TYPE = ['7z', 'dmg', 'rar', 'sit', 'zip', 'bzip', 'gz', 'tar', 'ace']
    EXEC_TYPE = ['exe', 'msi', 'mse']
    SCRIPT_TYPE = [
        'js', 'html', 'htm', 'xhtml', 'jsp', 'asp', 'aspx', 'php', 'xml',
        'css', 'py', 'bat', 'sh', 'rb', 'java'
    ]
    
    base = {"text":TEXT_TYPE, "audio":AUDIO_TYPE, "image":IMAGE_TYPE, "imagesource":IMAGESOURCE_TYPE,
            "video":VIDEO_TYPE, "archive":ARCHIVE_TYPE, "exec": EXEC_TYPE, "script":SCRIPT_TYPE,
            "pdf":"pdf"}

    if ftype == 'F':
        return 'folder'

    extension = filename.split('.')[-1]
    for k in base: 
        v = base[k]
        if extension in v:
            return k
    return "unknow"

