import json
import streamlit as st

# Hàm tải danh sách từ khóa từ file JSON
def load_violation_keywords(file_path):
    """Tải danh sách từ khóa vi phạm từ file JSON."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data.get("keywords", [])
    except FileNotFoundError:
        st.error(f"File {file_path} không tồn tại.")
        return []
    except json.JSONDecodeError:
        st.error("Lỗi khi đọc file JSON.")
        return []

# Hàm kiểm tra nội dung nhập vào
def check_content_violation(content, keywords):
    """So khớp nội dung nhập vào với danh sách từ khóa vi phạm."""
    violations = [keyword for keyword in keywords if keyword.lower() in content.lower()]
    if violations:
        return {"status": "violation", "violated_keywords": violations}
    else:
        return {"status": "safe", "violated_keywords": []}

# Đường dẫn đến file JSON
violation_file_path = "https://github.com/hoangnguyenhung1998/checkpolicyfb/blob/main/full_facebook_policy_keywords.json"

# Giao diện Streamlit
st.title("Kiểm tra Nội dung Quảng cáo Facebook")

# Nội dung nhập vào
content_to_check = st.text_area("Nhập nội dung cần kiểm tra:", "")

# Tải danh sách từ khóa vi phạm
keywords = load_violation_keywords(violation_file_path)

# Nút kiểm tra
if st.button("Kiểm tra nội dung"):
    if not content_to_check.strip():
        st.warning("Vui lòng nhập nội dung để kiểm tra!")
    else:
        # Kiểm tra nội dung
        result = check_content_violation(content_to_check, keywords)
        if result["status"] == "violation":
            st.error("Nội dung vi phạm các từ khóa sau:")
            st.write(", ".join(result["violated_keywords"]))
        else:
            st.success("Nội dung an toàn, không vi phạm chính sách.")
