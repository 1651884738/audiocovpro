from pydub import AudioSegment
import os
import tkinter as tk
from tkinter import filedialog, messagebox

from pydub.silence import detect_nonsilent


def trim_silence(input_file, output_file):
    AudioSegment.ffmpeg = os.getcwd() + "/ffmpeg/bin/ffmpeg.exe"

    # audio = AudioSegment.from_file(input_file, sample_width=4, frame_rate=8000, format="mp3")
    audio = AudioSegment.from_file(input_file, format="mp3")

    # 检测非静默部分
    non_silent = detect_nonsilent(audio, min_silence_len=25, silence_thresh=-50, seek_step=1)

    print(non_silent)

    # 获取非静默部分的结束时间
    end_time = non_silent[-1][1] if non_silent else len(audio)

    # 获取非静默部分的开始时间
    start_time = non_silent[0][0] if non_silent else 0

    # 截取音频文件
    audio = audio[start_time:end_time]

    # 设置采样率
    audio = audio.set_frame_rate(8000)

    # 设置采样位深    4 bytes = 32 bits
    audio = audio.set_sample_width(4)

    # 导出裁剪后的音频文件    比特率设置为128Kbps
    audio.export(output_file, bitrate="128k", format="mp3", tags={"album": "20230810", "artist": "lip"})


def select_input_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, folder_path)


def select_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder_path)


def start_batch_processing():
    input_folder = input_entry.get()
    output_folder = output_entry.get()

    if not input_folder or not output_folder:
        messagebox.showerror("Error", "Please select input and output folders.")
        return

    try:
        for file_name in os.listdir(input_folder):
            if file_name.endswith(".mp3"):
                input_file = os.path.join(input_folder, file_name)
                output_file = os.path.join(output_folder, file_name)
                trim_silence(input_file, output_file)
        messagebox.showinfo("Success", "Batch processing completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# 创建窗口
window = tk.Tk()
window.title("MP3 批处理")

# 设置窗口尺寸
window.geometry("400x300")  # 设置宽度为500像素，高度为300像素

# 创建菜单栏
menubar = tk.Menu(window)

# 创建一个file菜单项
filemenu = tk.Menu(menubar, tearoff=0)

menubar.add_cascade(label='操作', menu=filemenu)

# file菜单项的选项
# filemenu.add_command(label='批量转换', command=window.quit)
# filemenu.add_separator()    # 添加一条分割线
# filemenu.add_command(label='批量裁剪', command=window.quit)
# filemenu.add_separator()    # 添加一条分割线
filemenu.add_command(label='退出', command=window.quit)

# 输入文件夹路径
input_label = tk.Label(window, text="输入路径:")
input_label.pack()
input_entry = tk.Entry(window, width=50)
input_entry.pack()
input_button = tk.Button(window, text="选择文件夹", command=select_input_folder)
input_button.pack()

# 输出文件夹路径
output_label = tk.Label(window, text="输出路径:")
output_label.pack()
output_entry = tk.Entry(window, width=50)
output_entry.pack()
output_button = tk.Button(window, text="选择文件夹", command=select_output_folder)
output_button.pack()

# 开始批处理按钮
start_button = tk.Button(window, text="开始处理", command=start_batch_processing)
start_button.pack()

#
window.config(menu=menubar)

# 运行窗口
window.mainloop()
