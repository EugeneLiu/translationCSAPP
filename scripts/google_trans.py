import re
import pathlib
import gevent
from gevent.pool import Pool
from googletrans import Translator

global sou_file
global des_file
count = 0
global translator
translator = Translator(service_urls=['translate.google.cn'])
global re_text
re_text = re.compile(u"([\u2000-\u206F\u3000-\u303F\u4E00-\u9FBF\uFF00-\uFFEF]+)", re.VERBOSE)

def tran_sub(line):
    global des_file
    global count
    global translator
    count += 1
    print("count,%d" % count)
    line = line.decode('utf-8')
    if line.startswith('Dialogue') and 'student speaking' not in line:
        des_file.write(line.encode('utf-8'))
        head_str,english_str = tuple(line.rsplit(',,', 1))
        chinese_str = translator.translate(english_str, dest='zh-CN').text
        print(chinese_str)
        c_line = ',,'.join([head_str,chinese_str+'\n']).replace('English', 'Chinese').replace('您', '你').encode('utf-8')
        des_file.write(c_line)
    else:
        des_file.write(line.encode('utf-8'))


def format_sub(line):
    global re_text
    if line.startswith('Dialogue'):
        head_str, text = tuple(line.rsplit(',,', 1))
        if 'Chinese' in head_str:
            text = text.decode('utf-8')
            format_text = re_text.sub(r' \1 ', text).strip()
            des_file.write(',,'.join([head_str, format_text.encode('utf-8') + '\n']))
    else:
        des_file.write(line)


def main():
    sou_path = u"/Users/eugene/workspace/translationCSAPP/subtitle/English/"
    des_path = u"/Users/eugene/workspace/translationCSAPP/subtitle/Chinese_English/"

    filename = u"Lecture 23  Concurrent Programming.ass"

    global sou_file
    global des_file
    sou_file = open(sou_path+filename, 'rb')
    des_file = open(des_path+filename, 'wb+')
    # pool = Pool(10)
    # pool.map(tran_sub, sou_file)
    threads = [gevent.spawn(tran_sub, line) for line in sou_file.readlines()]
    gevent.joinall(threads)
    sou_file.close()
    des_file.close()

if __name__ == '__main__':
    main()


# for line in lines:
#      if line.startswith('Dialogue:'):
#         parts = line.rsplit(',,', 1)
#         line = ',,'.join([parts[0], parts[1].lstrip().capitalize()])
#     f.write(line)