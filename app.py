#!/usr/bin/env python2
from bottle import *
from utils import *
from upyun import UpYun
import config
import os
import md5
import time
import os.path

# UpYun Bucket Init
bucket = config.bucket
username = config.username
password = config.password
up = UpYun(bucket = bucket, username = username, password = password)

# User Manage
accounts = {'test': 'test', 'test2': 'test2'}
admins = ['test2']

# Bottle Init
app = Bottle()
app_dir = '/jerry'
s_path = os.path.abspath(os.path.dirname(sys.argv[0]))

# Login
@app.post(app_dir + '/login')
def login():
    user = request.forms.get('login')
    passwd = request.forms.get('password')
    if not user or not passwd:
        redirect(app_dir + '/?error=empty')
        return ''
    if user in accounts:
        if accounts[user] == passwd:
            hash = md5.new()
            hash.update(passwd)
            response.set_cookie('login', user)
            response.set_cookie('password', hash.hexdigest())
            redirect(app_dir + '/')
        else:
            redirect(app_dir + '/?error=badpass')
    else:
        redirect(app_dir + '/?error=badpass')
    return ''

# Logout
@app.route(app_dir + '/logout')
def logout():
    response.set_cookie('login', '')
    response.set_cookie('password', '')
    redirect(app_dir + '/')

@app.route('/')
def redirect_home():
    return redirect(app_dir+'/')

# List
@app.route(app_dir + '/')
@view('main')
def list():
    user = request.get_cookie('login') 
    passwd = request.get_cookie('password')
    error = request.GET.get('error')

    isAdmin = True if user in admins else False

    path = request.GET.get('path')
    if not path:
        path = '/'

    columns = []
    rawData = up.getlist(path)
    slist = sorted(rawData, key = lambda k : '%s %s' % (k['type'], k['time']))
    for k in range(len(slist)):
        column = {'id': k}
        column['fname'] = slist[k]['name']
        column['ftype'] = fmttype(slist[k]['type'])
        column['fsize'] = fmtsize(int(slist[k]['size']))
        column['ftime'] = fmttime(slist[k]['time'])
        column['fpath'] = join(path, column['fname'])
        if column['ftype'] == 'folder':
            column['href'] = '?path=' + column['fpath']
        else:
            column['href'] = 'http://%s.b0.upaiyun.com%s' % (bucket, column['fpath'])
        columns.append(column) 

    data = {
        'cwd': path, 'rowinfo': columns, 'login': user, 'pdir': dirname(path), \
        'password': passwd, 'isAdmin': isAdmin, 'error': error, 'app_dir': app_dir, \
    }
    return dict(data=data)

# AddFolder
@app.route(app_dir+'/addfolder')
def addfolder():
    up.mkdir(request.GET.get('path'))
    return None

# Upload
@app.route(app_dir+'/upload', method='POST')
def upload():
    upload_obj = request.files.file_data
    path = request.GET.get('path') + '/'
    fpath = path + upload_obj.filename
    try:
        os.remove('/tmp/mytmp')
    except:
        pass
    try:
        upload_obj.save('/tmp/mytmp')
        with open('/tmp/mytmp') as f:
            up.put(fpath, f)
    except Exception as e:
        print e
    return None

# Delete
@app.route(app_dir+'/delete')
def delete():
    up.delete(request.GET.get('path'))
    return None

# Rename

# Download
@app.route(app_dir+'/download')
def download():
    uri = 'http://%s.b0.upaiyun.com%s' % (bucket, request.GET.get('path'))
    return redirect(uri)

# Load Static Files
@app.route(app_dir+'/img/:filename')
def img_static(filename):
    return static_file(filename, root=s_path+'/views/static/img/')

@app.route(app_dir+'/img/view')
def view_img_static():
    filename = request.GET.get('path')
    return static_file(filename, root=s_path)

@app.route(app_dir+'/thumb')
def view_img_static():
    filename = request.GET.get('path')
    return static_file(filename, root=s_path)

@app.route(app_dir+'/img/icons/:filename')
def icons_static(filename):
    return static_file(filename, root=s_path+'/views/static/img/icons/')

@app.route(app_dir+'/img/fancybox/:filename')
def fancybox_static(filename):
    return static_file(filename, root=s_path+'/views/static/img/fancybox/')

@app.route(app_dir+'/js/:filename')
def js_static(filename):
    return static_file(filename, root=s_path+'/views/static/js/')

@app.route(app_dir+'/css/:filename')
def css_static(filename):
    return static_file(filename, root=s_path+'/views/static/css/')

@app.route(app_dir+'/fonts/:filename')
def css_static(filename):
    return static_file(filename, root=s_path+'/views/static/fonts/')

run(app, host='localhost', port=8070, debug = True)
