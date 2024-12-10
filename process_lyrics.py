import os
import re
from github import Github

# 定义文本拆分与处理函数
def transform_text(input_text):
    lines = input_text.split("\n")
    result_lines = []

    for line in lines:
        parts = re.split(r'(\(\()', line, maxsplit=1)
        if len(parts) == 3:
            prefix = parts[0].strip()
            rest = parts[1] + parts[2]
            result_lines.append(prefix)
            result_lines.append(rest)
        else:
            result_lines.append(line.strip())
    
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
            continue

        starts = [int(start) for start, duration in matches]
        durations = [int(duration) for start, duration in matches]
        total_start = min(starts)
        total_duration = max(starts[i] + durations[i] for i in range(len(starts))) - total_start

        new_line = f"[{total_start},{total_duration}]{line}"
        result_lines.append(new_line)
    
    return result_lines

# 获取环境变量
github_token = os.getenv("GITHUB_TOKEN")
issue_number = os.getenv("ISSUE_NUMBER")
repository_name = os.getenv("GITHUB_REPOSITORY")

# 初始化 GitHub 客户端
g = Github(github_token)
repo = g.get_repo(repository_name)
issue = repo.get_issue(int(issue_number))

# 从 Issue 中获取内容
input_text = issue.body

# 处理歌词
split_lines = transform_text(input_text)
processed_lines = process_lyrics(split_lines)

# 生成评论内容
output_text = "\n".join(processed_lines)

# 发布评论
issue.create_comment(f"处理结果：\n```\n{output_text}\n```")
