import pandas as pd

# Mock data: Each row represents a single vehicle,
# with city, dealer info, model, image link, and rental fee.
data = [
    {
        "City": "Hanoi",
        "Dealer Name": "ABC Vinfast Dealer",
        "Dealer Address": "123 Linh Dam, Hanoi",
        "Model": "VF e34",
        "Image Link/Path": "http://example.com/hanoi/abc/vfe34.jpg",
        "Rental Fee (per day)": 500000
    },
    {
        "City": "Hanoi",
        "Dealer Name": "ABC Vinfast Dealer",
        "Dealer Address": "123 Linh Dam, Hanoi",
        "Model": "VF 8",
        "Image Link/Path": "http://example.com/hanoi/abc/vf8.jpg",
        "Rental Fee (per day)": 700000
    },
    {
        "City": "Ho Chi Minh City",
        "Dealer Name": "XYZ Vinfast Dealer",
        "Dealer Address": "45 District 1, HCMC",
        "Model": "VF e34",
        "Image Link/Path": "http://example.com/hcm/xyz/vfe34.jpg",
        "Rental Fee (per day)": 600000
    },
    {
        "City": "Ho Chi Minh City",
        "Dealer Name": "XYZ Vinfast Dealer",
        "Dealer Address": "45 District 1, HCMC",
        "Model": "VF 7",
        "Image Link/Path": "http://example.com/hcm/xyz/vf7.jpg",
        "Rental Fee (per day)": 650000
    },
    {
        "City": "Da Nang",
        "Dealer Name": "Premier Vinfast Dealer",
        "Dealer Address": "98 Hai Chau, Da Nang",
        "Model": "VF 8",
        "Image Link/Path": "http://example.com/danang/premier/vf8.jpg",
        "Rental Fee (per day)": 700000
    },
    {
        "City": "Da Nang",
        "Dealer Name": "Green Motors Dealer",
        "Dealer Address": "10 Le Duan, Da Nang",
        "Model": "VF 9",
        "Image Link/Path": "http://example.com/danang/greenmotors/vf9.jpg",
        "Rental Fee (per day)": 750000
    },
    {
        "City": "Hai Phong",
        "Dealer Name": "Red Dragon Dealer",
        "Dealer Address": "73 Lac Long Quan, Hai Phong",
        "Model": "VF e34",
        "Image Link/Path": "http://example.com/haiphong/reddragon/vfe34.jpg",
        "Rental Fee (per day)": 520000
    },
    {
        "City": "Hai Phong",
        "Dealer Name": "Red Dragon Dealer",
        "Dealer Address": "73 Lac Long Quan, Hai Phong",
        "Model": "VF 7",
        "Image Link/Path": "http://example.com/haiphong/reddragon/vf7.jpg",
        "Rental Fee (per day)": 580000
    },
    {
        "City": "Can Tho",
        "Dealer Name": "ABC Vinfast Dealer",
        "Dealer Address": "35 Ninh Kieu, Can Tho",
        "Model": "VF e34",
        "Image Link/Path": "http://example.com/cantho/abc/vfe34.jpg",
        "Rental Fee (per day)": 450000
    },
    {
        "City": "Can Tho",
        "Dealer Name": "XYZ Vinfast Dealer",
        "Dealer Address": "27 Cai Rang, Can Tho",
        "Model": "VF 8",
        "Image Link/Path": "http://example.com/cantho/xyz/vf8.jpg",
        "Rental Fee (per day)": 650000
    },
    {
        "City": "Nha Trang",
        "Dealer Name": "Green Motors Dealer",
        "Dealer Address": "66 Tran Phu, Nha Trang",
        "Model": "VF 7",
        "Image Link/Path": "http://example.com/nhatrang/greenmotors/vf7.jpg",
        "Rental Fee (per day)": 700000
    },
    {
        "City": "Nha Trang",
        "Dealer Name": "Red Dragon Dealer",
        "Dealer Address": "89 Hung Vuong, Nha Trang",
        "Model": "VF 9",
        "Image Link/Path": "http://example.com/nhatrang/reddragon/vf9.jpg",
        "Rental Fee (per day)": 800000
    },
]

# Create a DataFrame
df = pd.DataFrame(data)

# Write DataFrame to an Excel file
output_file = "Vinfast_Dealer_Management_With_Fees.xlsx"
df.to_excel(output_file, sheet_name="DealerData", index=False)
print(f"Excel file '{output_file}' created successfully!")
