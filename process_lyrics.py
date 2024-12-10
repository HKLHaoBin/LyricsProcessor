import re

# 输入文本
input_text = """
"""

# 定义文本拆分与处理函数
def transform_text(input_text):
    lines = input_text.split("\n")
    result_lines = []

    for line in lines:
        # 查找 "((" 前的部分
        parts = re.split(r'(\(\()', line, maxsplit=1)
        if len(parts) == 3:
            prefix = parts[0].strip()
            rest = parts[1] + parts[2]
            result_lines.append(prefix)  # 将 "（换行）" 前部分加入结果
            result_lines.append(rest)   # 将剩余部分单独作为新行
        else:
            result_lines.append(line.strip())  # 如果没有 "(("，直接加入结果
    
    return result_lines

# 定义歌词时间戳处理函数
def process_lyrics(input_lines):
    """
    处理歌词行，生成包含 [start, duration] 和每个单词时间戳的格式化内容。
    忽略已经包含 [start, duration] 的行。

    Args:
        input_lines (list): 每行歌词的列表。

    Returns:
        list: 格式化后的歌词行。
    """
    result_lines = []

    for line in input_lines:
        # 检查是否已经有 [start, duration]
        if re.match(r'\[\d+,\d+\]', line):
            result_lines.append(line)
            continue

        # 提取行内的时间戳
        matches = re.findall(r'\((\d+),(\d+)\)', line)
        if not matches:
            result_lines.append(line)
            continue  # 如果没有时间戳，保留原行

        # 计算每行的起始时间和总时长
        starts = [int(start) for start, duration in matches]
        durations = [int(duration) for start, duration in matches]
        total_start = min(starts)  # 起始时间为最小的start
        total_duration = max(starts[i] + durations[i] for i in range(len(starts))) - total_start  # 总时长

        # 拼接行的 [start, duration] 和原内容
        new_line = f"[{total_start},{total_duration}]{line}"
        result_lines.append(new_line)
    
    return result_lines

# 执行拆分与处理
split_lines = transform_text(input_text)
processed_lines = process_lyrics(split_lines)

# 输出结果
for line in processed_lines:
    print(line)
