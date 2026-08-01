import sounddevice as sd
import soundfile as sf
import numpy as np

class VirtualMic:
    def __init__(self):
        self.MICROPHONE = "CABLE Input (VB-Audio Virtual Cable)"
        self.index = None
        
        for index, device in enumerate(sd.query_devices()):
            if self.MICROPHONE in device['name']:
                self.index = index
                break
                
        if self.index is None:
            raise RuntimeError(f"Could not find device: {self.MICROPHONE}")

    def play_in_mic(self, file_path: str):
        data, fs = sf.read(file_path, dtype='float32')

        if len(data.shape) == 1:
            data = np.column_stack((data, data))

        sd.play(data, samplerate=fs, device=self.index)
        sd.wait()

# Example usage:
# mic = VirtualMic()
# mic.play_in_mic("your_audio.wav")
