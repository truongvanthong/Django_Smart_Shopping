import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .sentiment_analysis import plot_sentiment
from products.models import Product, ProductSpec
from user.views import check_history
# Create your views here.

def search(request):
    if request.method == 'GET':
        search_text = request.GET.get('search_text', '')
        products = Product.objects.filter(product_name__icontains=search_text)
        return render(request, 'search_results.html', {'products': products})

@csrf_exempt
def compare(request):
    context = {}

    if request.method == 'POST':
        searchpr1 = request.POST.get('searchpr1')
        searchpr2 = request.POST.get('searchpr2')

        try:

            product1 = Product.objects.get(product_name=searchpr1)
            product2 = Product.objects.get(product_name=searchpr2)

            product1_specs = ProductSpec.objects.filter(product=product1)
            product2_specs = ProductSpec.objects.filter(product=product2)

            product1_thongtin_chung = json.loads(product1_specs[0].thongtin_chung.replace("'", '"'))
            product2_thongtin_chung = json.loads(product2_specs[0].thongtin_chung.replace("'", '"'))
            
            prod1_size_weight = product1_thongtin_chung.get('Kích thước, khối lượng:', '').split(' - ')
            prod2_size_weight = product2_thongtin_chung.get('Kích thước, khối lượng:', '').split(' - ')

            product1_tien_ich = json.loads(product1_specs[0].tien_ich.replace("'", '"'))
            product2_tien_ich = json.loads(product2_specs[0].tien_ich.replace("'", '"'))

            product1_os_cpu = json.loads(product1_specs[0].OS_CPU.replace("'", '"'))
            product2_os_cpu = json.loads(product2_specs[0].OS_CPU.replace("'", '"'))

            product1_memory_storage = json.loads(product1_specs[0].memory_storage.replace("'", '"'))
            product2_memory_storage = json.loads(product2_specs[0].memory_storage.replace("'", '"'))

            product1_screen = json.loads(json.dumps(eval(product1_specs[0].screen))) if product1_specs[0].screen is not None else {}
            product2_screen = json.loads(json.dumps(eval(product2_specs[0].screen))) if product2_specs[0].screen is not None else {}

            product1_size_refresh_rate = product1_screen.get('Màn hình rộng:', '').split(' - ')
            product2_size_refresh_rate = product2_screen.get('Màn hình rộng:', '').split(' - ')

            product1_resolution = product1_screen.get('Độ phân giải:', '').split('(')
            product2_resolution = product2_screen.get('Độ phân giải:', '').split('(')

            product1_rear_cam = json.loads(json.dumps(eval(product1_specs[0].rear_camera))) if product1_specs[0].rear_camera is not None else {}
            product2_rear_cam = json.loads(json.dumps(eval(product2_specs[0].rear_camera))) if product2_specs[0].rear_camera is not None else {}

            product1_front_cam = json.loads(json.dumps(eval(product1_specs[0].front_camera))) if product1_specs[0].front_camera is not None else {}
            product2_front_cam = json.loads(json.dumps(eval(product2_specs[0].front_camera))) if product2_specs[0].front_camera is not None else {}

            product1_ket_noi = json.loads(json.dumps(eval(product1_specs[0].ket_noi))) if product1_specs[0].ket_noi is not None else {}
            product2_ket_noi = json.loads(json.dumps(eval(product2_specs[0].ket_noi))) if product2_specs[0].ket_noi is not None else {}

            product1_battery = json.loads(json.dumps(eval(product1_specs[0].pin_sac))) if product1_specs[0].pin_sac is not None else {}
            product2_battery = json.loads(json.dumps(eval(product2_specs[0].pin_sac))) if product2_specs[0].pin_sac is not None else {}

            product1_fpt_price, product1_tgdd_price = product1.FPT_product_price, product1.TGDD_product_price
            product2_fpt_price, product2_tgdd_price = product2.FPT_product_price, product2.TGDD_product_price
                                                                                                        

            product1_min_price = min(product1_fpt_price, product1_tgdd_price)
            product2_min_price = min(product2_fpt_price, product2_tgdd_price)

            product1_tgdd_sa = plot_sentiment(product1.product_id, company_id=1).to_html(full_html=False, include_plotlyjs='cdn')
            product1_fpt_sa = plot_sentiment(product1.product_id, company_id=2).to_html(full_html=False, include_plotlyjs='cdn')

            product2_tgdd_sa = plot_sentiment(product2.product_id, company_id=1).to_html(full_html=False, include_plotlyjs='cdn')
            product2_fpt_sa = plot_sentiment(product2.product_id, company_id=2).to_html(full_html=False, include_plotlyjs='cdn')

            existing_history = check_history(product1.product_id, product2.product_id, request.user)

            context = {
                'product1': product1,
                'product2': product2,
                'product1_brand': product1_thongtin_chung.get('Hãng:', '').split('.')[0],
                'product2_brand': product2_thongtin_chung.get('Hãng:', '').split('.')[0],
                'product1_release_date': product1_thongtin_chung.get('Thời điểm ra mắt:', ''),
                'product2_release_date': product2_thongtin_chung.get('Thời điểm ra mắt:', ''),
                'product1_height':prod1_size_weight[0],
                'product2_height': prod2_size_weight[0],
                'product1_width': prod1_size_weight[1] if len(prod1_size_weight) > 1 else '',
                'product2_width': prod2_size_weight[1] if len(prod2_size_weight) > 1 else '',
                'product1_depth': prod1_size_weight[2] if len(prod1_size_weight) > 2 else '',
                'product2_depth': prod2_size_weight[2] if len(prod2_size_weight) > 2 else '',
                'product1_weight': prod1_size_weight[3] if len(prod1_size_weight) > 3 else '',
                'product2_weight': prod2_size_weight[3] if len(prod2_size_weight) > 3 else '',
                'product1_water_resistant': product1_tien_ich.get('Kháng nước, bụi:', ''),
                'product2_water_resistant': product2_tien_ich.get('Kháng nước, bụi:', ''),
                'product1_cpu': product1_os_cpu.get('Chip xử lý (CPU):', ''),
                'product2_cpu': product2_os_cpu.get('Chip xử lý (CPU):', ''),
                'product1_cpu_speed': product1_os_cpu.get('Tốc độ CPU:', ''),
                'product2_cpu_speed': product2_os_cpu.get('Tốc độ CPU:', ''),
                'product1_gpu': product1_os_cpu.get('Chip đồ họa (GPU):', ''),
                'product2_gpu': product2_os_cpu.get('Chip đồ họa (GPU):', ''),
                'product1_ram': product1_memory_storage.get('RAM:', ''),
                'product2_ram': product2_memory_storage.get('RAM:', ''),
                'product1_screen_size': product1_size_refresh_rate[0],
                'product2_screen_size': product2_size_refresh_rate[0],
                'product1_refresh_rate': product1_size_refresh_rate[1] if len(product1_size_refresh_rate) > 1 else '',
                'product2_refresh_rate': product2_size_refresh_rate[1] if len(product2_size_refresh_rate) > 1 else '',
                'product1_screen_tech': product1_screen.get('Công nghệ màn hình:', ''),
                'product2_screen_tech': product2_screen.get('Công nghệ màn hình:', ''),
                'product1_screen_std': product1_resolution[0],
                'product2_screen_std': product2_resolution[0],
                'product1_screen_res': product1_resolution[1].replace(')', '') if len(product1_resolution) > 1 else '',
                'product2_screen_res': product2_resolution[1].replace(')', '') if len(product2_resolution) > 1 else '',
                'product1_glass': product1_screen.get('Mặt kính cảm ứng:', ''),
                'product2_glass': product2_screen.get('Mặt kính cảm ứng:', ''),
                'product1_rom': product1_memory_storage.get('Dung lượng lưu trữ:', ''),
                'product2_rom': product2_memory_storage.get('Dung lượng lưu trữ:', ''),
                'product1_sdcard': product1_memory_storage.get('Thẻ nhớ:', 'Không'),
                'product2_sdcard': product2_memory_storage.get('Thẻ nhớ:', 'Không'),
                'product1_danhba': product1_memory_storage.get('Danh bạ:', ''),
                'product2_danhba': product2_memory_storage.get('Danh bạ:', ''),
                'product1_rear_cam': product1_rear_cam.get('Độ phân giải:', ''),
                'product2_rear_cam': product2_rear_cam.get('Độ phân giải:', ''),
                'product1_rear_cam_video': product1_rear_cam.get('Quay phim:', '').split('\n'),
                'product2_rear_cam_video': product2_rear_cam.get('Quay phim:', '').split('\n'),
                'product1_rear_cam_flash': product1_rear_cam.get('Đèn Flash:', 'Không'),
                'product2_rear_cam_flash': product2_rear_cam.get('Đèn Flash:', 'Không'),
                'product1_rear_cam_features': product1_rear_cam.get('Tính năng:', '').split('\n'),
                'product2_rear_cam_features': product2_rear_cam.get('Tính năng:', '').split('\n'),
                'product1_front_cam': product1_front_cam.get('Độ phân giải:', ''),
                'product2_front_cam': product2_front_cam.get('Độ phân giải:', ''),
                'product1_front_cam_features': product1_front_cam.get('Tính năng:', '').split('\n'),
                'product2_front_cam_features': product2_front_cam.get('Tính năng:', '').split('\n'),
                'product1_security': product1_tien_ich.get('Bảo mật nâng cao:', '').split('\n'),
                'product2_security': product2_tien_ich.get('Bảo mật nâng cao:', '').split('\n'),
                'product1_network': product1_ket_noi.get('Mạng di động:', ''),
                'product2_network': product2_ket_noi.get('Mạng di động:', ''),
                'product1_sim': product1_ket_noi.get('SIM:', ''),
                'product2_sim': product2_ket_noi.get('SIM:', ''),
                'product1_wifi': product1_ket_noi.get('Wifi:', '').split('\n'),
                'product2_wifi': product2_ket_noi.get('Wifi:', '').split('\n'),
                'product1_GPS': product1_ket_noi.get('GPS:', '').split('\n'),
                'product2_GPS': product2_ket_noi.get('GPS:', '').split('\n'),
                'product1_bluetooth': product1_ket_noi.get('Bluetooth:', '').split('\n'),
                'product2_bluetooth': product2_ket_noi.get('Bluetooth:', '').split('\n'),
                'product1_port': product1_ket_noi.get('Cổng kết nối/sạc:', '').split('\n'),
                'product2_port': product2_ket_noi.get('Cổng kết nối/sạc:', '').split('\n'),
                'product1_headphone': product1_ket_noi.get('Jack tai nghe:', ''),
                'product2_headphone': product2_ket_noi.get('Jack tai nghe:', ''),
                'product1_oth_connect': product1_ket_noi.get('Kết nối khác:', '').split('\n'),
                'product2_oth_connect': product2_ket_noi.get('Kết nối khác:', '').split('\n'),
                'product1_battery_capacity': product1_battery.get('Dung lượng pin:', ''),
                'product2_battery_capacity': product2_battery.get('Dung lượng pin:', ''),
                'product1_battery_type': product1_battery.get('Loại pin:', ''),
                'product2_battery_type': product2_battery.get('Loại pin:', ''),
                'product1_battery_charging': product1_battery.get('Hỗ trợ sạc tối đa:', ''),
                'product2_battery_charging': product2_battery.get('Hỗ trợ sạc tối đa:', ''),
                'product1_battery_tech': product1_battery.get('Công nghệ pin:', '').split('\n'),
                'product2_battery_tech': product2_battery.get('Công nghệ pin:', '').split('\n'),
                'product1_changer_include': product1_battery.get('Sạc kèm theo máy:', 'Không'),
                'product2_changer_include': product2_battery.get('Sạc kèm theo máy:', 'Không'),
                'product1_os': product1_os_cpu.get('Hệ điều hành:', '').split(' ')[0],
                'product2_os': product2_os_cpu.get('Hệ điều hành:', '').split(' ')[0],
                'product1_os_version': product1_os_cpu.get('Hệ điều hành:', ''),
                'product2_os_version': product2_os_cpu.get('Hệ điều hành:', ''),
                'product1_other_features': product1_tien_ich.get('Tính năng đặc biệt:', '').split('\n'),
                'product2_other_features': product2_tien_ich.get('Tính năng đặc biệt:', '').split('\n'),
                'product1_min_price': product1_min_price,
                'product2_min_price': product2_min_price,
                'product1_fpt_price': product1_fpt_price,
                'product2_fpt_price': product2_fpt_price,
                'product1_tgdd_price': product1_tgdd_price,
                'product2_tgdd_price': product2_tgdd_price,
                'product1_tgdd_sa': product1_tgdd_sa,
                'product1_fpt_sa': product1_fpt_sa,
                'product2_tgdd_sa': product2_tgdd_sa,
                'product2_fpt_sa': product2_fpt_sa,
                'existing_history': existing_history
            }

            return render(request, 'compare.html', context)
        
        except Product.DoesNotExist:
            # Xử lý khi sản phẩm không tồn tại
            pass
    # Trả về template và truyền test_string vào context
    return render(request, 'compare.html', context)