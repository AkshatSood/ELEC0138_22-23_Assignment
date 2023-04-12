"""Transformation Module"""

import time
import os

import parselmouth
from parselmouth.praat import call

from modules.utility import Utility
from constants import DATASET_DIR, TRANSFORMED_DIR, PROGRESS_NUM

class AudioTransformer:

    def __init__(self):
        """Default Constructor
        """
        self.utility = Utility()
        self.output_audio_encoding = parselmouth.SoundFileFormat.FLAC
        self.formant_shift_factor = 1.5
        self.pitch_shift = 60

        # Check if the transformed data directory exists. If not, create it
        self.utility.check_and_create_dir(TRANSFORMED_DIR)

    def __transform_audio(self, snd):
        """Transforms the provided audio file

        Args:
            snd (parselmouth.Sound): sound to be transformed

        Returns:
            parselmouth.Sound: the transformed sound
        """
        pitch = snd.to_pitch()
        medain_pitch = call(pitch, "Get quantile", 0, 0, 0.5, "Hertz")
        new_pitch = medain_pitch + self.pitch_shift
        transformed_snd = call(snd, "Change gender", 100, 500, self.formant_shift_factor, new_pitch, 1, 1)
        
        return transformed_snd
    
    def transform(self, data_dir, output_dir):
        """Transforms all the audio files from the raw dataset
        """
        print('\n\t=> Transforming raw audio files...')
        # # Get a list of all WAV files from the dataset directory
        # raw_files = self.utility.get_files_in_dir(dir_path=DATASET_DIR, ext='wav')
        # transformed_files = self.utility.get_files_in_dir(dir_path=TRANSFORMED_DIR, ext='wav')

        # # Filter files that have already been transformed
        # raw_files = [f for f in raw_files if f not in transformed_files]

        raw_files = set()

        self.utility.check_and_create_dir(output_dir)

        for dir_, _, files in os.walk(data_dir):
            for file_name in files:
                if file_name.endswith('.flac'):
                    rel_dir = os.path.relpath(dir_, data_dir)
                    rel_file = os.path.join(rel_dir, file_name)
                    raw_files.add(rel_file)

        # Check if any raw files need to be processed
        if len(raw_files) == 0:
            print('\t\tUnable to find any raw files. Skipping this step.')
        else:
            print(f'\t\tTransforming {len(raw_files)} audio files...')

            start_time = time.time()
            checkpoint = int(len(raw_files)/PROGRESS_NUM)

            # Transform the all the audio files
            for idx, file_sub_path in enumerate(raw_files):
                
                raw_file_path = os.path.join(data_dir, file_sub_path).replace('\\', '/')
                file_name = os.path.basename(file_sub_path)

                snd = parselmouth.Sound(raw_file_path)
                transformed_snd = self.__transform_audio(snd)
                transformed_snd.save(f'{output_dir}/transformed_{file_name}', self.output_audio_encoding)

                if checkpoint != 0 and ((idx+1) % checkpoint == 0):
                    self.utility.progress_print(len(raw_files), (idx+1), start_time)

            print('\t\tSuccessfully transformed audio files.')