import os
import sys

# python train_handwrite.py <폴더 명>
dir_name = sys.argv[1]

# 웹에서 저장된 폰트들이 저장된 폴더 이름이 crop
os.system('python font2img.py --src_font=dataset/font/NanumGothic.ttf  --dst_font=dataset/font/NanumGothic.ttf  --sample_count=1000 --sample_dir=dataset/%s/img --label=0 --handwriting_dir=dataset/%s/crop' %(dir_name,dir_name))

os.system('python package.py --fixed_sample=1 --dir=dataset/%s/img --save_dir=dataset/%s/binary' %(dir_name, dir_name))

# 학습 준비
os.system('mkdir experiment/%s'%dir_name)

os.system('mkdir experiment/%s/data'%dir_name)

os.system('cp -r experiment/pretrain_20fonts/checkpoint experiment/%s' %dir_name)

os.system('cp dataset/%s/binary/train.obj experiment/%s/data/train.obj'%(dir_name, dir_name))
os.system('cp dataset/%s/binary/val.obj experiment/%s/data/val.obj'%(dir_name, dir_name))

# 손글씨 학습
os.system('python train.py --experiment_dir=experiment/%s --experiment_id=0 --batch_size=16 --lr=0.001 --epoch=60 --sample_steps=100 --schedule=20 --L1_penalty=100 --Lconst_penalty=15 --freeze_encoder=1' %dir_name)

os.system('python train.py --experiment_dir=experiment/%s --experiment_id=0 --batch_size=16 --lr=0.001 --epoch=120 --sample_steps=100 --schedule=40  --L1_penalty=500 --Lconst_penalty=1000 --freeze_encoder=1' %dir_name)

# 인퍼런스
os.system('mkdir result')

os.system('mkdir result/%s' %dir_name)

os.system('python infer.py --model_dir=experiment/%s/checkpoint/experiment_0_batch_16 --batch_size=16 --source_obj=experiment/%s/data/val.obj --embedding_ids=0 --save_dir=result/%s' %(dir_name, dir_name, dir_name))

os.system('python final.py --result_dir=result/%s' %dir_name)
