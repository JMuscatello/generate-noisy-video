# generate-noisy-video

Python script to creates videos from a base image and a number of audio (.wav) files by adding Gaussian noise. The amount of noise is dependent on the total power of the spectrum of the audio file for a window with spacing corresponding to the frame rate of the video. 

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
