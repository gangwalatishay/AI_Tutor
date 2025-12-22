from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import pysrt

def burn_subtitles(video_path, srt_path, output_path):
    subs = pysrt.open(srt_path)
    video = VideoFileClip(video_path)

    text_clips = []

    for sub in subs:
        start = sub.start.ordinal / 1000
        end = sub.end.ordinal / 1000

        txt = TextClip(
            sub.text,
            fontsize=42,
            color="white",
            method="caption",
            size=(1600, None)
        ).set_position(("center", "bottom")).set_start(start).set_end(end)

        text_clips.append(txt)

    final = CompositeVideoClip([video, *text_clips])
    final.write_videofile(output_path, fps=24)
