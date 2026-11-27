# -*- coding: utf-8 -*-
"""
MASTER MARKDOWN REPORT BUILDER
Assembles the complete master final term paper in Markdown format directly
from the enhanced chapter modules to guarantee 100% parity with the Word DOCX report.
Author: Tran Van Hau (B23DCCN287)
"""

import sys
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

# Import section modules
from sec_mo_dau import add_mo_dau
from sec_chap1_history import add_chap1_history
from sec_chap2_ml_basic import add_chap2_ml_basic
from sec_chap3_cnn import add_chap3_cnn
from sec_chap4_rnn import add_chap4_rnn
from sec_chap5_kg_rag import add_chap5_kg_rag
from sec_chap6_deep_graph import add_chap6_deep_graph
from sec_chap7_multi_agent import add_chap7_multi_agent
from sec_conclusion_and_appendix import add_conclusion_and_appendix

ROOT = Path("c:/code/A2_CT_hautv.287").resolve()
FINAL_DIR = ROOT / "tieuluan_final"
MD_OUT = FINAL_DIR / "tieuluan_final_CT_09_Hautv.287.md"


class MarkdownCollector:
    def __init__(self):
        self.lines = []

    def add(self, text=""):
        self.lines.append(text)

    def get_content(self):
        return "\n".join(self.lines)


class DummyParagraph:
    def __init__(self, collector):
        self.collector = collector
        self.paragraph_format = type('obj', (), {'space_after': 0, 'line_spacing': 0, 'left_indent': 0, 'first_line_indent': 0})

    def add_run(self, text=""):
        self.collector.add(f"{text.strip()}\n")
        return type('obj', (), {'font': type('f', (), {'name': '', 'size': 0})})


class DummyDoc:
    def __init__(self, collector):
        self.collector = collector

    def add_page_break(self):
        self.collector.add("\n---\n")

    def add_paragraph(self, text=""):
        p = DummyParagraph(self.collector)
        if text:
            p.add_run(text)
        return p


collector = MarkdownCollector()
dummy_doc = DummyDoc(collector)


def h_chap(doc, text):
    collector.add(f"\n\n---\n\n# {text}\n")


def h_sec(doc, text):
    collector.add(f"\n## {text}\n")


def h_sub(doc, text):
    collector.add(f"\n### {text}\n")


def p_body(doc, text="", bold=False, italic=False, color=None, space_after=5, align=None):
    if not text:
        return
    t = text.strip()
    if bold:
        t = f"**{t}**"
    if italic:
        t = f"*{t}*"
    collector.add(f"{t}\n")


def p_bullet(doc, text, bold_prefix="", level=0):
    indent = "  " * level
    if bold_prefix:
        collector.add(f"{indent}- **{bold_prefix.strip()}** {text.strip()}")
    else:
        collector.add(f"{indent}- {text.strip()}")


def add_math(doc, formula_text, display=True):
    f = formula_text.strip()
    if display:
        collector.add(f"\n$$\n{f}\n$$\n")
    else:
        collector.add(f"${f}$")


def add_table_data(doc, headers, rows, widths=None, caption=None):
    if caption:
        collector.add(f"\n**{caption}**\n")
    collector.add("| " + " | ".join(str(h) for h in headers) + " |")
    collector.add("| " + " | ".join([":---" for _ in headers]) + " |")
    for r in rows:
        collector.add("| " + " | ".join(str(cell).replace("\n", " ") for cell in r) + " |")
    collector.add("\n")


def add_figure(doc, img_path, caption="", width=5.6):
    img_rel = Path(img_path).as_posix()
    if caption:
        collector.add(f"\n<div align=\"center\">\n\n![{caption}](../{img_rel})\n\n*{caption}*\n\n</div>\n")
    else:
        collector.add(f"\n<div align=\"center\">\n\n![Figure](../{img_rel})\n\n</div>\n")


def add_code_block(doc, code_str, title=""):
    collector.add(f"\n```python\n# {title}\n{code_str.strip()}\n```\n")


