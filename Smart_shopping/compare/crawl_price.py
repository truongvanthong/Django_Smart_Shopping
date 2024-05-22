from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor


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


def get_price(product1_FPT_link, product1_TGDD_link, product2_FPT_link, product2_TGDD_link):
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
    links = [
        product1_FPT_link,
        product1_TGDD_link,
        product2_FPT_link,
        product2_TGDD_link,
    ]

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(crawl_link, links))

    return results[0], results[1], results[2], results[3]
