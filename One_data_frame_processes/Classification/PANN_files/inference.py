import os
import librosa
import torch

from ..PANN_files.Config import PATH_TO_ROOT, labels, classes_num
from ..PANN_files.models import Cnn14
from ..PANN_files.pytorch_utils import move_data_to_device


def create_folder(fd):
    if not os.path.exists(fd):
        os.makedirs(fd)


def get_filename(path):
    path = os.path.realpath(path)
    na_ext = path.split('\\')[-1]
    na = os.path.splitext(na_ext)[0]
    return na


def wav_path_to_audio(wav_path):
    (audio, _) = librosa.core.load(PATH_TO_ROOT + "\\" + wav_path, sr=32000, mono=True)
    audio = audio[None, :]  # (batch_size, segment_samples)

    return audio


class AudioSetTagging(object):
    def __init__(self, model=None, checkpoint_path=None, device='cuda'):
        """Audio tagging inference wrapper.
        """
        if not checkpoint_path:
            checkpoint_path = '{}\\Cnn14_mAP=0.431.pth'.format(PATH_TO_ROOT)
        print('Checkpoint path: {}'.format(checkpoint_path))

        if not os.path.exists(checkpoint_path) or os.path.getsize(checkpoint_path) < 3e8:
            create_folder(os.path.dirname(checkpoint_path))
            zenodo_path = 'https://zenodo.org/record/3987831/files/Cnn14_mAP%3D0.431.pth?download=1'
            os.system('wget -O "{}" "{}"'.format(checkpoint_path, zenodo_path))

        if device == 'cuda' and torch.cuda.is_available():
            self.device = 'cuda'
        else:
            self.device = 'cpu'

        self.labels = labels
        self.classes_num = classes_num

        # Model
        if model is None:
            self.model = Cnn14(sample_rate=32000, window_size=1024,
                               hop_size=320, mel_bins=64, fmin=50, fmax=14000,
                               classes_num=self.classes_num)
        else:
            self.model = model

        checkpoint = torch.load(checkpoint_path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model'])

        # Parallel
        if 'cuda' in str(self.device):
            self.model.to(self.device)
            print('GPU number: {}'.format(torch.cuda.device_count()))
            self.model = torch.nn.DataParallel(self.model)
        else:
            print('Using CPU.')

    def inference(self, audio):
        audio = move_data_to_device(audio, self.device)

        with torch.no_grad():
            self.model.eval()
            output_dict = self.model(audio, None)

        clipwise_output = output_dict['clipwise_output'].data.cpu().numpy().reshape(-1)

        return clipwise_output

    def encode(self, audio):
        audio = move_data_to_device(audio, self.device)

        with torch.no_grad():
            self.model.eval()
            output_dict = self.model(audio, None)

        embedding = output_dict['embedding'].data.cpu().numpy().reshape(-1)

        return embedding


ast = AudioSetTagging(checkpoint_path=None, device='cuda')
