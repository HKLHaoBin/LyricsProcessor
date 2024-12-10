import re
from github import Github
import os

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

def main():
    # 从环境变量中获取 Issue 内容
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    issue_number = int(os.getenv("ISSUE_NUMBER"))

    g = Github(token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(number=issue_number)

    # 获取 Issue 内容
    input_text = issue.body

    # 处理歌词
    split_lines = transform_text(input_text)
    processed_lines = process_lyrics(split_lines)

    # 生成评论内容
    result = "\n".join(processed_lines)
    issue.create_comment(f"处理后的歌词内容：\n```\n{result}\n```")

if __name__ == "__main__":
    main()
