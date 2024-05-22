$(document).ready(function () {
    // Xử lý sự kiện click vào mỗi sản phẩm cho ô tìm kiếm 1
    $(document).on("click", ".product-item", function () {
        var productName = $(this).data("name");
        var inputId = $(this).closest('.cs-search-group').find('input[type="text"]').attr('id');
        $("#" + inputId).val(productName);
        $(this).closest('.cs-search-group').find('.dropdown-content').html('');
    });

    // Xử lý sự kiện keyup để tìm kiếm sản phẩm cho ô tìm kiếm 1
    $("#searchpr1").keyup(function () {
        var inputText = $(this).val();
        if (inputText !== '') {
            $.ajax({
                url: 'search/',
                method: 'GET',
                data: { 'search_text': inputText },
                success: function (data) {
                    $('.search-results-1').html(data);
                }
            });
        } else {
            $('.search-results-1').html('');
        }
    });

    // Xử lý sự kiện click vào mỗi sản phẩm cho ô tìm kiếm 2
    $(document).on("click", ".product-item", function () {
        var productName = $(this).data("name");
        var inputId = $(this).closest('.cs-search-group').find('input[type="text"]').attr('id');
        $("#" + inputId).val(productName);
        $(this).closest('.cs-search-group').find('.dropdown-content').html('');
    });

    // Xử lý sự kiện keyup để tìm kiếm sản phẩm cho ô tìm kiếm 2
    $("#searchpr2").keyup(function () {
        var inputText = $(this).val();
        if (inputText !== '') {
            $.ajax({
                url: 'search/',
                method: 'GET',
                data: { 'search_text': inputText },
                success: function (data) {
                    $('.search-results-2').html(data);
                }
            });
        } else {
            $('.search-results-2').html('');
        }
    });
});

