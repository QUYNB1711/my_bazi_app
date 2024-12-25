from bazi_core import BaziBase, BaziUtils
from datetime import datetime

class BaziAnalyzer(BaziBase):
    def __init__(self):
        super().__init__()
        self.career_suggestions = {
            "Kim":["Ngân hàng","Tài chính","Cơ khí","Vàng bạc"],
            "Mộc":["Giáo dục","Lâm nghiệp","Nghệ thuật","Y học cổ truyền"],
            "Thủy":["Truyền thông","Logistics","Ngoại giao","Công nghệ"],
            "Hỏa":["Marketing","Ẩm thực","Biểu diễn","Giải trí"],
            "Thổ":["Xây dựng","Bất động sản","Nông nghiệp","Khai khoáng"]
        }
        self.personality_traits = {
            "Kim":{
                "tích_cực":["Kiên định","Quyết đoán","Mạnh mẽ"],
                "tiêu_cực":["Cứng nhắc","Khó linh hoạt"]
            },
            "Mộc":{
                "tích_cực":["Sáng tạo","Nhân ái","Phát triển bền"],
                "tiêu_cực":["Thiếu quyết đoán","Dễ lung lay"]
            },
            "Thủy":{
                "tích_cực":["Thông minh","Linh hoạt","Thích nghi tốt"],
                "tiêu_cực":["Hay lo","Dễ đổi ý"]
            },
            "Hỏa":{
                "tích_cực":["Nhiệt tình","Năng động","Sôi nổi"],
                "tiêu_cực":["Nóng vội","Thiếu kiên nhẫn"]
            },
            "Thổ":{
                "tích_cực":["Điềm tĩnh","Vững vàng","Chăm chỉ"],
                "tiêu_cực":["Bảo thủ","Khó thay đổi"]
            }
        }

    def analyze_tu_tru(self, tu_tru):
        analysis={}
        for tru, info in tu_tru.items():
            can_chi= info["can_chi"]
            hanh=   info["ngu_hanh"]
            nap_am= info.get("nạp_am","")
            tang_can= info.get("tàng_can",[])
            than_sat= info.get("thần_sát",[])

            analysis[tru]= {
                "ý_nghĩa": self._get_tru_meaning(tru),
                "tính_chất": self.personality_traits.get(hanh,{}).get("tích_cực",[]),
                "lưu_ý":    self.personality_traits.get(hanh,{}).get("tiêu_cực",[]),
                "nạp_am":   nap_am,
                "tàng_can": tang_can,
                "thần_sát": than_sat
            }
        return analysis

    def _get_tru_meaning(self, tru):
        data= {
            "năm":{
                "chung":"Phản ánh vận mệnh tổng quát, di truyền gia đình",
                "chi_tiết":["Thiếu niên","Gốc rễ gia tộc"]
            },
            "tháng":{
                "chung":"Sự nghiệp, tài lộc, học vấn",
                "chi_tiết":["Thanh niên","Công danh, học tập"]
            },
            "ngày":{
                "chung":"Tính cách, hôn nhân, bản thân",
                "chi_tiết":["Trung niên","Quyết định chủ đạo cuộc đời"]
            },
            "giờ":{
                "chung":"Con cái, hậu vận, quan hệ xã hội về sau",
                "chi_tiết":["Sau 50 tuổi","Tương lai bền lâu"]
            }
        }
        return data.get(tru,{})

    def analyze_menh_cuc(self, menh, stats):
        vuong= max(stats.items(), key=lambda x:x[1])[0]
        suy=   min(stats.items(), key=lambda x:x[1])[0]
        bc= self.personality_traits.get(menh,{}).get("tích_cực",[])
        lu= self.personality_traits.get(menh,{}).get("tiêu_cực",[])

        return {
            "mệnh_cục":{
                "bản_chất": bc,
                "lưu_ý": lu,
                "phát_triển": self._get_development_advice(menh)
            },
            "ngũ_hành":{
                "vượng":{"hành": vuong},
                "suy":{"hành": suy}
            }
        }

    def _get_development_advice(self, menh):
        data={
            "Kim":["Rèn kỷ luật","Học quản lý tài chính","Tập trung khả năng phân tích"],
            "Mộc":["Khuyến khích sáng tạo","Bảo vệ môi trường","Tham gia nghệ thuật"],
            "Thủy":["Nâng cao giao tiếp","Ứng biến linh hoạt","Thương thảo giỏi"],
            "Hỏa":["Tập lãnh đạo","Hành động nhanh","Sôi nổi, nhiệt huyết"],
            "Thổ":["Xây nền tảng","Giá trị bền vững","Kiên trì nỗ lực"]
        }
        return data.get(menh,[])

    def analyze_relationships(self, menh):
        ts= self.get_tuong_sinh(menh)
        tk= self.get_tuong_khac(menh)
        return {
            "tương_sinh":{
                "sinh": ts.get("sinh",""),
                "được_sinh": ts.get("được_sinh","")
            },
            "tương_khắc":{
                "khắc": tk.get("khắc",""),
                "bị_khắc": tk.get("bị_khắc","")
            }
        }

    def get_career_advice(self, menh):
        return {
            "ngành_nghề_phù_hợp": self.career_suggestions.get(menh,[]),
            "lời_khuyên": f"Nên chọn hoặc phát triển lĩnh vực mệnh {menh}."
        }

    def analyze_luck_cycles(self, birth_year, current_year):
        """
        Thay vì chỉ giai đoạn hiện tại + next,
        ta luôn hiển thị 4 giai đoạn (thiếu niên, thanh niên, trung niên, hậu vận).
        """
        # Xác định giai đoạn hiện tại
        age= current_year- birth_year
        current_period= BaziUtils.get_current_period(age)

        # Xây dict 4 giai đoạn: { "Thiếu niên":..., "Thanh niên":..., "Trung niên":..., "Hậu vận":... }
        full_periods = ["Thiếu niên","Thanh niên","Trung niên","Hậu vận"]
        all_period_data = {}
        for p in full_periods:
            all_period_data[p] = {
                "đặc_điểm": BaziUtils.get_period_characteristics(p),
                "lời_khuyên": self._period_advice(p)
            }

        # Lấy chi tiết giai đoạn *hiện tại*
        detail= self._get_detailed_life_aspects(age)

        return {
            "hiện_tại":{
                "giai_đoạn": current_period,
                "đặc_điểm": BaziUtils.get_period_characteristics(current_period),
                "lời_khuyên": self._period_advice(current_period)
            },
            "bốn_giai_đoạn": all_period_data,  # Mới thêm
            "phân_tích_chi_tiết": detail
        }

    def _get_detailed_life_aspects(self, age):
        aspects={}
        period= BaziUtils.get_current_period(age)
        aspects["công_danh"]= f"Trong {period}, nên phát triển sự nghiệp chuyên sâu."
        aspects["tài_vận"]= f"Quản lý tài chính cẩn trọng, đầu tư phù hợp."
        aspects["gia_đình"]= f"Duy trì thời gian, vun đắp hạnh phúc gia đình."
        aspects["sức_khỏe"]= f"Chú ý rèn luyện, kiểm tra định kỳ."
        aspects["tình_cảm"]= f"Tôn trọng, chia sẻ giúp tình cảm bền vững."
        aspects["bạn_bè"]= f"Xây dựng bạn hữu cùng chí hướng."
        aspects["đồng_nghiệp"]= f"Tạo môi trường làm việc hài hòa, hỗ trợ lẫn nhau."
        return aspects

    def _period_advice(self, period):
        """
        Lời khuyên cụ thể cho 4 giai đoạn, in bullet points.
        """
        adv_map= {
            "Thiếu niên": [
                "Tập trung học tập, phát triển kỹ năng nền tảng",
                "Chú trọng thể chất, tham gia hoạt động bổ ích",
            ],
            "Thanh niên": [
                "Xây dựng mục tiêu nghề nghiệp rõ ràng",
                "Mở rộng mạng lưới quan hệ, cơ hội thăng tiến"
            ],
            "Trung niên": [
                "Cân đối gia đình và công việc",
                "Đầu tư bền vững, chuẩn bị tương lai con cái"
            ],
            "Hậu vận": [
                "Duy trì sức khỏe, tinh thần",
                "Chia sẻ kinh nghiệm, hưởng thành quả cuộc sống"
            ]
        }
        return adv_map.get(period, [])

    def _get_future_predictions(self, age):
        # (Ta không dùng nó nữa, vì ta hiển thị bốn_giai_đoạn)
        return {}

    def get_health_advice(self, menh, stats):
        return {
            "cơ_bản":{
                "cơ_quan":["Phổi","Da","Đại tràng"],
                "nên_chú_ý":["Hô hấp","Da liễu","Tiêu hóa"]
            },
            "khuyến_nghị":{
                "dinh_dưỡng":["Ăn nhiều rau quả","Uống đủ nước","Tránh đồ cay nóng"],
                "vận_động":["Đi bộ","Yoga","Tập nhẹ nhàng"],
                "tinh_thần":["Thiền","Nghe nhạc thư giãn","Suy nghĩ tích cực"]
            }
        }

    def get_full_analysis(self, bazi_data):
        menh= bazi_data["menh_cuc"]
        tu_tru= bazi_data["tu_tru"]
        stats= bazi_data["ngu_hanh"]["thống_kê"]
        return {
            "tổng_quan": self.analyze_menh_cuc(menh, stats),
            "chi_tiết_tứ_trụ": self.analyze_tu_tru(tu_tru),
            "quan_hệ": self.analyze_relationships(menh),
            "sự_nghiệp": self.get_career_advice(menh),
            "sức_khỏe": self.get_health_advice(menh, stats),
            # Lưu ý: ta thay "vận_hạn" => "analyze_luck_cycles" hiển thị all 4 giai đoạn
            "vận_hạn": self.analyze_luck_cycles(
                int(bazi_data["thong_tin"]["ngày_sinh_al"].split("/")[2]),
                datetime.now().year
            )
        }
