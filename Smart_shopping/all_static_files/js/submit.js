$(document).ready(function () {
    // Bắt sự kiện click nút submit
    $("#submitBtn").click(function () {
        // Lấy giá trị từ ô tìm kiếm 1 và 2
        var searchpr1 = $('#searchpr1').val();
        var searchpr2 = $('#searchpr2').val();

        // Gửi yêu cầu POST
        $.ajax({
            url: '/compare/', // Địa chỉ URL của endpoint xử lý tìm kiếm
            method: 'POST',
            data: {
                'searchpr1': searchpr1, // Truyền giá trị của ô tìm kiếm 1
                'searchpr2': searchpr2, // Truyền giá trị của ô tìm kiếm 2
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val() // Đảm bảo gửi CSRF token
            },
            success: function (data) {
                // Xử lý dữ liệu trả về nếu cần
                console.log(data);
            },
            error: function (xhr, errmsg, err) {
                // Xử lý lỗi nếu có
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });
});