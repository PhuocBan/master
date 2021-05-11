THÍ NGHIỆM 2

1. Mục đích: Đánh giá trường hợp nếu các từ nhạy cảm với bộ lọc chứa lỗi chính tả độc hại thì việc áp dụng các chương trình sửa lỗi chính tả ở bước tiền xử lí đem lại hiệu quả ra sao.

2. Toàn bộ source code của thí nghiệm được lưu trong file "Tạo_lỗi_hate_speech_và_test___TN1.ipynb"

3. Data thực hiện thí nghiệm được lưu trong thư mục data, trong đó:
	- Các file train_x, train_y, test_x, test_y được trích từ tập hatespeech
	- File "test_x_duoc_tao_loi.dump" là file kết quả sau quá trình tạo lỗi
	- File "cc.vi.300.vec" được tải từ trang fasttext.cc
	- File "model_9.h5" là file weight của mô hình LSTM sau khi train 10 echpoch
	- Các file kết quả sửa lỗi của các phương pháp được lưu tại thư mục correct
	- Kết quả classification_report của mô hình LSTM sau khi áp dụng sửa lỗi chính tả ở bước tiền xử lí được lưu tại file "report.txt"
	- Kết quả được trực quan hoá ở file TN2.xlsx. Kết quả này được tạo ra bằng cách chạy file .py cùng tên.

===================================