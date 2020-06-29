from tkinter import *
from tkinter import filedialog

import os
import struct

# populate fields when opening file
def open_btn_click():
    wavfile = filedialog.askopenfilename(title = "Select WAV file",filetypes = (("Wave PCM","*.wav"),("All Files","*.*")))
    dirname, filename = os.path.split(wavfile)
    label.configure(text=filename)

    # read the first 44 header bytes
    with open(wavfile, mode='rb') as wavfile:
        header = wavfile.read(44)

    riff = struct.unpack('>cccc', header[:4]) # 'RIFF'
    file_size = struct.unpack('<I', header[4:8]) 
    wave = struct.unpack('>cccc', header[8:12]) # 'WAVE'
    fmt = struct.unpack('>cccc', header[12:16]) # 'fmt '

    fmt_chunk_size = struct.unpack('<I', header[16:20]) # should always be 16

    audioformat = struct.unpack('<H', header[20:22]) # should be 1 for PCM
    num_channels = struct.unpack('<H', header[22:24]) 
    sample_rate = struct.unpack('<I', header[24:28])
    byte_rate = struct.unpack('<I', header[28:32]) # sample_rate * num_channels * bits_per_sample / 8
    block_align = struct.unpack('<H', header[32:34]) # num_channels * bits_per_sample / 8
    bits_per_sample = struct.unpack('<H', header[34:36])

    data_chunk = struct.unpack('>cccc', header[36:40]) # 'data'

    data_size = struct.unpack('<I', header[40:44]) # num_samples * num_channels * bits_per_sample / 8

    header_label.configure(text=header)

window = Tk()

window.title("WAV Headitor")
window.geometry('600x400')

label = Label(window, text="Please open a WAV file!")
label.grid(column=0, row=1)

open_btn = Button(window, text="Open", command=open_btn_click)
open_btn.grid(column=0, row=0)

header_label = Label(window, text='Header placeholder')
header_label.grid(column=0, row=2)

window.mainloop()

