import os

from google import genai
from google.genai import types

_client: genai.Client | None = None

_PREDICTION_SYSTEM = (
    "Kamu adalah analis investasi saham Indonesia yang berpengalaman. "
    "Buat narasi singkat (2-3 paragraf) tentang prediksi saham berdasarkan data model LSTM. "
    "Gunakan bahasa Indonesia yang profesional namun mudah dipahami investor retail. "
    "Penting: akurasi arah model hanya sekitar 48-49% (hampir acak), jadi jangan terlalu percaya diri "
    "terhadap sinyal BUY/SELL — sampaikan dengan nada hati-hati dan kontekstual. "
    "Fokus pada MAPE dan R² sebagai indikator keandalan harga, bukan arah. "
    "Selalu sertakan disclaimer bahwa prediksi ini bukan saran investasi."
)

_PROFIT_LOSS_SYSTEM = (
    "Kamu adalah analis investasi saham Indonesia yang berpengalaman. "
    "Buat narasi singkat (2-3 paragraf) tentang hasil kalkulasi profit/loss posisi saham. "
    "Gunakan bahasa Indonesia yang profesional namun mudah dipahami investor retail. "
    "Ingatkan bahwa harga exit yang digunakan adalah estimasi model, bukan harga pasti — "
    "akurasi arah model hanya sekitar 48-49% sehingga realisasi bisa berbeda signifikan. "
    "Selalu sertakan disclaimer bahwa ini adalah estimasi, bukan jaminan keuntungan."
)


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set")
        _client = genai.Client(api_key=api_key)
    return _client


def generate_prediction_narration(ticker: str, prediction: dict, metrics: dict) -> str:
    prompt = (
        f"Saham: {ticker}\n"
        f"Tanggal sinyal: {prediction['signal_date']}\n"
        f"Harga saat ini: Rp {prediction['base_close']:,.2f}\n"
        f"Prediksi harga besok: Rp {prediction['predicted_close']:,.2f}\n"
        f"Prediksi log return: {prediction['predicted_log_return']:.6f}\n"
        f"Sinyal: {prediction['signal']}\n\n"
        f"Performa Model:\n"
        f"- MAPE: {metrics.get('mape', 'N/A')}%\n"
        f"- R²: {metrics.get('r2', 'N/A')}\n"
        f"- Akurasi Arah: {metrics.get('direction_accuracy', 'N/A')}%\n"
        f"- Return RMSE: {metrics.get('return_rmse', 'N/A')}\n\n"
        "Buat narasi investasi singkat dalam bahasa Indonesia."
    )
    response = _get_client().models.generate_content(
        model="gemma-4-31b-it",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=_PREDICTION_SYSTEM,
            temperature=1.0,
            max_output_tokens=2048,
        ),
    )
    return response.text


def generate_profit_loss_narration(
    ticker: str, prediction: dict, metrics: dict, profit_loss: dict
) -> str:
    prompt = (
        f"Saham: {ticker}\n"
        f"Sinyal: {prediction['signal']}\n"
        f"Harga beli: Rp {profit_loss['buy_price']:.2f}\n"
        f"Harga jual (estimasi): Rp {profit_loss['sell_price']:.2f}\n"
        f"Jumlah saham: {profit_loss['quantity']['shares']} ({profit_loss['quantity']['lots']} lot)\n"
        f"Total modal: Rp {profit_loss['total_cost']:,.2f}\n"
        f"Net profit/loss: Rp {profit_loss['net_profit_loss']:,.2f}\n"
        f"Return bersih: {profit_loss['net_return_pct']:.4f}%\n"
        f"Status: {profit_loss['status']}\n"
        f"Breakeven price: Rp {profit_loss['breakeven_sell_price']:,.2f}\n\n"
        f"Performa Model:\n"
        f"- MAPE: {metrics.get('mape', 'N/A')}%\n"
        f"- Akurasi Arah: {metrics.get('direction_accuracy', 'N/A')}%\n\n"
        "Buat narasi kalkulasi profit/loss dalam bahasa Indonesia."
    )
    response = _get_client().models.generate_content(
        model="gemma-4-31b-it",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=_PROFIT_LOSS_SYSTEM,
            temperature=1.0,
            max_output_tokens=2048,
        ),
    )
    return response.text
