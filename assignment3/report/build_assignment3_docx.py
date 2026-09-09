#!/usr/bin/env python3
"""Create a Word report with selected code cells, outputs, analysis, and charts."""
import json
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'A03_CT_hautv.287.docx'
NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
rels, media, body, image_no = [], [], [], 0

projects = [
 ('PHAN 1: DU DOAN BENH TIEU DUONG', 'diabetes', 'Du lieu lam sang, phan loai nguy co mac benh.',
  [('Tai du lieu', 'pd.read_csv', 'Shape: (100000, 9)', 'Du lieu co 8 dac trung va 1 nhan diabetes; kich thuoc du lieu du lon de danh gia tren tap test doc lap.'),
   ('Kiem tra missing values', 'isnull', 'Khong co missing values.', 'Khong can bu khuyet du lieu; pipeline co the chuyen sang kiem tra trung lap va phan bo nhan.'),
   ('Loai bo trung lap', 'duplicated', '3,854 dong trung lap; sau xu ly con 96,146 dong.', 'Loai mau trung lap han che model hoc lai mot quan sat va lam ket qua danh gia tin cay hon.'),
   ('Kham pha phan bo nhan', 'value_counts', 'Lop 0: 87,664 | Lop 1: 8,482 | Ty le lop 1: 8.82%.', 'Nhan bi mat can bang; Recall, F1-score va AUC-ROC quan trong hon Accuracy don le.'),
   ('Tach tap va chuan hoa', 'StandardScaler', 'Train/Validation/Test duoc tach; scaler fit tren train.', 'Chuan hoa giup gradient on dinh va tranh ro ri du lieu tu validation/test.'),
   ('Logistic Regression', 'LogisticRegression', 'Accuracy 88.46% | Recall 87.34% | AUC-ROC 0.9591.', 'Baseline tuyen tinh co Recall tot nhung F1-score thap hon Random Forest.'),
   ('Random Forest', 'RandomForestClassifier', 'Accuracy 91.91% | F1-score 0.6515 | AUC-ROC 0.9740.', 'Ensemble cay quyet dinh dat hieu nang tong the tot nhat tren du lieu bang.'),
   ('Kien truc MLP', 'nn.Sequential', 'MLP: 8 -> 64 -> 32 -> 2.', 'Cac tang an hoc bieu dien phi tuyen cua dac trung lam sang.'),
   ('Can bang lop', 'SMOTE', 'SMOTE duoc ap dung tren tap train.', 'Tang kha nang phat hien lop thieu so ma khong lam thay doi tap test.'),
   ('Danh gia MLP', 'accuracy_score', 'MLP: Accuracy 89.48% | Recall 88.36% | F1 0.5971 | AUC 0.9718.', 'MLP co Recall cao, huu ich khi uu tien han che bo sot ca nguy co benh.')],
  ROOT/'diabetes/models/fig_model_comparison.png'),
 ('PHAN 2: DU DOAN GIA NHA VIET NAM', 'house_price', 'Hoi quy gia bat dong san tu vi tri va ket cau nha.',
  [('Tai du lieu', 'pd.read_csv', 'Du lieu VN housing duoc nap thanh DataFrame.', 'Moi dong la mot tin dang bat dong san voi cac dac trung vi tri, dien tich va phap ly.'),
   ('Bien doi gia muc tieu', 'LogPrice', 'LogPrice = log(1 + TotalPrice).', 'Log-transform giam do lech phai cua gia nha va lam qua trinh hoc on dinh hon.'),
   ('Ma hoa va tach tap', 'get_dummies', 'One-hot District, House_Type, Legal_Status; tach 70/15/15.', 'Ma hoa danh muc khong ap dat thu tu gia; scaler chi fit tren train.'),
   ('Chuan hoa', 'StandardScaler', 'Train, Validation, Test duoc transform bang cung scaler.', 'Cac dac trung co cung thang do truoc khi dua vao Ridge va MLP.'),
   ('Ridge Regression', 'Ridge', 'MAE 1,662.7 tr VND | R2 < 0.', 'Mo hinh tuyen tinh khong bat duoc quan he phi tuyen va ngoai lai gia.'),
   ('Decision Tree', 'DecisionTreeRegressor', 'MAE 1,401.0 tr VND | R2 = 0.5509.', 'Cay quyet dinh mo hinh hoa duoc nguong va tuong tac dac trung.'),
   ('Random Forest', 'RandomForestRegressor', 'MAE 1,320.2 tr VND | RMSE 2,870.5 tr VND | R2 = 0.6094.', 'Random Forest la ket qua tot nhat trong thuc nghiem hoi quy.'),
   ('Kien truc MLP', 'nn.Sequential', 'MLP du bao mot gia tri LogPrice.', 'BatchNorm va Dropout ho tro tong quat hoa cho mang hoi quy.'),
   ('Toi uu AdamW', 'AdamW', 'AdamW va log-target duoc dung trong qua trinh huan luyen.', 'Loss hoi tu on dinh hon so voi SGD tren gia tri gia tho.'),
   ('Danh gia MLP', 'mean_absolute_error', 'MLP: MAE 1,646.3 tr VND | R2 = -40.92.', 'Deep Learning nhay cam voi ngoai lai; khong mac dinh vuot Random Forest tren du lieu bang.')],
  ROOT/'house_price/models/fig_hp_model_comparison.png'),
 ('PHAN 3: PHAN TICH DANH GIA KHACH HANG', 'customer_behavior', 'Phan loai noi dung danh gia thanh khuyen nghi va khong khuyen nghi.',
  [('Tai du lieu van ban', 'pd.read_csv', 'Du lieu gom review, rating va thong tin san pham.', 'ReviewText la dau vao chinh; Recommended IND la nhan phan loai.'),
   ('Lam sach text', 'dropna', 'Loai cac dong khong co noi dung review.', 'Chi giu mau hop le de vector hoa van ban khong sinh chuoi rong.'),
   ('Tach va TF-IDF', 'TfidfVectorizer', 'TF-IDF toi da 3,000 dac trung; tach Train/Val/Test co stratify.', 'TF-IDF bien text thanh vector so thua, giu tu quan trong va giam anh huong tu qua pho bien.'),
   ('Luu vectorizer', 'joblib.dump', 'Da luu tfidf_vectorizer.pkl va cac tap du lieu.', 'Web deployment dung lai dung vectorizer da fit tren train, bao dam nhat quan dac trung.'),
   ('Naive Bayes', 'MultinomialNB', 'Accuracy 85.36% | F1-score 0.9173 | AUC 0.9222.', 'Baseline nhanh, phu hop vector khong am, nhung thua Logistic Regression.'),
   ('Logistic Regression', 'LogisticRegression', 'Accuracy 88.63% | F1-score 0.9332 | AUC 0.9331.', 'Day la model tot nhat tren khong gian TF-IDF thua.'),
   ('Random Forest', 'RandomForestClassifier', 'Accuracy 82.00% | F1-score 0.9010.', 'Cay ensemble kem phu hop voi vector TF-IDF co so chieu cao.'),
   ('Text MLP', 'CustomImprovedTextMLP', 'MLP: 3000 -> 128 -> 32 -> 2; BatchNorm va Dropout.', 'Kien truc hoc bieu dien tu vector TF-IDF; regularization giam overfitting.'),
   ('Hu an luyen AdamW', 'optim.AdamW', 'AdamW, weight decay 1e-4, 15 epochs.', 'AdamW hoi tu nhanh hon SGD tren khong gian text thua.'),
   ('Danh gia MLP', 'f1_score', 'MLP: Accuracy 86.98% | Precision 92.38% | F1 0.9202.', 'MLP cai tien tot hon model mau, nhung Logistic Regression van la lua chon tong the tot nhat.')],
  ROOT/'customer_behavior/models/fig_model_comparison.png')]

