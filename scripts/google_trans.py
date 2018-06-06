import gevent
from gevent.pool import Pool
from googletrans import Translator

global sou_file
global des_file
count = 0
global translator
translator = Translator(service_urls=['translate.google.cn'])

def tran_sub(line):
    global des_file
    global count
    global translator
    count += 1
    print("count,%d" % count)
    line = line.decode('utf-8')
    if line.startswith('Dialogue') and count >= 324:
        if ',English,,' in line:
            des_file.write(line.encode('utf-8'))
        if ',Chinese,,' in line:
            head_str,english_str = tuple(line.rsplit(',,', 1))
            chinese_str = translator.translate(english_str, dest='zh-CN').text
            print(chinese_str)
            des_file.write(',,'.join([head_str,chinese_str+'\n']).encode('utf-8'))
    else:
        des_file.write(line.encode('utf-8'))
    gevent.sleep(1)

def main():
    sou_path = u""
    des_path = u""

    filename = u""

    global sou_file
    global des_file
    sou_file = open(sou_path+filename, 'rb')
    des_file = open(des_path+filename, 'wb+')
    pool = Pool(10)
    pool.map(tran_sub, sou_file)
    sou_file.close()
    des_file.close()

if __name__ == '__main__':
    main()