1. CHƯƠNG TRÌNH DEMO
- Bước 1: Vào thư mục "SpellChecker_Demo"
- Bước 2: Mở terminal và tạo môi trường mới(nếu chạy lần đầu, chạy lần 2 thì bỏ qua bước này)
  Tạo môi trường mới với anaconda (nếu chạy lần đầu)
	Bước 2.1: Tạo môi trường với lệnh sau:
	  conda create -n myenv python=3.6
	Bước 2.2: Kích hoạt môi trường vừa tạo mới lệnh sau:
	  conda activate myenv
	Bước 2.3: Cài đặt thư viện django để chạy demo dạng website:
	  pip install Django==3.1.4
	Bước 2.3: Cài đặt các thư viện hỗ trợ:
	  pip install pyxDamerauLevenshtein==1.6.1
- Bước 3: cd terminal tới đường dẫn thư mục spellChecker_Demo và chạy ứng dụng với câu lệnh sau:
  	python manage.py runserver
- Bước 4: Vào trình duyệt với đường dẫn sau để đến với chương trình demo: 
	http://127.0.0.1:8000/

2. THÍ NGHIỆM
- Toàn bộ source của các thí nghiệm được chứa trong thư mục mang tên "Thí nghiệm", mô tả của từng thí nghiệm và các file sẽ được lưu trong file "readme.txt" của từng thu mục thí nghiệm.
==============================================