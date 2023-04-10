"""Dataset Module"""

import kaggle

from constants import DATASET_DIR
from modules.utility import Utility

class Dataset:

    def __init__(self):
        """Default constructor
        """
        self.utility = Utility()
        self.dataset_url = 'https://www.kaggle.com/datasets/uwrfkaggler/ravdess-emotional-song-audio/download?datasetVersionNumber=1'

        kaggle.api.authenticate()
        
        # Check if the dataset directory exists. If not, then create it
        self.utility.check_and_create_dir(DATASET_DIR)

    def download_data(self):
        # with urlopen(self.dataset_url) as zipresp:
        #     with ZipFile(BytesIO(zipresp.read())) as zfile:
        #         zfile.extractall(DATASET_DIR)
        kaggle.api.dataset_download_files('RAVDESS Emotional song audio', DATASET_DIR, unzip=True)

