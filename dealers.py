import pandas as pd

# Danh sách dữ liệu mẫu
data = [
    {
        "Tỉnh/Thành phố": "Hà Nội",
        "Quận/Huyện": "Hoàng Mai",
        "Dealer Name": "ABC Vinfast Dealer",
        "Địa chỉ cụ thể": "123 Linh Đàm",
        "Model": "VF e34",
        "Image Link/Path": "http://example.com/hanoi/hoangmai/abc_vfe34.jpg",
        "Rental Fee (per day)": 500000
    },
    {
        "Tỉnh/Thành phố": "Hà Nội",
        "Quận/Huyện": "Hoàng Mai",
        "Dealer Name": "ABC Vinfast Dealer",
        "Địa chỉ cụ thể": "123 Linh Đàm",
        "Model": "VF 8",
        "Image Link/Path": "http://example.com/hanoi/hoangmai/abc_vf8.jpg",
        "Rental Fee (per day)": 700000
    },
    {
        "Tỉnh/Thành phố": "Hồ Chí Minh",
        "Quận/Huyện": "Quận 1",
        "Dealer Name": "XYZ Vinfast Dealer",
        "Địa chỉ cụ thể": "45 Lê Lợi",
        "Model": "VF e34",
        "Image Link/Path": "http://example.com/hcm/q1/xyz_vfe34.jpg",
        "Rental Fee (per day)": 600000
    },
    {
        "Tỉnh/Thành phố": "Hồ Chí Minh",
        "Quận/Huyện": "Quận 1",
        "Dealer Name": "XYZ Vinfast Dealer",
        "Địa chỉ cụ thể": "45 Lê Lợi",
        "Model": "VF 7",
        "Image Link/Path": "http://example.com/hcm/q1/xyz_vf7.jpg",
        "Rental Fee (per day)": 650000
    },
    {
        "Tỉnh/Thành phố": "Đà Nẵng",
        "Quận/Huyện": "Hải Châu",
        "Dealer Name": "Premier Vinfast Dealer",
        "Địa chỉ cụ thể": "98 Hải Châu",
        "Model": "VF 8",
        "Image Link/Path": "http://example.com/danang/haichau/premier_vf8.jpg",
        "Rental Fee (per day)": 700000
    },
    {
        "Tỉnh/Thành phố": "Đà Nẵng",
        "Quận/Huyện": "Hải Châu",
        "Dealer Name": "Green Motors Dealer",
        "Địa chỉ cụ thể": "10 Lê Duẩn",
        "Model": "VF 9",
        "Image Link/Path": "http://example.com/danang/haichau/green_vf9.jpg",
        "Rental Fee (per day)": 750000
    },
    {
        "Tỉnh/Thành phố": "Cần Thơ",
        "Quận/Huyện": "Ninh Kiều",
        "Dealer Name": "ABC Vinfast Dealer",
        "Địa chỉ cụ thể": "35 Ninh Kiều",
        "Model": "VF e34",
        "Image Link/Path": "http://example.com/cantho/ninhkieu/abc_vfe34.jpg",
        "Rental Fee (per day)": 450000
    },
    {
        "Tỉnh/Thành phố": "Cần Thơ",
        "Quận/Huyện": "Cái Răng",
        "Dealer Name": "XYZ Vinfast Dealer",
        "Địa chỉ cụ thể": "27 Cái Răng",
        "Model": "VF 8",
        "Image Link/Path": "http://example.com/cantho/cairang/xyz_vf8.jpg",
        "Rental Fee (per day)": 650000
    },
    {
        "Tỉnh/Thành phố": "Hải Phòng",
        "Quận/Huyện": "Lê Chân",
        "Dealer Name": "Red Dragon Dealer",
        "Địa chỉ cụ thể": "73 Lạch Tray",
        "Model": "VF e34",
        "Image Link/Path": "http://example.com/haiphong/lechân/reddragon_vfe34.jpg",
        "Rental Fee (per day)": 520000
    },
    {
        "Tỉnh/Thành phố": "Hải Phòng",
        "Quận/Huyện": "Lê Chân",
        "Dealer Name": "Red Dragon Dealer",
        "Địa chỉ cụ thể": "73 Lạch Tray",
        "Model": "VF 7",
        "Image Link/Path": "http://example.com/haiphong/lechân/reddragon_vf7.jpg",
        "Rental Fee (per day)": 580000
    },
    {
        "Tỉnh/Thành phố": "Khánh Hòa",
        "Quận/Huyện": "Nha Trang",
        "Dealer Name": "Green Motors Dealer",
        "Địa chỉ cụ thể": "66 Trần Phú",
        "Model": "VF 7",
        "Image Link/Path": "http://example.com/nhatrang/greenmotors_vf7.jpg",
        "Rental Fee (per day)": 700000
    },
    {
        "Tỉnh/Thành phố": "Khánh Hòa",
        "Quận/Huyện": "Nha Trang",
        "Dealer Name": "Red Dragon Dealer",
        "Địa chỉ cụ thể": "89 Hùng Vương",
        "Model": "VF 9",
        "Image Link/Path": "http://example.com/nhatrang/reddragon_vf9.jpg",
        "Rental Fee (per day)": 800000
    },
]

# Tạo DataFrame
df = pd.DataFrame(data)

# Ghi DataFrame ra file Excel
output_file = "Vinfast_Dealer_Management_With_Fees_District.xlsx"
df.to_excel(output_file, sheet_name="DealerData", index=False)
print(f"File Excel '{output_file}' đã được tạo thành công!")
