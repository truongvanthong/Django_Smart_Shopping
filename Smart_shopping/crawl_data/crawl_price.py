from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import csv


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


def crawl_tgdd(link):
    """
    Thu thập giá của sản phẩm điện thoại di động trên thế giới di động

    Parameters:
        link (str): Đường link dẫn tới sản phẩm.

    Returns:
        price (str): Giá của sản phẩm. Nếu price là None thì sản phẩm là Hết hàng hoặc Dừng bán

    Ví dụ:
        >>> crawl_tgdd("https://www.thegioididong.com/dtdd/iphone-15-pro-max")
        29.990.000₫
    """
    # Tạo một đối tượng tùy chọn cho trình duyệt Chrome
    chrome_options = Options()
    # Thêm tùy chọn "--headless" để chạy trình duyệt ở chế độ không có giao diện người dùng,
    # nghĩa là không hiển thị cửa sổ trình duyệt lên màn hình
    chrome_options.add_argument("--headless")

    # Khởi tạo webdriver với tùy chọn trên và truy cập vào đường link sản phẩm
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)

    css_selectors = [
        "p.box-price-present",
        "div.bs_price > strong",
        "div.item.cf-left > b > b",
    ]
    # Kiểm tra tất cả các css_selector và trả về giá nếu tìm thấy
    for css_selector in css_selectors:
        try:
            price = driver.find_element(By.CSS_SELECTOR, css_selector).text
            if price != "":
                driver.quit()
                return price
        except:
            pass

    # Đóng webdriver
    driver.quit()
    return None


def crawl_fpt(link):
    """
    Thu thập giá của sản phẩm điện thoại di động trên fptshop

    Parameters:
        link (str): Đường link dẫn tới sản phẩm.

    Returns:
        price (str): Giá của sản phẩm. Nếu price là None thì sản phẩm là Hết hàng hoặc Dừng bán

    Ví dụ:
        >>> crawl_fpt("https://fptshop.com.vn/dien-thoai/iphone-15-pro-max")
        29.490.000₫
    """
    # Tạo một đối tượng tùy chọn cho trình duyệt Chrome
    chrome_options = Options()
    # Thêm tùy chọn "--headless" để chạy trình duyệt ở chế độ không có giao diện người dùng,
    # nghĩa là không hiển thị cửa sổ trình duyệt lên màn hình
    chrome_options.add_argument("--headless")

    # Khởi tạo webdriver với tùy chọn trên và truy cập vào đường link sản phẩm
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)

    # Kiểm tra và lấy giá của sản phẩm
    try:
        price = driver.find_element(By.CSS_SELECTOR, "div.st-price-main").text
        if price != "":
            driver.quit()
            return price
    except:
        pass

    # Đóng webdriver
    driver.quit()
    return None


def crawl_link(link):
    """
    Thu thập giá của sản phẩm điện thoại di động dựa trên link sản phẩm

    Parameters:
        link (str): Đường dẫn URL của sản phẩm cần thu thập

    Returns:
        Sử dung hàm crawl_tgdd hoặc crawl_fpt để thu thập giá sản phẩm dựa trên link sản phẩm tương ứng
    """
    if "thegioididong.com" in link:
        return crawl_tgdd(link)
    elif "fptshop.com.vn" in link:
        return crawl_fpt(link)
    else:
        return "Unsupported website"


def get_price(links):
    """
    Hàm này nhận vào các liên kết sản phẩm từ FPT và Thế Giới Di Động và trả về giá của các sản phẩm.

    Parameters:
        product1_FPT_link (str): Liên kết sản phẩm 1 từ FPT.
        product1_TGDD_link (str): Liên kết sản phẩm 1 từ Thế Giới Di Động.
        product2_FPT_link (str): Liên kết sản phẩm 2 từ FPT.
        product2_TGDD_link (str): Liên kết sản phẩm 2 từ Thế Giới Di Động.

    Returns:
        tuple: Một tuple chứa giá của các sản phẩm lần lượt từ FPT và Thế Giới Di Động.
    """

    with ThreadPoolExecutor(max_workers=len(links)) as executor:
        results = list(executor.map(crawl_link, links))

    return results


def main():
    data = pd.read_csv("data.csv")
    nums = range(0, 54)
    with open("data_tmp.csv", "a", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        for i in nums:
            name = data["Tên"][i]
            links_tgdd = convert_text(data["Link_tgdd"][i])
            links_fpt = convert_text(data["Link_fpt"][i])
            prices_tgdd = get_price(links_tgdd)
            prices_fpt = get_price(links_fpt)
            for link, price in zip(links_tgdd, prices_tgdd):
                writer.writerow([name, link, price])
            for link, price in zip(links_fpt, prices_fpt):
                writer.writerow([name, link, price])


if __name__ == "__main__":
    main()
