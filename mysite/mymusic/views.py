from django.shortcuts import render
from django.http import HttpResponse
import json
import codecs
import os
import sys
import re
import requests
import urllib
from PIL import Image
from scipy.stats import skew
import numpy


def get_song_list(keyword):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    keyword = urllib.parse.quote(keyword)
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?aggr=1&cr=1&p=1&n=20&w=%s' % keyword
    response = requests.get(url, headers=headers).text.encode(
        'gbk', 'ignore').decode('gbk').split('callback')[-1].strip('()')
    response = json.loads(response)
    return response['data']['song']


def print_info(songs):
    for num, song in enumerate(songs):
        songname = song['songname']
        singer_length = len(song['singer'])
        singers = []
        for i in range(singer_length):
            singers.append(song['singer'][i]['name'])
        singers = ('/').join(singers)
        try:
            media_mid = song['media_mid']
            album_name = song['albumname']
            time = song['interval']
            m, s = divmod(time, 60)
            time = "%02d:%02d" % (m, s)
            print(num,'歌曲名字：',songname,'作者：' ,singers, '专辑：',album_name, '时长：',time)
        except KeyError as e:
            pass

def get_mp3_url(songs,num):
    try:
        media_mid = songs['list'][num]['media_mid']
        url_1 = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&cid=205361747&songmid=%s&filename=C400%s.m4a&guid=6800588318' % (media_mid,media_mid)
        response = requests.get(url_1).json()
        #print(response)
        vkey= response['data']['items'][0]['vkey']
        #print("vkey=", vkey)
        if vkey and vkey != 'songinfo size error':
            url_2 = 'http://dl.stream.qqmusic.qq.com/C400%s.m4a?vkey=%s&guid=6800588318&uin=0&fromtag=66' % (media_mid,vkey)
            #print(media_mid, vkey)
            return url_2
    except KeyError as e:
        return None

def download_mp3(url,filename):
    abspath = os.path.abspath('.')  # 获取绝对路径
    os.chdir(abspath)
    response = requests.get(url).content
    urllib.request.urlretrieve(url, abspath+'\\Music\\src\\assets\\Crawl\\{}.mp3'.format(filename))
    path = os.path.join(abspath+'\\Music\\src\\assets\\Crawl\\',filename)
    #with open(filename + '.mp4', 'wb') as f:
        #f.write(response)
    print('下载完毕,可以在%s   路径下查看' % path + '.mp3')


def download_png(albummid, songname):
    url = 'https://y.gtimg.cn/music/photo_new/T002R300x300M000'+albummid+'.jpg?max_age=2592000'
    r = requests.request('get', url).content
    abspath = os.path.abspath('.')  # 获取绝对路径
    os.chdir(abspath)
    path = os.path.join(abspath+'/Music/src/assets/Crawl/', songname)
    with open(abspath+'\\Music\\src\\assets\\Crawl\\'+songname + '.png', 'wb') as f:
        f.write(r)
        print('下载完毕,可以在%s   路径下查看' % path + '.png')


def download_lyric(musicid,songmid,songname):
    abspath = os.path.abspath('.')  # 获取绝对路径
    os.chdir(abspath)
    path = os.path.join(abspath, songname)
    url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?nobase64=1&musicid='+musicid+'&callback=jsonp1&g_tk=5381&jsonpCallback=jsonp1&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
    header = {
    'user-agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'referer':'https://y.qq.com/n/yqq/song/{}.html'.format(songmid)
    }
    paramters = {
    'nobase64':'1',
    'callback':'jsonp1',
    'g_tk':'5381',
    'jsonpCallback':'jsonp1',
    'loginUin':'0',
    'hostUin':'0',
    'format':'jsonp',
    'inCharset':'utf8',
    'outCharset':'utf-8',
    'notice':'0',
    'platform':'yqq',
    'needNewCode':'0'
    }
    html = requests.get(url=url,params=paramters,headers=header)
    res = json.loads(html.text.lstrip('jsonp1(').rstrip(')'))
    lyric = json.loads(html.text.lstrip('jsonp1(').rstrip(')'))['lyric']
    dr1 = re.compile(r'&#\d.;',re.S)
    dr2 = re.compile(r'[\d+]',re.S)
    dd = dr1.sub(r'',lyric)
    dd = dr2.sub(r'\n',dd).replace('\n\n','')
    dd = dd.replace(']','')
    dd = dd.replace('[[', '\n')
    dd = dd.replace('[', '\n')
    with open(abspath+'\\Music\\src\\assets\\Crawl\\{}.txt'.format(songname), 'a', encoding='utf-8') as fp:
        fp.write(dd)
        print('下载完毕,可以在%s   路径下查看' % path + '.txt')


