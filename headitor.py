from tkinter import *
from tkinter import filedialog, messagebox

import os
import struct

class wav_header:
    header_data: bytes
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
        self.header_data = header_data
        self.riff = struct.unpack('>cccc', header_data[:4]) # 'RIFF'
        self.file_size = struct.unpack('<I', header_data[4:8])[0] 
        self.wave = struct.unpack('>cccc', header_data[8:12]) # 'WAVE'
        self.fmt_chunk = struct.unpack('>cccc', header_data[12:16]) # 'fmt '

        self.fmt_chunk_size = struct.unpack('<I', header_data[16:20])[0] # should always be 16

        self.audioformat = struct.unpack('<H', header_data[20:22])[0] # should be 1 for PCM
        self.num_channels = struct.unpack('<H', header_data[22:24])[0] 
        self.sample_rate = struct.unpack('<I', header_data[24:28])[0]
        self.byte_rate = struct.unpack('<I', header_data[28:32])[0] # sample_rate * num_channels * bits_per_sample / 8
        self.block_align = struct.unpack('<H', header_data[32:34])[0] # num_channels * bits_per_sample / 8
        self.bits_per_sample = struct.unpack('<H', header_data[34:36])[0]

        self.data_chunk = struct.unpack('>cccc', header_data[36:40]) # 'data'

        self.data_size = struct.unpack('<I', header_data[40:44])[0] # num_samples * num_channels * bits_per_sample / 8

    def pack_header(self):
        self.header_data = header_data
        self.riff = struct.unpack('>cccc', header_data[:4]) # 'RIFF'
        self.file_size = struct.unpack('<I', header_data[4:8])[0] 
        self.wave = struct.unpack('>cccc', header_data[8:12]) # 'WAVE'
        self.fmt_chunk = struct.unpack('>cccc', header_data[12:16]) # 'fmt '

        self.fmt_chunk_size = struct.unpack('<I', header_data[16:20])[0] # should always be 16

        self.audioformat = struct.unpack('<H', header_data[20:22])[0] # should be 1 for PCM
        self.num_channels = struct.unpack('<H', header_data[22:24])[0] 
        self.sample_rate = struct.unpack('<I', header_data[24:28])[0]
        self.byte_rate = struct.unpack('<I', header_data[28:32])[0] # sample_rate * num_channels * bits_per_sample / 8
        self.block_align = struct.unpack('<H', header_data[32:34])[0] # num_channels * bits_per_sample / 8
        self.bits_per_sample = struct.unpack('<H', header_data[34:36])[0]

        self.data_chunk = struct.unpack('>cccc', header_data[36:40]) # 'data'

        self.data_size = struct.unpack('<I', header_data[40:44])[0] # num_samples * num_channels * bits_per_sample / 8


def update_fields(header_data):
    for i in range(4):
        byte_display[i].configure(text=header.riff[i])
    
    for i in range(4, 8):
        byte_display[i].configure(text=hex(header_data[i]))

    for i in range(8,12):
        byte_display[i].configure(text=header.wave[i-8])

    for i in range(12,16):
        byte_display[i].configure(text=header.fmt_chunk[i-12])

    for i in range(16,36):
        byte_display[i].configure(text=hex(header_data[i]))

    for i in range(36,40):
        byte_display[i].configure(text=header.data_chunk[i-36])
    
    for i in range(40,44):
        byte_display[i].configure(text=hex(header_data[i]))

    byte_values[0].delete(0, END)
    byte_values[0].insert(0, str(header.file_size))

    byte_values[1].delete(0, END)
    byte_values[1].insert(0, str(header.fmt_chunk_size))

    byte_values[2].delete(0, END)
    byte_values[2].insert(0, str(header.audioformat))

    byte_values[3].delete(0, END)
    byte_values[3].insert(0, str(header.num_channels))

    byte_values[4].delete(0, END)
    byte_values[4].insert(0, str(header.sample_rate))

    byte_values[5].delete(0, END)
    byte_values[5].insert(0, str(header.byte_rate))
    
    byte_values[6].delete(0, END)
    byte_values[6].insert(0, str(header.block_align))
    
    byte_values[7].delete(0, END)
    byte_values[7].insert(0, str(header.bits_per_sample))
    
    byte_values[8].delete(0, END)
    byte_values[8].insert(0, str(header.data_size))


''' Button methods '''
# populate fields when opening file
def open_btn_click():
    wavfile = filedialog.askopenfilename(title = "Select WAV file",filetypes = (("Wave PCM","*.wav"),("All Files","*.*")))
    dirname, filename = os.path.split(wavfile)
    filename_label.configure(text=filename)

    # read the first 44 header bytes
    with open(wavfile, mode='rb') as wavfile:
        header_data = wavfile.read(44)

    header.unpack_header(header_data)
    update_fields(header_data)

