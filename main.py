"""Main Module"""

from modules.transformation import AudioTransformer
from modules.dataset import Dataset

# Create objects for classes
# dataset = 
transformer = AudioTransformer()
dataset = Dataset()

print('##############################################')
print('\tDOWNLOAD DATASET')
print('##############################################')
dataset.download_data()

print('##############################################')
print('\tTRANSFORM AUDIO FILES')
print('##############################################')
# transformer.transform()
