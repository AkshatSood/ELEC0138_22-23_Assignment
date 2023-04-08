"""Transformation Module"""

import time

import parselmouth
from parselmouth.praat import call

from modules.utility import Utility
from constants import DATASET_DIR, TRANSFORMED_DIR, PROGRESS_NUM

class Transformation:

    def __init__(self):
        """Default Constructor
        """
        self.utility = Utility()
        self.formant_shift_factor = 2
        self.pitch_shift = 60

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
    
    def transform(self):
        """Transforms all the audio files from the raw dataset
        """
        print('\n\t=> Transforming raw audio files...')
        # Get a list of all WAV files from the dataset directory
        raw_files = self.utility.get_files_in_dir(dir_path=DATASET_DIR, ext='wav')
        transformed_files = self.utility.get_files_in_dir(dir_path=TRANSFORMED_DIR, ext='wav')

        # Filter files that have already been transformed
        raw_files = [f for f in raw_files if f not in transformed_files]

        # Check if any raw files need to be processed
        if len(raw_files) == 0:
            print('\t\tAll raw files have already been transformed. Skipping this step.')
        else:
            print(f'\t\tTransforming {len(raw_files)} audio files...')

            start_time = time.time()
            checkpoint = int(len(raw_files)/PROGRESS_NUM)

            # Transform the all the audio files
            for idx, audio_file_name in enumerate(raw_files):
                snd = parselmouth.Sound(f'{DATASET_DIR}/{audio_file_name}')
                transformed_snd = self.__transform_audio(snd)
                transformed_snd.save(f'{TRANSFORMED_DIR}/{audio_file_name}', parselmouth.SoundFileFormat.WAV)

                if checkpoint != 0 and ((idx+1) % checkpoint == 0):
                    self.utility.progress_print(len(raw_files), (idx+1), start_time)
