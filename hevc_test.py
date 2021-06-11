import re
import os
import os.path
import sys
import csv
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

INPUT_PATH = '../original/4k'
OUTPUT_PATH = '../result/4k'

def run_mc(inputfile, speed='fast', crf=28):
    fps = FPS_DICT[os.path.basename(os.path.splitext(input)[0])]
    input = f'{INPUT_PATH}/{inputfile}.yuv'
    output = f'{OUTPUT_PATH}/mc/{inputfile}/{speed}/input_{speed}_crf{crf}.hevc'

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


def run_ffmpeg(inputfile, speed='fast', crf=28):
    input = f'{INPUT_PATH}/{inputfile}.yuv'
    output = f'{OUTPUT_PATH}/ff/{inputfile}/{speed}/input_{speed}_crf{crf}.hevc'
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
    try:
        fps, bitrate = _parse_stdout(pattern, stdout)
    except Exception as e:
        print('Parse Error!')
        raise e
    return fps, bitrate


def parse_mc(p):
    pattern = r'Average speed achieved \\t(\d*.*\d*) fps.*Average bitrate\s*(\d*.*\d*) kb/s'
    stdout = str(p.stdout.read())
    try:
        fps, bitrate = _parse_stdout(pattern, stdout)
    except Exception as e:
        print('Parse Error!')
        raise e
    return fps, bitrate


def _parse_stdout(pattern, stdout):
    r = re.compile(pattern, re.DOTALL)
    searched = r.search(stdout)
    if not searched:
        print(stdout)
        raise Exception('no match')

    return searched.group(1), searched.group(2)


def write_result_csv(csv_file, csv_columns, result_data):
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in result_data:
            writer.writerow(data)


if __name__ == '__main__':
    input_set = ['bike1', 'circuit1', 'city1', 'concert1', 'game1', 'movie1', 'tennis1']
    speed_set = ['fast', 'medium', 'slow']
    crf_set = [22, 24, 26, 28, 30, 32, 34]

    for inputfile in input_set:
        for speed in speed_set:
            csv_file = f'ff_{inputfile}_{speed}.csv'
            csv_columns = ['crf', 'fps', 'bitrate']
            result_data = []
            for crf in crf_set:
                print(f'Running FFmpeg {inputfile}_{speed}_crf...')
                p = run_ffmpeg(inputfile, speed=speed, crf=crf)
                fps, bitrate = parse_ffmpeg(p)
                result_data.append({'crf': crf,
                                    'fps': fps,
                                    'bitrate': bitrate
                                    })
            write_result_csv(csv_file, csv_columns, result_data)


    for inputfile in input_set:
        for speed in speed_set:
            csv_file = f'ff_{inputfile}_{speed}.csv'
            csv_columns = ['crf', 'fps', 'bitrate']
            result_data = []
            for crf in crf_set:
                print(f'Running MainConcept {inputfile}_{speed}_crf...')
                p = run_mc(inputfile, speed=speed, crf=crf)
                fps, bitrate = parse_mc(p)
                result_data.append({'crf': crf,
                                    'fps': fps,
                                    'bitrate': bitrate
                                    })
            write_result_csv(csv_file, csv_columns, result_data)


    print('done')
