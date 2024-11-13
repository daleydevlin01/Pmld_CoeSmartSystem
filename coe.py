import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Mengatur logging untuk debug
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Token dari BotFather (ganti dengan token asli Anda)
TOKEN = "7800146869:AAEiybVVnXZkQ7qdIevIOi0cqeyOY2NYmPU"  # Ganti dengan token bot Anda

# Direktori untuk menyimpan gambar denah
UPLOAD_DIR = './uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Variabel untuk menyimpan nama pengguna
user_names = {}

# Tata tertib ruangan
RULES_TEXT = """
Berikut adalah tata tertib yang perlu diperhatikan:
1. Pengunjung yang menggunakan ruangan/peralatan laboratorium harus dengan sepengetahuan Laboran.
2. Pengunjung ruangan/laboratorium wajib menjaga kebersihan ruangan/laboratorium.
3. Membuang sampah harus pada tempat sampah yang sudah disediakan di luar ruangan/laboratorium.
4. Pengunjung ruangan/laboratorium wajib merapikan kembali peralatan yang telah selesai digunakan.
5. Pengunjung ruangan/laboratorium dilarang membawa keluar peralatan tanpa izin dari Laboran dan Koordinator Laboratorium.
6. Pengunjung ruangan/laboratorium wajib menjaga keamanan inventaris ruangan/laboratorium.
7. Jika terjadi kerusakan dan kehilangan peralatan, pengunjung wajib melapor ke Laboran dan Koordinator Laboratorium untuk ditindaklanjuti.
"""

# Fungsi untuk menangani /start
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_names.pop(chat_id, None)  # Hapus nama pengguna jika ada sebelumnya
    context.bot.send_message(
        chat_id,
        "Halo, selamat datang di bot CoE Smart System. Silakan masukkan nama pengguna Anda:"
    )

# Fungsi untuk menangani nama pengguna
def handle_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_name = update.message.text
    user_names[chat_id] = user_name  # Simpan nama berdasarkan chat ID

    context.bot.send_message(
        chat_id,
        f"Halo {user_name}, silakan pilih menu yang Anda inginkan:"
    )
    show_main_menu(update, context)

# Fungsi untuk menampilkan menu utama
def show_main_menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Alat", callback_data='tools_menu')],
        [InlineKeyboardButton("Tata Tertib", callback_data='rules')],
        [InlineKeyboardButton("Peminjaman Ruang", callback_data='room_booking')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id,
        "Pilih menu utama:",
        reply_markup=reply_markup
    )

# Fungsi untuk menangani pilihan menu utama
def handle_main_menu_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == 'room_booking':
        query.edit_message_text(
            "Silakan isi form untuk peminjaman ruang di sini: [Form Peminjaman](http://ugm.id/formpenggunaanruanganSmartSystem)",
            parse_mode='Markdown'
        )
    elif data == 'rules':
        query.edit_message_text(RULES_TEXT)
    elif data == 'tools_menu':
        show_tools_menu(update, context)