def get_crawl(request):
    #print("success")
    name = request.POST.get("input", "")
    print(name)
    songs = get_song_list(name)
    if songs['totalnum'] == 0:
        print('没有搜索结果，请换个关键字')
    else:
        # print_info(songs['list'])
        # print(len(songs['list']))
        # num = input('请输入需要下载的歌曲，输入左边对应数字即可')
        for i in range(len(songs['list'])):
            url = get_mp3_url(songs, i)
            # print(url)
            if not url:
                print('歌曲已下架，找不到下载地址，下载失败')
            else:
                try:
                    songname = songs['list'][i]['songname']
                    albummid = songs['list'][i]['albummid']
                    musicid = str(songs['list'][i]['songid'])
                    songmid = songs['list'][i]['songmid']
                    download_mp3(url, songname)
                    download_png(albummid, songname)
                    download_lyric(musicid, songmid, songname)
                except KeyError as e:
                    pass
    return HttpResponse("Success")


def get_soft_music(request):
    file_list = []
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    # print(path)
    for root, dirctories, files in os.walk(path + "\\Music\\src\\assets\\Soft"):
        for filename in files:
            #filepath = os.path.join(root, filename)
            if filename.endswith(".mp3"):
                file_list.append(filename)
    data = []
    for i in range(len(file_list)):
        url = file_list[i]
        data.append(url)
    #print(json.dumps(data))
    return HttpResponse(json.dumps(data))

def get_noisy_music(request):
    file_list = []
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    # print(path)
    for root, dirctories, files in os.walk(path + "\\Music\\src\\assets\\Noisy"):
        for filename in files:
            #filepath = os.path.join(root, filename)
            if filename.endswith(".mp3"):
                file_list.append(filename)
    data = []
    for i in range(len(file_list)):
        url = file_list[i]
        data.append(url)
    #print(json.dumps(data))
    return HttpResponse(json.dumps(data))


def get_crawl_music(request):
    file_list = []
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    # print(path)
    for root, dirctories, files in os.walk(path + "\\Music\\src\\assets\\Crawl"):
        for filename in files:
            #filepath = os.path.join(root, filename)
            if filename.endswith(".mp3"):
                file_list.append(filename)
    data = []
    for i in range(len(file_list)):
        url = file_list[i]
        data.append(url)
    #print(json.dumps(data))
    return HttpResponse(json.dumps(data))


def get_soft_image(request):
    file_list = []
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    # print(path)
    for root, dirctories, files in os.walk(path + "\\Music\\src\\assets\\Soft"):
        for filename in files:
            # print("xx", filename)
            #filepath = os.path.join(root, filename)
            if filename.endswith(".png"):
                file_list.append(filename)
    data = []
    for i in range(len(file_list)):
        url = file_list[i]
        data.append(url)
    #print(data)
    return HttpResponse(json.dumps(data))

def get_noisy_image(request):
    file_list = []
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    # print(path)
    for root, dirctories, files in os.walk(path + "\\Music\\src\\assets\\Noisy"):
        for filename in files:
            # print("xx", filename)
            #filepath = os.path.join(root, filename)
            if filename.endswith(".png"):
                file_list.append(filename)
    data = []
    for i in range(len(file_list)):
        url = file_list[i]
        data.append(url)
    #print(data)
    return HttpResponse(json.dumps(data))