def p(text='', style=None, bold=False, code=False, page=False):
    props = '<w:pPr>' + (f'<w:pStyle w:val="{style}"/>' if style else '') + ('<w:pageBreakBefore/>' if page else '') + '</w:pPr>'
    rpr = '<w:rPr>' + ('<w:b/>' if bold else '') + ('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>' if code else '') + ('<w:sz w:val="18"/>' if code else '') + '</w:rPr>'
    lines = escape(text).split('\n')
    content = '<w:br/>'.join(f'<w:t xml:space="preserve">{line}</w:t>' for line in lines)
    body.append(f'<w:p {NS}>{props}<w:r>{rpr}{content}</w:r></w:p>')

def picture(path, caption, cx=5486400, cy=3086100):
    global image_no
    if not path.exists(): return
    image_no += 1; rid = f'rId{image_no}'; target = f'media/image{image_no}.png'
    media.append((path, target)); rels.append((rid, target));
    drawing = f'''<w:p {NS}><w:r><w:drawing><wp:inline xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{image_no}" name="Chart {image_no}"/><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic><pic:nvPicPr/><pic:blipFill><a:blip r:embed="{rid}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''
    body.append(drawing); p(caption, 'Caption')

def find_code(folder, keyword):
    for nb in sorted((ROOT/'assignment3'/folder/'notebook').glob('*.ipynb')):
        data = json.loads(nb.read_text(encoding='utf-8'))
        for c in data['cells']:
            s = ''.join(c.get('source', []))
            if c.get('cell_type') == 'code' and keyword.lower() in s.lower():
                return '\n'.join(s.strip().splitlines()[:22])
    return '# Cell code is in the corresponding notebook.'

p('BAO CAO MON HOC', 'Title', bold=True)
p('PHAT TRIEN CAC HE THONG THONG MINH', 'Title', bold=True)
p('ASSIGNMENT 03', 'Title', bold=True)
p('\nHo ten: Tran Van Hau\nMa sinh vien: B23DCCN287\nLop: D23CTPM01-B\nGiang vien: PGS. TS. Tran Dinh Que', 'Normal')
p('\nHa Noi - 2026', 'Normal')
p('MUC TIEU BAO CAO', 'Heading1', page=True)
p('Bao cao trinh bay ba du an. Moi cell duoc chon co code, output va phan tich; cac cell sinh bieu do deu duoc chen anh output tu thu muc models.', 'Normal')

for title, folder, intro, records, chart in projects:
    p(title, 'Heading1', page=True); p(intro, 'Normal')
    p('Cac cell duoc chon theo luong: tai du lieu -> tien xu ly -> mo hinh ML -> Deep Learning -> danh gia.', 'Normal')
    for n, (topic, key, output, analysis) in enumerate(records, 1):
        p(f'{n}. {topic}', 'Heading2')
        p('CELL CODE', 'Heading3', bold=True)
        p(find_code(folder, key), 'Code', code=True)
        p('OUTPUT', 'Heading3', bold=True)
        p(output, 'Normal')
        p('PHAN TICH THONG TIN RUT RA', 'Heading3', bold=True)
        p(analysis, 'Normal')
        if n in (4, 7, 10): picture(chart, f'Bieu do output cua {title}: ket qua EDA/so sanh mo hinh.')
    p('KET LUAN PHAN', 'Heading2', page=True)
    p('Ket qua can duoc doc dong thoi voi metric va bieu do. Model duoc chon de deploy la model co metric phu hop muc tieu bai toan, khong chi don thuan la mo hinh phuc tap nhat.', 'Normal')

p('DEPLOY', 'Heading1', page=True)
p('Anh chup giao dien web desktop va responsive mobile cho ba ung dung da nap artifact duoc huan luyen.', 'Normal')
for title, folder, intro, records, chart in projects:
    p(f'DEPLOY - {title}', 'Heading2', page=True)
    key = {'diabetes': 'diabetes', 'house_price': 'house_price', 'customer_behavior': 'customer_behavior'}[folder]
    picture(ROOT/'report'/'screenshots'/f'{key}_web_result.png', f'Giao dien web desktop: {title}.')
    picture(ROOT/'report'/'screenshots'/f'{key}_mobile_result.png', f'Giao dien responsive mobile: {title}.', 2100000, 4540000)

sect = '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/></w:sectPr>'
doc = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {NS} xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><w:body>{''.join(body)}{sect}</w:body></w:document>'''
styles = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {NS}><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="240"/></w:pPr><w:rPr><w:b/><w:sz w:val="34"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="Heading 1"/><w:rPr><w:b/><w:sz w:val="30"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="Heading 2"/><w:rPr><w:b/><w:sz w:val="27"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="Heading 3"/><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:pPr><w:shd w:fill="F1F5F9"/><w:spacing w:after="120"/></w:pPr><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="Caption"/><w:pPr><w:jc w:val="center"/></w:pPr><w:rPr><w:i/><w:sz w:val="20"/></w:rPr></w:style></w:styles>'''
content_types = '''<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>'''
root_rels = '''<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'''
doc_rels = ['<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">', '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
doc_rels += [f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{target}"/>' for rid, target in rels]
doc_rels.append('</Relationships>')
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', content_types); z.writestr('_rels/.rels', root_rels)
    z.writestr('word/document.xml', doc); z.writestr('word/styles.xml', styles)
    z.writestr('word/_rels/document.xml.rels', ''.join(doc_rels))
    for source, target in media: z.write(source, 'word/' + target)
print(f'Created {OUT}')
