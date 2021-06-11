import re
import os
import os.path
import sys
import subprocess


def run_mc(input, output, perf=15):
    fps_dict = {'bike1': 25,
                'circuit1': 29.97,
                'city1': 23.98,
                'concert1': 29.97,
                'game1': 59.44,
                'movie1': 23.98,
                'tennis1': 29.97
                }

    fps = fps_dict[os.path.basename(os.path.splitext(input)[0])]

    cmd = ['/home1/irteam/donghwan/demo_hevc_sdk_linux_x64_release/bin/sample_enc_hevc',
           '-I420',
           '-w', '3840',
           '-h', '2160',
           '-f', f'{fps}',
           '-v', f'{input}',
           '-o', f'{output}',
           ]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def run_ffmpeg(input, output, preset='fast', crf=26):
    print(f'input: {input} / preset: {preset}')
    cmd = ['/home1/irteam/donghwan/ffmpeg-git-20210528-amd64-static/ffmpeg',
    # cmd = ['ffmpeg',
           '-y',
           '-video_size', '3840x2160',
           '-i', f'{input}',
           '-c:v', 'libx265',
           '-crf', f'{crf}',
           '-preset', f'{preset}',
           '-c:a', 'aac',
           '-b:a', '128k',
           f'{output}'
           ]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def parse_ffmpeg(p):
    pattern = r'encoded .* frames in .*s \((.*) fps\), (.*) kb/s, Avg QP:.*'
    stdout = str(p.stdout.read())
    _parse_stdout(pattern, stdout)
    fps, bitrate = _parse_stdout(pattern, stdout)
    print(fps, bitrate)


def parse_mc(p):
    pattern = r'Average speed achieved  (\w*) fps .* Average bitrate         (\w*) kb/s'
    stdout = str(p.stdout.read())
    _parse_stdout(pattern, stdout)
    fps, bitrate = _parse_stdout(pattern, stdout)
    print(fps, bitrate)


def _parse_stdout(pattern, stdout):
    searched = re.search(pattern, stdout)
    if not searched:
        print('no match')
        return

    fps = searched.group(1)
    bitrate = searched.group(2)
    return fps, bitrate


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_path = '../original/4k'
    output_path = '../result/4k'
    presets = ['ultrafast',
               'superfast',
               'veryfast',
               'faster',
               'fast',
               'medium',
               'slow',
               'slower',
               'veryslow']

    input = f'{input_path}/bike1.yuv'
    output = f'{output_path}/bike1.hevc'

    for preset in presets:
        p = run_ffmpeg(input, output, preset)
        parse_ffmpeg(p)

    for perf in range(0, 31):
        p = run_mc(input, output)
        parse_mc(p)

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