def get_crawl_image(request):
    file_list = []
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    # print(path)
    for root, dirctories, files in os.walk(path + "\\Music\\src\\assets\\Crawl"):
        for filename in files:
            # print("xx", filename)
            #filepath = os.path.join(root, filename)
            if filename.endswith(".png"):
                file_list.append(filename)
    data = []
    for i in range(len(file_list)):
        url = file_list[i]
        data.append(url)
    #print(data)
    return HttpResponse(json.dumps(data))

def get_soft_txt(request):
    file_list = []
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    # print(path)
    for root, dirctories, files in os.walk(path+"\\Music\\src\\assets\\Soft"):
        for filename in files:
            filepath = os.path.join(root, filename)
            if filepath.endswith(".txt"):
                file_list.append(filepath)
    # print(file_list)
    # print(len(file_list))
    data = []
    print("ok")
    for i in range(len(file_list)):
        url = file_list[i]
        # print(url)
        f = codecs.open(url, "r", "UTF-8")
        line = f.readline()
        line = line[:-1]
        lines = str(line)
        while line:
            line = f.readline()
            line = line[:-1]
            lines += str(line)
        f.close()
        data.append(lines)
    # print(data, len(data))
    return HttpResponse(json.dumps(data))

def get_noisy_txt(request):
    file_list = []
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    # print(path)
    for root, dirctories, files in os.walk(path + "\\Music\\src\\assets\\Noisy"):
        for filename in files:
            filepath = os.path.join(root, filename)
            if filepath.endswith(".txt"):
                file_list.append(filepath)
    data = []
    print("ok")
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    for i in range(len(file_list)):
        url = file_list[i]
        f = codecs.open(url, "r", "UTF-8")
        line = f.readline()
        line = line[:-1]
        lines = str(line)
        while line:
            line = f.readline()
            line = line[:-1]
            lines += str(line)
        f.close()
        data.append(lines)
    #print(data, len(data))
    return HttpResponse(json.dumps(data))


def get_crawl_txt(request):
    file_list = []
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    # print(path)
    for root, dirctories, files in os.walk(path + "\\Music\\src\\assets\\Crawl"):
        for filename in files:
            filepath = os.path.join(root, filename)
            if filepath.endswith(".txt"):
                file_list.append(filepath)
    data = []
    print("ok")
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    for i in range(len(file_list)):
        url = file_list[i]
        f = codecs.open(url, "r", "UTF-8")
        line = f.readline()
        line = line[:-1]
        lines = str(line)
        while line:
            line = f.readline()
            line = line[:-1]
            lines += str(line)
        f.close()
        data.append(lines)
    #print(data, len(data))
    return HttpResponse(json.dumps(data))


def upload_image1(request):
    # url = request.POST.get("url", "")
    # id = request.POST.get("id", "")
    img = request.FILES.get("file")
    print(img)
    abspath = os.path.abspath('.')  # 获取绝对路径
    os.chdir(abspath)
    f = open(abspath + '\\Music\\src\\assets\\Image\\' + 'test' + '.png', 'wb')
    for chunk in img.chunks():
        f.write(chunk)
    # with open(abspath + '\\Music\\src\\assets\\Image\\' + img.name + '.png', 'wb') as f:
    #     f.write(file_obj)
    # response = requests.get(url[5:]).content
    # urllib.request.urlretrieve(url, abspath + '\\Music\\src\\assets\\Image\\' + id + '.png')
    return HttpResponse(request)


def upload_image2(request):
    # url = request.POST.get("url", "")
    # id = request.POST.get("id", "")
    img = request.FILES.get("file")
    print(img)
    abspath = os.path.abspath('.')  # 获取绝对路径
    os.chdir(abspath)
    f = open(abspath + '\\Music\\src\\assets\\Image\\' + '1' + '.png', 'wb')
    for chunk in img.chunks():
        f.write(chunk)
    # with open(abspath + '\\Music\\src\\assets\\Image\\' + img.name + '.png', 'wb') as f:
    #     f.write(file_obj)
    # response = requests.get(url[5:]).content
    # urllib.request.urlretrieve(url, abspath + '\\Music\\src\\assets\\Image\\' + id + '.png')
    return HttpResponse(request)


