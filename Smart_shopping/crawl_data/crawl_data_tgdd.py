from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import csv
import webcolors
import re


def closest_colour(requested_colour):
    """
    Tìm tên màu gần nhất từ danh sách màu được đặt tên CSS3
    tới màu RGB được cung cấp.

    Parameters:
        requested_colour (tuple): Một tuple chứa các giá trị RGB
                                  của màu cần tìm tên gần nhất.

    Returns:
        str: Tên của màu gần nhất trong danh sách màu được đặt tên CSS3.
    """
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    """
    Tìm tên màu tương ứng với màu RGB được cung cấp.

    Parameters:
        requested_colour (tuple): Một tuple chứa các giá trị RGB của màu.

    Returns:
        tuple: Một tuple chứa hai phần tử, tên thực tế của màu (nếu có) và tên gần nhất của màu.
    """
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name


def extract_text1(input_string):
    """
    Lấy thông số của sản phẩm từ outerHTML

    Args:
        input_string (str): Một outerHTML string chứa thông số sản phẩm

    Returns:
        str: thông số của sản phẩm cần tìm
    """
    if "</a>" in input_string:
        start_index = input_string.find(">") + 1
        start_index = input_string.find(">", start_index) + 1
        end_index = input_string.find("<")
        end_index = input_string.find("<", end_index + 1)
        end_index = input_string.find("<", end_index + 1)
        text = input_string[start_index:end_index].strip()
    else:
        start_index = input_string.find(">") + 1
        end_index = input_string.find("<")
        end_index = input_string.find("<", end_index + 1)
        text = input_string[start_index:end_index].strip()
    return text


def extract_text2(input_string):
    """
    Lấy thông số của sản phẩm từ outerHTML

    Args:
        input_string (str): Một outerHTML string chứa thông số sản phẩm

    Returns:
        str: thông số của sản phẩm cần tìm
    """
    if 'class="circle"' in input_string:
        end_tags_indices = []
        start_index = 0
        while True:
            start_index = input_string.find("</p>", start_index)
            if start_index == -1:
                break
            end_tags_indices.append(start_index)
            start_index += len("</p>")
        texts = ""
        for end_index in end_tags_indices:
            start_index = input_string.rfind('<p class="circle">', 0, end_index)
            text = input_string[start_index + 18 : end_index]
            if "</a>" in text:
                start_index_text = text.find(">") + 1
                end_index_text = text.find("<")
                end_index_text = text.find("<", end_index_text + 1)
                text = text[start_index_text:end_index_text].strip()
            texts += text.strip() + "\n"
        texts = texts.rstrip("\n")
        return texts
    elif 'class="comma"' in input_string:
        end_tags_indices = []
        start_index = 0
        while True:
            start_index = input_string.find("</a>", start_index)
            if start_index == -1:
                break
            end_tags_indices.append(start_index)
            start_index += len("</a>")
        texts = ""
        for end_index in end_tags_indices:
            start_index = input_string.rfind(">", 0, end_index)
            text = input_string[start_index + 1 : end_index]
            texts += text.strip() + ", "
        texts = texts.rstrip(", ")
        return texts
    else:
        start_index = input_string.find(">") + 1
        start_index = input_string.find(">", start_index) + 1
        end_index = input_string.find("<")
        end_index = input_string.find("<", end_index + 1)
        end_index = input_string.find("<", end_index + 1)
        text = input_string[start_index:end_index].strip()
        return text


