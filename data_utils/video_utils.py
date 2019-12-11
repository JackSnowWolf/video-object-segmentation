import os

TMP_FOLDER = "tmp"
MODEL_FOLDER = "models"
cached_video = set()
for f in os.listdir(MODEL_FOLDER):
    if os.path.isdir(os.path.join(MODEL_FOLDER, f)):
        cached_video.add(f)


def video2img(video_path, img_folder):
    cmd = "ffmpeg -i %s -r 24 -t 140 -start_number 0 %s/%%05d.png" % (video_path, img_folder)
    print(cmd)
    os.system(cmd)


def img2video(img_folder, video_path):
    cmd = "ffmpeg -f image2 -i %s/%%05d.png -c:v libx265 -preset" \
          " medium -crf 18 -r 24 %s" % (
              img_folder, video_path)
    print(cmd)
    os.system(cmd)


def init_video(video_name):
    if not video_name in cached_video:
        cached_video.add(video_name)
    video_folder = os.path.join(TMP_FOLDER, video_name)
    result_path = os.path.join(TMP_FOLDER, video_name, 'pred')
    concate_path = os.path.join(TMP_FOLDER, video_name, 'concat')
    img_path = os.path.join(TMP_FOLDER, video_name, 'img')
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    if not os.path.exists(concate_path):
        os.makedirs(concate_path)
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    first_mask_path = os.path.join(video_folder, "first_mask.png")
    video_path = os.path.join(video_folder, video_name + ".mp4")
    return video_path, img_path, first_mask_path


def render_video(video_name, method="CONCAT"):
    if method.upper() == "CONCAT":
        concate_path = os.path.join(TMP_FOLDER, video_name, 'concat')
        video_path = os.path.join(TMP_FOLDER, video_name,
                                  video_name + "-concat.mp4")
        img2video(concate_path, video_path)
        return video_path
    elif method.upper() == "ANNO":
        pred_path = os.path.join(TMP_FOLDER, video_name, 'pred')
        video_path = os.path.join(TMP_FOLDER, video_name,
                                  video_name + "-anno.mp4")
        img2video(pred_path, video_path)
        return video_path
    else:
        raise ValueError("Render Method %s is not supported" % method.upper())
