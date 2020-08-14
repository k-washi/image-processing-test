import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from util.log_conf import get_logger
from video_to_flame import config
from video_to_flame.utils import stop_watch

import cv2
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing


logger = get_logger(__file__)

IMAGE_NAME = '%s_%s.png'


def capture_setting():
    cap = cv2.VideoCapture(str(config.VIDEO_FILE))
    frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) + 1

    return cap, frame_num, fps


@stop_watch
def extraction_from_video(start=-1, end=-1):
    cap, frame_num, fps = capture_setting()
    if start < 0:
        start = 0
    if end < 0:
        end = frame_num

    cap.set(1, start)

    image_unit = int(fps / config.EXTRACT_FPS)
    frame_count = start
    save_img_count = 0
    while_safety = 0

    while (frame_count < end):
        _, img = cap.read()

        if while_safety > 100:
            logger.error(f"動画から画像を読み込めない状態が続きました。info: {start}, {end}")
            break

        if img is None:
            while_safety += 1
            continue

        frame_count += 1
        if frame_count % image_unit != 0:
            continue

        # 画像の前処理
        # rimg = cv2.resize(img, (config.WIDTH, config.HEIGHT))  # 1080pに変換

        while_safety = 0
        save_img_count += 1
        save_path = os.path.join(str(config.IMG_PATH), IMAGE_NAME %
                                 (config.IMAGE_NAME, str(frame_count).zfill(6)))
        cv2.imwrite(save_path, img)

    cap.release()
    return save_img_count


"""
並列化して画像を切り出す
"""


@stop_watch
def video_to_frames():
    # cv2.setNumThreads(0)  # opencvの並列処理を切る
    chunk_size = config.CHUNK_SIZE

    logger.debug(f"Video File: {config.VIDEO_FILE}")
    cap, frame_num, fps = capture_setting()
    logger.debug(f'frame_count:{frame_num}')
    logger.debug(f'fps:{fps}')
    cap.release()

    if frame_num < 0:
        logger.error("Video has no frame. Check your configuration.")
        return None

    frame_chunks = [[i, i + chunk_size]
                    for i in range(0, frame_num, chunk_size)]
    # 最後の処理のみ画像数に合わせてChunkを作成する。
    frame_chunks[-1][-1] = min(frame_chunks[-1][-1], frame_num - 1)
    logger.debug(f"cpu num: {multiprocessing.cpu_count()}")

    # a prefix string to be printed in progress bar
    prefix_str = f"Extracting frames from {str(config.VIDEO_FILE_NAME)}"

    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        futures = [executor.submit(extraction_from_video, f[0], f[1])
                   for f in frame_chunks]  # submit the processes: extract_frames(...)
        for i, f in enumerate(as_completed(futures)):  # as each process completes
            print_progress(i, len(frame_chunks) - 1, prefix=prefix_str,
                           suffix='Complete')  # print it's progress

    return True


def print_progress(iteration, total, prefix='', suffix='', decimals=3, bar_length=100):

    # format the % done number string
    format_str = "{0:." + str(decimals) + "f}"
    percents = format_str.format(
        100 * (iteration / float(total)))  # calculate the % done
    # calculate the filled bar length
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '#' * filled_length + '-' * \
        (bar_length - filled_length)  # generate the bar string
    sys.stdout.write('\r%s |%s| %s%s %s' %
                     (prefix, bar, percents, '%', suffix)),  # write out the bar
    sys.stdout.flush()  # flush to stdout


if __name__ == "__main__":
    # extraction_from_video : 146.4629669189453 sec 5分間の動画を5FPSで切り出した結果

    # extraction_from_video(
    #    start=config.START_FRAME, end=config.END_FRAME)
    # video_to_frames : 65.1673731803894 sec
    video_to_frames()
