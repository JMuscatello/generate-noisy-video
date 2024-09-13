# generate-noisy-video

Python script to create visualisations from a base image for a number of audio (.wav) files by adding variable Gaussian noise. The amount of noise in any given frame is dependent on the total power of the audio spectrum in a window with spacing in time corresponding to the frame rate of the video. Requires FFmpeg.

## Install requirements

Install `requirements.txt`
```console
foo@bar:~$ pip install requirements.txt
```

Install FFmpeg (Debian)
```console
foo@bar:~$ sudo apt install ffmpeg
```

## Run script

```console
foo@bar:~$ python process_video.py -a /path/to/audio/files/ -i /path/to/my/image.png -o /path/to/videos/
```