def add_watermark(request):
    abspath = os.path.abspath('.')  # 获取绝对路径
    os.chdir(abspath)
    img = Image.open(abspath + '\\Music\\src\\assets\\Image\\' + 'test.png')
    width = img.size[0]
    height = img.size[1]
    img_array = img.load()

    watermark = Image.open(abspath + '\\Music\\src\\assets\\Image\\' + '1.png')
    w = watermark.size[0]
    h = watermark.size[1]
    wm_array = watermark.load()

    if width < w:
        minw = width
    else:
        minw = w
    if height < h:
        minh = height
    else:
        minh = h

    for i in range(minw):
        for j in range(minh):
            new_array = []
            for k in range(3):
                img_bin = bin(img_array[i, j][k])
                wm_add = round(wm_array[i, j][k] / 85)
                # temp = wm_array[i,j][k]//85
                # print(img_bin, wm_add)
                if wm_add == 0:
                    wm_str = '00'
                elif wm_add == 1:
                    wm_str = '01'
                elif wm_add == 2:
                    wm_str = '10'
                else:
                    wm_str = '11'
                cut = str(img_bin)[:-2]
                # print(cut, img_bin)
                temp = int((cut + wm_str), 2)
                # print(temp)
                new_array.append(temp)
            # print(img_array[i,j], tuple(new_array))
            img_array[i, j] = tuple(new_array)
    img.save(abspath + '\\Music\\src\\assets\\Image\\' + 'new.png')
    for i in range(minw):
        for j in range(minh):
            new_array = []
            for k in range(3):
                wm_add = bin(img_array[i, j][k])[-2:]
                # print(wm_add)
                # wm_now = bin(wm_array[i,j][k])[8:]
                if wm_add == '00':
                    wm_str = 0
                elif wm_add == '01':
                    wm_str = 1
                elif wm_add == '10':
                    wm_str = 2
                else:
                    wm_str = 3
                wm_old = wm_str * 85
                new_array.append(wm_old)
            # print(wm_array[i,j], tuple(new_array))
            wm_array[i, j] = tuple(new_array)
    watermark.save(abspath + '\\Music\\src\\assets\\Image\\' + 'wm.png')
    return HttpResponse("Success")


def upload_image(request):
    img = request.FILES.get("file")
    print(img)
    abspath = os.path.abspath('.')  # 获取绝对路径
    os.chdir(abspath)
    f = open(abspath + '\\Music\\src\\assets\\Similarity\\' + '1' + '.png', 'wb')
    for chunk in img.chunks():
        f.write(chunk)
    return HttpResponse(request)


def upload_others(request):
    img = request.FILES.get("file")
    print(img)
    abspath = os.path.abspath('.')  # 获取绝对路径
    os.chdir(abspath)
    f = open(abspath + '\\Music\\src\\assets\\Similarity\\' + img.name + '.png', 'wb')
    for chunk in img.chunks():
        f.write(chunk)
    return HttpResponse(request)


