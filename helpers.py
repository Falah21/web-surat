# helpers.py
import datetime
from num2words import num2words

HARI_INDONESIA = {
    0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis",
    4: "Jumat", 5: "Sabtu", 6: "Minggu"
}
BULAN_INDONESIA = {
    1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
    5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
    9: "September", 10: "Oktober", 11: "November", 12: "Desember"
}

# def terbilang_desimal(angka: str):
#     if angka is None:
#         return ""
#     angka = str(angka).strip().replace(" ", "")
#     angka = angka.replace(",", ".")
#     if angka == "":
#         return ""
#     if "." in angka:
#         bagian = angka.split(".")
#         try:
#             integer = int(bagian[0])
#         except:
#             return angka.replace(".", ",")
#         decimal = bagian[1]

#         int_text = num2words(integer, lang='id').replace("-", " ").lower()
#         dec_text = " ".join([num2words(int(d), lang='id').title() for d in decimal if d.isdigit()])

#         return f"{angka.replace('.', ',')} ({int_text} Koma {dec_text})"
#     else:
#         try:
#             n = int(angka)
#             teks = num2words(n, lang='id').replace("-", " ").lower()
#             return f"{angka} ({teks})"
#         except:
#             return angka

# helpers.py - bagian terbilang_desimal
def terbilang_desimal(angka: str):
    if angka is None:
        return ""
    angka = str(angka).strip().replace(" ", "")
    angka = angka.replace(",", ".")
    if angka == "":
        return ""
    if "." in angka:
        bagian = angka.split(".")
        try:
            integer = int(bagian[0])
        except:
            return angka.replace(".", ",")
        decimal = bagian[1]

        int_text = num2words(integer, lang='id').replace("-", " ").lower()  # sudah lower
        
        # PERBAIKAN: ubah .title() menjadi .lower() untuk bagian decimal
        dec_text = " ".join([num2words(int(d), lang='id').lower() for d in decimal if d.isdigit()])  # ganti .title() ke .lower()

        return f"{angka.replace('.', ',')} ({int_text} koma {dec_text})"  # tambah "koma" lowercase
    else:
        try:
            n = int(angka)
            teks = num2words(n, lang='id').replace("-", " ").lower()
            return f"{angka} ({teks})"
        except:
            return angka

# def smart_title(text: str):
#     if text is None:
#         return ""
#     return " ".join([w.capitalize() for w in str(text).split(" ")])

# def smart_title(text: str):
#     if text is None:
#         return ""
#     text = str(text).strip()
#     if text == "":
#         return ""
#     # daftar singkatan yang harus tetap kapital
#     FIX = {"A.Md.", "S.Ag.", "S.Ak.", "S.E.", "S.Farm.", "S.H.", "S.I.Kom.", "S.IP.", "S.Kep.", 
#            "S.Kom.", "S.Pd.", "S.Psi.", "S.Sos.", "S.S.", "S.T.", "S.Ked.", "S.Pt.", "S.KM.",
#            "M.A.", "M.H.", "M.Hum.", "M.Kes.", "M.Kom.", "M.M.", "M.Pd.", "M.Psi.", "M.Si.", "M.T.",
#            "Dr.", "Drs.", "Dra.", "Ph.D.",
#            "H.", "Hj.", "K.H.", "R.", "R.A.", "R.M.", "R.K.", "Prof.",
#            "TBK", "CV", "UD", "PT",
#                    # optional: roman numerals
#             "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"
#            }
#     # pisahkan berdasarkan spasi
#     parts = text.split(" ")
#     result = []
#     for p in parts:
#         clean = p.replace(",", "").replace(".", "").upper()
#         if clean in FIX:
#             result.append(clean)        # biarkan kapital
#         else:
#             # selain itu → title case biasa
#             result.append(p.capitalize())
#     return " ".join(result)

# def smart_title(text: str):
#     if text is None:
#         return ""
#     text = str(text).strip()
#     if text == "":
#         return ""

