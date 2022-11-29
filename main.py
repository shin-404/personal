import cv2
import wave
import struct
import os
from tqdm import tqdm

def run_capture(file):
    cap = cv2.VideoCapture(file)

    if file[-3:] == "jpg":
        command = -1
    elif file[-3:] == "avi":
        print("get avi:", file)
        command = 1
    elif file == 1:
        print("get capture")
        command = 1

    print("{}x{}".format(cap.get(3), cap.get(4)))
    print("total:", int(cap.get(7)))
    step = 40
    k = 0
    for t in tqdm(range(int(cap.get(7)))):
        k += 1
        ret, frame = cap.read()
        f = open('outputVideo.txt', 'a+')
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if k % 10 != 1:
                continue
            for i in range(0, gray.shape[1], step):
                for j in range(0, gray.shape[0], step):
                    px = 0
                    for scan_y in range(j, j + step):
                        for scan_x in range(i, i + step):
                            px += gray[scan_y, scan_x]

                    try:
                        if px < 255 * 200:
                            char = "1"
                        else:
                            char = "0"
                        f.write(str(char))
                    except:
                        print("error!")
                f.write('\n')
            f.write('\n')
            f.close()

            cv2.imshow("form", gray)
        except cv2.error:
            print("video is over")
            break

        if cv2.waitKey(command) & 0xFF == ord('q'):
            print("exit")
            break
    cap.release()
    cv2.destroyAllWindows()

def get_hz(file):
    voice = wave.open(file, 'rb')
    channels = voice.getnchannels()  # 声道数
    samp_width = voice.getsampwidth()  # 采样大小
    frame_rate = voice.getframerate()  # 帧率
    numframes = voice.getnframes()  # 总帧数

    print("\nvoice:{}".format(file))
    print(voice)
    print("file type:{}".format(type(voice)))
    print("channels:{}".format(channels))
    print("samp_width:{}".format(samp_width))
    print("frame_rate:".format(frame_rate))
    print("numframes:{}".format(numframes))

    with open('outputVoice.txt', 'a+') as f:
        step = 0
        data = 0
        for i in tqdm(range(numframes)):
            frame = voice.readframes(1)
            step += 1
            data += struct.unpack("h", frame[0:2])[0]
            if step == 5:
                print(data)
                data = int(data / 6)
                f.write(str(hex(data)) + '\n')
                step = 0


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # file = input("put your video address:")
    file = 'BadApple.avi'
    run_capture(file)
    # os.system('ffmpeg -i {} {}wav -y'.format(file, file[:-3]))
    # get_hz(file[:-3] + 'wav')