def write_btn_click():
    if not hasattr(header, 'header_data'):
        messagebox.showerror('Error', 'Please open a WAV file first!', icon='error')
        return

    result = messagebox.askquestion("Write to file", "Are You Sure?", icon='warning')
    if result == 'yes':
        header.file_size = int(byte_values[0].get())
        header.fmt_chunk_size = int(byte_values[1].get())
        header.audioformat = int(byte_values[2].get())
        header.num_channels = int(byte_values[3].get())
        header.sample_rate = int(byte_values[4].get())
        header.byte_rate = int(byte_values[5].get())
        header.block_align = int(byte_values[6].get())
        header.bits_per_sample = int(byte_values[7].get())
        header.data_size = int(byte_values[8].get())

        header.pack_header()

''' Main window config and loop '''
header = wav_header()

window = Tk()

window.title("WAV Headitor")
window.geometry('1000x500')
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(14, weight=1)
window.grid_rowconfigure(15, weight=1)
window.grid_rowconfigure(16, weight=1)

filename_label = Label(window, text="Please open a WAV file!")
filename_label.grid(column=0, row=14, columnspan=9, sticky=NSEW)

open_btn = Button(window, text="Open", command=open_btn_click)
open_btn.grid(column=0, row=15, columnspan=9, sticky=NSEW)

open_btn = Button(window, text="Write", command=write_btn_click, width=16)
open_btn.grid(column=0, row=16, columnspan=9, sticky=NSEW)

# column headers
for col in range(1, 9):
    if col == 1:
        text = 'Name'
    elif col == 6:
        text = 'Value'
    elif col == 7:
        text = 'Unit'
    elif col == 8:
        text = 'Description'
    else:
        text = str(col-2)

    Label(window, text=text, padx=10, bg='white').grid(row=0, column=col)

# row headers / byte numbers
byte_offset = 0
for row in range(1, 14):
    if row == 6 or row == 7 or row == 10 or row == 11:
        text = str(byte_offset + 2)
        byte_offset+=2
    else:
        text = str(byte_offset + 4)
        byte_offset+=4

    Label(window, text=text, padx=10, pady=5).grid(row=row, column=0)

# row name labels
Label(window, width=16,anchor=W, text='Chunk ID').grid(row=1, column=1)
Label(window, width=16,anchor=W, text='File Size').grid(row=2, column=1)
Label(window, width=16,anchor=W, text='Format').grid(row=3, column=1)
Label(window, width=16,anchor=W, text='Subchunk 1 ID').grid(row=4, column=1)
Label(window, width=16,anchor=W, text='Subchunk 1 Size').grid(row=5, column=1)
Label(window, width=16,anchor=W, text='Audio Format').grid(row=6, column=1)
Label(window, width=16,anchor=W, text='Number of Channels').grid(row=7, column=1)
Label(window, width=16,anchor=W, text='Sample Rate').grid(row=8, column=1)
Label(window, width=16,anchor=W, text='Byte Rate').grid(row=9, column=1)
Label(window, width=16,anchor=W, text='Block Align').grid(row=10, column=1)
Label(window, width=16,anchor=W, text='Bits per Sample').grid(row=11, column=1)
Label(window, width=16,anchor=W, text='Subchunk 2 ID').grid(row=12, column=1)
Label(window, width=16,anchor=W, text='Subchunk 2 Size').grid(row=13, column=1)

# description column
Label(window, width=50, anchor=W, text='"RIFF" in ASCII (Big Endian)').grid(row=1, column=8)
Label(window, width=50, anchor=W, text='36 + Subchunk 2 Size / number of bytes until EOF').grid(row=2, column=8)
Label(window, width=50, anchor=W, text='"WAVE" in ASCII (Big Endian)').grid(row=3, column=8)
Label(window, width=50, anchor=W, text='"fmt " in ASCII (Big Endian)').grid(row=4, column=8)
Label(window, width=50, anchor=W, text='Number of following header bytes until "data" subchunk').grid(row=5, column=8)
Label(window, width=50, anchor=W, text='1 = PCM (Linear quantization). Other values indicate compression').grid(row=6, column=8)
# Label(window, width=50, anchor=W, text='').grid(row=7, column=8)
# Label(window, width=50, anchor=W, text='').grid(row=8, column=8)
Label(window, width=50, anchor=W, text='nchannels × fs × bps ÷ 8').grid(row=9, column=8)
Label(window, width=50, anchor=W, text='nchannels × bps ÷ 8').grid(row=10, column=8)
# Label(window, width=50, anchor=W, text='').grid(row=11, column=8)
Label(window, width=50, anchor=W, text='"data" in ASCII (Big Endian)').grid(row=12, column=8)
Label(window, width=50, anchor=W, text='nsamples × nchannels × bps ÷ 8 / number of bytes until EOF').grid(row=13, column=8)

# byte display labels
byte_display = []
offset = 0
for byte_num in range(44):
    r = (byte_num//4) + 1 + offset
    c = byte_num%4 + 2

    if byte_num >= 22:
        r +=1
    if r == 7:
        c-=2
    if byte_num >= 34:
        r +=1
    if r == 11:
        c-=2

    byte_display.append(Label(window, width=8, text='0x0'))
    byte_display[-1].grid(row=r, column=c)

# byte value labels
byte_values = []
for row in range(1,14):
    if row != 1 and row != 3 and row != 4 and row != 12:
        byte_values.append(Entry(window, width=16))
        byte_values[-1].grid(row=row, column=6)
# byte value unit labels

window.mainloop()