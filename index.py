import json
import requests
import streamlit as st

# Hàm tải danh sách từ khóa từ URL JSON
def load_violation_keywords(file_url):
    """Tải danh sách từ khóa vi phạm từ URL JSON."""
    try:
        response = requests.get(file_url)
        if response.status_code == 200:
            data = response.json()
            return data.get("keywords", [])
        else:
            st.error(f"Lỗi khi tải file JSON từ URL: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Lỗi khi đọc file JSON từ URL: {e}")
        return []

# Hàm kiểm tra nội dung nhập vào
def check_content_violation(content, keywords):
    """So khớp nội dung nhập vào với danh sách từ khóa vi phạm."""
    violations = [keyword for keyword in keywords if keyword.lower() in content.lower()]
    if violations:
        return {"status": "violation", "violated_keywords": violations}
    else:
        return {"status": "safe", "violated_keywords": []}

# URL tới file JSON trên GitHub
violation_file_url = "https://raw.githubusercontent.com/hoangnguyenhung1998/checkpolicyfb/main/full_facebook_policy_keywords.json"

# -----------------

# Access Token của Facebook API
ACCESS_TOKEN = "EAAFOwkjZA7ZAIBO5keO2G5ED6lwQrVnK7kCQOtrcS2pYPe1FJ5M5R6MziiyZC8BC8gE1MQFHzp36a9RUtVEcPPYuRFbsqdUZBOgEzqZBNH7BTZAAWfZBJZBo8C4Q0Vh3dikL1gIXTXqwJZCbKhe79vmhD4Lve11B9os18Hp2keZAiRxau8IcXesK3lBLm1JZBDZAmk9YCgZCJha4AiitQvoLYyAZDZD"  # Thay YOUR_FACEBOOK_ACCESS_TOKEN bằng Access Token thực tế

#---------------
# Giao diện Streamlit
st.title("Kiểm tra Nội dung Quảng cáo Facebook")

# Nội dung nhập vào
content_to_check = st.text_area("Nhập nội dung cần kiểm tra:", "")

# Tải danh sách từ khóa vi phạm
keywords = load_violation_keywords(violation_file_url)

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
st.markdown("---")
            
# Thêm Footer
st.markdown("---")
st.markdown("<center>Copyright by Bố Đậu Đậu</center>", unsafe_allow_html=True)

