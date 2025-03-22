import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import re
import os
import base64
from io import BytesIO

# Set page config at the start of the file
st.set_page_config(
    page_title="Green Future - Thuê xe VinFast",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for full-screen landscape layout
st.markdown("""
<style>
    /* Full screen layout */
    .stApp {
        max-width: 100vw !important;
        padding: 0 !important;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #1a472a, #2e8b57);
        color: white;
        padding: 2rem 4rem;
        margin: 0;
        width: 100%;
        text-align: center;
        font-size: 3.5rem;
    }
    
    .sub-header {
        background: rgba(46, 139, 87, 0.1);
        color: #1a472a;
        padding: 1rem 4rem;
        margin: 0 0 2rem 0;
        text-align: center;
        font-size: 1.8rem;
    }
    
    /* Banner container */
    .banner-container {
        width: 100%;
        max-height: 60vh;
        overflow: hidden;
        position: relative;
        margin-bottom: 2rem;
    }
    
    .banner-container img {
        width: 100%;
        object-fit: cover;
    }
    
    /* Statistics section */
    .section {
        padding: 2rem 4rem;
        margin: 0;
        background: white;
    }
    
    .stat-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 20px;
        padding: 2.5rem 1.5rem;
        text-align: center;
        box-shadow: 0 10px 20px rgba(46, 139, 87, 0.1),
                   0 6px 6px rgba(0, 0, 0, 0.05);
        margin: 1rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(46, 139, 87, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .stat-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #1a472a, #2e8b57);
    }
    
    .stat-box:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 30px rgba(46, 139, 87, 0.2),
                   0 10px 10px rgba(0, 0, 0, 0.05);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1a472a, #2e8b57);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 1.1rem;
        color: #495057;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    @media (max-width: 768px) {
        .stat-box {
            padding: 1.5rem 1rem;
        }
        
        .stat-number {
            font-size: 2.5rem;
        }
        
        .stat-label {
            font-size: 0.9rem;
        }
    }
    
    /* Search and filter section */
    .filter-panel {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
    }
    
    /* Car cards grid */
    .car-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    
    .car-card:hover {
        transform: translateY(-5px);
    }
    
    /* Price styling */
    .price {
        font-size: 1.5rem;
        color: #2e8b57;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #2e8b57;
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        font-weight: bold;
        transition: background-color 0.2s;
    }
    
    .stButton button:hover {
        background-color: #1a472a;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
            padding: 1.5rem 2rem;
        }
        
        .sub-header {
            font-size: 1.3rem;
            padding: 1rem 2rem;
        }
        
        .section {
            padding: 1rem 2rem;
        }
        
        .stat-number {
            font-size: 2rem;
        }
        
        .stat-label {
            font-size: 1rem;
        }
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2e8b57;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #1a472a;
    }
</style>
""", unsafe_allow_html=True)

# Add this JavaScript function at the beginning of your script, after the CSS styles
st.markdown("""
    <script>
        function scrollToTop() {
            window.scrollTo(0, 0);
        }
    </script>
""", unsafe_allow_html=True)

# Add this CSS to ensure smooth scrolling
st.markdown("""
    <style>
        html {
            scroll-behavior: smooth;
        }
    </style>
""", unsafe_allow_html=True)


# Tạo dữ liệu xe
@st.cache_data
def load_data():
    data = {
        'Tỉnh/Thành phố': [
            # Hà Nội
            'Hà Nội', 'Hà Nội', 'Hà Nội', 'Hà Nội', 'Hà Nội', 'Hà Nội',
            # Hồ Chí Minh
            'Hồ Chí Minh', 'Hồ Chí Minh', 'Hồ Chí Minh', 'Hồ Chí Minh', 'Hồ Chí Minh', 'Hồ Chí Minh',
            # Đà Nẵng
            'Đà Nẵng', 'Đà Nẵng', 'Đà Nẵng', 'Đà Nẵng',
            # Hải Phòng
            'Hải Phòng', 'Hải Phòng', 'Hải Phòng',
            # Cần Thơ
            'Cần Thơ', 'Cần Thơ', 'Cần Thơ',
            # Khánh Hòa
            'Khánh Hòa', 'Khánh Hòa', 'Khánh Hòa',
            # Adding more entries for new models
            'Hà Nội', 'Hà Nội', 'Hà Nội',
            'Hồ Chí Minh', 'Hồ Chí Minh', 'Hồ Chí Minh',
            'Đà Nẵng', 'Đà Nẵng',
            'Hải Phòng', 'Cần Thơ'
        ],
        'Quận/Huyện': [
            # Hà Nội
            'Cầu Giấy', 'Nam Từ Liêm', 'Hoàng Mai', 'Đống Đa', 'Thanh Xuân', 'Hà Đông',
            # Hồ Chí Minh
            'Quận 1', 'Quận 7', 'Thủ Đức', 'Quận 3', 'Tân Bình', 'Bình Thạnh',
            # Đà Nẵng
            'Hải Châu', 'Thanh Khê', 'Sơn Trà', 'Ngũ Hành Sơn',
            # Hải Phòng
            'Hồng Bàng', 'Ngô Quyền', 'Lê Chân',
            # Cần Thơ
            'Ninh Kiều', 'Cái Răng', 'Bình Thủy',
            # Khánh Hòa
            'Nha Trang', 'Cam Ranh', 'Ninh Hòa',
            # Adding more entries for new models
            'Long Biên', 'Tây Hồ', 'Ba Đình',
            'Quận 5', 'Quận 10', 'Quận 4',
            'Liên Chiểu', 'Cẩm Lệ',
            'Kiến An', 'Ô Môn'
        ],
        'Dealer Name': [
            # Hà Nội
            'VinFast Cầu Giấy Auto', 'Green Future HN Premium', 'VinFast Hoàng Mai', 
            'Green Future Đống Đa', 'VinFast Thanh Xuân', 'Green Future Hà Đông',
            # Hồ Chí Minh
            'VinFast Central Sài Gòn', 'Green Future District 7', 'VinFast Thủ Đức', 
            'Saigon Green Mobility', 'VinFast Tân Bình', 'Green Future Bình Thạnh',
            # Đà Nẵng
            'VinFast Đà Nẵng Center', 'Green Future Đà Nẵng', 'Dragon Auto DN', 'VinFast NGS',
            # Hải Phòng
            'VinFast Hải Phòng', 'HP Green Auto', 'Green Future HP',
            # Cần Thơ
            'Mekong Auto', 'Green Future CT', 'VinFast Cần Thơ',
            # Khánh Hòa
            'VinFast Nha Trang', 'Green Future KH', 'Nha Trang Green Auto',
            # Adding more entries for new models
            'VinFast Long Biên', 'Green Future Tây Hồ', 'VinFast Ba Đình',
            'VinFast Quận 5', 'Green Future Q10', 'VinFast Quận 4',
            'VinFast Liên Chiểu', 'Green Future Cẩm Lệ',
            'VinFast Kiến An', 'VinFast Ô Môn'
        ],
        'Địa chỉ cụ thể': [
            # Hà Nội
            '258 Xuân Thủy', '68 Mỹ Đình', '159 Giải Phóng',
            '475 Xã Đàn', '235 Nguyễn Trãi', '198 Quang Trung',
            # Hồ Chí Minh
            '11-13 Lê Duẩn', '1059 Nguyễn Văn Linh', '12 Võ Văn Ngân',
            '86 Nam Kỳ Khởi Nghĩa', '120 Hoàng Văn Thụ', '11 Xô Viết Nghệ Tĩnh',
            # Đà Nẵng
            '156 Nguyễn Văn Linh', '68 Điện Biên Phủ', '365 Ngô Quyền', '99 Võ Nguyên Giáp',
            # Hải Phòng
            '7 Lạch Tray', '189 Đà Nẵng', '68 Trần Nguyên Hãn',
            # Cần Thơ
            '131 Trần Hưng Đạo', '246 CMT8', '78 Võ Văn Kiệt',
            # Khánh Hòa
            '86 Trần Phú', '168 23/10', '55 Thái Nguyên',
            # Adding more entries for new models
            '456 Nguyễn Văn Cừ', '789 Lạc Long Quân', '101 Đội Cấn',
            '234 An Dương Vương', '567 Lý Thường Kiệt', '890 Khánh Hội',
            '123 Hoàng Văn Thái', '456 Ông Ích Khiêm',
            '789 Trần Thành Ngọ', '101 Nguyễn Văn Cừ'
        ],
        'Model': [
            # Hà Nội
            'VF e34', 'VF 8', 'VF 9', 'VF 7', 'VF e34', 'VF 8',
            # Hồ Chí Minh
            'VF 9', 'VF 8', 'VF 7', 'VF e34', 'VF 8', 'VF 9',
            # Đà Nẵng
            'VF e34', 'VF 8', 'VF 7', 'VF 9',
            # Hải Phòng
            'VF e34', 'VF 7', 'VF 8',
            # Cần Thơ
            'VF e34', 'VF 8', 'VF 9',
            # Khánh Hòa
            'VF 7', 'VF 8', 'VF 9',
            # Adding entries for VF3, VF5, VF6
            'VF3', 'VF3', 'VF3',
            'VF5', 'VF5', 'VF5',
            'VF6', 'VF6',
            'VF6', 'VF3'
        ],
        'Image Path': [
            # Hà Nội
            'img/vfe34.png', 'img/vf8.png', 'img/vf9.png', 'img/vf7.png', 'img/vfe34.png', 'img/vf8.png',
            # Hồ Chí Minh
            'img/vf9.png', 'img/vf8.png', 'img/vf7.png', 'img/vfe34.png', 'img/vf8.png', 'img/vf9.png',
            # Đà Nẵng
            'img/vfe34.png', 'img/vf8.png', 'img/vf7.png', 'img/vf9.png',
            # Hải Phòng
            'img/vfe34.png', 'img/vf7.png', 'img/vf8.png',
            # Cần Thơ
            'img/vfe34.png', 'img/vf8.png', 'img/vf9.png',
            # Khánh Hòa
            'img/vf7.png', 'img/vf8.png', 'img/vf9.png',
            # Adding entries for new models
            'img/vf3.png', 'img/vf3.png', 'img/vf3.png',
            'img/vf5.png', 'img/vf5.png', 'img/vf5.png',
            'img/vf6.png', 'img/vf6.png',
            'img/vf6.png', 'img/vf3.png'
        ],
        'Rental Fee (per day)': [
            # Hà Nội
            550000, 780000, 950000, 680000, 520000, 750000,
            # Hồ Chí Minh
            980000, 800000, 700000, 580000, 820000, 950000,
            # Đà Nẵng
            500000, 750000, 650000, 900000,
            # Hải Phòng
            480000, 620000, 730000,
            # Cần Thơ
            450000, 700000, 880000,
            # Khánh Hòa
            600000, 720000, 850000,
            # Adding entries for new models (with appropriate pricing)
            400000, 420000, 410000,  # VF3 (most affordable)
            480000, 500000, 490000,  # VF5
            580000, 600000, 590000, 400000  # VF6 and VF3
        ]
    }
    return pd.DataFrame(data)


# Load data
df = load_data()

# Mô tả mẫu xe
model_descriptions = {
    "VF 3": {
        "description": "Mẫu xe đô thị cỡ nhỏ, lý tưởng cho di chuyển trong phố.",
        "image": "vf3.png"
    },
    "VF e34": {
        "description": "Mẫu SUV cỡ nhỏ chạy điện với phạm vi hoạt động 285km, công suất 147 mã lực. Phù hợp cho di chuyển trong phố.",
        "image": "vfe34.png"
    },
    "VF 5": {
        "description": "Mẫu SUV đô thị nhỏ gọn với thiết kế hiện đại.",
        "image": "vf5.png"
    },
    "VF 6": {
        "description": "Mẫu SUV cỡ C với thiết kế thời trang, công nghệ hiện đại.",
        "image": "vf6.png"
    },
    "VF 7": {
        "description": "Mẫu SUV cỡ vừa với thiết kế thể thao, công suất lên đến 349 mã lực, phạm vi hoạt động 400km. Lựa chọn lý tưởng cho gia đình.",
        "image": "vf7.png"
    },
    "VF 8": {
        "description": "Mẫu SUV cỡ trung với không gian rộng rãi, công suất 402 mã lực, phạm vi hoạt động 420km. Đáp ứng nhu cầu di chuyển xa và thoải mái.",
        "image": "vf8.png"
    },
    "VF 9": {
        "description": "Mẫu SUV cỡ lớn với 3 hàng ghế, không gian rộng rãi, công suất 408 mã lực, phạm vi hoạt động 438km. Phù hợp cho gia đình đông người.",
        "image": "vf9.png"
    }
}

# Thông số kỹ thuật chi tiết
model_specs = {
    "VF 3": {
        "Công suất": "100 kW (134 mã lực)",
        "Mô-men xoắn": "190 Nm",
        "Phạm vi hoạt động": "200 km",
        "Thời gian sạc": "5 giờ (10-80%)",
        "Số chỗ ngồi": "4",
        "Dài x Rộng x Cao": "3.114 x 1.670 x 1.621 mm",
        "Trọng lượng": "1.165 kg",
        "Dung lượng pin": "35 kWh"
    },
    "VF e34": {
        "Công suất": "150 kW (201 mã lực)",
        "Mô-men xoắn": "242 Nm",
        "Phạm vi hoạt động": "300 km",
        "Thời gian sạc": "6 giờ (10-80%)",
        "Số chỗ ngồi": "5",
        "Dài x Rộng x Cao": "4.300 x 1.793 x 1.613 mm",
        "Trọng lượng": "1.490 kg",
        "Dung lượng pin": "51 kWh"
    },
    "VF 5": {
        "Công suất": "130 kW (174 mã lực)",
        "Mô-men xoắn": "220 Nm",
        "Phạm vi hoạt động": "280 km",
        "Thời gian sạc": "5.5 giờ (10-80%)",
        "Số chỗ ngồi": "5",
        "Dài x Rộng x Cao": "3.965 x 1.720 x 1.580 mm",
        "Trọng lượng": "1.350 kg",
        "Dung lượng pin": "42 kWh"
    },
    "VF 6": {
        "Công suất": "170 kW (228 mã lực)",
        "Mô-men xoắn": "350 Nm",
        "Phạm vi hoạt động": "350 km",
        "Thời gian sạc": "5.5 giờ (10-80%)",
        "Số chỗ ngồi": "5",
        "Dài x Rộng x Cao": "4.238 x 1.820 x 1.594 mm",
        "Trọng lượng": "1.600 kg",
        "Dung lượng pin": "59.6 kWh"
    },
    "VF 7": {
        "Công suất": "260 kW (349 mã lực)",
        "Mô-men xoắn": "500 Nm",
        "Phạm vi hoạt động": "450 km",
        "Thời gian sạc": "5 giờ (10-80%)",
        "Số chỗ ngồi": "5",
        "Dài x Rộng x Cao": "4.545 x 1.890 x 1.635 mm",
        "Trọng lượng": "1.680 kg",
        "Dung lượng pin": "75.3 kWh"
    },
    "VF 8": {
        "Công suất": "300 kW (402 mã lực)",
        "Mô-men xoắn": "620 Nm",
        "Phạm vi hoạt động": "550 km",
        "Thời gian sạc": "5.5 giờ (10-80%)",
        "Số chỗ ngồi": "5",
        "Dài x Rộng x Cao": "4.750 x 1.934 x 1.667 mm",
        "Trọng lượng": "2.050 kg",
        "Dung lượng pin": "87.7 kWh"
    },
    "VF 9": {
        "Công suất": "300 kW (402 mã lực)",
        "Mô-men xoắn": "640 Nm",
        "Phạm vi hoạt động": "600 km",
        "Thời gian sạc": "6 giờ (10-80%)",
        "Số chỗ ngồi": "7",
        "Dài x Rộng x Cao": "5.120 x 2.000 x 1.721 mm",
        "Trọng lượng": "2.470 kg",
        "Dung lượng pin": "92 kWh"
    }
}

# Update the features dictionary to include all models
features = {
    "VF 3": [
        "Hệ thống phanh ABS/EBD/ESC",
        "Camera lùi",
        "Cảm biến áp suất lốp",
        "Màn hình cảm ứng 10 inch"
    ],
    "VF e34": [
        "Hệ thống hỗ trợ lái ADAS",
        "Cảnh báo điểm mù",
        "Cảnh báo va chạm phía trước",
        "Hỗ trợ đỗ xe tự động"
    ],
    "VF 5": [
        "Hệ thống kiểm soát hành trình",
        "Cảm biến đỗ xe",
        "Màn hình giải trí 10 inch",
        "Kết nối Apple CarPlay/Android Auto"
    ],
    "VF 6": [
        "Hệ thống hỗ trợ lái thông minh",
        "Màn hình cảm ứng 12.9 inch",
        "Camera 360 độ",
        "Trợ lý ảo thông minh"
    ],
    "VF 7": [
        "Hệ thống hỗ trợ lái nâng cao",
        "Màn hình cảm ứng trung tâm 12.9 inch",
        "Trợ lý ảo",
        "Hệ thống âm thanh cao cấp"
    ],
    "VF 8": [
        "Hệ thống tự lái cấp độ 2",
        "Màn hình AR-HUD",
        "Ghế massage",
        "Cửa sổ trời toàn cảnh"
    ],
    "VF 9": [
        "Hệ thống tự lái cấp độ 2+",
        "7 ghế ngồi rộng rãi",
        "Màn hình giải trí 15.6 inch",
        "Hệ thống làm mát/sưởi ghế toàn xe"
    ]
}


# Hàm lấy ảnh cho mỗi mẫu xe
@st.cache_data
def get_model_image(model):
    """Get image for a specific VinFast model from local img folder"""
    try:
        # Convert model name to lowercase and remove spaces for filename
        # e.g., 'VF e34' -> 'vfe34', 'VF 8' -> 'vf8'
        model_filename = f"img/{''.join(model.lower().split())}.png"
        return Image.open(model_filename)
    except FileNotFoundError:
        st.warning(f"Image not found: {model_filename}. Please ensure the image exists in the img folder.")
        # Fallback to placeholder image
        return None

# Ensure img directory exists
if not os.path.exists("img"):
    os.makedirs("img")
    st.warning("""
        The 'img' directory has been created. Please add the following images:
        - img/vf3.png
        - img/vfe34.png
        - img/vf5.png
        - img/vf6.png
        - img/vf7.png
        - img/vf8.png
        - img/vf9.png
    """)


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

def get_image_base64(model):
    """Convert image to base64 string"""
    try:
        img = get_model_image(model)
        if img is not None:
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode()
    except Exception:
        return ""  # Return empty string if image processing fails
    return ""  # Return empty string if image processing fails

# Hàm hiển thị thẻ xe
def display_car_card(car):
    st.markdown("""
        <div class='car-card'>
            <div class='car-grid'>
                <div class='car-image'>
                    <img src="data:image/png;base64,{}" alt="{}" style="width: 100%; height: auto;">
                </div>
                <div class='car-info'>
                    <h4 class='car-model'>{}</h4>
                    <div class='dealer-info'>
                        <p><i class='fas fa-store'></i> <b>Đại lý:</b> {}</p>
                        <p><i class='fas fa-map-marker-alt'></i> <b>Địa chỉ:</b> {}, {}, {}</p>
                    </div>
                    <p class='price'>{}/ngày</p>
                </div>
            </div>
        </div>
    """.format(
        get_image_base64(car['Model']),
        car['Model'],
        car['Model'],
        car['Dealer Name'],
        car['Địa chỉ cụ thể'],
        car['Quận/Huyện'],
        car['Tỉnh/Thành phố'],
        format_currency(car['Rental Fee (per day)'])
    ), unsafe_allow_html=True)

    # Add buttons using Streamlit's native components
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Đặt xe ngay", key=f"book_{car['Model']}_{car['Địa chỉ cụ thể']}", use_container_width=True):
            st.session_state.booking_state['car_selected'] = {
                'model': car['Model'],
                'dealer': car['Dealer Name'],
                'address': f"{car['Địa chỉ cụ thể']}, {car['Quận/Huyện']}, {car['Tỉnh/Thành phố']}",
                'rental_fee': car['Rental Fee (per day)']
            }
            st.session_state.current_page = 'booking'
            st.session_state.booking_state['booking_step'] = 1
            st.rerun()

    with col2:
        if st.button("Xem chi tiết", key=f"details_{car['Model']}_{car['Địa chỉ cụ thể']}", use_container_width=True):
            st.session_state.car_detail = car['Model']
            st.session_state.car_detail_info = {
                'model': car['Model'],
                'dealer': car['Dealer Name'],
                'address': f"{car['Địa chỉ cụ thể']}, {car['Quận/Huyện']}, {car['Tỉnh/Thành phố']}",
                'rental_fee': car['Rental Fee (per day)']
            }
            # Add technical specifications to session state
            st.session_state.car_specs = model_specs.get(car['Model'], {})
            st.session_state.current_page = 'car_detail'
            st.rerun()

    # CSS for styling
    st.markdown("""
        <style>
            .car-card {
                background: white;
                border-radius: 15px;
                padding: 20px;
                margin: 15px 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .car-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
            }
            
            .car-grid {
                display: grid;
                grid-template-columns: 1fr 1.5fr;
                gap: 20px;
                align-items: start;
            }
            
            .car-image {
                width: 100%;
                border-radius: 10px;
                overflow: hidden;
            }
            
            .car-info {
                padding: 10px 0;
            }
            
            .car-model {
                font-size: 1.5rem;
                font-weight: 600;
                color: #1a472a;
                margin-bottom: 15px;
            }
            
            .dealer-info {
                margin: 15px 0;
            }
            
            .dealer-info p {
                margin: 8px 0;
                color: #495057;
            }
            
            .dealer-info i {
                color: #2e8b57;
                margin-right: 8px;
            }
            
            .price {
                font-size: 1.3rem;
                font-weight: 700;
                color: #2e8b57;
                margin: 15px 0;
            }
            
            @media (max-width: 768px) {
                .car-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    """, unsafe_allow_html=True)

    # Handle button clicks using Streamlit components
    book_key = f"book_{car['Model']}_{car['Địa chỉ cụ thể']}"
    details_key = f"details_{car['Model']}_{car['Địa chỉ cụ thể']}"
    
    if st.session_state.get(book_key):
        st.session_state.booking_state['car_selected'] = {
            'model': car['Model'],
            'dealer': car['Dealer Name'],
            'address': f"{car['Địa chỉ cụ thể']}, {car['Quận/Huyện']}, {car['Tỉnh/Thành phố']}",
            'rental_fee': car['Rental Fee (per day)']
        }
        st.session_state.current_page = 'booking'
        st.session_state.booking_state['booking_step'] = 1
        st.rerun()
    
    if st.session_state.get(details_key):
        st.session_state.car_detail = car['Model']
        st.session_state.car_detail_info = {
            'model': car['Model'],
            'dealer': car['Dealer Name'],
            'address': f"{car['Địa chỉ cụ thể']}, {car['Quận/Huyện']}, {car['Tỉnh/Thành phố']}",
            'rental_fee': car['Rental Fee (per day)']
        }
        st.session_state.current_page = 'car_detail'
        st.rerun()




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

    # Calculate dynamic statistics
    total_cars = len(df)
    total_provinces = len(df['Tỉnh/Thành phố'].unique())
    total_models = len(df['Model'].unique())
    support_hours = "24/7"

    # Format large numbers with comma separator
    def format_number(num):
        return f"{num:,}"

    # Thống kê chính
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class='stat-box'>
                <div class='stat-number'>{format_number(total_cars)}</div>
                <div class='stat-label'>Xe VinFast sẵn sàng</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class='stat-box'>
                <div class='stat-number'>{format_number(total_provinces)}</div>
                <div class='stat-label'>Tỉnh/Thành phố</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class='stat-box'>
                <div class='stat-number'>{format_number(total_models)}</div>
                <div class='stat-label'>Mẫu xe khác nhau</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class='stat-box'>
                <div class='stat-number'>{support_hours}</div>
                <div class='stat-label'>Hỗ trợ khách hàng</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Khu vực tìm kiếm và lọc
    # st.markdown("<div class='section'>", unsafe_allow_html=True)
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
    
    # Create two columns for image and info
    col_img, col_info = st.columns([1, 1.5])
    
    with col_img:
        # Display car image
        img = get_model_image(car_selected['model'])
        if img is not None:
            st.image(img, use_container_width=True)
    
    with col_info:
        st.markdown(f"<h4>Xe đã chọn: {car_selected['model']}</h4>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Đại lý:</b> {car_selected['dealer']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Địa chỉ:</b> {car_selected['address']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='price'>{format_currency(car_selected['rental_fee'])}/ngày</p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Add some CSS to style the booking car card
    st.markdown("""
        <style>
        .car-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }
        .car-card h4 {
            color: #1a1a1a;
            margin-bottom: 1rem;
            font-size: 1.2rem;
        }
        .car-card p {
            margin-bottom: 0.5rem;
            color: #4a4a4a;
        }
        .car-card .price {
            color: #28a745;
            font-size: 1.2rem;
            font-weight: bold;
            margin-top: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

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