def detect_similarity(request):
    abspath = os.path.abspath('.')  # 获取绝对路径
    os.chdir(abspath)
    img = Image.open(abspath + '\\Music\\src\\assets\\Similarity\\' + '1.png')
    width = img.size[0]
    height = img.size[1]
    img_array = img.load()
    r_o = []
    g_o = []
    b_o = []

    file_list = []
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    for root, dirctories, files in os.walk(path + "\\Music\\src\\assets\\Similarity"):
        for filename in files:
            #print("xx", filename)
            filepath = os.path.join(root, filename)
            if filename.endswith(".png") and filename != '1.png' and filename != 'similar.png':
                file_list.append(filepath)
                # print(filename)
    # print(file_list)

    for i in range(width):
        for j in range(height):
            r_o.append(img_array[i, j][0])
            g_o.append(img_array[i, j][1])
            b_o.append(img_array[i, j][2])

    mean_ro = numpy.mean(r_o)
    mean_go = numpy.mean(g_o)
    mean_bo = numpy.mean(b_o)
    var_ro = numpy.var(r_o)
    var_go = numpy.var(g_o)
    var_bo = numpy.var(b_o)
    skew_ro = skew(r_o)
    skew_go = skew(g_o)
    skew_bo = skew(b_o)

    vector_o = [mean_ro, mean_go, mean_bo, var_ro, var_go, var_bo,
                skew_ro, skew_go, skew_bo]
    # print("origin: ", vector_o)

    # print(numpy.mean(r), numpy.mean(g), numpy.mean(b))
    # print(numpy.var(r), numpy.var(g), numpy.var(b))
    # print(skew(r), skew(g), skew(b))
    flag = 0
    for p in file_list:
        img_new = Image.open(p)
        width = img_new.size[0]
        height = img_new.size[1]
        new_array = img_new.load()
        r_n = []
        g_n = []
        b_n = []
        # print(r_n)
        try:
            for i in range(width):
                for j in range(height):
                    r_n.append(new_array[i, j][0])
                    g_n.append(new_array[i, j][1])
                    b_n.append(new_array[i, j][2])

            mean_rn = numpy.mean(r_n)
            mean_gn = numpy.mean(g_n)
            mean_bn = numpy.mean(b_n)
            var_rn = numpy.var(r_n)
            var_gn = numpy.var(g_n)
            var_bn = numpy.var(b_n)
            skew_rn = skew(r_n)
            skew_gn = skew(g_n)
            skew_bn = skew(b_n)

            vector_n = [mean_rn, mean_gn, mean_bn,
                        var_rn, var_gn, var_bn, skew_rn, skew_gn, skew_bn]
        except:
            print(i, j)

        if flag == 0:
            num = mean_ro * mean_rn + mean_go * mean_gn + mean_bo * mean_bn + var_ro * var_rn + var_go * var_gn + var_bo * var_bn + skew_ro * skew_rn + skew_go * skew_gn + skew_bo * skew_bn
            den1 = pow((mean_ro * mean_ro + mean_go * mean_go + mean_bo * mean_bo + var_ro * var_ro + var_go * var_go + var_bo * var_bo + skew_ro * skew_ro + skew_go * skew_go + skew_bo * skew_bo), 0.5)
            den2 = pow((mean_rn * mean_rn + mean_gn * mean_gn + mean_bn * mean_bn + var_rn * var_rn + var_gn * var_gn + var_bn * var_bn + skew_rn * skew_rn + skew_gn * skew_gn + skew_bn * skew_bn), 0.5)
            max = num / (den1 * den2)
            flag = 1
            index = file_list.index(p)
        else:
            num = mean_ro * mean_rn + mean_go * mean_gn + mean_bo * mean_bn + var_ro * var_rn + var_go * var_gn + var_bo * var_bn + skew_ro * skew_rn + skew_go * skew_gn + skew_bo * skew_bn
            den1 = pow((mean_ro * mean_ro + mean_go * mean_go + mean_bo * mean_bo + var_ro * var_ro + var_go * var_go + var_bo * var_bo + skew_ro * skew_ro + skew_go * skew_go + skew_bo * skew_bo), 0.5)
            den2 = pow((mean_rn * mean_rn + mean_gn * mean_gn + mean_bn * mean_bn + var_rn * var_rn + var_gn * var_gn + var_bn * var_bn + skew_rn * skew_rn + skew_gn * skew_gn + skew_bn * skew_bn), 0.5)
            temp = num / (den1 * den2)
            if temp > max:
                max = temp
                index = file_list.index(p)
        # print(file_list.index(p), vector_n, max)
    # print(index)
    similar = Image.open(file_list[index])
    similar.save(abspath + '\\Music\\src\\assets\\Similarity\\' + 'similar.png')

    return HttpResponse("Success")
