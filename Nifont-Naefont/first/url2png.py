import urllib.request
import argparse

parser = argparse.ArgumentParser(description='url2png')
parser.add_argument('--url', dest='url', required=True,
                    help='url')
args = parser.parse_args()

data = args.url
#data = 'data:image/png;base64,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'

response = urllib.request.urlopen(data)
with open('/home/ubuntu/CUAI_2021/DaeWoong/Goodrug/first/image.png', 'wb') as f:
    f.write(response.file.read())

# 콘솔에서 python3 url2png.py --url=data:image/png;base64,iV....  치면 됩니다
# 하은시는 --url= 뒤에 그 url만 넣도록 코딩해주시고
# 두번째로 해야할 건 지금 url2png.py가 있는 경로에 image.png가 저장되도록 했는데 crop 폴더 안에 이미지 이름도 유니코드 맞출 수 있도록 해서 저장하도록 13행 수정하면 됩니다!