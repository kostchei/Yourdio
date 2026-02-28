import sys
import torchaudio
import soundfile as sf

def patched_save(filepath, src, sample_rate, *args, **kwargs):
    if src.dim() == 2:
        src = src.transpose(0, 1)
    sf.write(str(filepath), src.cpu().numpy(), sample_rate, subtype='PCM_16')

torchaudio.save = patched_save

from demucs.separate import main
if __name__ == "__main__":
    main()
