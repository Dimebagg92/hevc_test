import re
import os
import os.path
import sys
import subprocess

FPS_DICT = {'bike1': 25,
            'circuit1': 29.97,
            'city1': 23.98,
            'concert1': 29.97,
            'game1': 59.44,
            'movie1': 23.98,
            'tennis1': 29.97
            }

MC_PRESET = {'fast': 19,
             'medium': 23,
             'slow': 27
             }

FF_PRESET = {'fast': 'superfast',
             'medium': 'fast',
             'slow': 'slow'
             }

def run_mc(input, output, speed='fast', crf=28):
    fps = FPS_DICT[os.path.basename(os.path.splitext(input)[0])]

    cmd = ['/home1/irteam/donghwan/demo_hevc_sdk_linux_x64_release/bin/sample_enc_hevc',
           '-I420',
           '-w', '3840',
           '-h', '2160',
           '-f', f'{fps}',
           '-v', f'{input}',
           '-o', f'{output}',
           '-perf', f'{MC_PRESET[speed]}',
           '-preset', '4k',
           '-c', f'../config/crf{crf}.ini'
           ]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def run_ffmpeg(input, output, speed='fast', crf=28):
    cmd = ['/home1/irteam/donghwan/ffmpeg-git-20210528-amd64-static/ffmpeg',
           '-y',
           '-video_size', '3840x2160',
           '-i', f'{input}',
           '-c:v', 'libx265',
           '-crf', f'{crf}',
           '-preset', f'{FF_PRESET[speed]}',
           '-c:a', 'aac',
           '-b:a', '128k',
           f'{output}'
           ]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def parse_ffmpeg(p):
    pattern = r'encoded .* frames in .*s \((.*) fps\), (.*) kb/s, Avg QP:.*'
    stdout = str(p.stdout.read())
    fps, bitrate = _parse_stdout(pattern, stdout)
    print(fps, bitrate)


def parse_mc(p):
    pattern = r'Average speed achieved \\t(\d*.*\d*) fps.*\nAverage bitrate.* (\d*.*\d*) kb/s'
    # pattern_fps = r'Average speed achieved.*\t(\d*.*\d*) fps'
    # pattern_bitrate = r'Average bitrate.* (\d*.*\d*) kb/s'
    stdout = str(p.stdout.read())
    fps, bitrate = _parse_stdout(pattern, stdout)
    print(fps, bitrate)


def _parse_stdout(pattern, stdout):
    r = re.compile(pattern, re.DOTALL)
    searched = r.search(stdout)
    if not searched:
        print('no match')
        return

    return searched.group(1), searched.group(2)


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

    speed_set = ['fast']

    for speed in speed_set:
        p = run_ffmpeg(input, 'mc_test.hevc', speed=speed)
        parse_ffmpeg(p)

    for speed in speed_set:
        p = run_mc(input, 'ff_test.hevc', speed=speed)
        parse_mc(p)

    print('done')