def generate_markdown():
    print("==================================================")
    print("STARTING BUILD MASTER FINAL TERM PAPER MARKDOWN")
    print("==================================================")

    # 1. Front Matter
    collector.add(r"""# BÁO CÁO TIỂU LUẬN FINAL MÔN HỌC
# PHÁT TRIỂN HỆ THỐNG THÔNG MINH

<div align="center">

### HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG (PTIT)
### KHOA CÔNG NGHỆ THÔNG TIN 1
———————o0o———————

<img src="../agent/ptit_logo.png" alt="PTIT Logo" width="160"/>

## ĐỀ TÀI:
# NGHIÊN CỨU VÀ PHÁT TRIỂN HỆ THỐNG THÔNG MINH TOÀN DIỆN:
## TỪ HỌC MÁY CƠ BẢN, CNN, RNN–LSTM ĐẾN KNOWLEDGE GRAPH, DEEP GRAPH VÀ HỆ ĐA TÁC TỬ TỰ CHỦ
*(Dual Domains: Hệ Y tế Chuyển hóa & Hệ Tài chính Định lượng)*

| Thuộc tính | Chi tiết thông tin |
| :--- | :--- |
| **Giảng viên hướng dẫn:** | **PGS. TS. Trần Đình Quế** |
| **Sinh viên thực hiện:** | **Trần Văn Hậu** |
| **Mã sinh viên:** | **B23DCCN287** |
| **Lớp chuyên ngành:** | **D23CTPM01** |
| **Nhóm môn học:** | **CT** |
| **Nhóm tiểu luận:** | **09** |
| **Địa điểm & Thời gian:** | Hà Nội, Tháng 11 Năm 2026 |

</div>

---

## LỜI CAM ĐOAN VÀ LỜI CẢM ƠN

Tôi xin cam đoan đây là công trình nghiên cứu và thực nghiệm độc lập của bản thân tôi — sinh viên **Trần Văn Hậu**, dưới sự giảng dạy, định hướng và hướng dẫn khoa học tận tình của **PGS. TS. Trần Đình Quế**. Toàn bộ các kết quả thực nghiệm, số liệu phân tích trong các bảng biểu, các đồ thị trực quan hóa không gian ẩn, các ma trận nhầm lẫn và kết quả đo đạc kiểm chứng chéo (cross-validation) trong báo cáo này đều được tính toán và trích xuất trực tiếp từ các mã nguồn, tập dữ liệu thực tế và các kịch bản chạy thật của bản thân tôi trong suốt quá trình học tập môn học Phát triển Hệ thống Thông minh.

Mọi thông tin, tri thức tham khảo, các định lý toán học, các kiến trúc kinh điển của các nhà khoa học tiền bối (như Alan Turing, Yann LeCun, Thomas Kipf, Ashish Vaswani...) đều được dẫn chiếu nguồn gốc minh bạch, đầy đủ theo đúng chuẩn học thuật quốc tế IEEE.

Tôi xin gửi lời tri ân sâu sắc nhất tới **PGS. TS. Trần Đình Quế** — người thầy đã truyền thụ cho chúng tôi tư duy hệ thống mạch lạc, phương pháp luận nghiên cứu sâu sắc: *"Hiểu bản chất toán học, biểu diễn tường minh thông tin, học từ dữ liệu thực tế và hiện thực hóa thành ứng dụng hoàn chỉnh có thể kiểm chứng được"*. Nhờ những lời chỉ dẫn quý báu, những yêu cầu khắt khe về tính đúng đắn khoa học và kiểm chứng tương đương, tôi đã hoàn thiện được công trình tiểu luận tổng hợp này với tất cả niềm đam mê nghiên cứu khoa học công nghệ.

<div align="right">
<i>Hà Nội, tháng 11 năm 2026</i><br/>
<b>Sinh viên thực hiện</b><br/><br/>
<b>Trần Văn Hậu — B23DCCN287</b>
</div>

---

## DANH MỤC TỪ VIẾT TẮT

| Ký hiệu | Tên tiếng Anh đầy đủ | Ý nghĩa / Diễn giải tiếng Việt |
| :--- | :--- | :--- |
| **AI** | Artificial Intelligence | Trí tuệ Nhân tạo |
| **ML** | Machine Learning | Học máy |
| **DL** | Deep Learning | Học sâu |
| **ANN / MLP** | Artificial Neural Network / Multilayer Perceptron | Mạng nơ-ron nhân tạo / Mạng nơ-ron truyền thẳng nhiều lớp |
| **CNN** | Convolutional Neural Network | Mạng nơ-ron tích chập (chuyên xử lý dữ liệu lưới không gian / ảnh) |
| **RNN** | Recurrent Neural Network | Mạng nơ-ron hồi quy (chuyên xử lý dữ liệu chuỗi tuần tự / thời gian) |
| **LSTM** | Long Short-Term Memory | Mạng nơ-ron bộ nhớ dài - ngắn hạn có cơ chế cổng điều khiển |
| **GRU** | Gated Recurrent Unit | Đơn vị hồi quy có cổng (phiên bản tinh gọn của LSTM) |
| **BPTT** | Backpropagation Through Time | Thuật toán lan truyền ngược qua thời gian trong mạng hồi quy |
| **Grad-CAM** | Gradient-weighted Class Activation Mapping | Bản đồ kích hoạt lớp có trọng số gradient để giải thích trực quan CNN |
| **KG** | Knowledge Graph | Đồ thị tri thức (biểu diễn tri thức dưới dạng các bộ ba thực thể - quan hệ) |
| **RAG** | Retrieval-Augmented Generation | Sinh văn bản tăng cường bằng truy xuất tri thức có căn cứ |
| **RRF** | Reciprocal Rank Fusion | Thuật toán hợp nhất thứ hạng nghịch đảo cho truy hồi lai Hybrid |
| **GNN** | Graph Neural Network | Mạng nơ-ron đồ thị (học sâu trên dữ liệu cấu trúc phi Euclid) |
| **GCN** | Graph Convolutional Network | Mạng tích chập đồ thị (biến đổi Fourier trên phổ Laplacian chuẩn hóa) |
| **GraphSAGE** | Sample and Aggregate | Khung lấy mẫu và gộp quy nạp cho mạng nơ-ron đồ thị |
| **GAT** | Graph Attention Network | Mạng chú ý đồ thị (cơ chế tự chú ý gán trọng số cho từng cạnh liên kết) |
| **MPNN** | Message Passing Neural Network | Khung truyền thông điệp tổng quát hóa cho các mạng nơ-ron đồ thị |
| **1-WL** | 1-Weisfeiler-Lehman Test | Phép thử đẳng cấu đồ thị xác định giới hạn biểu diễn của GNN |
| **MAD** | Mean Average Distance | Khoảng cách trung bình giữa các nút (thước đo hiện tượng làm trơn quá mức) |
| **MAS** | Multi-Agent Systems | Hệ đa tác tử (hệ thống gồm nhiều tác tử phần mềm phối hợp/đối kháng) |
| **MARL** | Multi-Agent Reinforcement Learning | Học tăng cường đa tác tử |
| **LLM** | Large Language Model | Mô hình ngôn ngữ lớn (như GPT-4, Qwen, Llama, Gemini) |
| **PEAS** | Performance, Environment, Actuators, Sensors | Mô hình đặc tả chuẩn cho hệ thống tác tử thông minh |
| **EDA** | Exploratory Data Analysis | Phân tích và khám phá dữ liệu |
| **ROC-AUC** | Receiver Operating Characteristic - Area Under Curve | Diện tích dưới đường cong đặc trưng hoạt động bộ thu |
| **PR-AUC** | Precision-Recall Area Under Curve | Diện tích dưới đường cong độ chính xác - độ bao phủ |
| **CGM** | Continuous Glucose Monitoring | Hệ thống theo dõi nồng độ đường huyết liên tục (15 phút/lần) |
| **TF-IDF** | Term Frequency - Inverse Document Frequency | Tần suất từ - nghịch đảo tần suất tài liệu |
| **SGD** | Stochastic Gradient Descent | Thuật toán hạ gradient ngẫu nhiên |
| **GEMM** | General Matrix Multiply | Phép nhân ma trận tổng quát tối ưu hóa hiệu năng cao |

---
""")

    print("Adding MỞ ĐẦU...")
    add_mo_dau(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data)

    print("Adding CHƯƠNG 1 (Lịch sử phát triển AI)...")
    add_chap1_history(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("Adding CHƯƠNG 2 (Học máy cơ bản)...")
    add_chap2_ml_basic(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("Adding CHƯƠNG 3 (CNN, Grad-CAM)...")
    add_chap3_cnn(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("Adding CHƯƠNG 4 (RNN, LSTM, GRU)...")
    add_chap4_rnn(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("Adding CHƯƠNG 5 (Knowledge Graph & GraphRAG)...")
    add_chap5_kg_rag(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("Adding CHƯƠNG 6 (Deep Graph Learning, GCN & GAT)...")
    add_chap6_deep_graph(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("Adding CHƯƠNG 7 (Multi-Agent Systems)...")
    add_chap7_multi_agent(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    print("Adding KẾT LUẬN, TÀI LIỆU THAM KHẢO VÀ PHỤ LỤC...")
    add_conclusion_and_appendix(dummy_doc, h_chap, h_sec, h_sub, p_body, p_bullet, add_table_data, add_figure, add_code_block, add_math)

    md_text = collector.get_content()
    with open(MD_OUT, "w", encoding="utf-8") as f:
        f.write(md_text)

    print(f"Markdown successfully saved to: {MD_OUT}")
    print(f"Total lines: {len(md_text.splitlines())}")
    print(f"Total characters: {len(md_text)}")


if __name__ == "__main__":
    generate_markdown()