#     # daftar singkatan yang harus tetap kapital
#     FIX = {
#         "A.MD.", "S.AG.", "S.AK.", "S.E.", "S.FARM.", "S.H.", "S.I.KOM.", "S.IP.", "S.KEP.",
#         "S.KOM.", "S.PD.", "S.PSI.", "S.SOS.", "S.S.", "S.T.", "S.KED.", "S.PT.", "S.KM.",
#         "M.A.", "M.H.", "M.HUM.", "M.KES.", "M.KOM.", "M.M.", "M.PD.", "M.PSI.", "M.SI.", "M.T.",
#         "DR.", "DRS.", "DRA.", "PH.D.",
#         "H.", "HJ.", "K.H.", "R.", "R.A.", "R.M.", "R.K.", "PROF.",
#         "TBK", "CV", "UD", "PT",
#         # optional: roman numerals
#         "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"
#     }

#     parts = text.split(" ")
#     result = []
#     for p in parts:
#         original = p
#         clean = original.replace(",", "").replace(".", "").upper()

#         if clean in FIX:
#             # kalau di FIX → pakai versi uppercase
#             result.append(clean)
#         elif original.isupper() and len(original) <= 3:
#             # kalau sudah ALL CAPS (misal VI, VII, A12) → biarin
#             result.append(original)
#         else:
#             result.append(original.capitalize())

#     return " ".join(result)

def smart_title(text: str):
    if text is None:
        return ""
    text = str(text).strip()
    if text == "":
        return ""

    # 1) Map gelar berdasarkan huruf saja (tanpa titik)
    DEGREE_MAP = {
        "AMD": "A.Md.", "SAG": "S.Ag.", "SAK": "S.Ak.", "SE": "S.E.", "SFARM": "S.Farm.",
        "SH": "S.H.", "SIKOM": "S.I.Kom.", "SIP": "S.IP.", "SKEP": "S.Kep.", "SKOM": "S.Kom.",
        "SPD": "S.Pd.", "SPSI": "S.Psi.", "SSOS": "S.Sos.", "SS": "S.S.", "ST": "S.T.", 
        "SKED": "S.Ked.", "SPT": "S.Pt.", "SKM": "S.KM.", "MA": "M.A.", "MH": "M.H.", 
        "MHUM": "M.Hum.", "MKES": "M.Kes.", "MKOM": "M.Kom.", "MM": "M.M.", "MPD": "M.Pd.",
        "MPSI": "M.Psi.", "MSI": "M.Si.", "MT": "M.T.", "DR": "Dr.", "DRS": "Drs.",
        "DRA": "Dra.", "PHD": "Ph.D.",
    }

    # 2) Singkatan yang cukup di-UPPER-kan saja (plus roman)
    UPPER_SET = {
        "H", "HJ", "KH", "R", "RA", "RM", "RK", "PROF",
        "PT", "CV", "UD", "TBK",
        # Roman numerals
        "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", 
        "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX", 
        "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX"
    }

    # 3) Kata-kata khusus dengan hyphen yang perlu di-preserve case-nya
    # Contoh: EX-DIVISI → Ex-Divisi, NON-ACTIVE → Non-Active
    def handle_hyphenated_word(word):
        parts = word.split("-")
        result_parts = []
        for part in parts:
            letters_only = "".join(ch for ch in part if ch.isalpha()).upper()
            if letters_only in DEGREE_MAP:
                result_parts.append(DEGREE_MAP[letters_only])
            elif letters_only in UPPER_SET:
                result_parts.append(part.upper())
            else:
                result_parts.append(part.capitalize())
        return "-".join(result_parts)

    parts = text.split()
    result = []

    # for p in parts:
    #     # Pisah core & tanda baca di belakang (koma, titik, titik koma)
    #     core = p.rstrip(",.;:")
    #     trailing = p[len(core):]  # tanda baca di belakang, misal ",", "."
        
    #     # Cek apakah ada hyphen
    #     if "-" in core:
    #         # Handle kata dengan hyphen
    #         base = handle_hyphenated_word(core)
    #     else:
    #         # Ambil cuma huruf dari core, buat dicek
    #         letters_only = "".join(ch for ch in core if ch.isalpha()).upper()

    #         if letters_only in DEGREE_MAP:
    #             # Contoh: "s.h", "S.H", "sh." → "S.H." lalu tambahin trailing
    #             base = DEGREE_MAP[letters_only]
    #         elif letters_only in UPPER_SET:
    #             # Contoh: "vi/27" → "VI/27", "pt" → "PT"
    #             base = core.upper()
    #         else:
    #             # Normal: kapital huruf pertama saja
    #             base = core.capitalize()
        
    #     result.append(base + trailing)

    # return " ".join(result)

    for p in parts:
        core = p.rstrip(",.;:")
        trailing = p[len(core):]
    
        # ⬅️ INI TAMBAHANNYA
        if any(sym in core for sym in ["&", "@", "/"]):
            result.append(core + trailing)
            continue
    
        # Cek apakah ada hyphen
        if "-" in core:
            base = handle_hyphenated_word(core)
        else:
            letters_only = "".join(ch for ch in core if ch.isalpha()).upper()
    
            if letters_only in DEGREE_MAP:
                base = DEGREE_MAP[letters_only]
            elif letters_only in UPPER_SET:
                base = core.upper()
            else:
                base = core.capitalize()
    
        result.append(base + trailing)
    return " ".join(result)


