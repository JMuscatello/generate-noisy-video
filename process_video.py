import os
from shlex import quote


from pathlib import Path
import numpy as np

import click

import cv2

import librosa
from scipy.integrate import trapezoid
from tqdm import tqdm


def get_paths_to_audio(directory: str) -> list[Path]:
    paths = list(Path(directory).glob('*.wav'))
    if not paths:
        raise FileNotFoundError('No .wav files found')
    else:
        return paths


def add_gaussian_noise(image: np.ndarray, mean=0, std=10, scale=1.0) -> np.ndarray:
    noise = (scale*np.random.normal(mean, std, image.shape)).astype(np.uint8)
    noisy_image = image+noise
    return noisy_image


def calculate_power_values_from_audio(path_to_audio: Path, fps=30, n_fft=256) -> np.ndarray:
    """Extract power from each calculated spectrum of audio window"""
    y, sr = librosa.load(path_to_audio)
    hop_length = int(sr/fps)
    D = librosa.stft(y, hop_length=hop_length, n_fft=n_fft)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    powers = trapezoid(np.absolute(D.T), freqs)

    return powers


def generate_video(
        output_dir: str,
        path_to_audio: str,
        path_to_image: str,
        audio_powers: np.ndarray,
        fps: int=30
    ):

    path_to_temp_video = Path(output_dir) / Path(Path(path_to_audio).stem + '_temp').with_suffix('.mp4')
    path_to_video = Path(output_dir) / Path(Path(path_to_audio).name).with_suffix('.mp4')

    original_image = cv2.imread(path_to_image)
    height, width, channels = original_image.shape
    max_noise = 255
    max_power = float(max(audio_powers))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    video = cv2.VideoWriter(str(path_to_temp_video), fourcc, fps=fps, frameSize=(width, height))

    old_image = original_image
    for power in tqdm(audio_powers):
    
        mean = max_noise*(power/max_power)
        new_image = add_gaussian_noise(old_image, mean, std=5)
        new_image = cv2.addWeighted(new_image,power/max_power, original_image,1-power/max_power, 0)
        video.write(new_image)
        old_image = new_image
    
    video.release()

    # Use ffmpg to add audio to video
    print('Adding audio')
    os.system(f'ffmpeg -i "{str(path_to_temp_video)}" -i "{str(path_to_audio)}" -c:a aac -vcodec copy -map 0:v:0 -map 1:a:0 "{str(path_to_video)}"')
    print('Removing temp file')
    os.system(f'rm {quote(str(path_to_temp_video))}')


@click.command()
@click.option('-d', '--directory', help='Directory containing audio files (.wav)')
@click.option('-i', '--image_path', help='Image file to use')
@click.option('-o', '--output', help='')
def process_video(directory, image_path, output):
    """Command to generate noisy videos based on specified image and audio files
    """

    audio_paths = get_paths_to_audio(directory)
    print(f'Found {len(audio_paths)} files.')

    for path_to_audio in tqdm(audio_paths):
        print(f'Processing {str(path_to_audio)}...')
        powers = calculate_power_values_from_audio(path_to_audio)
        generate_video(
            output_dir=output,
            path_to_audio=path_to_audio,
            path_to_image=image_path,
            audio_powers=powers
        )
        print('Done.')


if __name__ == '__main__':
    print('doing')
    process_video()