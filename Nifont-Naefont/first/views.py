from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import os
import shutil
from datetime import datetime
import time
from io import BytesIO
from PIL import Image
import re
import json
import urllib.request
import argparse
import base64

import sys
sys.path.insert(0, '/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/')

import train_handwrite
import make_font

array_uni = ['AC00', 'AC1D', 'AC3A', 'AC57', 'AC74', 'AC91', 'ACAE', 'ACCB', 'ACE8', 'AD05', 'AD22', 'AD3F', 'AD5C', 'AD79', 'AD96', 'ADB3', 'ADD0', 'ADED', 'AE0A', 'AE27', 'AE44', 'AE61', 'AE7E', 'AE9B',
         'AEB8', 'AED5', 'AEF2', 'AF0F', 'AF10', 'AF2D', 'AF4A', 'AF67', 'AF84', 'AFA1', 'AFBE', 'AFDB', 'AFF8', 'B015', 'B032', 'B04F', 'B06C', 'B089', 'B0A6', 'B0C3', 'B0E0', 'B0FD', 'B11A', 'B137', 'B154', 'B171', 
         'B18E', 'B1AB', 'B1C8', 'B1E5', 'B202', 'B21F', 'B220', 'B23D', 'B25A', 'B277', 'B294', 'B2B1', 'B2CE', 'B2EB', 'B308', 'B325', 'B342', 'B35F', 'B37C', 'B399', 'B3B6', 'B3D3', 'B3F0', 'B40D', 'B42A', 'B447',
         'B464', 'B481', 'B49E', 'B4BB', 'B4D8', 'B4F5', 'B512', 'B52F', 'B530', 'B54D', 'B56A', 'B587', 'B5A4', 'B5C1', 'B5DE', 'B5FB', 'B618', 'B635', 'B652', 'B66F', 'B68C', 'B6A9', 'B6C6', 'B6E3', 'B700', 'B71D',
         'B73A', 'B757', 'B774', 'B791', 'B7AE', 'B7CB', 'B7E8', 'B805', 'B822', 'B83F', 'B840', 'B85D', 'B87A', 'B897', 'B8B4', 'B8D1', 'B8EE', 'B90B', 'B928', 'B945', 'B962', 'B97F', 'B99C', 'B9B9', 'B9D6', 'B9F3',
         'BA10', 'BA2D', 'BA4A', 'BA67', 'BA84', 'BAA1', 'BABE', 'BADB', 'BAF8', 'BB15', 'BB32', 'BB4F', 'BB50', 'BB6D', 'BB8A', 'BBA7', 'BBC4', 'BBE1', 'BBFE', 'BC1B', 'BC38', 'BC55', 'BC72', 'BC8F', 'BCAC', 'BCC9',
         'BCE6', 'BD03', 'BD20', 'BD3D', 'BD5A', 'BD77', 'BD94', 'BDB1', 'BDCE', 'BDEB', 'BE08', 'BE25', 'BE42', 'BE5F', 'BE60', 'BE7D', 'BE9A', 'BEB7', 'BED4', 'BEF1', 'BF0E', 'BF2B', 'BF48', 'BF65', 'BF82', 'BF9F', 
         'BFBC', 'BFD9', 'BFF6', 'C013', 'C030', 'C04D', 'C06A', 'C087', 'C0A4', 'C0C1', 'C0DE', 'C0FB', 'C118', 'C135', 'C152', 'C16F', 'C170', 'C18D', 'C1AA', 'C1C7', 'C1E4', 'C201', 'C21E', 'C23B', 'C258', 'C275', 
         'C292', 'C2AF', 'C2CC', 'C2E9', 'C306', 'C323', 'C340', 'C35D', 'C37A', 'C397', 'C3B4', 'C3D1', 'C3EE', 'C40B', 'C428', 'C445', 'C462', 'C47F', 'C480', 'C49D', 'C4BA', 'C4D7', 'C4F4', 'C511', 'C52E', 'C54B', 
         'C568', 'C585', 'C5A2', 'C5BF', 'C5DC', 'C5F9', 'C616', 'C633', 'C650', 'C66D', 'C68A', 'C6A7', 'C6C4', 'C6E1', 'C6FE', 'C71B', 'C738', 'C755', 'C772', 'C78F', 'C790', 'C7AD', 'C7CA', 'C7E7', 'C804', 'C821', 
         'C83E', 'C85B', 'C878', 'C895', 'C8B2', 'C8CF', 'C8EC', 'C909', 'C926', 'C943', 'C960', 'C97D', 'C99A', 'C9B7', 'C9D4', 'C9F1', 'CA0E', 'CA2B', 'CA48', 'CA65', 'CA82', 'CA9F', 'CAA0', 'CABD', 'CADA', 'CAF7', 
         'CB14', 'CB31', 'CB4E', 'CB6B', 'CB88', 'CBA5', 'CBC2', 'CBDF', 'CBFC', 'CC19', 'CC36', 'CC53', 'CC70', 'CC8D', 'CCAA', 'CCC7', 'CCE4', 'CD01', 'CD1E', 'CD3B', 'CD58', 'CD75', 'CD92', 'CDAF', 'CDB0', 'CDCD', 
         'CDEA', 'CE07', 'CE24', 'CE41', 'CE5E', 'CE7B', 'CE98', 'CEB5', 'CED2', 'CEEF', 'CF0C', 'CF29', 'CF46', 'CF63', 'CF80', 'CF9D', 'CFBA', 'CFD7', 'CFF4', 'D011', 'D02E', 'D04B', 'D068', 'D085', 'D0A2', 'D0BF', 
         'D0C0', 'D0DD', 'D0FA', 'D117', 'D134', 'D151', 'D16E', 'D18B', 'D1A8', 'D1C5', 'D1E2', 'D1FF', 'D21C', 'D239', 'D256', 'D273', 'D290', 'D2AD', 'D2CA', 'D2E7', 'D304', 'D321', 'D33E', 'D35B', 'D378', 'D395', 
         'D3B2', 'D3CF', 'D3D0', 'D3ED', 'D40A', 'D427', 'D444', 'D461', 'D47E', 'D49B', 'D4B8', 'D4D5', 'D4F2', 'D50F', 'D52C', 'D549', 'D566', 'D583', 'D5A0', 'D5BD', 'D5DA', 'D5F7', 'D614', 'D631', 'D64E', 'D66B', 
         'D688', 'D6A5', 'D6C2', 'D6DF', 'D6E0', 'D6FD', 'D71A', 'D737', 'D754', 'D771', 'D78E']

