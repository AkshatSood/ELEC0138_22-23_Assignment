
from constants import DATASET_DIR

from modules.utility import Utility

class Dataset:

    def __init__(self):
        """Default constructor
        """
        self.utility = Utility()

        # Check if the dataset directory exists. If not, then create it
        self.utility.check_and_create_dir(DATASET_DIR)

    def download_data(self):
        pass

