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
ACCESS_TOKEN = "EAAFOwkjZA7ZAIBOwRGPqbkaHN96yCdR57Kb7Ll6hPDkJPfDDe0nCEBfgGm5X3JNc2ndBCrT5GecVh35ZCZBCV9IrzS2bPqJT67M3s5oQ9qJ2t0vjf3WINAZAOHCZC69SvVdvqWcTnRC4enprWJo0g8Xq6hZBW0og0ZCpRR7RmnZCHc3ad76j2VEZAeez5un2w1cOWcRsZA0yTj5HCBe04gx0AZDZD"  # Thay YOUR_FACEBOOK_ACCESS_TOKEN bằng Access Token thực tế

# Hàm kiểm tra ảnh qua Facebook API
def check_image_with_facebook_api(image_url):
    """Kiểm tra tỷ lệ text/hình ảnh qua Facebook API."""
    api_url = "https://graph.facebook.com/v17.0/adimages"
    params = {"access_token": ACCESS_TOKEN}
    data = {"url": image_url}
    try:
        response = requests.post(api_url, params=params, data=data)
        if response.status_code == 200:
            result = response.json()
            if result.get("success", False):
                return {"status": "approved", "message": "Hình ảnh đạt tiêu chuẩn text/hình."}
            else:
                return {"status": "rejected", "message": "Hình ảnh không đạt tiêu chuẩn text/hình."}
        else:
            return {"status": "error", "message": f"Lỗi: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi kết nối API: {e}"}

# Hàm tải ảnh lên và kiểm tra
def upload_and_check_image(image_file):
    """Tải ảnh lên và kiểm tra qua API."""
    if image_file:
        # Lưu ảnh tạm thời
        with open("temp_image.jpg", "wb") as temp_file:
            temp_file.write(image_file.getvalue())
        # Đường dẫn URL thực tế của ảnh (ở đây chỉ demo)
        image_url = "https://example.com/temp_image.jpg"  # Thay bằng hệ thống lưu trữ thực tế nếu cần
        return check_image_with_facebook_api(image_url)
    return {"status": "error", "message": "Không có ảnh để kiểm tra."}

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

# Upload file ảnh
uploaded_file = st.file_uploader("Tải ảnh lên để kiểm tra:", type=["jpg", "jpeg", "png"])

# Kiểm tra ảnh
if st.button("Kiểm tra ảnh"):
    if not uploaded_file:
        st.warning("Vui lòng tải lên một ảnh!")
    else:
        # Gọi hàm kiểm tra ảnh
        result = upload_and_check_image(uploaded_file)
        if result["status"] == "approved":
            st.success(result["message"])
        elif result["status"] == "rejected":
            st.error(result["message"])
        else:
            st.error(result["message"])
            
# Thêm Footer
st.markdown("---")
st.markdown("<center>Copyright by Bố Đậu Đậu</center>", unsafe_allow_html=True)

