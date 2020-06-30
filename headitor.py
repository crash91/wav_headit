from tkinter import *
from tkinter import filedialog
# from dataclass import dataclass
import os
import struct

# @dataclass
class wav_header:
    riff: str = 'RIFF'
    file_size: int
    wave: str = 'WAVE'
    fmt_chunk: str = 'fmt '

    fmt_chunk_size: int = 16

    audioformat: int = 1
    num_channels: int
    sample_rate: int
    byte_rate: int
    block_align: int
    bits_per_sample: int

    data_chunk: str = 'data'

    data_size: int

    def unpack_header(self, header_data):
        self.riff = struct.unpack('>cccc', header_data[:4]) # 'RIFF'
        self.file_size = struct.unpack('<I', header_data[4:8]) 
        self.wave = struct.unpack('>cccc', header_data[8:12]) # 'WAVE'
        self.fmt_chunk = struct.unpack('>cccc', header_data[12:16]) # 'fmt '

        self.fmt_chunk_size = struct.unpack('<I', header_data[16:20]) # should always be 16

        self.audioformat = struct.unpack('<H', header_data[20:22]) # should be 1 for PCM
        self.num_channels = struct.unpack('<H', header_data[22:24]) 
        self.sample_rate = struct.unpack('<I', header_data[24:28])
        self.byte_rate = struct.unpack('<I', header_data[28:32]) # sample_rate * num_channels * bits_per_sample / 8
        self.block_align = struct.unpack('<H', header_data[32:34]) # num_channels * bits_per_sample / 8
        self.bits_per_sample = struct.unpack('<H', header_data[34:36])

        self.data_chunk = struct.unpack('>cccc', header_data[36:40]) # 'data'

        self.data_size = struct.unpack('<I', header_data[40:44]) # num_samples * num_channels * bits_per_sample / 8

    def pack_header(self, buffer):
        pass


def update_fields():
    for i in range(4):
        textboxes[i].insert(0, header.riff[i])
    
    # for i in range(4, 8):
        # textboxes[i].insert(0, str(header.file_size))

    for i in range(8,12):
        textboxes[i].insert(0, header.wave[i-8])

    for i in range(12,16):
        textboxes[i].insert(0, header.fmt_chunk[i-12])

    # for i in range(16,20):
        #textboxes[i].insert(0, header.fmt_chunk_size)

    

''' Button methods '''
# populate fields when opening file
def open_btn_click():
    wavfile = filedialog.askopenfilename(title = "Select WAV file",filetypes = (("Wave PCM","*.wav"),("All Files","*.*")))
    dirname, filename = os.path.split(wavfile)
    label.configure(text=filename)

    # read the first 44 header bytes
    with open(wavfile, mode='rb') as wavfile:
        header_data = wavfile.read(44)

    header.unpack_header(header_data)
    update_fields()

def write_btn_click():
    pass


''' Main window config and loop '''
header = wav_header()

window = Tk()

window.title("WAV Headitor")
window.geometry('600x400')

label = Label(window, text="Please open a WAV file!")
label.grid(column=0, row=1, columnspan=8)

open_btn = Button(window, text="Open", command=open_btn_click)
open_btn.grid(column=0, row=0, columnspan=8)

for byte_num in range(44):
    r = 2*(byte_num//8) + 2
    c = byte_num%8
    Label(window, text=str(byte_num)).grid(row=r, column=c)

textboxes = []
for byte_num in range(44):
    r = 2*(byte_num//8) + 3
    c = byte_num%8
    textboxes.append(Entry(window, width=4))
    textboxes[-1].grid(row=r, column=c)

window.mainloop()

