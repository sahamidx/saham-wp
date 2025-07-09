#!/usr/bin/env python3
"""
Download EOD price & fundamental data per ticker
Usage:
  python update_data.py --codes-file ../../data/static_info.csv --output-dir ../../data
"""

import argparse, csv, json, os, sys, datetime
import pandas as pd
import yfinance as yf

def fetch_fundamental(ticker):
    ti = yf.Ticker(f"{ticker}.JK").info
    dy = ti.get("dividendYield")
    dividen_yield = round(dy * 100, 2) if dy else 0
    return {
        "kode": ticker,
        "market_cap": ti.get("marketCap"),
        "eps": ti.get("trailingEps"),
        "per": ti.get("trailingPE"),
        "pbv": ti.get("priceToBook"),
        "roe": None,
        "der": None,
        "dividen_yield": dividen_yield,
        "harga": ti.get("regularMarketPrice"),
        "saham_beredar": ti.get("sharesOutstanding"),
        "last_updated": datetime.date.today().isoformat()
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--codes-file", required=True)
    p.add_argument("--output-dir", required=True)
    args = p.parse_args()

    codes_df = pd.read_csv(args.codes_file)
    if "kode" not in codes_df.columns:
        print("CSV must have column 'kode'.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    fundamental_data = []

    for _, row in codes_df.iterrows():
        kode = row["kode"].strip().upper()
        print(f"Fetching {kode} ...")

        # Simpan harga
        df = yf.download(f"{kode}.JK", period="5y", interval="1d", auto_adjust=False)
        price_path = os.path.join(args.output_dir, "prices", f"{kode}.csv")
        os.makedirs(os.path.dirname(price_path), exist_ok=True)
        df.to_csv(price_path)

        # Simpan fundamental gabungan
        fdata = fetch_fundamental(kode)
        fundamental_data.append(fdata)

        # Simpan per-emiten
        fund_path = os.path.join(args.output_dir, "fundamentals", f"{kode}.json")
        os.makedirs(os.path.dirname(fund_path), exist_ok=True)
        with open(fund_path, "w") as f:
            json.dump(fdata, f, indent=2)

    # Optional: dump semua gabungan
    combined_path = os.path.join(args.output_dir, "fundamental.json")
    with open(combined_path, "w") as f:
        json.dump(fundamental_data, f, indent=2)

    print("Selesai. Semua data sudah disimpan.")

if __name__ == "__main__":
    main()
