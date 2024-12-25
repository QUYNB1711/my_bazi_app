from datetime import datetime
from bazi_core import BaziBase, LunarConverter, BaziUtils

class BaziCalculator(BaziBase):
    def __init__(self):
        super().__init__()
        # Mệnh cục
        self.menh_cuc = {
            0: {"nam": "Kim","nữ": "Thủy"},
            1: {"nam": "Thủy","nữ": "Hỏa"},
            2: {"nam": "Hỏa","nữ": "Thổ"},
            3: {"nam": "Thổ","nữ": "Mộc"},
            4: {"nam": "Mộc","nữ": "Kim"},
            5: {"nam": "Kim","nữ": "Thủy"},
            6: {"nam": "Thủy","nữ": "Hỏa"},
            7: {"nam": "Hỏa","nữ": "Thổ"},
            8: {"nam": "Thổ","nữ": "Mộc"},
            9: {"nam": "Mộc","nữ": "Kim"}
        }

        # Cục quẻ giờ
        self.cuc_que_gio = {
            "Tý":"Thủy nhị cục","Sửu":"Thổ ngũ cục",
            "Dần":"Mộc tam cục","Mão":"Mộc tam cục",
            "Thìn":"Thổ ngũ cục","Tỵ":"Hỏa tứ cục",
            "Ngọ":"Hỏa tứ cục","Mùi":"Thổ ngũ cục",
            "Thân":"Kim tứ cục","Dậu":"Kim tứ cục",
            "Tuất":"Thổ ngũ cục","Hợi":"Thủy nhị cục"
        }

        self.offset_first_month_can = {
            "Giáp":2,"Kỷ":2,
            "Ất":4,"Canh":4,
            "Bính":6,"Tân":6,
            "Đinh":8,"Nhâm":8,
            "Mậu":0,"Quý":0
        }

        self.solar_terms_table = [
            (1,(2,4)), (2,(3,6)), (3,(4,5)), (4,(5,6)),
            (5,(6,6)), (6,(7,8)), (7,(8,8)), (8,(9,8)),
            (9,(10,8)),(10,(11,8)),(11,(12,7)),(12,(1,6))
        ]

        # 60 Can–Chi => Nạp Âm (ĐỦ)
        self.nap_am_map = {
            ("Giáp","Tý"): "Hải Trung Kim",      ("Ất","Sửu"): "Hải Trung Kim",
            ("Bính","Dần"): "Lô Trung Hỏa",      ("Đinh","Mão"): "Lô Trung Hỏa",
            ("Mậu","Thìn"): "Đại Lâm Mộc",       ("Kỷ","Tỵ"):  "Đại Lâm Mộc",
            ("Canh","Ngọ"): "Lộ Bàng Thổ",       ("Tân","Mùi"): "Lộ Bàng Thổ",
            ("Nhâm","Thân"): "Kiếm Phong Kim",   ("Quý","Dậu"): "Kiếm Phong Kim",
            ("Giáp","Tuất"): "Sơn Đầu Hỏa",      ("Ất","Hợi"): "Sơn Đầu Hỏa",

            ("Bính","Tý"): "Giản Hạ Thủy",       ("Đinh","Sửu"): "Giản Hạ Thủy",
            ("Mậu","Dần"): "Thành Đầu Thổ",      ("Kỷ","Mão"): "Thành Đầu Thổ",
            ("Canh","Thìn"): "Bạch Lạp Kim",     ("Tân","Tỵ"): "Bạch Lạp Kim",
            ("Nhâm","Ngọ"): "Dương Liễu Mộc",    ("Quý","Mùi"): "Dương Liễu Mộc",
            ("Giáp","Thân"): "Tuyền Trung Thủy", ("Ất","Dậu"): "Tuyền Trung Thủy",
            ("Bính","Tuất"): "Ốc Thượng Thổ",    ("Đinh","Hợi"): "Ốc Thượng Thổ",

            ("Mậu","Tý"): "Tích Lịch Hỏa",       ("Kỷ","Sửu"): "Tích Lịch Hỏa",
            ("Canh","Dần"): "Tùng Bách Mộc",     ("Tân","Mão"): "Tùng Bách Mộc",
            ("Nhâm","Thìn"): "Trường Lưu Thủy",  ("Quý","Tỵ"):  "Trường Lưu Thủy",
            ("Giáp","Ngọ"): "Sa Trung Kim",      ("Ất","Mùi"): "Sa Trung Kim",
            ("Bính","Thân"): "Sơn Hạ Hỏa",       ("Đinh","Dậu"): "Sơn Hạ Hỏa",
            ("Mậu","Tuất"): "Bình Địa Mộc",      ("Kỷ","Hợi"): "Bình Địa Mộc",

            ("Canh","Tý"): "Bích Thượng Thổ",    ("Tân","Sửu"): "Bích Thượng Thổ",
            ("Nhâm","Dần"): "Kim Bạch Kim",      ("Quý","Mão"): "Kim Bạch Kim",
            ("Giáp","Thìn"): "Phú Đăng Hỏa",     ("Ất","Tỵ"):  "Phú Đăng Hỏa",
            ("Bính","Ngọ"): "Thiên Hà Thủy",     ("Đinh","Mùi"): "Thiên Hà Thủy",
            ("Mậu","Thân"): "Đại Trạch Thổ",     ("Kỷ","Dậu"): "Đại Dịch Thổ (Đại Trạch Thổ)",

            ("Canh","Tuất"): "Thoa Xuyến Kim",   ("Tân","Hợi"): "Thoa Xuyến Kim",
            ("Nhâm","Tý"): "Tang Đố Mộc",        ("Quý","Sửu"): "Tang Đố Mộc",
            ("Giáp","Dần"): "Đại Khê Thủy",      ("Ất","Mão"): "Đại Khê Thủy",
            ("Bính","Thìn"): "Sa Trung Thổ",     ("Đinh","Tỵ"): "Sa Trung Thổ",
            ("Mậu","Ngọ"): "Thiên Thượng Hỏa",   ("Kỷ","Mùi"): "Thiên Thượng Hỏa",
            ("Canh","Thân"): "Thạch Lựu Mộc",    ("Tân","Dậu"): "Thạch Lựu Mộc",
            ("Nhâm","Tuất"): "Đại Hải Thủy",     ("Quý","Hợi"): "Đại Hải Thủy"
        }
        # Ví dụ Thần Sát
        self.than_sat_map = {
            ("Quý","Hợi"): ["Tang Môn","Điều Khách"],
            ("Kỷ","Dậu"):  ["Tam Sát","Lưu Hạ"],
            ("Canh","Ngọ"):["Thập Can Lộc"]
        }

    def get_month_by_solar_table(self, date_solar: datetime)->int:
        if date_solar.year<1 or date_solar.year>9999:
            raise ValueError(f"Năm {date_solar.year} ngoài 1..9999")
        anchor=[]
        for (tk,(mm,dd)) in self.solar_terms_table:
            ry= date_solar.year
            if mm==1: ry+=1
            anchor.append((tk, datetime(ry,mm,dd)))
        anchor.sort(key=lambda x:x[1])
        thang=12
        for (tk, dt_moc) in anchor:
            if date_solar>=dt_moc:
                thang=tk
            else:
                break
        return thang

    def get_can_chi(self, type_date, value, day_stem=None):
        try:
            if type_date=="năm":
                can_i= (value-4)%10
                chi_i= (value-4)%12
            elif type_date=="tháng":
                offset= self.offset_first_month_can.get(day_stem, 0)
                can_i= (offset + (value-1))%10
                chi_i= (2 + (value-1))%12
            elif type_date=="ngày":
                jd= LunarConverter.get_julian_date(value)
                can_i= int((jd+9.5)%10)
                chi_i= int((jd+1.5)%12)
            elif type_date=="giờ":
                hour= value
                chi_i= ((hour+1)//2)%12
                if day_stem:
                    si= self.thien_can.index(day_stem)
                    can_i= (si*2 + chi_i)%10
                else:
                    can_i= hour%10
            else:
                can_i=0; chi_i=0

            return {
                "can": self.thien_can[can_i],
                "chi": self.dia_chi[chi_i]
            }
        except (ValueError,OverflowError,IndexError) as e:
            raise ValueError(f"Lỗi tính Can Chi cho {type_date}, {value}: {e}")

    def get_nap_am(self, can_str, chi_str):
        return self.nap_am_map.get((can_str, chi_str), "Chưa xác định")

    def get_than_sat(self, can_str, chi_str):
        return self.than_sat_map.get((can_str, chi_str), [])

    def calculate_menh_cuc(self, birth_year, gender):
        if gender not in ["Nam","Nữ"]:
            raise ValueError(f"Giới tính '{gender}' không hợp lệ.")
        last_digit= birth_year%10
        return self.menh_cuc[last_digit][gender.lower()]

    def get_cuc_que(self, chi_gio):
        return self.cuc_que_gio.get(chi_gio,"Chưa xác định")

    def calculate_bazi(self, birth_date, birth_time, gender, name):
        if birth_date.year<1 or birth_date.year>9999:
            raise ValueError(f"Năm {birth_date.year} ngoài 1..9999.")
        # Năm
        lunar= LunarConverter.solar_to_lunar(birth_date)
        nam_canchi= self.get_can_chi("năm", lunar["year"])

        # Tháng
        dt_solar= datetime.combine(birth_date,birth_time)
        thang_num= self.get_month_by_solar_table(dt_solar)
        thang_canchi= self.get_can_chi("tháng", thang_num, nam_canchi["can"])

        # Ngày
        ngay_canchi= self.get_can_chi("ngày", birth_date)

        # Giờ
        gio_canchi= self.get_can_chi("giờ", birth_time.hour, ngay_canchi["can"])

        # Ngũ hành
        nam_hanh=   self.get_ngu_hanh_from_can(nam_canchi["can"])
        thang_hanh= self.get_ngu_hanh_from_can(thang_canchi["can"])
        ngay_hanh=  self.get_ngu_hanh_from_can(ngay_canchi["can"])
        gio_hanh=   self.get_ngu_hanh_from_chi(gio_canchi["chi"])

        # Nạp âm
        nam_na=   self.get_nap_am(nam_canchi["can"], nam_canchi["chi"])
        thang_na= self.get_nap_am(thang_canchi["can"], thang_canchi["chi"])
        ngay_na=  self.get_nap_am(ngay_canchi["can"], ngay_canchi["chi"])
        gio_na=   self.get_nap_am(gio_canchi["can"], gio_canchi["chi"])

        # Tàng Can
        nam_tang=   self.get_tang_can(nam_canchi["chi"])
        thang_tang= self.get_tang_can(thang_canchi["chi"])
        ngay_tang=  self.get_tang_can(ngay_canchi["chi"])
        gio_tang=   self.get_tang_can(gio_canchi["chi"])

        # Thần Sát
        nam_ts=   self.get_than_sat(nam_canchi["can"], nam_canchi["chi"])
        thang_ts= self.get_than_sat(thang_canchi["can"], thang_canchi["chi"])
        ngay_ts=  self.get_than_sat(ngay_canchi["can"], ngay_canchi["chi"])
        gio_ts=   self.get_than_sat(gio_canchi["can"], gio_canchi["chi"])

        # Mệnh Cục
        menh= self.calculate_menh_cuc(lunar["year"], gender)
        cuc_que= self.get_cuc_que(gio_canchi["chi"])

        # Thống kê ngũ hành
        stats= {"Kim":0,"Mộc":0,"Thủy":0,"Hỏa":0,"Thổ":0}
        for h in [nam_hanh, thang_hanh, ngay_hanh, gio_hanh]:
            if h in stats: stats[h]+=1
        vuong= max(stats.items(), key=lambda x:x[1])[0]
        suy=   min(stats.items(), key=lambda x:x[1])[0]

        return {
            "thong_tin":{
                "họ_tên": name,
                "giới_tính": gender,
                "ngày_sinh_dl": birth_date.strftime("%d/%m/%Y"),
                "giờ_sinh": birth_time.strftime("%H:%M"),
                "ngày_sinh_al": f"{lunar['day']}/{lunar['month']}/{lunar['year']}"
            },
            "tu_tru":{
                "năm":{
                    "can_chi": nam_canchi,
                    "ngu_hanh": nam_hanh,
                    "nạp_am": nam_na,
                    "tàng_can": nam_tang,
                    "thần_sát": nam_ts
                },
                "tháng":{
                    "can_chi": thang_canchi,
                    "ngu_hanh": thang_hanh,
                    "nạp_am": thang_na,
                    "tàng_can": thang_tang,
                    "thần_sát": thang_ts
                },
                "ngày":{
                    "can_chi": ngay_canchi,
                    "ngu_hanh": ngay_hanh,
                    "nạp_am": ngay_na,
                    "tàng_can": ngay_tang,
                    "thần_sát": ngay_ts
                },
                "giờ":{
                    "can_chi": gio_canchi,
                    "ngu_hanh": gio_hanh,
                    "nạp_am": gio_na,
                    "tàng_can": gio_tang,
                    "thần_sát": gio_ts
                }
            },
            "menh_cuc": menh,
            "cuc_que": cuc_que,
            "ngu_hanh":{
                "thống_kê": stats,
                "vượng": vuong,
                "suy": suy
            }
        }
