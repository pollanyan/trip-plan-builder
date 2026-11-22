#!/usr/bin/env python3
"""把自包含 HTML（图片均为 data URI）打包成 MHTML，便于邮件/微信/离线分享。

用法：
  python3 mhtml_pack.py <input.html> [output.mhtml] [--title "标题"]

要点：
- 输入 HTML 必须是自包含的：所有图片用 data: URI 内嵌，无外链资源。
- Content-Location 用固定的 file:///TripPlan.html，MHTML 内部自洽。
- 同时保留 .html 与 .mhtml 两份交付：HTML 便于浏览器预览与再编辑，MHTML 便于单文件分享。
"""
import argparse, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from email import policy as ep


def pack(src, dst, title):
    html = open(src, encoding='utf-8').read()
    root = MIMEMultipart('related')
    root['Subject'] = title or os.path.splitext(os.path.basename(src))[0]
    root['Date'] = formatdate(localtime=True)
    root['MIME-Version'] = '1.0'
    alt = MIMEMultipart('alternative')
    part = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
    part['Content-Location'] = 'file:///TripPlan.html'
    alt.attach(part)
    root.attach(alt)
    with open(dst, 'wb') as f:
        f.write(root.as_bytes(policy=ep.default))
    print(f'MHTML 已生成: {dst} ({os.path.getsize(dst)} bytes)')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('dst', nargs='?')
    ap.add_argument('--title', default='')
    a = ap.parse_args()
    dst = a.dst or os.path.splitext(a.src)[0] + '.mhtml'
    pack(a.src, dst, a.title)


if __name__ == '__main__':
    main()
