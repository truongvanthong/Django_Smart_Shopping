document.addEventListener("DOMContentLoaded", function () {
    const heartButton = document.getElementById("heart-button");
    const heartImg = document.getElementById("heart-img");
    const heartContainer = document.getElementById("heart-container");
    const productPrice = document.querySelector(".price");

    if (productPrice) {
        heartButton.addEventListener("click", function () {
            const product1Id = heartContainer.getAttribute("data-product1-id");
            const product2Id = heartContainer.getAttribute("data-product2-id");
            if (product1Id && product2Id) {
                // Gửi product_id về server
                const xhr = new XMLHttpRequest();
                xhr.open("POST", "/save_history/", true);
                xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                xhr.onreadystatechange = function () {
                    if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                        // Xử lý kết quả từ server nếu cần
                    }
                };
                xhr.send(`product1_id=${product1Id}&product2_id=${product2Id}`);
                
                // Thay đổi hình ảnh trái tim
                if (heartImg.src.includes("heart-off.png")) {
                    heartImg.src = "/static/img/heart-on.png";
                } else {
                    heartImg.src = "/static/img/heart-off.png";
                }
            }
        });
    } else {
        heartButton.style.pointerEvents = "none";
        heartButton.style.opacity = "0.5";
    }
});