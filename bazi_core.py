import streamlit as st
import pandas as pd
import ephem
from lunardate import LunarDate
from datetime import datetime

class BaziBase:
    def __init__(self):
        # Thiên Can
        self.thien_can = [
            "Giáp","Ất","Bính","Đinh","Mậu",
            "Kỷ","Canh","Tân","Nhâm","Quý"
        ]
        # Địa Chi
        self.dia_chi = [
            "Tý","Sửu","Dần","Mão","Thìn","Tỵ",
            "Ngọ","Mùi","Thân","Dậu","Tuất","Hợi"
        ]
        # Ngũ Hành
        self.ngu_hanh = {
            "Kim":  ["Canh","Tân","Thân","Dậu"],
            "Mộc":  ["Giáp","Ất","Dần","Mão"],
            "Thủy": ["Nhâm","Quý","Tý","Hợi"],
            "Hỏa":  ["Bính","Đinh","Tỵ","Ngọ"],
            "Thổ":  ["Mậu","Kỷ","Thìn","Tuất","Sửu","Mùi"]
        }
        # Tương Sinh, Tương Khắc
        self.tuong_sinh = {
            "Kim":  {"sinh":"Thủy","được_sinh":"Thổ"},
            "Mộc":  {"sinh":"Hỏa","được_sinh":"Thủy"},
            "Thủy": {"sinh":"Mộc","được_sinh":"Kim"},
            "Hỏa":  {"sinh":"Thổ","được_sinh":"Mộc"},
            "Thổ":  {"sinh":"Kim","được_sinh":"Hỏa"}
        }
        self.tuong_khac = {
            "Kim":  {"khắc":"Mộc","bị_khắc":"Hỏa"},
            "Mộc":  {"khắc":"Thổ","bị_khắc":"Kim"},
            "Thủy": {"khắc":"Hỏa","bị_khắc":"Thổ"},
            "Hỏa":  {"khắc":"Kim","bị_khắc":"Thủy"},
            "Thổ":  {"khắc":"Thủy","bị_khắc":"Mộc"}
        }
        # Tàng Can
        self.tang_can_map = {
            "Tý":["Quý"],          "Sửu":["Kỷ","Quý","Tân"],
            "Dần":["Giáp","Bính"], "Mão":["Ất"],
            "Thìn":["Mậu","Ất","Quý"],  "Tỵ":["Bính","Mậu"],
            "Ngọ":["Đinh","Kỷ"],   "Mùi":["Kỷ","Ất","Đinh"],
            "Thân":["Canh","Nhâm"],"Dậu":["Tân"],
            "Tuất":["Mậu","Tân","Đinh"],"Hợi":["Nhâm","Giáp"]
        }

    def get_ngu_hanh_from_can(self, can_name):
        for hanh, arr in self.ngu_hanh.items():
            if can_name in arr:
                return hanh
        return None

    def get_ngu_hanh_from_chi(self, chi_name):
        for hanh, arr in self.ngu_hanh.items():
            if chi_name in arr:
                return hanh
        return None

    def get_tang_can(self, chi_name):
        return self.tang_can_map.get(chi_name,[])

    def get_tuong_sinh(self, element):
        return self.tuong_sinh.get(element,{})

    def get_tuong_khac(self, element):
        return self.tuong_khac.get(element,{})

class LunarConverter:
    @staticmethod
    def solar_to_lunar(solar_date: datetime):
        try:
            lunar = LunarDate.fromSolarDate(
                solar_date.year,
                solar_date.month,
                solar_date.day
            )
        except ValueError as e:
            raise ValueError(f"Không tính được âm lịch cho ngày {solar_date}: {e}")
        return {
            "year":  lunar.year,
            "month": lunar.month,
            "day":   lunar.day
        }

    @staticmethod
    def get_julian_date(date: datetime):
        try:
            jd= ephem.julian_date(date)
        except OverflowError as e:
            raise ValueError(f"Không tính được Julian date cho {date}: {e}")
        return jd

class BaziUtils:
    @staticmethod
    def get_age(birth_date: datetime):
        today = datetime.now()
        age = today.year - birth_date.year
        if (today.month < birth_date.month) or (
           (today.month == birth_date.month and today.day < birth_date.day)):
            age -= 1
        return age

    @staticmethod
    def get_current_period(age: int):
        if age < 10:
            return "Thiếu niên"
        elif age < 30:
            return "Thanh niên"
        elif age < 50:
            return "Trung niên"
        else:
            return "Hậu vận"

    @staticmethod
    def get_period_characteristics(period: str):
        data= {
            "Thiếu niên":"Giai đoạn học tập và phát triển nền tảng.",
            "Thanh niên":"Thời kỳ lập nghiệp, mở rộng quan hệ.",
            "Trung niên":"Giai đoạn ổn định, xây dựng gia đình - sự nghiệp.",
            "Hậu vận":"Thời gian hưởng thụ, truyền đạt kinh nghiệm."
        }
        return data.get(period,"")
