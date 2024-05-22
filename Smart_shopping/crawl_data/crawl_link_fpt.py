from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import csv


def crawl(index):
    """
    Thu thập đường link sản phẩm điện thoại di động trên fptshop và lưu vào file

    Parameters:
    index (int): Chỉ số của sản phẩm. Nếu index % 10 == 0 sẽ sinh ra lỗi vì đây không phải sản phẩm

    Ví dụ:
    >>> crawl_tgdd(1)
    file data_tmp.csv sẽ bao gồm 2 cột là Tên và Link sản phẩm iPhone 15 Pro Max trên fptshop
    """

    # Tạo một đối tượng tùy chọn cho trình duyệt Chrome
    chrome_options = Options()
    # Thêm tùy chọn "--headless" để chạy trình duyệt ở chế độ không có giao diện người dùng,
    # nghĩa là không hiển thị cửa sổ trình duyệt lên màn hình
    chrome_options.add_argument("--headless")

    # Khởi tạo webdriver với tùy chọn trên và mở trang web sản phẩm điện thoại di động trên fpt
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"https://fptshop.com.vn/dien-thoai?sort=ban-chay-nhat&trang=4")
    sleep(5)

    # Kiểm tra và lấy tên của sản phẩm
    try:

        # Lấy tên của sản phẩm
        name = driver.find_element(
            By.XPATH,
            "//*[@id='root']/main/div/div[3]/div[2]/div[2]/div/div[2]/div["
            + str(index)
            + "]/div[2]/h3/a",
        ).text

    except:
        pass

    # Kiểm tra và Click vào sản phẩm
    try:

        # Click vào sản phẩm
        driver.find_element(
            By.XPATH,
            "//*[@id='root']/main/div/div[3]/div[2]/div[2]/div/div[2]/div["
            + str(index)
            + "]",
        ).click()
        sleep(5)

    except:
        pass

    # Kiểm tra và Click vào sản phẩm
    try:

        # Click vào sản phẩm
        driver.find_element(
            By.XPATH,
            "//*[@id='root']/main/div/div[3]/div[2]/div[2]/div/div[2]/div["
            + str(index)
            + "]/div[1]",
        ).click()
        sleep(5)

    except:
        pass

    # Khởi tạo danh sách links với phần tử đầu tiên là link sản phẩm hiện tạo
    links = [driver.current_url]

    # Kiểm tra và Tìm các đường link phiên bản khác của sản phẩm.
    try:

        # Tìm các đường link phiên bản khác của sản phẩm
        link_list = driver.find_elements(
            By.XPATH,
            "//div[@class='st-select']/a[@class='st-select__item js--select-item']",
        )
        for link in link_list:
            if link.get_attribute("href") not in links:
                links.append(link.get_attribute("href"))

    except:
        pass

    # Lưu Tên và các đường links vào file data_tmp.csv
    with open("data_tmp.csv", "a", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, links])

    # Đóng webdriver
    sleep(5)
    driver.close()


def main():

    # Thu thập các đường link từ fptshop
    nums = range(1, 96)
    for i in nums:
        if i % 10 == 0:
            continue
        crawl(i)


if __name__ == "__main__":
    main()
