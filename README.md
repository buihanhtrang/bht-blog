# Bạn hỏi, tôi tư duy — ETE16

## Nội dung từ DOCX

Blog hiện có 8 bài chuyển từ hai tài liệu gốc trong thư mục cha: bài đăng ký học phần kèm 3 hình minh họa và 7 bài về học tập, project, nghiên cứu, tốt nghiệp, kỹ năng, nghề nghiệp, rà soát học kỳ. Giữ nguyên nội dung văn bản nguồn; mô tả ngắn được biên tập để hiển thị trên thẻ bài. Ngày hiển thị là ngày đưa nội dung lên bản blog này, không phải ngày ban hành tài liệu. Mốc đăng ký trong tài liệu là ví dụ, cần đối chiếu thông báo chính thức.

Chạy `python import_documents.py` để nhập lại khi DOCX gốc thay đổi. Lệnh ghi lại posts.json và ảnh trong assets, vì vậy hãy sao lưu các bài tự thêm trước khi nhập lại. Script chỉ đọc, không sửa DOCX gốc. Khi deploy, nhớ đưa cả thư mục assets lên repository. Không cần đưa DOCX gốc lên GitHub.

Blog lập trình tiếng Việt, chạy trên GitHub Pages, không cần cài thư viện hay build. Có tìm kiếm, lọc chuyên mục, giao diện sáng/tối, đọc Markdown và trình soạn bài có xem trước.

## Chạy trên máy

Trong thư mục này chạy `python -m http.server 8080`, rồi mở http://localhost:8080. Không mở index.html trực tiếp bằng file:// vì trình duyệt cần tải posts.json qua HTTP.

## Deploy lên GitHub

1. Tạo repository GitHub. Đưa toàn bộ nội dung thư mục `code-blog` vào gốc repository, bao gồm `.github/workflows/deploy.yml`.
2. Dùng nhánh `main`. Vào **Settings → Pages → Build and deployment → Source → GitHub Actions**.
3. Push code lên `main` hoặc chạy workflow **Deploy blog to GitHub Pages** trong tab Actions.
4. Khi workflow thành công, mở URL tại Settings → Pages. Thường có dạng `https://USERNAME.github.io/REPOSITORY/`.

Các đường dẫn tài nguyên đều tương đối, hỗ trợ cả repository Pages và user Pages. Nếu dùng nhánh khác main, sửa `branches` trong workflow.

## Viết và đăng bài

1. Chọn **Viết bài**, nhập tiêu đề, chuyên mục, mô tả, ngày và nội dung Markdown.
2. Chọn **Lưu bài trên máy**. Bài sẽ hiển thị trong blog ở chính trình duyệt này.
3. Chọn **Xuất posts.json** để tải toàn bộ thư viện đã lưu. Nhớ lưu nội dung đang soạn trước khi xuất.
4. Trên GitHub, thay file `posts.json` ở gốc repository bằng file vừa tải, rồi commit lên main. GitHub Actions tự cập nhật trang công khai.

Lưu trên máy dùng localStorage, không đồng bộ giữa thiết bị. Xóa dữ liệu trình duyệt sẽ mất thay đổi chưa xuất. Người đọc không thể sửa repository của bạn qua trình soạn bài. Không có tài khoản, mật khẩu hay token GitHub trong ứng dụng.

Chọn **Sửa** để cập nhật bài hiện có. **Nhập dữ liệu** gộp các bài từ file JSON và thay bài có cùng id. Muốn xóa bài công khai, xóa đối tượng tương ứng trong posts.json trên repository. Các bài mẫu có thể thay thế toàn bộ. Để tùy chỉnh tên blog, sửa index.html và app.js; màu sắc nằm trong style.css.

## Markdown hỗ trợ

Tiêu đề cấp 1–3, đoạn văn, chữ đậm, inline code, khối code bằng ba dấu nháy ngược, trích dẫn, danh sách đơn giản với `- ` và liên kết HTTP/HTTPS. HTML trong bài được hiển thị như văn bản để tránh chạy mã nhúng. Đây là bộ Markdown tối giản, không hỗ trợ toàn bộ CommonMark.

Font Google có font hệ thống dự phòng. Không cần backend hoặc dịch vụ trả phí.
