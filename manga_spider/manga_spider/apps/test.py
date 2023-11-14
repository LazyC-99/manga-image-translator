import numpy as np
from scipy.fftpack import fft

# 模拟采集到的数据，假设是正弦波
sample_rate = 518518  # 采样率
t = np.arange(0, 1, 1 / sample_rate)  # 时间向量
frequency = 50  # 正弦波频率
amplitude = 1  # 振幅


# signal = amplitude * np.sin(2 * np.pi * frequency * t)
def hex_to_decimal(hex_string):
    return int(hex_string, 16)


def read_hex_file(file_path):
    with open(file_path, 'r') as file:
        hex_values = file.read().split()

    decimal_values = [hex_to_decimal(hex_value) for hex_value in hex_values]
    return decimal_values


file_path = 'C:\\Users\\Administrator\\Desktop\\rrr.txt'  # 替换成你的文件路径
decimal_array = read_hex_file(file_path)
print(decimal_array)
my_array = np.array(decimal_array)
signal = my_array

# 进行FFT变换
fft_result = fft(signal)

# 查找主要频率分量
abs_fft_result = np.abs(fft_result)
max_frequency_index = np.argmax(abs_fft_result)
main_frequency = max_frequency_index * sample_rate / len(signal)

print(f"主要频率：{main_frequency} Hz")
