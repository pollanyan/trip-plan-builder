#!/usr/bin/env python3
"""图片规范化：统一比例(模糊填充不裁切) + 可选 base64 内嵌。

用法：
  # 统一大图/小图比例（原地覆盖，模糊填充保留完整画面）
  python3 normalize_images.py --dir <图片目录> --big 22:10 --small 16:9

  # 精确指定大图文件名（推荐，避免按名称猜测出错）
  python3 normalize_images.py --dir <目录> --big 22:10 --small 16:9 --big-files "春海湾_招牌菜整桌.webp,人才公园_航拍全景.webp"

  # 只列出目录内图片尺寸
  python3 normalize_images.py --dir <目录> --list

  # 输出某图为 data URI（供 HTML 内嵌）
  python3 normalize_images.py --data-uri <图片路径>

设计要点（来自实战）：
- 绝不用 object-fit:cover 硬裁用户照片，"为了缩小而裁边"会严重破坏观感。
- 正确做法：在文件层面把素材画布归一化到目标比例，用高斯模糊的同图做底、
  前景按比例完整缩放居中，空白由模糊底自然填充。随后 CSS 用 cover 即不裁内容、无白边。
"""
import argparse, base64, os, sys
from PIL import Image, ImageFilter

EXTS = ('.webp', '.png', '.jpg', '.jpeg')


def normalize(path, ratio_w, ratio_h, quality=86):
    im = Image.open(path).convert('RGB')
    w, h = im.size
    # 完整放入目标比例所需的画布尺寸（由原图较短边决定）
    if w / h > ratio_w / ratio_h:
        cw, ch = int(h * ratio_w / ratio_h), h
    else:
        cw, ch = w, int(w * ratio_h / ratio_w)
    canvas = Image.new('RGB', (cw, ch))
    bg = im.copy()
    scale = max(cw / w, ch / h)
    bg = bg.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
    bx, by = (bg.width - cw) // 2, (bg.height - ch) // 2
    bg = bg.crop((bx, by, bx + cw, by + ch)).filter(
        ImageFilter.GaussianBlur(max(8, cw // 22))
    )
    canvas.paste(bg, (0, 0))
    fscale = min(cw / w, ch / h)
    fg = im.resize((max(1, int(w * fscale)), max(1, int(h * fscale))), Image.LANCZOS)
    canvas.paste(fg, ((cw - fg.width) // 2, (ch - fg.height) // 2))
    canvas.save(path, 'WEBP', quality=quality, method=6)
    return (w, h), (cw, ch)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', help='图片目录')
    ap.add_argument('--big', help='大图比例 如 22:10')
    ap.add_argument('--small', help='小图比例 如 16:9')
    ap.add_argument('--big-files', help='按文件名精确指定哪些是大图，逗号分隔；未列出的按小图处理')
    ap.add_argument('--list', action='store_true', help='列出尺寸')
    ap.add_argument('--data-uri', help='输出该图的 data URI')
    ap.add_argument('--quality', type=int, default=86)
    a = ap.parse_args()

    if a.data_uri:
        raw = open(a.data_uri, 'rb').read()
        print('data:image/webp;base64,' + base64.b64encode(raw).decode())
        return

    if not a.dir:
        ap.error('需要 --dir 或 --data-uri')

    files = sorted(f for f in os.listdir(a.dir) if f.lower().endswith(EXTS))
    if a.list or (not a.big and not a.small):
        for f in files:
            im = Image.open(os.path.join(a.dir, f))
            print(f'{f}\t{im.size[0]}x{im.size[1]}')
        return

    def parse(r):
        x, y = r.split(':')
        return int(x), int(y)

    big_names = set(x.strip() for x in a.big_files.split(',')) if a.big_files else set()
    for f in files:
        path = os.path.join(a.dir, f)
        is_big = (f in big_names) if big_names else (
            '全景' in f or '航拍' in f or '大楼招牌' in f
        )
        if a.big and is_big:
            before, after = normalize(path, *parse(a.big), a.quality)
        elif a.small:
            before, after = normalize(path, *parse(a.small), a.quality)
        else:
            continue
        print(f'{f}\t{before[0]}x{before[1]} -> {after[0]}x{after[1]}')


if __name__ == '__main__':
    main()