def parse_tanggal_ke_terbilang(tgl: datetime.date):
    if not isinstance(tgl, (datetime.date, datetime.datetime)):
        return "", "", "", ""
    hari = HARI_INDONESIA[tgl.weekday()]
    from_num = terbilang_desimal(str(tgl.day))
    bulan = BULAN_INDONESIA[tgl.month]
    tahun = terbilang_desimal(str(tgl.year))
    return hari, from_num, bulan, tahun

# helpers.py

def format_rupiah_terbilang(value):
    """
    Format angka menjadi string Rupiah dengan terbilang
    Contoh: 350000 -> "350.000,- (tiga ratus lima puluh ribu rupiah)"
    """
    # from terbilang_desimal import terbilang_desimal  # pastikan terbilang_desimal ada di helpers.py

    try:
        value_num = float(str(value).replace(".", "").replace(",", "").strip())

        angka = f"{value_num:,.0f}".replace(",", ".") + ",-"

        terbilang_raw = terbilang_desimal(str(int(value_num)))
        if "(" in terbilang_raw and ")" in terbilang_raw:
            terbilang_only = terbilang_raw.split("(")[1].replace(")", "").strip()
        else:
            terbilang_only = terbilang_raw

        # Pakai lowercase
        terbilang_only = terbilang_only.lower()

        return f"{angka} ({terbilang_only} rupiah)"
    except:
        return "0,- (nol rupiah)"

# helpers.py - versi lebih simple

def parse_angka_simple(value):
    """Parse angka sederhana dari string"""
    try:
        if not value or str(value).strip() == "":
            return 0
        cleaned = str(value).strip().replace(".", "").replace(",", "")
        return int(cleaned) if cleaned.isdigit() else 0
    except:
        return 0

def format_display(value_input, value_num=None):
    """Format display untuk biaya dengan terbilang"""
    if value_num is None:
        value_num = parse_angka_simple(value_input)
    
    try:
        formatted = format_rupiah_terbilang(str(value_num))
        return formatted
    except:
        try:
            terbilang_raw = terbilang_desimal(value_num)
            terbilang_only = terbilang_raw.split("(")[-1].replace(")", "").strip().lower() if "(" in terbilang_raw else "nol"
            return f"{value_num:,.0f}".replace(",", ".") + f",- ({terbilang_only} rupiah)"
        except:
            return "0,- (nol rupiah)"



