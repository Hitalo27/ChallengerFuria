import asyncio
import aiosqlite
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

openai.api_key = ''

TOKEN = '7492463109:AAH6jWn858WyYwI-fg0fGsVaGpAZfDwSyIY'

bot = Bot(token=TOKEN)
dp = Dispatcher()

DB_FILE = 'furia_fans.db'

async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                                user_id INTEGER PRIMARY KEY,
                                cpf TEXT,
                                universo TEXT,
                                acertou_quiz INTEGER,
                                participou INTEGER,
                                jogo_desejado TEXT
                            )''')
        await db.commit()

async def get_chatgpt_response(user_message: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um especialista da FURIA, uma organização de esports."},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception:
        return "Desculpe, ocorreu um erro com nossa IA especialista da FURIA ao processar sua solicitação."

async def enviar_menu(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Próximos Jogos")],
            [KeyboardButton(text="👥 Jogadores da FURIA")],
            [KeyboardButton(text="🏆 História da FURIA")],
            [KeyboardButton(text="📞 Contato")]
        ],
        resize_keyboard=True
    )
    await message.answer("🎯 Menu de Informações da FURIA:", reply_markup=keyboard)

@dp.message(CommandStart())
async def start(message: types.Message):
    user_id = message.from_user.id

    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT participou FROM usuarios WHERE user_id = ?', (user_id,))
        user = await cursor.fetchone()

    if user and user[0] == 1:
        await message.answer("🔥 Bem-vindo de volta, Furioso! Continue interagindo!")
        await enviar_menu(message)
        return

    await message.answer(
    "🔥 Bem-vindo ao FURIA Fans Bot! 🔥\n\n🎉 Participe do sorteio para ganhar ingressos e ver um jogo presencial da nossa equipe 🎮⚽\n\nEscolha o seu universo para começar:\n\n1️⃣ Futebol ⚽\n2️⃣ Jogos 🎮\n\nApós escolher, você passará por um quiz rápido para concorrer ao sorteio!"
    )

@dp.message()
async def handle_all(message: types.Message):
    user_id = message.from_user.id
    text = message.text.strip()

    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute('SELECT universo, acertou_quiz, participou, jogo_desejado FROM usuarios WHERE user_id = ?', (user_id,))
        user = await cursor.fetchone()

    if user and user[2] == 1:  # Se o usuário participou
        if text == "📅 Próximos Jogos":
            await message.answer("🎮 Próximos Jogos:\n\n- LoL: 05/05 vs Pain Gaming\n- Valorant: 06/05 vs LOUD\n- Kings League: 07/05 vs Porcinos FC")
            return

        if text == "👥 Jogadores da FURIA":
            await message.answer("👥 Jogadores da FURIA:\n\n- CS: KSCERATO, yuurih, FalleN, chelo, arT\n- LoL: Envy, fNb, Netuno, RedBert\n- Valorant: mwzera, Khalil, kon4n")
            return

        if text == "🏆 História da FURIA":
            await message.answer("🏆 História:\n\nFundada em 2017, a FURIA é uma das maiores organizações de esports do Brasil, famosa pelo estilo agressivo e paixão nos jogos.")
            return

        if text == "📞 Contato":
            await message.answer("📞 Contato:\n\n- Email: contato@furia.gg\n- Instagram: @furiagg\n- Site: www.furia.gg")
            return

        # Resposta livre usando ChatGPT
        response = await get_chatgpt_response(text)
        await message.answer(response)
        return

    if not user:
        if text == '1':  
            universo = 'Futebol'
            pergunta_quiz = "Quem é o presidente da Kings League? \n1 - Gerard Piqué \n2 - Sergio Agüero \n3 - Ronaldinho Gaúcho"
            jogo_desejado = ''
            await message.answer(f"PERGUNTA RÁPIDA:\n{pergunta_quiz}")
        elif text == '2':  
            universo = 'Jogos'
            pergunta_quiz = "Qual jogador da FURIA é conhecido como 'Rei da Mira'? \n1 - KSCERATO \n2 - yuurih \n3 - FalleN"
            jogo_desejado = ''
            await message.answer(f"PERGUNTA RÁPIDA:\n{pergunta_quiz}")
        else:
            await message.answer("Escolha válida: 1 - Futebol ou 2 - Jogos")
            return

        async with aiosqlite.connect(DB_FILE) as db:
            await db.execute('INSERT INTO usuarios (user_id, universo, acertou_quiz, participou, jogo_desejado) VALUES (?, ?, ?, ?, ?)',
                             (user_id, universo, 0, 0, jogo_desejado))
            await db.commit()


    elif user[1] == 0:
        if user[0] == 'Futebol':
            if text == '1':
                async with aiosqlite.connect(DB_FILE) as db:
                    await db.execute('UPDATE usuarios SET acertou_quiz = 1 WHERE user_id = ?', (user_id,))
                    await db.commit()
                await message.answer("✅ Acertou! Agora envie seu CPF para cadastro no sorteio:")
            else:
                pergunta_quiz = "Quem é o presidente da Kings League? \n1 - Gerard Piqué \n2 - Sergio Agüero \n3 - Ronaldinho Gaúcho"
                await message.answer(f"❌ Errou! Vamos tentar de novo! {pergunta_quiz}")
                    
        elif user[0] == 'Jogos':
            if text == '1': 
                async with aiosqlite.connect(DB_FILE) as db:
                    await db.execute('UPDATE usuarios SET acertou_quiz = 1 WHERE user_id = ?', (user_id,))
                    await db.commit()
                await message.answer("✅ Acertou! Agora escolha qual jogo você quer acompanhar ao vivo: \n1 - LoL \n2 - CS \n3 - Valorant")
            else:
                pergunta_quiz = "Qual jogador da FURIA é conhecido como 'Rei da Mira'? \n1 - KSCERATO \n2 - yuurih \n3 - FalleN"
                await message.answer(f"❌ Errou! Vamos tentar de novo! {pergunta_quiz}")

    elif user[2] == 0:
        if len(text) == 11 and text.isdigit():
            async with aiosqlite.connect(DB_FILE) as db:
                await db.execute('UPDATE usuarios SET cpf = ?, participou = 1 WHERE user_id = ?', (text, user_id))
                await db.commit()
            await message.answer("🔥 Cadastro confirmado! Você já está participando do sorteio! Agora confira mais sobre a FURIA abaixo: 👇")
            await enviar_menu(message)
        else:
            await message.answer("Por favor, envie um CPF válido (apenas números, 11 dígitos).")

    elif user[3] == '':
        if text.lower() in ['lol', 'cs', 'valorant']:
            async with aiosqlite.connect(DB_FILE) as db:
                await db.execute('UPDATE usuarios SET jogo_desejado = ? WHERE user_id = ?', (text.capitalize(), user_id))
                await db.commit()
            await message.answer(f"✅ Você escolheu {text.capitalize()} para acompanhar ao vivo! Agora, envie seu CPF para completar o cadastro.")
        else:
            await message.answer("Por favor, escolha um jogo válido: LoL, CS ou Valorant.")

    else:
        response = await get_chatgpt_response(text)
        await message.answer(response)

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
