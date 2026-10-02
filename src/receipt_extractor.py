import json, os
from pathlib import Path
import lmstudio as lms

IMAGE = Path("data/raw/nota-sample.png")
MODEL = os.environ["LM_STUDIO_MODEL"]
image = lms.prepare_image(str(IMAGE))
model = lms.llm(MODEL)
chat = lms.Chat()
chat.add_user_message(
    "Baca nota. Ekstrak merchant, tanggal, item, subtotal, pajak, dan total. "
    "Keluarkan HANYA JSON valid tanpa blok markdown atau teks tambahan. Jika pajak tidak terlihat, isi 0. Jangan mengarang.",
    images=[image],
)
prediction = model.respond(chat)

# Ambil teks mentah hasil prediksi
raw_content = prediction.content.strip()

# Hapus format blok kode markdown jika ada (seperti ```json ... ```)
if raw_content.startswith("```"):
    lines = raw_content.splitlines()
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    raw_content = "\n".join(lines).strip()

# Parsing JSON
result = json.loads(raw_content)

# Simpan ke file
Path("reports/receipt.json").write_text(
    json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
)
print(json.dumps(result, indent=2, ensure_ascii=False))
