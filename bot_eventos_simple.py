import requests
import asyncio
import time
from telegram import Bot

# === CONFIGURACIÓN ===
TE_API_KEY = 'fabricioctruji@gmail.com:8ac255235f95443:rmci81jlbupx65h'  # ← en formato usuario:clave
TOKEN = '7870331565:AAGd5WoqeCWMWavfRmTavvy6TxFzKbwoCVM'
USER_ID = '6282948925'

# === FUNCIÓN PARA OBTENER EVENTOS ===
def obtener_eventos_eeuu():
    try:
        url = f'https://api.tradingeconomics.com/calendar/country/united%20states?c={TE_API_KEY}'
        res = requests.get(url)

        if res.status_code != 200:
            return f"❌ Error HTTP {res.status_code}: {res.text}"

        data = res.json()
        eventos = []

        for e in data:
            if e.get('Importance') in ['High', 'Medium']:
                eventos.append({
                    'hora': e['Date'][11:16],
                    'evento': e['Event'],
                    'actual': e.get('Actual', 'N/D'),
                    'previsto': e.get('Forecast', 'N/D')
                })

        if not eventos:
            return "✅ No hay eventos de alta o media relevancia hoy."

        mensaje = "📊 *Eventos económicos relevantes (EE.UU)*\n\n"
        for ev in eventos:
            mensaje += f"🕒 {ev['hora']} - {ev['evento']}\n➡️ Actual: {ev['actual']} | Previsto: {ev['previsto']}\n\n"
        return mensaje.strip()

    except Exception as e:
        return f"❌ Error al obtener eventos: {e}"

# === ENVÍO DEL MENSAJE ===
async def main():
    bot = Bot(token=TOKEN)
    mensaje = obtener_eventos_eeuu()
    await bot.send_message(chat_id=USER_ID, text=mensaje, parse_mode='Markdown')

# === LOOP PARA ENVIAR CADA 24 HORAS ===
if __name__ == "__main__":
    while True:
        print("⏳ Enviando resumen económico diario a Telegram...")
        asyncio.run(main())
        print("✅ Mensaje enviado. Esperando 24 horas...")
        time.sleep(86400)  # Espera 24 horas

