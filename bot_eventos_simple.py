import asyncio
import requests
from telegram import Bot

# --- CONFIGURACIÓN ---
TE_API_KEY = '7870331565:AAGd5WoqeCWMWavfRmTavvy6TxFzKbwoCVM'      # ← tu API key de TradingEconomics
TOKEN = 6282948925          # ← tu token de Telegram Bot
USER_ID = '8ac255235f95443:rmci81jlbupx65h'            # ← tu chat_id de Telegram

# --- Obtener eventos desde TradingEconomics API ---
def obtener_eventos_eeuu():
    try:
        url = f'https://api.tradingeconomics.com/calendar/country/united states?c={TE_API_KEY}'
        res = requests.get(url)
        data = res.json()

        eventos = []
        for e in data:
            if e['Importance'] in ['High', 'Medium']:
                eventos.append({
                    'hora': e['Date'][11:16],
                    'evento': e['Event'],
                    'actual': e.get('Actual', 'N/D'),
                    'previsto': e.get('Forecast', 'N/D')
                })

        return eventos
    except Exception as e:
        return f"❌ Error al obtener eventos: {e}"

# --- Formatear mensaje ---
def generar_mensaje(eventos):
    if isinstance(eventos, str):
        return eventos

    if not eventos:
        return "✅ No hay eventos económicos importantes hoy en EE.UU."

    mensaje = "📆 *Eventos Económicos de EE.UU. (Hoy)*\n\n"
    for e in eventos:
        mensaje += f"🕒 {e['hora']} - {e['evento']}\n"
        mensaje += f"   Actual: {e['actual']} | Previsto: {e['previsto']}\n\n"
    return mensaje

# --- Enviar mensaje ---
async def main():
    bot = Bot(token=TOKEN)
    eventos = obtener_eventos_eeuu()
    mensaje = generar_mensaje(eventos)
    await bot.send_message(chat_id=USER_ID, text=mensaje, parse_mode='Markdown')

if __name__ == "__main__":
    asyncio.run(main())