# Fungsi untuk menampilkan menu alat
def show_tools_menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Photoplotter Machine", callback_data='photoplotter')],
        [InlineKeyboardButton("Brushing Machine", callback_data='brushing_milling')],
        [InlineKeyboardButton("Through Hole Plating Machine", callback_data='thp')],
        [InlineKeyboardButton("Spray Etching Machine", callback_data='spray_etching')],
        [InlineKeyboardButton("Splash Etching Machine", callback_data='splash_etching')],
        [InlineKeyboardButton("Waste Water Treatment Unit", callback_data='wwtu')],
        [InlineKeyboardButton("Dry Film Laminator Machine", callback_data='dfl')],
        [InlineKeyboardButton("Kembali ke Menu Utama", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id,
        "Pilih alat yang ingin Anda pelajari:",
        reply_markup=reply_markup
    )

# Fungsi untuk menangani pilihan alat
def handle_tool_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == 'back_to_main':
        show_main_menu(update, context)

    keyboard = [
        [InlineKeyboardButton("Deskripsi Alat", callback_data=f"{data}_description")],
        [InlineKeyboardButton("Panduan Alat (YouTube)", callback_data=f"{data}_guide")],
        [InlineKeyboardButton("Lokasi Alat (Denah)", callback_data=f"{data}_location")],
        [InlineKeyboardButton("Kembali ke Daftar Alat", callback_data='tools_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        f"Anda memilih {data.replace('_', ' ').title()}. Pilih opsi di bawah ini:",
        reply_markup=reply_markup
    )

# Fungsi untuk menangani deskripsi, panduan, dan denah alat
def handle_option_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    # Deskripsi alat
    descriptions = {
        'photoplotter_description': 'Photoplotter digunakan untuk mencetak desain PCB pada film dengan akurasi tinggi.',
        'brushing_milling_description': 'Brushing Machine membersihkan permukaan PCB sebelum proses selanjutnya.',
        'thp_description': 'Through Hole Plating Machine melapisi lubang PCB agar dapat menghantarkan listrik antar lapisan.',
        'spray_etching_description': 'Spray Etching Machine menghilangkan tembaga berlebih dari PCB dengan larutan kimia.',
        'splash_etching_description': 'Splash Etching Machine etsa PCB dengan menyemprotkan larutan kimia.',
        'wwtu_description': 'Waste Water Treatment Unit mengolah limbah cair dari proses fabrikasi PCB.',
        'dfl_description': 'Dry Film Laminator melapisi PCB dengan film kering sebelum eksposur UV.'
    }

    # Link panduan video YouTube
    youtube_links = {
        'photoplotter_guide': 'https://www.youtube.com/watch?v=link_photoplotter',
        'brushing_milling_guide': 'https://www.youtube.com/watch?v=link_brushing_milling',
        'thp_guide': 'https://www.youtube.com/watch?v=link_thp',
        'spray_etching_guide': 'https://www.youtube.com/watch?v=link_spray_etching',
        'splash_etching_guide': 'https://www.youtube.com/watch?v=link_splash_etching',
        'wwtu_guide': 'https://www.youtube.com/watch?v=link_wwtu',
        'dfl_guide': 'https://www.youtube.com/watch?v=link_dfl'
    }

    # Gambar denah lokasi alat
    image_files = {
        'photoplotter_location': os.path.join(UPLOAD_DIR, 'photoplotter.png'),
        'brushing_milling_location': os.path.join(UPLOAD_DIR, 'brushing_milling.png'),
        'thp_location': os.path.join(UPLOAD_DIR, 'thp.png'),
        'spray_etching_location': os.path.join(UPLOAD_DIR, 'spray_etching.png'),
        'splash_etching_location': os.path.join(UPLOAD_DIR, 'splash_etching.png'),
        'wwtu_location': os.path.join(UPLOAD_DIR, 'wwtu.png'),
        'dfl_location': os.path.join(UPLOAD_DIR, 'dfl.png')
    }

    chat_id = query.message.chat_id

    # Mengirim Deskripsi Alat
    if data.endswith('_description'):
        description = descriptions.get(data)
        if description:
            context.bot.send_message(chat_id, description)
        else:
            context.bot.send_message(chat_id, "Deskripsi untuk alat ini tidak tersedia.")

    # Mengirim Panduan Video YouTube
    elif data.endswith('_guide'):
        youtube_link = youtube_links.get(data)
        if youtube_link:
            context.bot.send_message(chat_id, f"Panduan Alat: {youtube_link}")
        else:
            context.bot.send_message(chat_id, "Panduan YouTube untuk alat ini tidak tersedia.")

    # Mengirim Denah Lokasi Alat
    elif data.endswith('_location'):
        image_file = image_files.get(data)
        if image_file and os.path.exists(image_file):
            context.bot.send_photo(chat_id, photo=open(image_file, 'rb'))
        else:
            context.bot.send_message(chat_id, "Lokasi alat ini tidak tersedia.")

# Fungsi utama untuk menjalankan bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Menambahkan handler untuk command dan callback
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(CallbackQueryHandler(handle_main_menu_selection, pattern='^(tools_menu|rules|room_booking)$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_tool_selection, pattern='^(photoplotter|brushing_milling|thp|spray_etching|splash_etching|wwtu|dfl)$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_option_selection))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
