import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import requests
from io import BytesIO
import re

# Add this at the beginning of your file, after imports
st.markdown("""
<style>
    /* Color Variables */
    :root {
        --primary-color: #06F567;
        --primary-dark: #05d45a;
        --primary-light: #39f786;
        --primary-bg: #e6fff0;
        --text-dark: #1a1a1a;
        --text-light: #ffffff;
    }

    /* Global Styles */
    [data-testid="stAppViewContainer"] {
        background-color: var(--primary-bg);
    }
    
    /* Header Styles */
    .main-header {
        color: var(--text-dark);
        text-align: center;
        padding: 2rem 0;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0;
        text-shadow: 2px 2px 4px rgba(6, 245, 103, 0.2);
    }
    
    .sub-header {
        color: var(--text-dark);
        text-align: center;
        font-size: 1.5rem;
        margin-top: 0;
        margin-bottom: 2rem;
        opacity: 0.8;
    }
    
    /* Stats Section */
    .section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(6, 245, 103, 0.1);
        margin: 2rem 0;
        border: 1px solid rgba(6, 245, 103, 0.1);
    }
    
    .stat-box {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: var(--text-dark);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        height: 100%;
        transition: transform 0.2s;
    }
    
    .stat-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(6, 245, 103, 0.2);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Section Headers */
    .section-header {
        color: var(--text-dark);
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 0.5rem;
    }
    
    /* Car Card Styles */
    .car-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 15px rgba(6, 245, 103, 0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(6, 245, 103, 0.1);
    }
    
    .car-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(6, 245, 103, 0.2);
        border-color: var(--primary-color);
    }
    
    .car-card h4 {
        color: var(--text-dark);
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .car-card .price {
        color: var(--primary-dark);
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: var(--text-dark);
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(6, 245, 103, 0.3);
    }
    
    /* Filter Panel */
    .filter-panel {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(6, 245, 103, 0.1);
        border: 1px solid rgba(6, 245, 103, 0.1);
    }
    
    /* Form Fields */
    [data-testid="stTextInput"] > div > div > input {
        border-color: var(--primary-color);
    }
    
    [data-testid="stTextInput"] > div > div > input:focus {
        box-shadow: 0 0 0 2px rgba(6, 245, 103, 0.2);
    }
    
    /* Select Boxes */
    [data-testid="stSelectbox"] {
        border-color: var(--primary-color);
    }
    
    /* Alerts and Info Boxes */
    .stAlert {
        background-color: var(--primary-bg);
        border-left-color: var(--primary-color);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: var(--primary-color);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: var(--primary-bg);
        border: 1px solid var(--primary-color);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 10px;
        margin-top: 3rem;
        box-shadow: 0 -2px 10px rgba(6, 245, 103, 0.1);
    }
    
    .footer p {
        color: var(--text-dark);
        opacity: 0.8;
    }
    
    /* Booking Steps */
    .booking-step {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid var(--primary-color);
    }
    
    .booking-step.active {
        background: var(--primary-bg);
        box-shadow: 0 2px 10px rgba(6, 245, 103, 0.2);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .sub-header {
            font-size: 1.2rem;
        }
        
        .section {
            padding: 1rem;
        }
        
        .car-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# Tạo dữ liệu xe
@st.cache_data
def load_data():
    data = {
        'Tỉnh/Thành phố': ['Hà Nội', 'Hà Nội', 'Hồ Chí Minh', 'Hồ Chí Minh', 'Đà Nẵng',
                           'Đà Nẵng', 'Cần Thơ', 'Cần Thơ', 'Hải Phòng', 'Hải Phòng',
                           'Khánh Hòa', 'Khánh Hòa'],
        'Quận/Huyện': ['Hoàng Mai', 'Hoàng Mai', 'Quận 1', 'Quận 1', 'Hải Châu',
                       'Hải Châu', 'Ninh Kiều', 'Cái Răng', 'Lê Chân', 'Lê Chân',
                       'Nha Trang', 'Nha Trang'],
        'Dealer Name': ['ABC Vinfast Dealer', 'ABC Vinfast Dealer', 'XYZ Vinfast Dealer',
                        'XYZ Vinfast Dealer', 'Premier Vinfast Dealer', 'Green Motors Dealer',
                        'ABC Vinfast Dealer', 'XYZ Vinfast Dealer', 'Red Dragon Dealer',
                        'Red Dragon Dealer', 'Green Motors Dealer', 'Red Dragon Dealer'],
        'Địa chỉ cụ thể': ['123 Linh Đàm', '123 Linh Đàm', '45 Lê Lợi', '45 Lê Lợi',
                           '98 Hải Châu', '10 Lê Duẩn', '35 Ninh Kiều', '27 Cái Răng',
                           '73 Lạch Tray', '73 Lạch Tray', '66 Trần Phú', '89 Hùng Vương'],
        'Model': ['VF e34', 'VF 8', 'VF e34', 'VF 7', 'VF 8', 'VF 9', 'VF e34', 'VF 8',
                  'VF e34', 'VF 7', 'VF 7', 'VF 9'],
        'Image Path': ['vf_e34.jpg', 'vf_8.jpg', 'vf_e34.jpg', 'vf_7.jpg', 'vf_8.jpg',
                       'vf_9.jpg', 'vf_e34.jpg', 'vf_8.jpg', 'vf_e34.jpg', 'vf_7.jpg',
                       'vf_7.jpg', 'vf_9.jpg'],
        'Rental Fee (per day)': [500000, 700000, 600000, 650000, 700000, 750000, 450000,
                                 650000, 520000, 580000, 700000, 800000]
    }
    return pd.DataFrame(data)


# Load data
df = load_data()

# Mô tả mẫu xe
model_descriptions = {
    "VF e34": "Mẫu SUV cỡ nhỏ chạy điện với phạm vi hoạt động 285km, công suất 147 mã lực. Phù hợp cho di chuyển trong phố.",
    "VF 7": "Mẫu SUV cỡ vừa với thiết kế thể thao, công suất lên đến 349 mã lực, phạm vi hoạt động 400km. Lựa chọn lý tưởng cho gia đình.",
    "VF 8": "Mẫu SUV cỡ trung với không gian rộng rãi, công suất 402 mã lực, phạm vi hoạt động 420km. Đáp ứng nhu cầu di chuyển xa và thoải mái.",
    "VF 9": "Mẫu SUV cỡ lớn với 3 hàng ghế, không gian rộng rãi, công suất 408 mã lực, phạm vi hoạt động 438km. Phù hợp cho gia đình đông người."
}

# Thông số kỹ thuật chi tiết
model_specs = {
    "VF e34": {
        "Công suất": "147 mã lực",
        "Mô-men xoắn": "242 Nm",
        "Phạm vi hoạt động": "285 km",
        "Thời gian sạc": "6 giờ (10-80%)",
        "Số chỗ ngồi": "5",
        "Dài x Rộng x Cao": "4.300 x 1.793 x 1.613 mm",
        "Trọng lượng": "1.490 kg"
    },
    "VF 7": {
        "Công suất": "349 mã lực",
        "Mô-men xoắn": "500 Nm",
        "Phạm vi hoạt động": "400 km",
        "Thời gian sạc": "5 giờ (10-80%)",
        "Số chỗ ngồi": "5",
        "Dài x Rộng x Cao": "4.545 x 1.890 x 1.635 mm",
        "Trọng lượng": "1.680 kg"
    },
    "VF 8": {
        "Công suất": "402 mã lực",
        "Mô-men xoắn": "620 Nm",
        "Phạm vi hoạt động": "420 km",
        "Thời gian sạc": "5.5 giờ (10-80%)",
        "Số chỗ ngồi": "5",
        "Dài x Rộng x Cao": "4.750 x 1.934 x 1.667 mm",
        "Trọng lượng": "2.050 kg"
    },
    "VF 9": {
        "Công suất": "408 mã lực",
        "Mô-men xoắn": "640 Nm",
        "Phạm vi hoạt động": "438 km",
        "Thời gian sạc": "6 giờ (10-80%)",
        "Số chỗ ngồi": "7",
        "Dài x Rộng x Cao": "5.120 x 2.000 x 1.721 mm",
        "Trọng lượng": "2.470 kg"
    }
}


# Hàm lấy ảnh cho mỗi mẫu xe
@st.cache_data
def get_model_image(model):
    # VF8 và VF9 sử dụng ảnh từ thư mục img
    if model in ["VF 8", "VF 9"]:
        try:
            img_path = f"img/vf{model.split()[-1].lower()}.png"
            return Image.open(img_path)
        except FileNotFoundError:
            st.warning(f"{model} image not found. Please place {img_path} in the img folder.")
            return None
    
    # Các mẫu xe khác sử dụng URL công khai
    model_images = {
        "VF e34": "https://cdn.tgdd.vn/Products/Images/42/251903/Kit/vinfast-vf-e34-slider.jpg",
        "VF 7": "https://cdn.motor1.com/images/mgl/kooLPk/s1/vinfast-vf-7-phev.jpg",
    }

    # Sử dụng URL ảnh nếu có kết nối internet
    try:
        response = requests.get(model_images.get(model, "https://via.placeholder.com/400x300?text=VinFast"))
        img = Image.open(BytesIO(response.content))
        return img
    except:
        # Fallback if image can't be loaded
        return None


# Định dạng tiền
def format_currency(amount):
    return f"{amount:,.0f} VNĐ"


# Hàm tìm kiếm nâng cao
def advanced_search(df, keywords="", province=None, district=None, model=None, price_min=None, price_max=None):
    """
    Hàm tìm kiếm nâng cao với nhiều tiêu chí
    """
    result = df.copy()

    # Tìm kiếm theo từ khóa
    if keywords:
        keyword_pattern = '|'.join(re.escape(keyword.strip()) for keyword in keywords.split())
        mask = (
                result['Model'].str.contains(keyword_pattern, case=False, regex=True) |
                result['Dealer Name'].str.contains(keyword_pattern, case=False, regex=True) |
                result['Tỉnh/Thành phố'].str.contains(keyword_pattern, case=False, regex=True) |
                result['Quận/Huyện'].str.contains(keyword_pattern, case=False, regex=True) |
                result['Địa chỉ cụ thể'].str.contains(keyword_pattern, case=False, regex=True)
        )
        result = result[mask]

    # Lọc theo tỉnh/thành phố
    if province and province != "Tất cả":
        result = result[result['Tỉnh/Thành phố'] == province]

    # Lọc theo quận/huyện
    if district and district != "Tất cả":
        result = result[result['Quận/Huyện'] == district]

    # Lọc theo mẫu xe
    if model and model != "Tất cả":
        result = result[result['Model'] == model]

    # Lọc theo khoảng giá
    if price_min is not None:
        result = result[result['Rental Fee (per day)'] >= price_min]
    if price_max is not None:
        result = result[result['Rental Fee (per day)'] <= price_max]

    return result


# Hàm hiển thị thẻ xe
def display_car_card(car):
    st.markdown("<div class='car-card'>", unsafe_allow_html=True)

    # Layout thẻ xe
    col_img, col_info = st.columns([1, 1.5])

    with col_img:
        # Hiển thị ảnh xe
        img = get_model_image(car['Model'])
        if img is not None:
            st.image(img, use_container_width=True)

    with col_info:
        # Thông tin xe
        st.markdown(f"<h4>{car['Model']}</h4>", unsafe_allow_html=True)

        # Thông tin đại lý và địa chỉ
        st.markdown(f"<p><i class='fas fa-store'></i> <b>Đại lý:</b> {car['Dealer Name']}</p>", unsafe_allow_html=True)
        st.markdown(
            f"<p><i class='fas fa-map-marker-alt'></i> <b>Địa chỉ:</b> {car['Địa chỉ cụ thể']}, {car['Quận/Huyện']}, {car['Tỉnh/Thành phố']}</p>",
            unsafe_allow_html=True)

        # Hiển thị giá
        st.markdown(f"<p class='price'>{format_currency(car['Rental Fee (per day)'])}/ngày</p>", unsafe_allow_html=True)

        # Nút đặt xe và chi tiết
        book_key = f"book_{car['Model']}_{car['Địa chỉ cụ thể']}"
        details_key = f"details_{car['Model']}_{car['Địa chỉ cụ thể']}"

        # Sử dụng CSS để tạo layout cho buttons
        st.markdown("""
            <style>
            .button-container {
                display: flex;
                gap: 10px;
                margin-top: 10px;
            }
            .button-container > div {
                flex: 1;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='button-container'>", unsafe_allow_html=True)
        
        # Đặt xe ngay
        if st.button("Đặt xe ngay", key=book_key, use_container_width=True):
            st.session_state.booking_state['car_selected'] = {
                'model': car['Model'],
                'dealer': car['Dealer Name'],
                'address': f"{car['Địa chỉ cụ thể']}, {car['Quận/Huyện']}, {car['Tỉnh/Thành phố']}",
                'rental_fee': car['Rental Fee (per day)']
            }
            st.session_state.current_page = 'booking'
            st.session_state.booking_state['booking_step'] = 1
            st.rerun()

        # Xem chi tiết - Chuyển hướng đến trang chi tiết
        if st.button("Xem chi tiết", key=details_key, use_container_width=True):
            # Lưu thông tin xe được chọn
            st.session_state.car_detail = car['Model']
            st.session_state.car_detail_info = {
                'model': car['Model'],
                'dealer': car['Dealer Name'],
                'address': f"{car['Địa chỉ cụ thể']}, {car['Quận/Huyện']}, {car['Tỉnh/Thành phố']}",
                'rental_fee': car['Rental Fee (per day)']
            }
            # Chuyển đến trang chi tiết
            st.session_state.current_page = 'car_detail'
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# Kiểm tra trạng thái phiên làm việc và khởi tạo nếu cần
if 'booking_state' not in st.session_state:
    st.session_state.booking_state = {
        'car_selected': None,
        'booking_step': 0,
        'customer_info': {},
        'booking_dates': {},
        'total_days': 0,
        'total_amount': 0
    }

# Thêm session state để theo dõi trang hiện tại
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'  # Trang chủ là trang mặc định

# Thêm trạng thái cho xe được chọn để xem chi tiết
if 'car_detail' not in st.session_state:
    st.session_state.car_detail = None

# Add this at the beginning of your main script, with other session state initializations
if 'car_detail_info' not in st.session_state:
    st.session_state.car_detail_info = None

# Header
st.markdown("<h1 class='main-header'>🌿 Green Future</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-header'>Dịch vụ cho thuê xe điện VinFast hàng đầu Việt Nam</h2>", unsafe_allow_html=True)

# Nút quay lại trang chủ nếu đang ở trang khác
if st.session_state.current_page != 'home':
    if st.button('← Quay lại trang chủ'):
        st.session_state.current_page = 'home'
        st.session_state.car_detail = None
        st.session_state.booking_state['booking_step'] = 0
        st.rerun()

# Xử lý hiển thị trang dựa trên current_page
if st.session_state.current_page == 'home':
    # Trang chủ
    # Image Banner
    st.markdown("<div class='banner-container'>", unsafe_allow_html=True)
    try:
        banner_image = Image.open("img/banner.png")
        st.image(banner_image, use_container_width=True)
    except FileNotFoundError:
        st.warning("Banner image not found. Please place banner.png in the img folder.")
        st.image("https://via.placeholder.com/1200x400?text=Green+Future+Banner", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Thống kê chính
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
        st.markdown("<div class='stat-number'>12+</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-label'>Xe VinFast sẵn sàng</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
        st.markdown("<div class='stat-number'>6</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-label'>Tỉnh/Thành phố</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
        st.markdown("<div class='stat-number'>4</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-label'>Mẫu xe khác nhau</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
        st.markdown("<div class='stat-number'>24/7</div>", unsafe_allow_html=True)
        st.markdown("<div class='stat-label'>Hỗ trợ khách hàng</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Khu vực tìm kiếm và lọc
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-header'>Tìm kiếm xe VinFast</h3>", unsafe_allow_html=True)

    # Tìm kiếm đơn giản
    search_keyword = st.text_input("🔍 Tìm kiếm theo từ khóa", placeholder="Nhập tên mẫu xe, đại lý, địa điểm...")

    # Panel lọc nâng cao
    with st.expander("Lọc nâng cao", expanded=True):
        st.markdown("<div class='filter-panel'>", unsafe_allow_html=True)

        # Hàng 1: Lọc địa điểm và dòng xe
        col1, col2, col3 = st.columns(3)

        with col1:
            filter_province = st.selectbox("Tỉnh/Thành phố",
                                           options=["Tất cả"] + sorted(list(df['Tỉnh/Thành phố'].unique())),
                                           key="province_filter")

        with col2:
            if filter_province != "Tất cả":
                district_options = ["Tất cả"] + sorted(
                    list(df[df['Tỉnh/Thành phố'] == filter_province]['Quận/Huyện'].unique()))
            else:
                district_options = ["Tất cả"] + sorted(list(df['Quận/Huyện'].unique()))

            filter_district = st.selectbox("Quận/Huyện",
                                           options=district_options,
                                           key="district_filter")

        with col3:
            filter_model = st.selectbox("Dòng xe VinFast",
                                        options=["Tất cả"] + sorted(list(df['Model'].unique())),
                                        key="model_filter")

        # Hàng 2: Khoảng giá và sắp xếp
        col1, col2 = st.columns(2)

        with col1:
            min_price, max_price = st.select_slider(
                "Khoảng giá (VNĐ/ngày)",
                options=[400000, 450000, 500000, 550000, 600000, 650000, 700000, 750000, 800000],
                value=(400000, 800000)
            )

        with col2:
            sort_by = st.selectbox(
                "Sắp xếp theo",
                options=["Giá thấp đến cao", "Giá cao đến thấp", "A-Z theo mẫu xe"]
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # Áp dụng tìm kiếm và lọc
    filtered_results = advanced_search(
        df,
        keywords=search_keyword,
        province=filter_province,
        district=filter_district,
        model=filter_model,
        price_min=min_price,
        price_max=max_price
    )

    # Sắp xếp kết quả
    if sort_by == "Giá thấp đến cao":
        filtered_results = filtered_results.sort_values(by="Rental Fee (per day)")
    elif sort_by == "Giá cao đến thấp":
        filtered_results = filtered_results.sort_values(by="Rental Fee (per day)", ascending=False)
    elif sort_by == "A-Z theo mẫu xe":
        filtered_results = filtered_results.sort_values(by="Model")

    # Hiển thị kết quả tìm kiếm
    if not filtered_results.empty:
        st.markdown(f"<p>Tìm thấy <span class='highlight'>{len(filtered_results)}</span> kết quả</p>",
                    unsafe_allow_html=True)

        # Hiện thị kết quả trong grid
        for i in range(0, len(filtered_results), 2):
            col1, col2 = st.columns(2)

            # Xử lý cột 1
            if i < len(filtered_results):
                with col1:
                    car = filtered_results.iloc[i]
                    display_car_card(car)

            # Xử lý cột 2
            if i + 1 < len(filtered_results):
                with col2:
                    car = filtered_results.iloc[i + 1]
                    display_car_card(car)
    else:
        st.info("Không tìm thấy xe phù hợp với tiêu chí tìm kiếm. Vui lòng thử lại với điều kiện khác.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Giới thiệu dịch vụ
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-header'>Tại sao chọn Green Future?</h3>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("<h4 class='feature-header'>🌿 Thân thiện môi trường</h4>", unsafe_allow_html=True)
        st.write("Giảm phát thải carbon và góp phần bảo vệ môi trường với xe điện không khí thải.")

    with col2:
        st.markdown("<h4 class='feature-header'>💰 Tiết kiệm chi phí</h4>", unsafe_allow_html=True)
        st.write("Chi phí vận hành thấp hơn so với xe xăng truyền thống, tiết kiệm đáng kể.")

    with col3:
        st.markdown("<h4 class='feature-header'>🛡️ An toàn tuyệt đối</h4>", unsafe_allow_html=True)
        st.write("Các mẫu xe VinFast đều đạt chuẩn an toàn cao nhất, bảo vệ bạn và gia đình.")

    with col4:
        st.markdown("<h4 class='feature-header'>🎧 Hỗ trợ 24/7</h4>", unsafe_allow_html=True)
        st.write("Đội ngũ hỗ trợ kỹ thuật luôn sẵn sàng phục vụ bạn mọi lúc, mọi nơi.")

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_page == 'car_detail':
    # Trang chi tiết xe
    if st.session_state.car_detail and st.session_state.car_detail_info:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown(f"<h3 class='section-header'>Chi tiết xe {st.session_state.car_detail}</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1.5])

        with col1:
            img = get_model_image(st.session_state.car_detail)
            if img is not None:
                st.image(img, use_container_width=True)

        with col2:
            car_info = st.session_state.car_detail_info
            st.markdown(f"<h4>{car_info['model']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p><b>Đại lý:</b> {car_info['dealer']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p><b>Địa chỉ:</b> {car_info['address']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='price'>{format_currency(car_info['rental_fee'])}/ngày</p>", unsafe_allow_html=True)

            # Thêm nút đặt xe
            if st.button("Đặt xe ngay", key="detail_booking_btn", use_container_width=True):
                st.session_state.booking_state['car_selected'] = car_info
                st.session_state.current_page = 'booking'
                st.session_state.booking_state['booking_step'] = 1
                st.rerun()

        # Hiển thị thông số kỹ thuật
        st.markdown("<h5>Thông số kỹ thuật</h5>", unsafe_allow_html=True)
        specs = model_specs.get(st.session_state.car_detail, {})

        # Hiển thị thông số trong bảng
        specs_data = {'Thông số': list(specs.keys()), 'Giá trị': list(specs.values())}
        specs_df = pd.DataFrame(specs_data)
        st.table(specs_df)

        # Tính năng nổi bật
        st.markdown("<h5>Tính năng nổi bật</h5>", unsafe_allow_html=True)
        if st.session_state.car_detail == "VF e34":
            features = ["Hệ thống hỗ trợ lái ADAS", "Cảnh báo điểm mù", "Cảnh báo va chạm phía trước",
                        "Hỗ trợ đỗ xe tự động"]
        elif st.session_state.car_detail == "VF 7":
            features = ["Hệ thống hỗ trợ lái nâng cao", "Màn hình cảm ứng trung tâm 12.9 inch", "Trợ lý ảo",
                        "Hệ thống âm thanh cao cấp"]
        elif st.session_state.car_detail == "VF 8":
            features = ["Hệ thống tự lái cấp độ 2", "Màn hình AR-HUD", "Ghế massage", "Cửa sổ trời toàn cảnh"]
        elif st.session_state.car_detail == "VF 9":
            features = ["Hệ thống tự lái cấp độ 2+", "7 ghế ngồi rộng rãi", "Màn hình giải trí 15.6 inch",
                        "Hệ thống làm mát/sưởi ghế toàn xe"]
        else:
            features = []

        for feature in features:
            st.markdown(f"✓ {feature}")

    # Hiển thị đánh giá và nhận xét
    st.markdown("<h4>Đánh giá từ khách hàng</h4>", unsafe_allow_html=True)

    # Dữ liệu đánh giá giả lập
    reviews = [
        {"name": "Nguyễn Văn A", "rating": 5, "comment": "Xe chạy rất êm, pin trâu, rất hài lòng với dịch vụ!"},
        {"name": "Trần Thị B", "rating": 4, "comment": "Xe đẹp, rộng rãi. Chỉ tiếc là trạm sạc hơi ít."},
        {"name": "Lê Văn C", "rating": 5,
         "comment": "Thuê cho chuyến du lịch gia đình, mọi người đều thích. Sẽ thuê lại!"}
    ]

    for review in reviews:
        st.markdown(f"""
        <div style="border-left: 3px solid #00af66; padding-left: 10px; margin-bottom: 15px;">
            <p><b>{review['name']}</b> - {'⭐' * review['rating']}</p>
            <p>{review['comment']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Hiển thị xe tương tự
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-header'>Xe tương tự</h3>", unsafe_allow_html=True)

    # Lọc các xe khác cùng model nhưng khác đại lý hoặc địa điểm
    similar_cars = df[df['Model'] != st.session_state.car_detail].sample(min(4, len(df[df['Model'] != st.session_state.car_detail]))).reset_index()

    # Hiển thị trong lưới 2x2
    for i in range(0, len(similar_cars), 2):
        cols = st.columns(2)
        if i < len(similar_cars):
            with cols[0]:
                display_car_card(similar_cars.iloc[i])
        if i + 1 < len(similar_cars):
            with cols[1]:
                display_car_card(similar_cars.iloc[i + 1])

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_page == 'booking':
    # Trang đặt xe
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-header'>Đặt thuê xe</h3>", unsafe_allow_html=True)

    # Hiển thị thông tin xe đã chọn
    car_selected = st.session_state.booking_state['car_selected']
    st.markdown("<div class='car-card'>", unsafe_allow_html=True)
    st.markdown(f"<h4>Xe đã chọn: {car_selected['model']}</h4>", unsafe_allow_html=True)
    st.markdown(f"<p><b>Đại lý:</b> {car_selected['dealer']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p><b>Địa chỉ:</b> {car_selected['address']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='price'>{format_currency(car_selected['rental_fee'])}/ngày</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Form đặt xe
    with st.form("booking_form"):
        st.write("### Thông tin đặt xe")

        # Ngày nhận và trả xe
        col_date1, col_date2 = st.columns(2)
        with col_date1:
            start_date = st.date_input(
                "Ngày nhận xe:",
                value=datetime.date.today() + datetime.timedelta(days=1),
                min_value=datetime.date.today() + datetime.timedelta(days=1)
            )
        with col_date2:
            end_date = st.date_input(
                "Ngày trả xe:",
                value=datetime.date.today() + datetime.timedelta(days=3),
                min_value=start_date + datetime.timedelta(days=1)
            )

        # Tính số ngày thuê và tổng tiền
        rental_days = (end_date - start_date).days
        total_cost = car_selected['rental_fee'] * rental_days

        st.markdown(f"<p><b>Số ngày thuê:</b> {rental_days} ngày</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='price'>Tổng tiền: {format_currency(total_cost)}</p>", unsafe_allow_html=True)

        st.write("### Thông tin khách hàng")

        # Form thông tin khách hàng
        full_name = st.text_input("Họ và tên:")
        phone = st.text_input("Số điện thoại:")
        email = st.text_input("Email:")
        address = st.text_area("Địa chỉ:")
        id_number = st.text_input("Số CMND/CCCD:")

        st.write("### Phương thức thanh toán")
        payment_method = st.radio(
            "Chọn phương thức thanh toán:",
            options=["Thanh toán khi nhận xe", "Chuyển khoản ngân hàng", "Thẻ tín dụng/ghi nợ"]
        )

        agreement = st.checkbox("Tôi đồng ý với các điều khoản và điều kiện thuê xe")

        # Nút đặt xe và hủy (không lồng cột trong cột)
        submit_booking = st.form_submit_button("Xác nhận đặt xe", use_container_width=True)
        cancel_booking = st.form_submit_button("Hủy", use_container_width=True)

    # Xử lý sau khi form được submit
    if submit_booking:
        if full_name and phone and email and address and id_number and agreement:
            # Lưu thông tin đặt xe
            st.session_state.booking_state['customer_info'] = {
                'full_name': full_name,
                'phone': phone,
                'email': email,
                'address': address,
                'id_number': id_number
            }
            st.session_state.booking_state['booking_dates'] = {
                'start_date': start_date,
                'end_date': end_date
            }
            st.session_state.booking_state['total_days'] = rental_days
            st.session_state.booking_state['total_amount'] = total_cost
            st.session_state.booking_state['payment_method'] = payment_method
            st.session_state.booking_state['booking_step'] = 2

            # Chuyển sang trang xác nhận đặt xe
            st.session_state.current_page = 'booking_confirmation'
            st.rerun()
        else:
            st.error("Vui lòng điền đầy đủ thông tin và đồng ý với điều khoản để hoàn tất đặt xe.")

    if cancel_booking:
        # Reset trạng thái đặt xe và quay về trang chủ
        st.session_state.booking_state = {
            'car_selected': None,
            'booking_step': 0,
            'customer_info': {},
            'booking_dates': {},
            'total_days': 0,
            'total_amount': 0
        }
        st.session_state.current_page = 'home'
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.current_page == 'booking_confirmation':
    # Trang xác nhận đặt xe
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-header'>Xác nhận đặt xe</h3>", unsafe_allow_html=True)

    booking_info = st.session_state.booking_state
    customer_info = booking_info['customer_info']
    booking_dates = booking_info['booking_dates']

    # Sử dụng container thay vì columns
    left_info, right_info = st.columns(2)

    with left_info:
        st.write("### Thông tin xe")
        st.markdown(f"<p><b>Mẫu xe:</b> {booking_info['car_selected']['model']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Đại lý:</b> {booking_info['car_selected']['dealer']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Địa chỉ nhận xe:</b> {booking_info['car_selected']['address']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Ngày nhận xe:</b> {booking_dates['start_date'].strftime('%d/%m/%Y')}</p>",
                    unsafe_allow_html=True)
        st.markdown(f"<p><b>Ngày trả xe:</b> {booking_dates['end_date'].strftime('%d/%m/%Y')}</p>",
                    unsafe_allow_html=True)
        st.markdown(f"<p><b>Số ngày thuê:</b> {booking_info['total_days']} ngày</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Giá thuê:</b> {format_currency(booking_info['car_selected']['rental_fee'])}/ngày</p>",
                    unsafe_allow_html=True)
        st.markdown(f"<p class='price'>Tổng tiền: {format_currency(booking_info['total_amount'])}</p>",
                    unsafe_allow_html=True)

    with right_info:
        st.write("### Thông tin khách hàng")
        st.markdown(f"<p><b>Họ và tên:</b> {customer_info['full_name']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Số điện thoại:</b> {customer_info['phone']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Email:</b> {customer_info['email']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Địa chỉ:</b> {customer_info['address']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Số CMND/CCCD:</b> {customer_info['id_number']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Phương thức thanh toán:</b> {booking_info.get('payment_method', 'Chưa chọn')}</p>",
                    unsafe_allow_html=True)

    # Thông tin mã đặt xe
    booking_code = "GF" + datetime.datetime.now().strftime("%y%m%d%H%M%S")
    st.info(f"Mã đặt xe của bạn là: **{booking_code}**")
    st.success(
        "Cảm ơn bạn đã sử dụng dịch vụ của Green Future. Nhân viên của chúng tôi sẽ liên hệ với bạn trong vòng 30 phút để xác nhận thông tin đặt xe.")

    # Hiển thị thông tin thanh toán nếu chọn chuyển khoản
    if booking_info.get('payment_method') == "Chuyển khoản ngân hàng":
        st.markdown("""
        ### Thông tin thanh toán
        Vui lòng chuyển khoản đến tài khoản sau:

        **Ngân hàng:** Vietcombank  
        **Số tài khoản:** 0123456789  
        **Chủ tài khoản:** CÔNG TY TNHH GREEN FUTURE  
        **Nội dung chuyển khoản:** Mã đặt xe {0}
        """.format(booking_code), unsafe_allow_html=True)

    # Nút đặt xe mới
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Đặt xe mới", use_container_width=True):
            # Reset trạng thái đặt xe
            st.session_state.booking_state = {
                'car_selected': None,
                'booking_step': 0,
                'customer_info': {},
                'booking_dates': {},
                'total_days': 0,
                'total_amount': 0
            }
            st.session_state.current_page = 'home'
            st.rerun()

    with col2:
        # Tùy chọn để in hóa đơn
        if st.button("In hóa đơn", use_container_width=True):
            st.info(
                "Tính năng in hóa đơn đang được phát triển. Vui lòng kiểm tra email của bạn để nhận hóa đơn điện tử.")

    st.markdown("</div>", unsafe_allow_html=True)

# Giới thiệu dịch vụ và footer ở tất cả các trang
# Giới thiệu về VinFast
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("<h3 class='section-header'>Về xe điện VinFast</h3>", unsafe_allow_html=True)

st.write("""
VinFast là thương hiệu ô tô điện hàng đầu Việt Nam, với cam kết mang đến những sản phẩm chất lượng cao 
và thân thiện với môi trường. Green Future tự hào là đối tác chính thức của VinFast, cung cấp dịch vụ 
cho thuê xe điện VinFast với đa dạng mẫu xe từ VF e34, VF 7, VF 8 đến VF 9.

Tất cả các xe cho thuê tại Green Future đều là xe mới, được bảo dưỡng định kỳ và trang bị đầy đủ 
các tính năng an toàn hiện đại. Chúng tôi cam kết mang đến trải nghiệm thuê xe thuận tiện, 
an toàn và thân thiện với môi trường.
""")

# FAQ
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("<h3 class='section-header'>Câu hỏi thường gặp</h3>", unsafe_allow_html=True)

with st.expander("Làm thế nào để thuê xe VinFast tại Green Future?"):
    st.write("""
    Để thuê xe VinFast tại Green Future, bạn chỉ cần thực hiện các bước đơn giản sau:

    1. Tìm kiếm và chọn mẫu xe phù hợp trên trang web
    2. Nhấp vào nút "Đặt xe ngay"
    3. Điền thông tin cá nhân và thời gian thuê
    4. Xác nhận đặt xe
    5. Nhân viên của chúng tôi sẽ liên hệ để xác nhận và hướng dẫn thủ tục nhận xe
    """)

with st.expander("Chi phí thuê xe bao gồm những gì?"):
    st.write("""
    Chi phí thuê xe tại Green Future bao gồm:

    - Phí thuê xe theo ngày
    - Bảo hiểm xe cơ bản
    - Hỗ trợ kỹ thuật 24/7
    - Pin xe đã được sạc đầy khi giao

    Chi phí không bao gồm:

    - Phí sạc pin trong quá trình sử dụng
    - Phí cầu đường, bến bãi
    - Phí vệ sinh xe (nếu xe quá bẩn khi trả)
    - Phí sửa chữa nếu có hư hỏng do người thuê gây ra
    """)

with st.expander("Cần những giấy tờ gì để thuê xe?"):
    st.write("""
    Để thuê xe tại Green Future, bạn cần chuẩn bị:

    - CMND/CCCD hoặc Hộ chiếu (bản gốc)
    - Giấy phép lái xe hợp lệ (bản gốc)
    - Hộ khẩu/KT3 hoặc giấy tờ chứng minh nơi cư trú
    - Đặt cọc theo quy định (tiền mặt hoặc chuyển khoản)
    """)

with st.expander("Làm thế nào để sạc xe điện VinFast?"):
    st.write("""
    Xe điện VinFast có thể được sạc bằng nhiều cách:

    1. Trạm sạc công cộng VinFast trên toàn quốc
    2. Sạc tại nhà với bộ sạc tiêu chuẩn (đối với VF e34)
    3. Trạm sạc tại các đại lý VinFast

    Green Future sẽ cung cấp thẻ sạc và hướng dẫn chi tiết cách sạc xe khi bàn giao.
    """)

with st.expander("Chính sách hủy đặt xe như thế nào?"):
    st.write("""
    Chính sách hủy đặt xe của Green Future:

    - Hủy trước 48 giờ: Hoàn tiền 100%
    - Hủy trong vòng 24-48 giờ: Hoàn tiền 70%
    - Hủy trong vòng 12-24 giờ: Hoàn tiền 50%
    - Hủy dưới 12 giờ: Không hoàn tiền

    Trường hợp bất khả kháng sẽ được xem xét cụ thể.
    """)

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("© 2025 Green Future. Tất cả quyền được bảo lưu.", unsafe_allow_html=True)
st.markdown("Địa chỉ: Tòa văn phòng Symphony, Đường Chu Huy Mân, Khu đô thị Vinhomes Riverside, Phường Phúc Lợi, Quận Long Biên, Thành phố Hà Nội, Việt Nam | Hotline: 0896 229 555 | Email: support@greenfuture.tech",
            unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
