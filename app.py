from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
import pandas as pd # type: ignore
import os

app = Flask(__name__)
CORS(app)  # Allow CORS for local frontend

FILE_PATH = "Template_Refleksi_Harian_Jurnal_Perasaan.xlsx"

# Jika file tidak ada, buat file baru dengan header
if not os.path.exists(FILE_PATH):
    df = pd.DataFrame(columns=[
        "Tanggal", "Perasaan Hari Ini (1-10)", "Emosi yang Dirasakan",
        "Pemicu Emosi", "Reaksi Saya", "Hal Positif yang Terjadi Hari Ini",
        "Pelajaran Hari Ini", "Apa yang Bisa Saya Lakukan Besok untuk Membaik?",
        "Catatan Tambahan / Beban Pikiran"
    ])
    df.to_excel(FILE_PATH, index=False)

@app.route("/api/refleksi", methods=["POST"])
def simpan_refleksi():
    data = request.get_json()

    # Format ke dataframe
    new_data = pd.DataFrame([{
        "Tanggal": data.get("tanggal"),
        "Perasaan Hari Ini (1-10)": data.get("skor_perasaan"),
        "Emosi yang Dirasakan": data.get("emosi"),
        "Pemicu Emosi": data.get("pemicu"),
        "Reaksi Saya": data.get("reaksi"),
        "Hal Positif yang Terjadi Hari Ini": data.get("positif"),
        "Pelajaran Hari Ini": data.get("pelajaran"),
        "Apa yang Bisa Saya Lakukan Besok untuk Membaik?": data.get("rencana_besok"),
        "Catatan Tambahan / Beban Pikiran": data.get("catatan"),
    }])

    # Tambahkan ke Excel
    df_existing = pd.read_excel(FILE_PATH)
    df_all = pd.concat([df_existing, new_data], ignore_index=True)
    df_all.to_excel(FILE_PATH, index=False)

    return jsonify({"message": "Data berhasil disimpan!"})

if __name__ == "__main__":
    app.run(debug=True)