def home(request):
    context = {
    }
    return render(request, 'first/home.html', context)

def about(request):
    context = {
    }
    return render(request, 'first/about.html', context)

def start(request):
    return render(request, 'first/canvas_home.html')

def loading(request):
        if request.method == 'POST':
                print("run")

        return render(request, 'first/loading.html')

def run(request):
    train_handwrite.run()
    return render(request, 'first/select.html')

def run_font1(request):
    make_font.run1()
    return render(request, 'first/result.html')

def run_font2(request):
    make_font.run2()
    return render(request, 'first/result.html')

def run_font3(request):
    make_font.run3()
    return render(request, 'first/result.html')

def run_font4(request):
    make_font.run4()
    return render(request, 'first/result.html')

def run_font5(request):
    make_font.run5()
    return render(request, 'first/result.html')

def canvas0(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[0] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas0.html')
def canvas1(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[1] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas1.html')
def canvas2(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[2] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas2.html')
def canvas3(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[3] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas3.html')
def canvas4(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[4] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas4.html')
def canvas5(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[5] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas5.html')
def canvas6(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[6] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas6.html')
def canvas7(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[7] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas7.html')
def canvas8(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[8] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas8.html')
def canvas9(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[9] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas9.html')
def canvas10(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[10] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas10.html')
def canvas11(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[11] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas11.html')
def canvas12(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[12] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas12.html')
def canvas13(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[13] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas13.html')
def canvas14(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[14] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas14.html')
def canvas15(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[15] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas15.html')
def canvas16(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[16] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas16.html')
def canvas17(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[17] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas17.html')
def canvas18(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[18] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas18.html')
def canvas19(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[19] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas19.html')
def canvas20(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[20] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas20.html')
def canvas21(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[21] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas21.html')
def canvas22(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[22] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas22.html')
def canvas23(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[23] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas23.html')
def canvas24(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[24] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas24.html')
def canvas25(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[25] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas25.html')
def canvas26(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[26] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas26.html')
def canvas27(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[27] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas27.html')
def canvas28(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[28] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas28.html')
def canvas29(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[29] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas29.html')
def canvas30(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[30] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas30.html')
def canvas31(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[31] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas31.html')
def canvas32(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[32] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas32.html')
def canvas33(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[33] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas33.html')
def canvas34(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[34] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas34.html')
def canvas35(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[35] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas35.html')
def canvas36(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[36] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas36.html')
def canvas37(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[37] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas37.html')
def canvas38(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[38] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas38.html')
def canvas39(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[39] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas39.html')
def canvas40(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[40] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas40.html')
def canvas41(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[41] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas41.html')
def canvas42(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[42] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas42.html')
def canvas43(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[43] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas43.html')
def canvas44(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[44] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas44.html')
def canvas45(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[45] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas45.html')
def canvas46(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[46] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas46.html')
def canvas47(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[47] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas47.html')
def canvas48(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[48] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas48.html')
def canvas49(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[49] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas49.html')
def canvas50(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[50] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas50.html')
def canvas51(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[51] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas51.html')
def canvas52(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[52] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas52.html')
def canvas53(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[53] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas53.html')
def canvas54(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[54] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas54.html')
def canvas55(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[55] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas55.html')
def canvas56(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[56] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas56.html')
def canvas57(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[57] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas57.html')
def canvas58(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[58] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas58.html')
def canvas59(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[59] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas59.html')
def canvas60(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[60] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas60.html')
def canvas61(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[61] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas61.html')
def canvas62(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[62] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas62.html')
def canvas63(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[63] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas63.html')
def canvas64(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[64] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas64.html')
def canvas65(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[65] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas65.html')
def canvas66(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[66] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas66.html')
def canvas67(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[67] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas67.html')
def canvas68(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[68] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas68.html')
def canvas69(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[69] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas69.html')
def canvas70(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[70] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas70.html')
def canvas71(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[71] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas71.html')
def canvas72(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[72] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas72.html')
def canvas73(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[73] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas73.html')
def canvas74(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[74] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas74.html')
def canvas75(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[75] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas75.html')
def canvas76(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[76] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas76.html')
def canvas77(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[77] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas77.html')
def canvas78(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[78] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas78.html')
def canvas79(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[79] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas79.html')
def canvas80(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[80] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas80.html')
def canvas81(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[81] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas81.html')
def canvas82(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[82] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas82.html')
def canvas83(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[83] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas83.html')
def canvas84(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[84] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas84.html')
def canvas85(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[85] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas85.html')
def canvas86(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[86] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas86.html')
def canvas87(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[87] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas87.html')
def canvas88(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[88] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas88.html')
def canvas89(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[89] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas89.html')
def canvas90(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[90] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas90.html')
def canvas91(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[91] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas91.html')
def canvas92(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[92] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas92.html')
def canvas93(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[93] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas93.html')
def canvas94(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[94] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas94.html')
def canvas95(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[95] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas95.html')
def canvas96(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[96] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas96.html')
def canvas97(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[97] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas97.html')
def canvas98(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[98] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas98.html')
def canvas99(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[99] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas99.html')
def canvas100(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[100] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas100.html')
def canvas101(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[101] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas101.html')
def canvas102(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[102] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas102.html')
def canvas103(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[103] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas103.html')
def canvas104(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[104] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas104.html')
def canvas105(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[105] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas105.html')
def canvas106(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[106] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas106.html')
def canvas107(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[107] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas107.html')
def canvas108(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[108] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas108.html')
def canvas109(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[109] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas109.html')
def canvas110(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[110] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas110.html')
def canvas111(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[111] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas111.html')
def canvas112(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[112] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas112.html')
def canvas113(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[113] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas113.html')
def canvas114(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[114] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas114.html')
def canvas115(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[115] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas115.html')
def canvas116(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[116] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas116.html')
def canvas117(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[117] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas117.html')
def canvas118(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[118] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas118.html')
def canvas119(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[119] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas119.html')
def canvas120(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[120] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas120.html')
def canvas121(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[121] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas121.html')
def canvas122(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[122] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas122.html')
def canvas123(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[123] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas123.html')
def canvas124(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[124] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas124.html')
def canvas125(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[125] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas125.html')
def canvas126(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[126] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas126.html')
def canvas127(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[127] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas127.html')
def canvas128(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[128] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas128.html')
def canvas129(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[129] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas129.html')
def canvas130(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[130] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas130.html')
def canvas131(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[131] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas131.html')
def canvas132(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[132] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas132.html')
def canvas133(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[133] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas133.html')
def canvas134(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[134] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas134.html')
def canvas135(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[135] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas135.html')
def canvas136(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[136] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas136.html')
def canvas137(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[137] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas137.html')
def canvas138(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[138] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas138.html')
def canvas139(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[139] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas139.html')
def canvas140(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[140] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas140.html')
def canvas141(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[141] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas141.html')
def canvas142(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[142] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas142.html')
def canvas143(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[143] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas143.html')
def canvas144(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[144] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas144.html')
def canvas145(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[145] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas145.html')
def canvas146(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[146] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas146.html')
def canvas147(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[147] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas147.html')
def canvas148(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[148] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas148.html')
def canvas149(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[149] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas149.html')
def canvas150(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[150] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas150.html')
def canvas151(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[151] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas151.html')
def canvas152(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[152] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas152.html')
def canvas153(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[153] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas153.html')
def canvas154(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[154] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas154.html')
def canvas155(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[155] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas155.html')
def canvas156(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[156] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas156.html')
def canvas157(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[157] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas157.html')
def canvas158(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[158] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas158.html')
def canvas159(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[159] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas159.html')
def canvas160(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[160] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas160.html')
def canvas161(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[161] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas161.html')
def canvas162(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[162] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas162.html')
def canvas163(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[163] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas163.html')
def canvas164(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[164] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas164.html')
def canvas165(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[165] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas165.html')
def canvas166(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[166] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas166.html')
def canvas167(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[167] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas167.html')
def canvas168(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[168] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas168.html')
def canvas169(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[169] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas169.html')
def canvas170(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[170] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas170.html')
def canvas171(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[171] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas171.html')
def canvas172(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[172] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas172.html')
def canvas173(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[173] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas173.html')
def canvas174(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[174] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas174.html')
def canvas175(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[175] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas175.html')
def canvas176(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[176] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas176.html')
def canvas177(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[177] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas177.html')
def canvas178(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[178] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas178.html')
def canvas179(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[179] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas179.html')
def canvas180(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[180] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas180.html')
def canvas181(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[181] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas181.html')
def canvas182(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[182] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas182.html')
def canvas183(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[183] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas183.html')
def canvas184(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[184] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas184.html')
def canvas185(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[185] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas185.html')
def canvas186(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[186] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas186.html')
def canvas187(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[187] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas187.html')
def canvas188(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[188] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas188.html')
def canvas189(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[189] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas189.html')
def canvas190(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[190] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas190.html')
def canvas191(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[191] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas191.html')
def canvas192(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[192] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas192.html')
def canvas193(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[193] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas193.html')
def canvas194(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[194] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas194.html')
def canvas195(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[195] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas195.html')
def canvas196(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[196] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas196.html')
def canvas197(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[197] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas197.html')
def canvas198(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[198] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas198.html')
def canvas199(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[199] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas199.html')
def canvas200(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[200] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas200.html')
def canvas201(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[201] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas201.html')
def canvas202(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[202] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas202.html')
def canvas203(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[203] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas203.html')
def canvas204(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[204] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas204.html')
def canvas205(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[205] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas205.html')
def canvas206(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[206] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas206.html')
def canvas207(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[207] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas207.html')
def canvas208(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[208] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas208.html')
def canvas209(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[209] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas209.html')
def canvas210(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[210] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas210.html')
def canvas211(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[211] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas211.html')
def canvas212(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[212] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas212.html')
def canvas213(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[213] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas213.html')
def canvas214(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[214] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas214.html')
def canvas215(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[215] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas215.html')
def canvas216(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[216] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas216.html')
def canvas217(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[217] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas217.html')
def canvas218(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[218] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas218.html')
def canvas219(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[219] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas219.html')
def canvas220(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[220] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas220.html')
def canvas221(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[221] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas221.html')
def canvas222(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[222] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas222.html')
def canvas223(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[223] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas223.html')
def canvas224(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[224] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas224.html')
def canvas225(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[225] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas225.html')
def canvas226(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[226] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas226.html')
def canvas227(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[227] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas227.html')
def canvas228(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[228] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas228.html')
def canvas229(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[229] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas229.html')
def canvas230(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[230] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas230.html')
def canvas231(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[231] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas231.html')
def canvas232(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[232] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas232.html')
def canvas233(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[233] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas233.html')
def canvas234(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[234] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas234.html')
def canvas235(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[235] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas235.html')
def canvas236(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[236] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas236.html')
def canvas237(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[237] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas237.html')
def canvas238(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[238] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas238.html')
def canvas239(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[239] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas239.html')
def canvas240(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[240] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas240.html')
def canvas241(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[241] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas241.html')
def canvas242(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[242] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas242.html')
def canvas243(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[243] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas243.html')
def canvas244(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[244] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas244.html')
def canvas245(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[245] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas245.html')
def canvas246(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[246] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas246.html')
def canvas247(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[247] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas247.html')
def canvas248(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[248] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas248.html')
def canvas249(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[249] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas249.html')
def canvas250(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[250] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas250.html')
def canvas251(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[251] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas251.html')
def canvas252(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[252] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas252.html')
def canvas253(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[253] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas253.html')
def canvas254(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[254] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas254.html')
def canvas255(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[255] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas255.html')
def canvas256(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[256] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas256.html')
def canvas257(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[257] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas257.html')
def canvas258(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[258] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas258.html')
def canvas259(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[259] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas259.html')
def canvas260(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[260] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas260.html')
def canvas261(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[261] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas261.html')
def canvas262(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[262] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas262.html')
def canvas263(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[263] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas263.html')
def canvas264(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[264] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas264.html')
def canvas265(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[265] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas265.html')
def canvas266(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[266] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas266.html')
def canvas267(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[267] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas267.html')
def canvas268(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[268] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas268.html')
def canvas269(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[269] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas269.html')
def canvas270(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[270] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas270.html')
def canvas271(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[271] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas271.html')
def canvas272(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[272] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas272.html')
def canvas273(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[273] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas273.html')
def canvas274(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[274] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas274.html')
def canvas275(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[275] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas275.html')
def canvas276(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[276] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas276.html')
def canvas277(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[277] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas277.html')
def canvas278(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[278] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas278.html')
def canvas279(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[279] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas279.html')
def canvas280(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[280] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas280.html')
def canvas281(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[281] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas281.html')
def canvas282(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[282] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas282.html')
def canvas283(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[283] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas283.html')
def canvas284(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[284] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas284.html')
def canvas285(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[285] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas285.html')
def canvas286(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[286] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas286.html')
def canvas287(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[287] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas287.html')
def canvas288(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[288] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas288.html')
def canvas289(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[289] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas289.html')
def canvas290(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[290] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas290.html')
def canvas291(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[291] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas291.html')
def canvas292(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[292] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas292.html')
def canvas293(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[293] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas293.html')
def canvas294(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[294] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas294.html')
def canvas295(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[295] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas295.html')
def canvas296(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[296] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas296.html')
def canvas297(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[297] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas297.html')
def canvas298(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[298] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas298.html')
def canvas299(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[299] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas299.html')
def canvas300(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[300] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas300.html')
def canvas301(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[301] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas301.html')
def canvas302(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[302] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas302.html')
def canvas303(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[303] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas303.html')
def canvas304(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[304] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas304.html')
def canvas305(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[305] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas305.html')
def canvas306(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[306] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas306.html')
def canvas307(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[307] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas307.html')
def canvas308(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[308] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas308.html')
def canvas309(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[309] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas309.html')
def canvas310(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[310] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas310.html')
def canvas311(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[311] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas311.html')
def canvas312(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[312] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas312.html')
def canvas313(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[313] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas313.html')
def canvas314(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[314] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas314.html')
def canvas315(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[315] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas315.html')
def canvas316(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[316] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas316.html')
def canvas317(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[317] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas317.html')
def canvas318(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[318] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas318.html')
def canvas319(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[319] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas319.html')
def canvas320(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[320] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas320.html')
def canvas321(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[321] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas321.html')
def canvas322(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[322] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas322.html')
def canvas323(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[323] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas323.html')
def canvas324(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[324] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas324.html')
def canvas325(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[325] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas325.html')
def canvas326(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[326] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas326.html')
def canvas327(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[327] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas327.html')
def canvas328(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[328] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas328.html')
def canvas329(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[329] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas329.html')
def canvas330(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[330] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas330.html')
def canvas331(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[331] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas331.html')
def canvas332(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[332] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas332.html')
def canvas333(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[333] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas333.html')
def canvas334(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[334] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas334.html')
def canvas335(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[335] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas335.html')
def canvas336(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[336] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas336.html')
def canvas337(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[337] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas337.html')
def canvas338(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[338] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas338.html')
def canvas339(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[339] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas339.html')
def canvas340(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[340] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas340.html')
def canvas341(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[341] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas341.html')
def canvas342(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[342] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas342.html')
def canvas343(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[343] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas343.html')
def canvas344(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[344] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas344.html')
def canvas345(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[345] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas345.html')
def canvas346(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[346] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas346.html')
def canvas347(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[347] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas347.html')
def canvas348(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[348] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas348.html')
def canvas349(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[349] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas349.html')
def canvas350(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[350] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas350.html')
def canvas351(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[351] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas351.html')
def canvas352(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[352] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas352.html')
def canvas353(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[353] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas353.html')
def canvas354(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[354] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas354.html')
def canvas355(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[355] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas355.html')
def canvas356(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[356] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas356.html')
def canvas357(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[357] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas357.html')
def canvas358(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[358] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas358.html')
def canvas359(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[359] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas359.html')
def canvas360(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[360] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas360.html')
def canvas361(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[361] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas361.html')
def canvas362(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[362] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas362.html')
def canvas363(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[363] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas363.html')
def canvas364(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[364] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas364.html')
def canvas365(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[365] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas365.html')
def canvas366(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[366] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas366.html')
def canvas367(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[367] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas367.html')
def canvas368(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[368] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas368.html')
def canvas369(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[369] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas369.html')
def canvas370(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[370] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas370.html')
def canvas371(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[371] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas371.html')
def canvas372(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[372] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas372.html')
def canvas373(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[373] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas373.html')
def canvas374(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[374] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas374.html')
def canvas375(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[375] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas375.html')
def canvas376(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[376] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas376.html')
def canvas377(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[377] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas377.html')
def canvas378(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[378] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas378.html')
def canvas379(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[379] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas379.html')
def canvas380(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[380] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas380.html')
def canvas381(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[381] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas381.html')
def canvas382(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[382] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas382.html')
def canvas383(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[383] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas383.html')
def canvas384(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[384] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas384.html')
def canvas385(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[385] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas385.html')
def canvas386(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[386] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas386.html')
def canvas387(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[387] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas387.html')
def canvas388(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[388] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas388.html')
def canvas389(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[389] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas389.html')
def canvas390(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[390] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas390.html')
def canvas391(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[391] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas391.html')
def canvas392(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[392] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas392.html')
def canvas393(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[393] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas393.html')
def canvas394(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[394] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas394.html')
def canvas395(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[395] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas395.html')
def canvas396(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[396] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas396.html')
def canvas397(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[397] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas397.html')
def canvas398(request):
        if request.method == 'POST':
                data = json.loads(request.body)
                response = urllib.request.urlopen(data)
                with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/neural-fonts/dataset/make/crop/uni'+ array_uni[398] +'.png', 'wb') as f:
                        f.write(response.file.read())
        return render(request, 'first/canvas398.html')