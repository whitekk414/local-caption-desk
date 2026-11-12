"""Generate local transcripts with OpenAI Whisper."""

import argparse
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory


def timestamp(seconds):
    milliseconds = max(0, round(seconds * 1000))
    hours, rest = divmod(milliseconds, 3600000)
    minutes, rest = divmod(rest, 60000)
    seconds, millis = divmod(rest, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"


def export(media, destination, segments):
    with TemporaryDirectory(prefix=".captions-", dir=destination) as staging:
        folder = Path(staging)
        srt = folder / "transcript.srt"
        txt = folder / "transcript.txt"
        with srt.open("w", encoding="utf-8") as subtitles, txt.open("w", encoding="utf-8") as transcript:
            count = 0
            for segment in segments:
                line = segment["text"].strip()
                if not line:
                    continue
                count += 1
                interval = f'{timestamp(segment["start"])} --> {timestamp(segment["end"])}'
                subtitles.write(f"{count}\n{interval}\n{line}\n\n")
                transcript.write(line + "\n")
        # Publish both files together and preserve earlier exports.
        for version in range(1, sys.maxsize):
            name = f"{media.stem}-captions"
            if version > 1:
                name += f"-{version}"
            target = destination / name
            if target.exists():
                continue
            try:
                folder.rename(target)
            except OSError:
                if target.exists():
                    continue
                raise
            return target


def main():
    parser = argparse.ArgumentParser(description="在本机将录音或视频转成 SRT 字幕与 TXT 文稿")
    parser.add_argument("media", type=Path, help="音频或视频文件")
    parser.add_argument("--out", type=Path, help="输出父目录，默认与输入文件同目录")
    parser.add_argument("--model", default="base", help="Whisper 模型名或本地 .pt 文件")
    parser.add_argument("--language", help="语言代码，如 zh 或 en，默认自动识别")
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    args = parser.parse_args()
    if not args.media.is_file():
        parser.error(f"找不到文件 {args.media}")
    if not shutil.which("ffmpeg"):
        parser.error("请先安装 FFmpeg 并将 ffmpeg 加入 PATH")
    try:
        import whisper
        model = whisper.load_model(args.model, device=args.device)
        result = model.transcribe(str(args.media), language=args.language, fp16=args.device == "cuda")
        destination = args.out or args.media.parent
        destination.mkdir(parents=True, exist_ok=True)
        target = export(args.media, destination, result["segments"])
    except (ImportError, OSError, RuntimeError, ValueError, KeyError) as error:
        parser.exit(1, f"转写失败：{error}\n")
    print(target.resolve())


if __name__ == "__main__":
    main()
