THÍ NGHIỆM 1

1. Tạo tập test cho công cụ sửa:
	* Mục đích: Vì bộ hatespeech ban đầu chứa rất ít lỗi chính tả độc hại nên bước này sẽ tạo ra các lỗi chính tả để phục vụ công việc đánh giá chương trình sửa lỗi chính tả
	- Hai file train_x.dump và test_x.dump được trích xuất từ tập dữ liệu hate speech
	- Tập badword.txt chính là tập badword sau khi tìm được
	- "data_processed.txt" là tập dữ liệu thực tế thu thập từ các bình luận trên YouTube tại địa chỉ:
		https://drive.google.com/file/d/1-SWPD1NilNGwLNDfgwd1GT4L-mc51jKT/view?usp=sharing
	- auto_misspell_badwords.txt là tập dữ liệu sau khi tạo lỗi chính tả tự động (cần phải xem xét lại thủ công) tại địa chỉ: 		https://drive.google.com/file/d/1-33VSRHGAhrTXYamdFadzIdNzcwv1hZA/view?usp=sharing
	- misspell_badwords_edited.txt là tập dữ liệu sau khi lọc thủ công tập dữ liệu tự động ở trên, tập dữ liệu này được lưu tại địa chỉ 		https://drive.google.com/file/d/1DJx0QnVYnUsbs9viBZMVMoG-_C4Td_a5/view?usp=sharing
	- vocab.txt là tập từ vựng được tạo bằng cách kết hợp 2 tập từ vựng VnExpress và HateSpeech, tại địa chỉ: 
		https://drive.google.com/file/d/1-CNea7bYYg3WbcBqyUH3PIMpIiAk8MfQ/view?usp=sharing
	- Hai file orig_hate.csv và orig_offensive.csv là các câu thuộc lớp hate và offensive ở tập test sau khi chia tập train HateSpeech thành 2 phần (train/test)
	- Kết quả sau bước này tạo ra 2 file là "sai_chinh_ta_khong_dong_nghia.csv" và "sai_chinh_ta_dong_nghia.csv". Trong đó, mỗi file bao gồm: loại lỗi, từ sai, từ gốc, câu gốc và câu sau khi tạo lỗi.
2. Sửa lỗi chính tả cho tập hate và offensive:
	* Mục đích: Đánh giá các chương trình sữa lỗi chính tả, trực quan hoá và so sánh giữa các chương trình và phương pháp với nhau
	- 2 file là "sai_chinh_ta_khong_dong_nghia.csv" và "sai_chinh_ta_dong_nghia.csv" giống ở phần 1
	- small_corpus.txt: là tập từ vựng được tạo ra từ tập dữ liệu HateSpeech
	- hate_offensive_vocab.txt: là tập từ vựng chứa các từ của lớp hate và lớp offensive
	- Hai file model và vocab của các phương pháp được lưu tại đường dẫn https://drive.google.com/drive/folders/1SwykNIYR13M1uHy5sjucOZUogIpKWyOk?usp=sharing
	- Hai tập monogram.txt và bigram.txt dùng để khởi tạo SymSpell được lưu tại thư mục https://drive.google.com/drive/folders/1YiTBwqbfPq6FRrYbfx_fUZFQKVIFip3P?usp=sharing
	- gg_out.txt: Là những câu đã dùng google spell checker sửa lỗi
	- Kết quả sau khi sửa lỗi của tất cả các phương pháp được lưu tại thư mục hate_offensive. Trong đó những tệp có đuôi _kdn.txt là kết quả khi không xét đồng nghĩa và ngược lại _dn.txt là khi xét đồng nghĩa. Kết quả trực quan hoá ở hai file excel, trong đó ô màu đỏ thể hiện đã bị sửa sai, mục giải thích từ đầu tiên là từ sai chính tả và từ thứ 2 là từ đúng chính tả của câu. Các file excel này được trực quan hoá bằng đoạn mã trong 2 file .py cùng tên.
3. Sửa lỗi trên tập dữ liệu clean gốc
	* Mục đích: Đánh giá xem với các câu thông thường thì sẽ có bao nhiêu lỗi chính tả thông thường bị sửa thành các từ nhạy cảm với bộ lọc và có khả năng bị phân lớp nhầm
	- Các file badword.txt, small_corpus.txt, hate_offensive_vocab.txt, model và vocab của các phương pháp đều như trên
	- Hai file dùng cho Symspell cũng như trên
	- gg_input.txt: chứa các câu thuộc lớp clean của tập test
	- clean_test_gg.txt: Chứa các câu sau khi dùng google spell checker sửa lỗi
	- Kết quả sau khi sửa lỗi được lưu tại thư mục clean_goc tại địa chỉ https://drive.google.com/drive/folders/1-X7Fmej6fQmELOuGQuN4wvefzsJN6gqn?usp=sharing và trực quan hoá tại file clean_goc.xlsx. Trong đó, các ô màu đỏ của file excel thể hiện câu đã bị sửa các lỗi bình thường thành badword. Các file excel này được trực quan hoá bằng đoạn mã trong 2 file .py cùng tên.
4. Tạo lỗi trên tất cả badword ở tập test và sử dụng công cụ sửa lỗi chính tả
	* Mục đích: Đánh giá khả năng sữa lỗi chính tả của các chương trình khi tất cả các từ nhạy cảm với bộ lọc đều được tạo lỗi
	- Hai file train_x và test_x như trên
	- Các file badword.txt, small_corpus.txt, hate_offensive_vocab.txt, model và vocab của các phương pháp đều như trên
	- Hai file dùng cho Symspell cũng như trên

==============================================