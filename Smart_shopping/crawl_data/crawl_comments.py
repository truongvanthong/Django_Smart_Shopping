from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import csv
import pandas as pd


def convert_text(text) -> list:
    """
    Chuyển đổi một chuỗi văn bản chứa các phần tử được phân tách bằng dấu "', '"
    thành một danh sách các phần tử.

    Parameters:
    text (str): Chuỗi văn bản chứa các phần tử được phân tách bằng dấu "', '".

    Returns:
    list: Danh sách các phần tử được trích xuất từ chuỗi.

    Ví dụ:
    >>> convert_text("['item1', 'item2', 'item3']")
    ['item1', 'item2', 'item3']
    """
    text = text.strip("[']")
    texts = text.split("', '")
    return texts


def crawl_comments_tgdd(link):
    """
    Thu thập các bình luận đánh giá từ sản phẩm điện thoại di động trên thế giới di động.

    Parameters:
    link (str): Đường link dẫn tới sản phẩm.

    Returns:
    list: Danh sách chứa các bình luận đánh giá trong đường link sản phẩm đó

    Ví dụ:
    >>> crawl_comments_tgdd("https://www.thegioididong.com/dtdd/iphone-15-pro-max")
    ['comment1', 'comment2', 'comment3']
    """

    # Tạo một đối tượng tùy chọn cho trình duyệt Chrome
    chrome_options = Options()
    # Thêm tùy chọn "--headless" để chạy trình duyệt ở chế độ không có giao diện người dùng,
    # nghĩa là không hiển thị cửa sổ trình duyệt lên màn hình
    chrome_options.add_argument("--headless")

    # Khởi tạo webdriver với tùy chọn trên và truy cập vào đường link sản phẩm
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    sleep(5)

    list_comments = []

    # Kiểm tra và Click vào xem tất cả đánh giá
    try:

        # Click vào xem tất cả đánh giá
        driver.find_element(By.XPATH, "//a[@class='c-btn-rate btn-view-all']").click()
        sleep(5)

    except:
        pass

    # Kiểm tra và Thu thập các đánh giá
    try:

        # Thu thập các đánh giá
        comments = driver.find_elements(By.XPATH, "//p[@class='cmt-txt']")
        for comment in comments:
            comment = comment.text
            if comment.strip():
                list_comments.append(comment)

    except:
        pass

    # Kiểm tra và Click vào các trang đánh giá tiếp theo. Sau đó Thu thập các đánh giá
    try:
        index = 2
        while True:

            # Click vào các trang đánh giá tiếp theo
            driver.find_element(
                By.XPATH,
                f"//div[@class='rt-list']/div[@class='pgrc']/div[@class='pagcomment']/a[@title='trang {str(index)}']",
            ).click()
            sleep(1)
            index += 1

            # Thu thập các đánh giá
            comments = driver.find_elements(By.XPATH, "//p[@class='cmt-txt']")
            for comment in comments:
                comment = comment.text
                if comment.strip():
                    list_comments.append(comment)

    except:
        pass

    # Đóng webdriver
    sleep(5)
    driver.close()

    return list_comments


def crawl_comments_fpt(link):
    """
    Thu thập các bình luận đánh giá từ sản phẩm điện thoại di động trên fptshop

    Parameters:
    link (str): Đường link dẫn tới sản phẩm.

    Returns:
    list: Danh sách chứa các bình luận đánh giá trong đường link sản phẩm đó

    Ví dụ:
    >>> crawl_comments_tgdd("https://fptshop.com.vn/dien-thoai/iphone-15-pro-max")
    ['comment1', 'comment2', 'comment3']
    """

    # Tạo một đối tượng tùy chọn cho trình duyệt Chrome
    chrome_options = Options()
    # Thêm tùy chọn "--headless" để chạy trình duyệt ở chế độ không có giao diện người dùng,
    # nghĩa là không hiển thị cửa sổ trình duyệt lên màn hình
    chrome_options.add_argument("--headless")

    # Khởi tạo webdriver với tùy chọn trên và truy cập vào đường link sản phẩm
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    sleep(5)

    list_comments = []

    # Kiểm tra và Thu thập các đánh giá
    try:

        # Thu thập các đánh giá
        comments = driver.find_elements(
            By.XPATH,
            "//div[@id='root-review']/div/div/div/div[@class='card-body']/div[@class='user-content']/div[@class='user-wrapper']/div[@class='user-block']/div[@class='avatar avatar-md avatar-text avatar-circle']/div[@class='avatar-info']/div[@class='avatar-para']/div[@class='text']",
        )
        for comment in comments:
            comment = comment.text
            if comment.strip():
                list_comments.append(comment)

    except:
        pass

    # Kiểm tra và Click vào các trang đánh giá tiếp theo. Sau đó Thu thập các đánh giá
    try:
        while True:

            # Click vào các trang đánh giá tiếp theo
            driver.find_element(
                By.XPATH,
                "//div[@id='root-review']/div/div/div/div[@class='card-body']/div[@class='user-content']/div[@class='pages']/div[@class='select-device__pagination']/ul[@class='pagination pagination-space']/li[@class='pagination-item']/a[@class='pagination-link']/i[@class='cm-ic-angle-right']",
            ).click()
            sleep(1)

            # Thu thập các đánh giá
            comments = driver.find_elements(
                By.XPATH,
                "//div[@id='root-review']/div/div/div/div[@class='card-body']/div[@class='user-content']/div[@class='user-wrapper']/div[@class='user-block']/div[@class='avatar avatar-md avatar-text avatar-circle']/div[@class='avatar-info']/div[@class='avatar-para']/div[@class='text']",
            )
            for comment in comments:
                comment = comment.text
                if comment.strip():
                    list_comments.append(comment)

    except:
        pass

    # Đóng webdriver
    sleep(5)
    driver.close()

    return list_comments


def main():

    # Thu thập đánh giá dựa trên index của sản phẩm trong data.csv
    data = pd.read_csv("data.csv")
    start, end = 1, 1
    nums = range(start, end + 1)
    with open("data_tmp.csv", "a", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        for i in nums:
            name = data["Tên"][i]
            links_tgdd = convert_text(data["Link_tgdd"][i])
            links_fpt = convert_text(data["Link_fpt"][i])
            for tgdd in links_tgdd:
                cmts = crawl_comments_tgdd(tgdd)
                writer.writerow([name, tgdd, cmts])
            for fpt in links_fpt:
                cmts = crawl_comments_fpt(fpt)
                writer.writerow([name, fpt, cmts])

    # # Thu thập đánh giá dựa trên link của sản phẩm
    # link = "https://www.thegioididong.com/dtdd/iphone-15-pro-max"
    # name = "iPhone 15 Pro Max"
    # with open("data_tmp.csv", "a", newline="", encoding="utf-8-sig") as csvfile:
    #     writer = csv.writer(csvfile)
    #     if "thegioididong.com" in link:
    #         cmts = crawl_comments_tgdd(link)
    #         writer.writerow([name, link, cmts])
    #     elif "fptshop.com.vn" in link:
    #         cmts = crawl_comments_fpt(link)
    #         writer.writerow([name, link, cmts])


if __name__ == "__main__":
    main()
