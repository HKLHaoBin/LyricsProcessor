import os
import re
from github import Github

# 从环境变量中获取 GitHub Token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPOSITORY")
ISSUE_NUMBER = os.getenv("ISSUE_NUMBER")
if not ISSUE_NUMBER:
    raise ValueError("ISSUE_NUMBER environment variable is not set. Ensure the workflow passes the issue number.")

# 初始化 GitHub 客户端
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)
issue = repo.get_issue(int(ISSUE_NUMBER))
input_text = issue.body

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
    result_lines = []

    for line in input_lines:
        if re.match(r'\[\d+,\d+\]', line):
            result_lines.append(line)
            continue

        matches = re.findall(r'\((\d+),(\d+)\)', line)
        if not matches:
            result_lines.append(line)
            continue  # 如果没有时间戳，保留原行

        starts = [int(start) for start, duration in matches]
        durations = [int(duration) for start, duration in matches]
        total_start = min(starts)  # 起始时间为最小的start
        total_duration = max(starts[i] + durations[i] for i in range(len(starts))) - total_start  # 总时长

        new_line = f"[{total_start},{total_duration}]{line}"
        result_lines.append(new_line)
    
    return result_lines

# 执行拆分与处理
split_lines = transform_text(input_text)
processed_lines = process_lyrics(split_lines)

# 将结果发送为评论
result = "\n".join(processed_lines)
issue.create_comment(f"Processed Lyrics:\n\n```\n{result}\n```")
