import re
import os
import sys
import subprocess


def run_ffmpeg(input, output, preset='fast', crf=26):
    print(f'input: {input} / preset: {preset}')
    cmd = ['/usr/local/bin/ffmpeg',
           '-y',
           '-i', f'{input}',
           '-c:v', 'libx265',
           '-crf', f'{crf}',
           '-preset', f'{preset}',
           '-c:a', 'aac',
           '-b:a', '128k',
           f'{output}'
           ]
    return subprocess.run(cmd, capture_output=True, text=True)

def parse_ffmpeg(p):
    pattern = re.compile(r'encoded .* frames in .*s \((.*) fps\), (.*) kb/s, Avg QP:.*')
    searched = pattern.search(p.stderr)

    if searched:
        fps = searched.group(1)
        bitrate = searched.group(2)
        print(f'fps: {fps}, bitrate: {bitrate}')
    else:
        print('no')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_path = '/Users/dhkim/Downloads/donghwan/original/4k'
    output_path = '/Users/dhkim/Downloads/donghwan/result/4k'
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

    print('done')
