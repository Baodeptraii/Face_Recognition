import cv2
import os
import face_recognition
import pickle

# Thư mục chứa dữ liệu ảnh đã thu thập
dataset_path = "dataset"

# Tải dữ liệu mã hóa hiện có nếu tồn tại
if os.path.exists('encodings.pkl'):
    with open('encodings.pkl', 'rb') as f:
        encodeListKnown, classNames = pickle.load(f)
else:
    encodeListKnown, classNames = [], []

# Duyệt qua thư mục dataset để tìm ảnh chưa mã hóa
for person in os.listdir(dataset_path):
    person_path = os.path.join(dataset_path, person)
    if os.path.isdir(person_path):
        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)
            if not any(person == name for name in classNames):  # chỉ mã hóa nếu người chưa có
                img = cv2.imread(img_path)
                if img is not None:
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    try:
                        encode = face_recognition.face_encodings(img_rgb)[0]
                        encodeListKnown.append(encode)
                        classNames.append(person)
                        print(f"Đã mã hóa khuôn mặt: {person}")
                    except IndexError:
                        print(f"Không nhận diện được khuôn mặt trong: {img_name}, ảnh có thể bị lỗi")
                else:
                    print(f"Không thể đọc ảnh: {img_path}")

# Lưu lại dữ liệu đã cập nhật
with open('encodings.pkl', 'wb') as f:
    pickle.dump((encodeListKnown, classNames), f)

print("Cập nhật mã hóa khuôn mặt hoàn tất.")
# Đoạn mã này sẽ tự động mã hóa các khuôn mặt trong thư mục dataset và lưu lại vào file encodings.pkl.
# Nếu có khuôn mặt nào không nhận diện được, nó sẽ thông báo cho bạn biết.