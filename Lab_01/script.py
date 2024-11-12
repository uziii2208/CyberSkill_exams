import zipfile
import os
import re
from PyPDF2 import PdfReader  # Phải chắc chắn là PyPDF2 được cài đặt (pip install PyPDF2)

# Step 1: Giải nén tệp session2.zip vào thư mục 'extracted_pdfs'
zip_file_path = os.path.join(os.path.dirname(__file__), 'session2.zip')
extract_folder_path = 'extracted_pdfs'

# Đảm bảo file tồn tại
if not os.path.isfile(zip_file_path):
    print(f"Error: File '{zip_file_path}' not found.")
else:
    print(f"Found file at '{zip_file_path}'")
    # Tiếp tục xử lý file

# Trích xuất file ZIP ở file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_folder_path)
print(f"Extracted files to '{extract_folder_path}'")

# Step 2: Định nghĩa một hàm để trích xuất văn bản từ mỗi tệp PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:  # Kiểm tra xem việc trích xuất văn bản có thành công không
                text += page_text
    return text

# Step 3: Trích xuất các từ tiếng Anh duy nhất từ văn bản
def extract_words(text):
    words = re.findall(r'\b[a-zA-Z]+\b', text)  # Chỉ khớp các từ chỉ chứa chữ cái tiếng Anh
    unique_words = set(words)  # Loại bỏ các từ trùng lặp bằng cách chuyển sang tập hợp (set)
    return unique_words

# Step 4: Xác định vị trí thư mục con 'session2' trong 'extracted_pdfs' và xử lý từng tệp PDF
session2_folder_path = os.path.join(extract_folder_path, 'session2')

# Kiểm tra xem thư mục con 'session2' có tồn tại không
if os.path.isdir(session2_folder_path):
    for filename in os.listdir(session2_folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(session2_folder_path, filename)
            
            # Trích xuất văn bản từ tệp PDF
            text = extract_text_from_pdf(pdf_path)
            
            # Trích xuất các từ duy nhất
            words = extract_words(text)
            
            # Tạo một thư mục được đặt tên theo tên tệp PDF (không bao gồm phần mở rộng .pdf)
            folder_name = os.path.splitext(filename)[0]
            folder_path = os.path.join(extract_folder_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            
            # Tạo các tệp văn bản riêng lẻ cho mỗi từ duy nhất
            for word in words:
                word_filename = f"{folder_path}/{word}.txt"
                with open(word_filename, "w") as word_file:
                    word_file.write(word)

    print("Processing complete. Check the 'extracted_pdfs' folder for results.")
else:
    print(f"Error: '{session2_folder_path}' not found.")

#=======================================================================================#

#Mọi yêu cầu của lab đều được automation qua file script này.
#Quá trình debug diễn ra lâu nhanh sẽ tùy vào kích thước file, cám ơn đã review code ạ !

#=======================================================================================#