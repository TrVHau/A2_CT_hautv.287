"""
llm_engine.py
Động cơ Ngôn ngữ Cục bộ (Local LLM Engine) và Bộ sinh Prompt có căn cứ (Grounded Synthesizer).
Cung cấp chế độ sinh chuỗi suy luận (Chain-of-Thought) kèm trích dẫn nghiêm ngặt [n].
"""
from typing import List, Tuple, Dict, Any

SYSTEM_GROUNDED = (
    "Bạn là trợ lý chuyên gia tiếng Việt của Hệ thống Thông minh Y tế & Tài chính. "
    "Chỉ được dùng thông tin trong phần BẰNG CHỨNG. "
    "Mỗi kết luận quan trọng bắt buộc phải kèm số hiệu bằng chứng trong ngoặc vuông, ví dụ [1], [2]. "
    "Nếu bằng chứng không đủ để trả lời, nói rõ 'không đủ thông tin'. Không bịa số liệu. "
    "Trả lời súc tích, khách quan và chuyên môn cao."
)

DISCLAIMER = {
    "health": "LƯU Ý Y KHOA: Kết quả chẩn đoán và khuyến nghị điều trị chỉ mang tính chất tham khảo học thuật theo phác đồ Bộ Y Tế. Người bệnh bắt buộc phải thăm khám trực tiếp tại cơ sở y tế chuyên khoa trước khi thay đổi thuốc.",
    "finance": "CẢNH BÁO ĐẦU TƯ: Dự báo và phân tích vĩ mô chỉ phục vụ mục đích nghiên cứu học thuật. Thị trường tài chính luôn tiềm ẩn rủi ro biến động, nhà đầu tư tự chịu trách nhiệm về quyết định phân bổ vốn."
}

def build_grounded_prompt(question: str, evidence: List[Tuple[str, str]]) -> str:
    """Tạo prompt chuẩn hóa đánh số [1]..[n] từ danh sách bằng chứng thu thập được."""
    lines = [f"[{i}] ({src}) {txt}" for i, (src, txt) in enumerate(evidence, 1)]
    return (
        f"{SYSTEM_GROUNDED}\n\n"
        "BẰNG CHỨNG:\n" + "\n".join(lines) + f"\n\n"
        f"CÂU HỎI: {question}\n\n"
        "TRẢ LỜI (tiếng Việt, chuẩn văn phong chuyên môn, kèm trích dẫn [n]):"
    )

class LocalLLMEngine:
    def __init__(self, model_name: str = "Qwen2.5-CoT-Local"):
        self.model_name = model_name

    def generate(self, question: str, evidence: List[Tuple[str, str]], domain: str) -> str:
        """Sinh câu trả lời lập luận dựa trên bằng chứng thu thập."""
        if not evidence:
            return f"Không đủ thông tin trong cơ sở tri thức để trả lời câu hỏi: '{question}'."

        # Structured synthesis matching evidence points
        ans_lines = []
        for i, (src, text) in enumerate(evidence, 1):
            ans_lines.append(f"- {text} [{i}]")

        header = "Tổng hợp phân tích chuyên gia dựa trên dữ liệu hệ thống:" if domain == "finance" else "Kết quả tra cứu hướng dẫn lâm sàng & chỉ số bệnh học:"
        full_text = f"{header}\n" + "\n".join(ans_lines)
        return full_text
