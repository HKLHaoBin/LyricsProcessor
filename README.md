# LyricsProcessor - 处理QRC歌词的背景人声歌词与其他歌词在同一行的情况

A GitHub Actions workflow that processes lyrics with timestamps provided in GitHub Issues and posts the processed results as comments.

一个 GitHub Actions 工作流，用于处理 GitHub Issue 中提供的带时间戳的歌词，并将处理结果以评论的形式发布。

---

## Features | 功能

- Extracts input text from a GitHub Issue.  
  从 GitHub Issue 中提取输入文本。
- Processes text to add `[start, duration]` format for timestamped lyrics.  
  处理文本，生成带 `[start, duration]` 格式的时间戳歌词。
- Posts the processed output as a comment in the same Issue.  
  将处理后的结果作为评论回复到同一 Issue。

---

## How to Use | 使用方法

### Trigger the Workflow | 触发工作流

1. Create a new Issue in your repository and include the text you want to process in the body.  
   在仓库中创建一个新的 Issue，并在正文中输入需要处理的文本。
2. Add any comment to the Issue to trigger the workflow.  
   在 Issue 中添加任意评论以触发工作流。
3. The workflow will process the input text and reply to the Issue with the formatted output.  
   工作流将处理输入的文本，并将格式化后的结果回复到该 Issue。

---

## Input Format | 输入格式

The input text should contain lyrics and optionally timestamps in the format `(start, duration)`. For example:  
输入文本应包含歌词，并可选带有时间戳，格式为 `(start, duration)`。例如：

```
Hello, world ((1000,500))
This is a test ((2000,600))
No timestamps here
```

---

## Output Format | 输出格式

The output will include a `[start, duration]` format for each line with timestamps. For example:  
输出结果将包含每行时间戳的 `[start, duration]` 格式。例如：

```
[1000,1500]Hello, world ((1000,500))
[2000,2600]This is a test ((2000,600))
No timestamps here
```

---

## File Structure | 文件结构

```
.
├── .github/
│   └── workflows/
│       └── main.yml         # GitHub Actions workflow | GitHub Actions 工作流
├── process_lyrics.py        # Python script for text processing | 处理文本的 Python 脚本
└── README.md                # Documentation | 文档
```

---

## Contributing | 贡献

Contributions are welcome! If you have any suggestions, please open an Issue or submit a pull request.  
欢迎贡献代码或意见！如果有任何建议，请提交 Issue 或 Pull Request。

---

## License | 许可

This project is licensed under the MIT License.
本项目基于 MIT 许可证。
