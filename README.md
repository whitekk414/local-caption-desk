# Local Caption Desk · 本地字幕台

把一段采访、课程录像或语音备忘录转成可导入播放器的 SRT 字幕和方便检索的 TXT 文稿。识别在自己的电脑上运行，使用 OpenAI Whisper 开源模型，无需 API 密钥。

## 安装

准备 Python 3.11 和 [FFmpeg](https://ffmpeg.org/download.html)。在终端运行 `ffmpeg -version` 确认可以找到解码器。在本项目目录创建独立环境并安装依赖。

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

在 macOS 或 Linux 上，将命令中的 `.\.venv\Scripts\python` 替换为 `.venv/bin/python`。

## 转写

```powershell
.\.venv\Scripts\python caption.py "采访.mp4" --language zh --out "字幕"
```

完成后打开终端打印的目录。示例会生成 `字幕/采访-captions/transcript.srt` 与 `transcript.txt`，均为 UTF-8。将 SRT 拖入播放器即可查看时间轴。再次转写同名文件时，输出目录自动加编号。

默认使用 CPU 和多语种 `base` 模型。首次使用指定的模型名时会联网下载权重，之后复用本机缓存。也可以通过 `--model "模型/base.pt"` 指定预先下载的 Whisper 权重，在离线环境使用。已安装支持 CUDA 的 PyTorch 时，可以加 `--device cuda`。

省略 `--language` 可自动检测语言。输入可以是 FFmpeg 能够解码且包含音轨的音频或视频。识别结果按片段组织，人名、数字和重叠讲话建议对照原音校对。

## 依赖

[OpenAI Whisper](https://github.com/openai/whisper) 负责语音识别，[FFmpeg](https://ffmpeg.org/) 负责解码音轨。项目代码采用 MIT 许可证。
