import os

from google import genai
from google.genai import errors, types

_MODEL = "gemma-4-31b-it"

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

_clients: list[genai.Client] | None = None


def _get_clients() -> list[genai.Client]:
    global _clients
    if _clients is None:
        keys = []
        # Dedicated fallback keys are tried first; GEMINI_API_KEY holds the
        # shared last-resort key (e.g. a teammate's), so it is attempted last.
        for name in ("GEMINI_API_KEY_2", "GEMINI_API_KEY_3", "GEMINI_API_KEY"):
            key = os.getenv(name)
            if key:
                keys.append(key)
        if not keys:
            raise RuntimeError("GEMINI_API_KEY not set")
        _clients = [genai.Client(api_key=key) for key in keys]
    return _clients


def _generate(system_instruction: str, prompt: str) -> str:
    """Generate narration, falling back to the next API key on rate limit (429)
    or transient server error (5xx). Re-raises the last error if every key fails."""
    last_error: Exception | None = None
    for client in _get_clients():
        try:
            response = client.models.generate_content(
                model=_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=1.0,
                    max_output_tokens=8192,
                ),
            )
            return response.text
        except errors.ClientError as e:
            if e.code != 429:
                raise
            last_error = e
        except errors.ServerError as e:
            last_error = e
    raise last_error


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
    return _generate(_PREDICTION_SYSTEM, prompt)


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
    return _generate(_PROFIT_LOSS_SYSTEM, prompt)
