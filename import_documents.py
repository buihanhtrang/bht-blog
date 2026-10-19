"""Convert the two original DOCX sources into static blog articles.

Run from this directory: python import_documents.py
Original documents are read only. Only public blog content and image assets are written.
"""
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import json
import re

ROOT = Path(__file__).resolve().parent
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}


def text(element):
    return ''.join(t.text or '' for t in element.findall('.//w:t', NS)).strip()


def read_document(path, images=False):
    with ZipFile(path) as archive:
        body = ET.fromstring(archive.read('word/document.xml')).find('w:body', NS)
        rels = ET.fromstring(archive.read('word/_rels/document.xml.rels'))
        targets = {r.attrib['Id']: r.attrib['Target'] for r in rels}
        lines = []
        image_count = 0
        for element in body:
            kind = element.tag.rsplit('}', 1)[-1]
            if kind == 'p':
                value = text(element)
                if value:
                    lines.append(value)
                if images:
                    for blip in element.findall('.//a:blip', NS):
                        target = targets[blip.attrib['{' + NS['r'] + '}embed']]
                        image_count += 1
                        name = 'dang-ky-hoc-tap-' + str(image_count) + Path(target).suffix
                        destination = ROOT / 'assets' / name
                        destination.parent.mkdir(exist_ok=True)
                        destination.write_bytes(archive.read('word/' + target))
                        caption = ['Khung kế hoạch học tập minh họa trong tài liệu',
                                   'Bảng theo dõi chương trình đào tạo minh họa',
                                   'Thông tin khối lượng học phần minh họa'][image_count - 1]
                        lines.append(f'![{caption}](assets/{name})')
            elif kind == 'tbl':
                rows = element.findall('w:tr', NS)
                # Convert the checklist table into readable headings and paragraphs.
                for row in rows[1:]:
                    cells = [text(c) for c in row.findall('w:tc', NS)]
                    if len(cells) >= 2:
                        lines.extend(['### ' + cells[0], cells[1]])
        return lines


registration = read_document(ROOT.parent / '1. Dang_ky_hoc_tap.docx', images=True)
headings = {'Đăng ký học phần', 'Trước khi đăng ký', 'Sau khi đăng ký', 'Một số lưu ý:'}
registration_body = [('## ' + line.rstrip(':')) if line in headings else line for line in registration[2:]]
posts = [{
    'id': 'dang-ky-hoc-phan',
    'title': 'Bài 1: Hướng dẫn đăng ký học phần cho sinh viên ETE16',
    'excerpt': 'Đăng ký học phần khác đăng ký lớp như thế nào? Cách lập kế hoạch, cân đối khối lượng học và kiểm tra kết quả đăng ký.',
    'category': 'Đăng ký học tập',
    'date': '2026-10-19',
    'source': '1. Dang_ky_hoc_tap.docx',
    'content': '\n\n'.join(registration_body)
}]

guide = read_document(ROOT.parent / 'Huong_dan_hoc_tap_ETE16.docx')
sections = []
for line in guide:
    match = re.match(r'^(\d) (.+)$', line)
    if match:
        sections.append({'number': int(match[1]), 'title': match[2], 'lines': []})
    elif sections:
        sections[-1]['lines'].append(line)

details = {
    2: ('hoc-tap-hieu-qua', 'Học tập', 'Đọc đề cương, duy trì lịch học và lưu lại sản phẩm để hiểu rõ mình đã học được gì sau mỗi học phần.'),
    3: ('do-an-mon-hoc-va-project', 'Đồ án & project', 'Xác định bài toán, phân công, kiểm thử và hoàn thành phiên bản cơ bản trước khi mở rộng project.'),
    4: ('nghien-cuu-khoa-hoc', 'Nghiên cứu', 'Tìm hiểu lab, liên hệ giảng viên và bắt đầu từ những nhiệm vụ nghiên cứu phù hợp với nền tảng của mình.'),
    5: ('do-an-tot-nghiep', 'Đồ án & project', 'Chuẩn bị hướng chuyên môn, giảng viên hướng dẫn, nguồn lực và tiến độ cho đồ án tốt nghiệp.'),
    6: ('tieng-anh-cong-cu-va-ai', 'Kỹ năng', 'Rèn tiếng Anh chuyên ngành, chọn công cụ thực hành và sử dụng AI có trách nhiệm trong học tập.'),
    7: ('thuc-tap-va-nghe-nghiep', 'Nghề nghiệp', 'Chuẩn bị CV, portfolio và kết nối nghề nghiệp từ năm 3, đồng thời cân đối với yêu cầu học tập.'),
    8: ('ra-soat-cuoi-hoc-ky', 'Học tập', 'Bộ câu hỏi tự kiểm tra về tín chỉ, kỹ năng, project và hướng đi trước khi đặt mục tiêu cho học kỳ tiếp theo.')
}
subheads = {'Tiếng Anh chuyên ngành', 'Công cụ thực hành', 'Sử dụng AI có trách nhiệm'}
for section in sections:
    if section['number'] == 1:
        # Retain the shorter source's additional advice alongside the detailed article.
        extra = next(line for line in section['lines'] if line.startswith('Lưu ý:'))
        posts[0]['content'] += '\n\n## Lưu ý thêm từ hướng dẫn học tập\n\n' + extra
        posts[0]['source'] += '; Huong_dan_hoc_tap_ETE16.docx (lưu ý bổ sung)'
        continue
    slug, category, excerpt = details[section['number']]
    content = ['## ' + line if line in subheads else line for line in section['lines']]
    posts.append({'id': slug, 'title': section['title'], 'excerpt': excerpt,
                  'category': category, 'date': '2026-10-19',
                  'source': 'Huong_dan_hoc_tap_ETE16.docx', 'content': '\n\n'.join(content)})

(ROOT / 'posts.json').write_text(json.dumps(posts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Imported {len(posts)} articles and 3 original illustrations.')
