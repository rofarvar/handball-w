#!/usr/bin/env python3
"""Generate data.js from ranking.txt (only teams that have played a match)."""
import json
import re

INPUT = "ranking.txt"
FEED = "feed.txt"
PREV = "ranking last.txt"
OUTPUT = "data.js"

LINE_RE = re.compile(r"^(.*?):\s*([\d.]+)\s*elo\s*$")
MATCH_RE = re.compile(r"^\./match\s+(\S+)\s+(\S+)\s+")

NAME_TO_CODE = {
    "Afghanistan": "AF", "Albania": "AL", "Algeria": "DZ",
    "American_Samoa": "AS", "Andorra": "AD", "Angola": "AO",
    "Antigua_and_Barbuda": "AG", "Argentina": "AR", "Armenia": "AM",
    "Australia": "AU", "Austria": "AT", "Azerbaijan": "AZ",
    "Bahamas": "BS", "Bahrain": "BH", "Bangladesh": "BD",
    "Barbados": "BB", "Belarus": "BY", "Belgium": "BE", "Belize": "BZ",
    "Benin": "BJ", "Bhutan": "BT", "Bolivia": "BO",
    "Bosnia_and_Herzegovina": "BA", "Botswana": "BW", "Brazil": "BR",
    "British_Virgin_Islands": "VG", "Brunei": "BN", "Bulgaria": "BG",
    "Burkina_Faso": "BF", "Burundi": "BI", "Cambodia": "KH",
    "Cameroon": "CM", "Canada": "CA", "Cape_Verde": "CV", "CAR": "CF",
    "Cayman_Islands": "KY", "Chad": "TD", "Chile": "CL", "Colombia": "CO",
    "Comoros": "KM", "Congo": "CG", "Cook_Islands": "CK",
    "Costa_Rica": "CR", "Côte_d'Ivoire": "CI", "Cote_dIvoire": "CI", "Croatia": "HR",
    "Cuba": "CU", "Cyprus": "CY", "Czechia": "CZ", "Denmark": "DK",
    "Djibouti": "DJ", "Dominica": "DM", "Dominican_Republic": "DO",
    "DPR_Korea": "KP", "DR_Congo": "CD", "Ecuador": "EC", "Egypt": "EG",
    "El_Salvador": "SV", "England": "GBENG", "Equatorial_Guinea": "GQ",
    "Estonia": "EE", "Eswatini": "SZ", "Ethiopia": "ET",
    "Faroe_Islands": "FO", "Fiji": "FJ", "Finland": "FI", "France": "FR",
    "FS_Micronesia": "FM", "Gabon": "GA", "Gambia": "GM", "Georgia": "GE",
    "Germany": "DE", "Ghana": "GH", "Great_Britain": "GB", "Greece": "GR",
    "Greenland": "GL", "Grenada": "GD", "Guadeloupe": "GP", "Guam": "GU",
    "Guatemala": "GT", "Guiana": "GF", "Guinea": "GN",
    "Guinea-Bissau": "GW", "Guyana": "GY", "Haiti": "HT",
    "Honduras": "HN", "Hong_Kong": "HK", "Hungary": "HU", "Iceland": "IS",
    "India": "IN", "Indonesia": "ID", "Iran": "IR", "Iraq": "IQ",
    "Ireland": "IE", "Israel": "IL", "Italy": "IT", "Jamaica": "JM",
    "Japan": "JP", "Jordan": "JO", "Kazakhstan": "KZ", "Kenya": "KE",
    "Kiribati": "KI", "Korea_Republic": "KR", "Kosovo": "XK",
    "Kuwait": "KW", "Kyrgystan": "KG", "Lao_PDR": "LA", "Latvia": "LV",
    "Lebanon": "LB", "Lesotho": "LS", "Liberia": "LR",
    "Liechtenstein": "LI", "Lithuania": "LT", "Luxembourg": "LU",
    "Libya": "LY", "Macao": "MO", "Madagascar": "MG", "Malawi": "MW",
    "Malaysia": "MY", "Maldives": "MV", "Mali": "ML", "Malta": "MT",
    "Marshall_Islands": "MH", "Martinique": "MQ", "Mauritania": "MR",
    "Mauritius": "MU", "Mayotte": "YT", "Mexico": "MX", "Moldova": "MD",
    "Monaco": "MC", "Mongolia": "MN", "Montenegro": "ME",
    "Morocco": "MA", "Mozambique": "MZ", "Namibia": "NA", "Nauru": "NR",
    "Nepal": "NP", "Netherlands": "NL", "New_Caledonia": "NC",
    "New_Zealand": "NZ", "Nicaragua": "NI", "Niger": "NE",
    "Nigeria": "NG", "North_Macedonia": "MK", "Northern_Mariana_Islands": "MP",
    "Norway": "NO", "Oman": "OM", "Pakistan": "PK", "Palau": "PW",
    "Palestine": "PS", "Panama": "PA", "Papua_New_Guinea": "PG",
    "Paraguay": "PY", "Peru": "PE", "Philippines": "PH", "Poland": "PL",
    "Portugal": "PT", "China": "CN", "PR_China": "CN", "Puerto_Rico": "PR", "Qatar": "QA",
    "Réunion": "RE", "Romania": "RO", "Russia": "RU", "Rwanda": "RW",
    "Saint_Kitts_and_Nevis": "KN", "Saint_Lucia": "LC", "Samoa": "WS",
    "São_Tomé_e_Príncipe": "ST", "Saudi_Arabia": "SA", "Scotland": "GBSCT",
    "Senegal": "SN", "Serbia": "RS", "Seychelles": "SC",
    "Sierra_Leone": "SL", "Singapore": "SG", "Slovakia": "SK",
    "Slovenia": "SI", "Solomon_Islands": "SB", "Somalia": "SO",
    "South_Africa": "ZA", "South_Sudan": "SS", "Spain": "ES",
    "Sri_Lanka": "LK", "Sudan": "SD", "Sweden": "SE", "Switzerland": "CH",
    "Syria": "SY", "Tahiti": "PF", "Taipei": "TW", "Tajikistan": "TJ",
    "Tanzania": "TZ", "Thailand": "TH", "Timor-Leste": "TL", "Togo": "TG",
    "Tonga": "TO", "Trinidad_and_Tobago": "TT", "Tunisia": "TN",
    "Türkiye": "TR", "Turkmenistan": "TM", "Tuvalu": "TV", "UAE": "AE",
    "Uganda": "UG", "Ukraine": "UA", "Uruguay": "UY", "USA": "US",
    "Uzbekistan": "UZ", "Vanuatu": "VU", "Venezuela": "VE",
    "Vietnam": "VN", "Yemen": "YE", "Zambia": "ZM", "Zimbabwe": "ZW",
}

