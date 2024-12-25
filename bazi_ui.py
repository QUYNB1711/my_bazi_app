import logging
logging.basicConfig(level=logging.DEBUG)
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

from bazi_calculator import BaziCalculator
from bazi_analyzer import BaziAnalyzer

class BaziUI:
    def __init__(self):
        st.set_page_config(
            page_title="Phân Tích Bát Tự (Hoàn Thiện)",
            page_icon="🎴",
            layout="wide"
        )
        st.markdown("""
        <style>
        .card {
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
            background-color: #f8f9fa;
        }
        .big-font { font-size: 24px !important; font-weight: bold; }
        .medium-font { font-size:18px !important; }
        </style>
        """, unsafe_allow_html=True)

    def create_input_form(self):
        # Đã đổi phần title:
        st.title("Nhập thông tin")
        with st.form("bazi_input"):
            col1, col2= st.columns(2)
            with col1:
                name= st.text_input("Họ và Tên", "Nguyễn Văn A")
                gender= st.selectbox("Giới Tính", ["Nam","Nữ"])
            with col2:
                bdate= st.date_input("Ngày Sinh (DL)", datetime(1983,11,17))
                btime= st.time_input("Giờ Sinh", datetime(1983,11,17,11,30).time())
            submitted= st.form_submit_button("Phân Tích")
        return submitted, name, gender, bdate, btime

    def display_basic_info(self, bazi_data):
        info= bazi_data["thong_tin"]
        st.header("📌 Thông Tin Cơ Bản")
        col1,col2= st.columns(2)
        with col1:
            st.markdown(f"- **Họ Tên**: {info['họ_tên']}")
            st.markdown(f"- **Giới Tính**: {info['giới_tính']}")
            st.markdown(f"- **Ngày Sinh (DL)**: {info['ngày_sinh_dl']}")
            st.markdown(f"- **Giờ Sinh**: {info['giờ_sinh']}")
        with col2:
            st.markdown(f"- **Ngày Sinh (AL)**: {info['ngày_sinh_al']}")
            st.markdown(f"- **Mệnh Cục**: {bazi_data['menh_cuc']}")
            st.markdown(f"- **Cục Quẻ Giờ**: {bazi_data['cuc_que']}")

    def display_tu_tru(self, bazi_data):
        st.header("🎴 Tứ Trụ")
        tu_tru= bazi_data["tu_tru"]
        color_map= {
            "Kim":"#FFD700","Mộc":"#4CAF50",
            "Thủy":"#2196F3","Hỏa":"#F44336",
            "Thổ":"#FF9800"
        }
        order=["năm","tháng","ngày","giờ"]
        name=["Trụ Năm","Trụ Tháng","Trụ Ngày","Trụ Giờ"]
        cols= st.columns(4)
        for i,k in enumerate(order):
            val= tu_tru[k]
            can= val["can_chi"]["can"]
            chi= val["can_chi"]["chi"]
            hanh= val["ngu_hanh"]
            nap_am= val.get("nạp_am","")
            tang_can= val.get("tàng_can",[])
            than_sat= ", ".join(val.get("thần_sát",[]))
            c= color_map.get(hanh,"#888")
            with cols[i]:
                st.markdown(f"""
                <div style="background-color:{c}; padding:20px; border-radius:10px; text-align:center; color:white">
                   <h3>{name[i]}</h3>
                   <p style="font-size:24px">{can} {chi}</p>
                   <p>Ngũ Hành: {hanh}</p>
                   <p>Nạp Âm: {nap_am}</p>
                   <p>Tàng Can: {', '.join(tang_can)}</p>
                   <p>Thần Sát: {than_sat}</p>
                </div>
                """, unsafe_allow_html=True)

    def display_ngu_hanh_analysis(self, nh_data):
        st.header("🌟 Phân Tích Ngũ Hành")
        fig= go.Figure()
        col_map= {
            "Kim":"#FFD700","Mộc":"#4CAF50",
            "Thủy":"#2196F3","Hỏa":"#F44336",
            "Thổ":"#FF9800"
        }
        for e, cnt in nh_data["thống_kê"].items():
            fig.add_trace(go.Bar(name=e, x=[e], y=[cnt], marker_color=col_map.get(e,"#888")))
        fig.update_layout(title="Phân Bố Ngũ Hành", showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

        st.write(f"**Ngũ Hành Vượng**: {nh_data['vượng']}")
        st.write(f"**Ngũ Hành Suy**: {nh_data['suy']}")

    def display_detailed_analysis(self, analysis):
        st.header("📊 Phân Tích Chi Tiết")
        tab1, tab2, tab3, tab4= st.tabs(["Tổng Quan","Tứ Trụ Chi Tiết","Vận Hạn","Tư Vấn"])

        with tab1:
            self._display_overview(analysis["tổng_quan"])
        with tab2:
            self._display_tu_tru_details(analysis["chi_tiết_tứ_trụ"])
        with tab3:
            self._display_van_han(analysis["vận_hạn"])
        with tab4:
            self._display_advice(analysis)

    def _display_overview(self, overview):
        st.subheader("Mệnh Cục & Ngũ Hành")
        mc= overview["mệnh_cục"]
        # In "bản_chất", "lưu_ý", "phát_triển" dưới dạng bullet
        st.markdown("**Bản Chất:**")
        st.markdown("<ul>", unsafe_allow_html=True)
        for item in mc["bản_chất"]:
            st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

        st.markdown("**Lưu Ý:**")
        st.markdown("<ul>", unsafe_allow_html=True)
        for item in mc["lưu_ý"]:
            st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

        st.markdown("**Phát Triển:**")
        st.markdown("<ul>", unsafe_allow_html=True)
        for item in mc["phát_triển"]:
            st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

        nh= overview["ngũ_hành"]
        st.markdown(f"**Ngũ Hành Vượng**: {nh['vượng']['hành']}")
        st.markdown(f"**Ngũ Hành Suy**: {nh['suy']['hành']}")

    def _display_tu_tru_details(self, details):
        for tru, val in details.items():
            st.markdown(f"### Trụ {tru.capitalize()}")
            st.write(f"**Ý Nghĩa**: {val['ý_nghĩa']['chung']}")
            st.write("**Chi Tiết**:")
            st.markdown("<ul>", unsafe_allow_html=True)
            for c in val["ý_nghĩa"]["chi_tiết"]:
                st.markdown(f"<li>{c}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)

            st.write("**Tính Chất (hành):**")
            st.markdown("<ul>", unsafe_allow_html=True)
            for t in val["tính_chất"]:
                st.markdown(f"<li>{t}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)

            st.write("**Lưu Ý (hành):**")
            st.markdown("<ul>", unsafe_allow_html=True)
            for t in val["lưu_ý"]:
                st.markdown(f"<li>{t}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)

            st.write(f"**Nạp Âm**: {val['nạp_am']}")
            st.write(f"**Tàng Can**: {', '.join(val['tàng_can'])}")
            st.write(f"**Thần Sát**: {', '.join(val['thần_sát'])}")
            st.markdown("---")

    def _display_van_han(self, van_han):
        st.subheader("Vận Hạn Hiện Tại")
        hv= van_han["hiện_tại"]
        st.write(f"**Giai Đoạn**: {hv['giai_đoạn']}")
        st.write(f"**Đặc Điểm**: {hv['đặc_điểm']}")

        st.write("**Lời Khuyên**:")
        st.markdown("<ul>", unsafe_allow_html=True)
        for adv in hv["lời_khuyên"]:
            st.markdown(f"<li>{adv}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

        st.subheader("Bốn Giai Đoạn Cuộc Đời")
        b4= van_han["bốn_giai_đoạn"]
        for stage, info in b4.items():
            st.markdown(f"**{stage}**: {info['đặc_điểm']}")
            st.markdown("Lời khuyên:")
            st.markdown("<ul>", unsafe_allow_html=True)
            for tip in info["lời_khuyên"]:
                st.markdown(f"<li>{tip}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)

        st.subheader("Phân Tích Chi Tiết")
        detail= van_han.get("phân_tích_chi_tiết",{})
        st.write("**Công Danh**:", detail.get("công_danh",""))
        st.write("**Tài Vận**:", detail.get("tài_vận",""))
        st.write("**Gia Đình**:", detail.get("gia_đình",""))
        st.write("**Sức Khỏe**:", detail.get("sức_khỏe",""))
        st.write("**Tình Cảm**:", detail.get("tình_cảm",""))
        st.write("**Bạn Bè**:", detail.get("bạn_bè",""))
        st.write("**Đồng Nghiệp**:", detail.get("đồng_nghiệp",""))

    def _display_advice(self,analysis):
        st.subheader("Quan Hệ")
        qh= analysis["quan_hệ"]
        st.write("**Tương Sinh**:")
        st.write(f"- Sinh: {qh['tương_sinh']['sinh']}")
        st.write(f"- Được Sinh: {qh['tương_sinh']['được_sinh']}")

        st.write("**Tương Khắc**:")
        st.write(f"- Khắc: {qh['tương_khắc']['khắc']}")
        st.write(f"- Bị Khắc: {qh['tương_khắc']['bị_khắc']}")

        st.subheader("Sự Nghiệp")
        sn= analysis["sự_nghiệp"]
        st.write("**Ngành Nghề Phù Hợp**:")
        st.markdown("<ul>", unsafe_allow_html=True)
        for job in sn["ngành_nghề_phù_hợp"]:
            st.markdown(f"<li>{job}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)
        st.write("**Lời Khuyên**:", sn["lời_khuyên"])

        st.subheader("Sức Khỏe")
        sk= analysis["sức_khỏe"]
        st.write("**Cơ Bản**:")
        st.markdown(f"- Cơ quan: {', '.join(sk['cơ_bản']['cơ_quan'])}")
        st.markdown(f"- Nên Chú Ý: {', '.join(sk['cơ_bản']['nên_chú_ý'])}")

        st.write("**Khuyến Nghị**:")
        st.markdown("**Dinh Dưỡng:**")
        st.markdown("<ul>", unsafe_allow_html=True)
        for dd in sk["khuyến_nghị"]["dinh_dưỡng"]:
            st.markdown(f"<li>{dd}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

        st.markdown("**Vận Động:**")
        st.markdown("<ul>", unsafe_allow_html=True)
        for vd in sk["khuyến_nghị"]["vận_động"]:
            st.markdown(f"<li>{vd}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

        st.markdown("**Tinh Thần:**")
        st.markdown("<ul>", unsafe_allow_html=True)
        for tt in sk["khuyến_nghị"]["tinh_thần"]:
            st.markdown(f"<li>{tt}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)

def main():
    ui= BaziUI()
    calc= BaziCalculator()
    ana= BaziAnalyzer()

    submitted, name, gender, bdate, btime= ui.create_input_form()
    if submitted and name and bdate and btime:
        try:
            bazi_data= calc.calculate_bazi(bdate,btime,gender,name)
            analysis= ana.get_full_analysis(bazi_data)

            ui.display_basic_info(bazi_data)
            ui.display_tu_tru(bazi_data)
            ui.display_ngu_hanh_analysis(bazi_data["ngu_hanh"])
            ui.display_detailed_analysis(analysis)

        except Exception as e:
            st.error(f"Lỗi: {str(e)}")

if __name__=="__main__":
    main()