def crawl(index):
    """
    Lấy tất cả thông tin của sản phẩm điện thoại di động trên thế giới di động

    Args:
        index (int): Index của sản phẩm
    """

    # Tạo một đối tượng tùy chọn cho trình duyệt Chrome
    chrome_options = Options()
    # Thêm tùy chọn "--headless" để chạy trình duyệt ở chế độ không có giao diện người dùng,
    # nghĩa là không hiển thị cửa sổ trình duyệt lên màn hình
    chrome_options.add_argument("--headless")

    # Khởi tạo webdriver với tùy chọn trên và mở trang web sản phẩm điện thoại di động trên thế giới di động
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.thegioididong.com/dtdd#c=42&o=17&pi=5")
    sleep(5)

    # Kiểm tra và lấy Tên, Ảnh của sản phẩm đồng thời click vào sản phẩm
    try:

        # Lấy Tên của sản phẩm
        name = driver.find_element(
            By.XPATH, "//*[@id='categoryPage']/div[3]/ul/li[" + str(index) + "]/a[1]/h3"
        ).text

        # Lấy Ảnh của sản phẩm
        image = driver.find_element(
            By.XPATH,
            "//*[@id='categoryPage']/div[3]/ul/li[" + str(index) + "]/a[1]/div[2]/img",
        ).get_attribute("src")

        # Click vào sản phẩm
        driver.find_element(
            By.XPATH, "//*[@id='categoryPage']/div[3]/ul/li[" + str(index) + "]"
        ).click()
        sleep(5)
    except:
        return

    # Các phiên bản của sản phẩm (thường là bộ nhớ: 128GB, 256GB, 512GB, 1TB, ...)
    storages = []

    # Các màu của sản phẩm
    colors = []

    # Các đường link của sản phẩm
    links = []

    # Kiểm tra và lấy các phiên bản của sản phẩm
    try:

        # Lấy phiên bản hiện tại của sản phẩm
        storage = driver.find_element(
            By.XPATH,
            "//div[@class='box03 group desk']/a[@class='box03__item item act']",
        ).text
        storages.append(storage)

        # Lấy các phiên bản khác của sản phẩm
        storage_list = driver.find_elements(
            By.XPATH, "//div[@class='box03 group desk']/a[@class='box03__item item ']"
        )
        for storage in storage_list:
            if storage.text != "" and storage not in storages:
                storages.append(storage.text)

    except:
        pass

    # Nếu chưa lấy được phiên bản nào của sản phẩm (đoạn code trên không hoạt động với một số sản phẩm)
    if len(storages) == 0:
        # Sử dụng XPATH khác để kiểm tra và lấy các phiên bản của sản phẩm
        try:

            # Lấy các phiên bản của sản phẩm
            storage_list = driver.find_elements(
                By.XPATH, "//div[@class='tab']/a[@class]"
            )
            for storage in storage_list:
                if storage.text != "" and storage not in storages:
                    storages.append(storage.text)

        except:
            pass

    # Kiểm tra và lấy các màu của sản phẩm
    try:

        # Lấy màu hiện tại của sản phẩm
        color = driver.find_element(
            By.XPATH,
            "//div[@class='box03 color group desk']/a[@class='box03__item item act']",
        ).text
        colors.append(color)

        # Lấy các màu khác của sản phẩm
        color_list = driver.find_elements(
            By.XPATH,
            "//div[@class='box03 color group desk']/a[@class='box03__item item ']",
        )
        for color in color_list:
            if color.text != "" and color not in colors:
                colors.append(color.text)

    except:
        pass

    # Nếu chưa lấy được màu nào của sản phẩm (đoạn code trên không hoạt động với một số sản phẩm)
    if len(colors) == 0:
        # Sử dụng XPATH khác để kiểm tra và lấy các màu của sản phẩm
        try:
            color_list = driver.find_elements(
                By.XPATH,
                "//div[@class='p-color']/a[@class]",
            )
            # Duyệt qua các màu và chuyển chúng từ rgb sang tên
            for color in color_list:
                color = color.get_attribute("style")
                color = re.search(r"rgb\((\d+), (\d+), (\d+)\)", color)
                if color:
                    rgb = tuple(map(int, color.groups()))
                    actual_name, closest_name = get_colour_name(rgb)
                    if actual_name != None:
                        color_name = actual_name
                    else:
                        color_name = closest_name
                    if color_name not in colors:
                        colors.append(color_name)

        except:
            pass

    # Kiểm tra và lấy các link của sản phẩm
    try:

        # Lấy link của sản phẩm
        link_list = driver.find_elements(By.XPATH, "//div[@class='tab']/a[@class]")
        for link in link_list:
            if link.get_attribute("href") not in links:
                links.append(link.get_attribute("href"))

    except:
        pass

    # Nếu chưa lấy được link nào của sản phẩm (đoạn code trên không hoạt động với một số sản phẩm)
    if len(links) == 0:
        # Sử dụng XPATH khác để kiểm tra và lấy các màu của sản phẩm
        try:

            # Lấy link hiện tại của sản phẩm
            # Bỏ phần sales sau dấu "?", các link vẫn hoạt động bình thường
            links.append(driver.current_url.split("?")[0])

            # Lấy các link khác của sản phẩm
            link_list = driver.find_elements(
                By.XPATH,
                "//div[@class='box03 group desk']/a[@class='box03__item item ']",
            )
            for link in link_list:
                link = link.get_attribute("href")
                links.append(link.split("?")[0])

        except:
            pass

    # Khởi tạo danh sách toàn bộ thông số của sản phẩm
    details = [name, image, links, colors, storages]

    # Kiểm tra và Lấy các thông số còn lại của sản phẩm bao gồm:
    # Màn hình,Camera sau,Camera trước,Hệ điều hành & CPU,Bộ nhớ & Lưu trữ,Kết nối,Pin & Sạc,Tiện ích,Thông tin chung
    try:

        # Click vào Xem thêm cấu hình chi tiết
        driver.find_element(
            By.XPATH, "//span[@class='btn-detail btn-short-spec ']"
        ).click()
        sleep(5)

        """
        "29"   : Màn hình           (Công nghệ màn hình, Độ phân giải, Màn hình rộng, Độ sáng tối đa, Mặt kính cảm ứng)
        "1841" : Camera sau         (Độ phân giải, Quay phim, Đèn Flash, Tính năng)
        "2701" : Camera trước       (Độ phân giải, Tính năng)
        "2121" : Hệ điều hành & CPU (Hệ điều hành, Chip xử lý (CPU), Tốc độ CPU, Chip đồ họa (GPU))
        "22"   : Bộ nhớ & Lưu trữ   (RAM, Dung lượng lưu trữ, Danh bạ)
        "24"   : Kết nối            (Mạng di động, SIM, Wifi, GPS, Bluetooth, Cổng kết nối/sạc, Jack tai nghe)
        "2122" : Pin & Sạc          (Dung lượng pin, Loại pin, Hỗ trợ sạc tối đa, Công nghệ pin)
        "19"   : Tiện ích           (Bảo mật nâng cao, Tính năng đặc biệt, Kháng nước, bụi, Ghi âm, Xem phim, Nghe nhạc)
        "28"   : Thông tin chung    (Thiết kế, Chất liệu, Kích thước, khối lượng, Thời điểm ra mắt, Hãng)
        
        Các thông số trên sẽ được lưu dưới sang dictionary như sau:
        {
        'Công nghệ màn hình': 'OLED',
        'Độ phân giải': 'Super Retina XDR (1290 x 2796 Pixels)',
        'Màn hình rộng': '6.7" - Tần số quét 120 Hz',
        'Độ sáng tối đa': '2000 nits',
        'Mặt kính cảm ứng': 'Kính cường lực Ceramic Shield'
        }
        
        Sản phẩm nào thiếu thông số nào sẽ để trống thông số đó
        """
        param_list = ["29", "1841", "2701", "2121", "22", "24", "2122", "19", "28"]
        for param in param_list:
            try:
                elements_left = driver.find_elements(
                    By.XPATH,
                    "//ul[@class='ulist ']/li[@data-group-id='"
                    + param
                    + "']/div[@class='ctLeft']",
                )
                elements_right = driver.find_elements(
                    By.XPATH,
                    "//ul[@class='ulist ']/li[@data-group-id='"
                    + param
                    + "']/div[@class='ctRight']",
                )
                data_dict = {
                    left.text: right.text
                    for left, right in zip(elements_left, elements_right)
                }
                details.append(data_dict.copy())
            except:
                details.append({})

    except:
        pass

    # Một vài sản phẩm sẽ có XPATH khác sẽ chạy đoạn code dưới đây với chức năng tương tự như trên
    try:
        driver.find_element(
            By.XPATH, "//span[@class='btn-detail btn-short-spec not-have-instruction']"
        ).click()
        sleep(5)

        param_list = ["29", "1841", "2701", "2121", "22", "24", "2122", "19", "28"]
        for param in param_list:
            elements_left = driver.find_elements(
                By.XPATH,
                "//ul[@class='ulist ']/li[@data-group-id='"
                + param
                + "']/div[@class='ctLeft']",
            )
            elements_right = driver.find_elements(
                By.XPATH,
                "//ul[@class='ulist ']/li[@data-group-id='"
                + param
                + "']/div[@class='ctRight']",
            )
            data_dict = {
                left.text: right.text
                for left, right in zip(elements_left, elements_right)
            }
            details.append(data_dict.copy())
    except:
        pass

    # Một vài sản phẩm sẽ có XPATH khác sẽ chạy đoạn code dưới đây với chức năng tương tự như trên
    try:
        driver.find_element(By.XPATH, "//a[@class='viewmore']").click()
        sleep(5)

        elements = driver.find_elements(By.XPATH, "//ul[@class='parameterfull']/li")

        data_dict = {}
        for idx, element in enumerate(elements):
            if idx == 0:
                continue
            attribute = element.get_attribute("class")
            if attribute != "":
                left = driver.find_element(
                    By.XPATH,
                    f"//ul[@class='parameterfull']/li[@class='{attribute}']/span",
                )
                right = driver.find_element(
                    By.XPATH,
                    f"//ul[@class='parameterfull']/li[@class='{attribute}']/div",
                )
                left_text = extract_text1(left.get_attribute("outerHTML"))
                right_text = extract_text2(right.get_attribute("outerHTML"))
                data_dict[left_text] = right_text
            else:
                details.append(data_dict.copy())
                data_dict.clear()
        details.append(data_dict.copy())

    except:
        pass

    # Lưu các thông số vào file data_tmp.csv
    with open("data_tmp.csv", "a", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(details)

    # Đóng webdriver
    sleep(5)
    driver.close()


def main():

    # Thu thập các thông số từ thế giới di động
    nums = [1]
    for i in nums:
        crawl(i)


if __name__ == "__main__":
    main()