FLAG_DIR = "flags"
FLAG_WIDTH = 40
FLAG_URL = "https://flagcdn.com/w{width}/{code}.png"


def code_to_file(code):
    if code == "GBENG":
        return "gb-eng"
    if code == "GBSCT":
        return "gb-sct"
    return code.lower()


def download_flags(codes):
    import os
    import urllib.request

    os.makedirs(FLAG_DIR, exist_ok=True)
    for code in sorted(codes):
        name = code_to_file(code) + ".png"
        path = os.path.join(FLAG_DIR, name)
        if os.path.exists(path):
            continue
        url = FLAG_URL.format(width=FLAG_WIDTH, code=code_to_file(code))
        try:
            with urllib.request.urlopen(url, timeout=20) as resp, open(path, "wb") as fh:
                fh.write(resp.read())
        except Exception as exc:
            print(f"Warning: failed to download {url}: {exc}")


def read_elo(path):
    data = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            m = LINE_RE.match(line)
            if m:
                data[m.group(1)] = float(m.group(2))
    return data


def read_feed_teams(path):
    teams = set()
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = MATCH_RE.match(line.strip())
            if m:
                teams.add(m.group(1))
                teams.add(m.group(2))
    return teams


def rank_order(data):
    return {name: i + 1 for i, name in enumerate(
        sorted(data, key=lambda n: (-data[n], n)))}


def parse():
    elo = read_elo(INPUT)
    prev_elo = read_elo(PREV)
    played = read_feed_teams(FEED)
    prev_rank = rank_order({n: e for n, e in prev_elo.items() if n in played})
    cur_rank = rank_order({n: e for n, e in elo.items() if n in played})

    teams = []
    for key in sorted(cur_rank, key=cur_rank.get):
        name = key.replace("_", " ").strip()
        code = NAME_TO_CODE.get(key)
        if code is None:
            print(f"Warning: no flag mapping for {name!r}; using fallback")
        prev = prev_rank.get(key)
        move = 0 if prev is None else prev - cur_rank[key]
        teams.append({
            "name": name,
            "elo": elo[key],
            "move": move,
            "code": code_to_file(code) if code else None,
        })
    return teams


def main():
    teams = parse()
    codes = {t["code"] for t in teams if t["code"]}
    download_flags(codes)
    with open(OUTPUT, "w", encoding="utf-8") as fh:
        fh.write("const teams = " + json.dumps(teams, ensure_ascii=False) + ";\n")
    print(f"Wrote {len(teams)} teams to {OUTPUT}")


if __name__ == "__main__":
    main()
