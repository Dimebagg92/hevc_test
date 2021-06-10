import re
import os
import sys
import subprocess


def run_ffmpeg(input, output, preset='fast', crf=26):
    print(f'input: {input} / preset: {preset}')
    cmd = ['/home1/irteam/donghwan/ffmpeg-git-20210528-amd64-static/ffmpeg',
           '-y',
           '-i', f'{input}',
           '-c:v', 'libx265',
           '-crf', f'{crf}',
           '-preset', f'{preset}',
           '-c:a', 'aac',
           '-b:a', '128k',
           f'{output}'
           ]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

def parse_ffmpeg(p):
    lastline = p.stdout.readlines()[-1]
    print(lastline)
    pattern = re.compile(r'encoded .* frames in .*s \((.*) fps\), (.*) kb/s, Avg QP:.*')
    searched = pattern.search(lastline)

    if searched:
        fps = searched.group(1)
        bitrate = searched.group(2)
        print(f'fps: {fps}, bitrate: {bitrate}')
    else:
        print('no')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_path = '/home1/irteam/donghwan/original/4k'
    output_path = '/home1/irteam/donghwan/result/4k'
    presets = ['ultrafast',
               'superfast',
               'veryfast',
               'faster',
               'fast',
               'medium',
               'slow',
               'slower',
               'veryslow']

    input = f'{input_path}/bike1.mp4'
    output = f'{output_path}/bike1.hevc'
    for preset in presets:
        p = run_ffmpeg(input, output, preset)
        parse_ffmpeg(p)

    # for filename in os.listdir(input_path):
    #     if filename == '.DS_Store':
    #         continue
    #     input = f'{input_path}/{filename}'
    #     output = f'{output_path}/{filename}'
    #     p = run_ffmpeg(input, output, 'ultrafast')
    #     parse_ffmpeg(p)

    # input = f'{input_path}/bike1_short.mp4'
    # output = f'{output_path}/bike1_short.mp4'
    # p = run_ffmpeg(input, output, 'ultrafast')
    # print(p.stdout.readlines()[-1])

    print('done')
