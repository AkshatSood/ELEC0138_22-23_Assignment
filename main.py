"""Main Module"""

from modules.transformation import AudioTransformer

transformer = AudioTransformer()

print('##############################################')
print('\tTRANSFORM AUDIO FILES')
print('##############################################')
transformer.transform(data_dir='./dataset/LibriSpeech/dev-clean/', output_dir='./transformed/dev-clean')
transformer.transform(data_dir='./dataset/LibriSpeech/test-clean/', output_dir='./transformed/test-clean')
