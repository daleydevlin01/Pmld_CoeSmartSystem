import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Mengatur logging untuk debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Token bot dari BotFather (ganti dengan token asli Anda)
TOKEN = "7800146869:AAEiybVVnXZkQ7qdIevIOi0cqeyOY2NYmPU"  # Ganti dengan token bot Anda

# Direktori untuk menyimpan gambar lokasi
UPLOAD_DIR = './uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Dictionary untuk menyimpan nama pengguna
user_names = {}

# Teks peraturan ruangan
RULES_TEXT = """
Berikut adalah peraturan yang harus diperhatikan:
1. Pengunjung yang menggunakan ruang/lab harus diketahui oleh Teknisi Lab.
2. Pengunjung wajib menjaga kebersihan ruang/lab.
3. Sampah harus dibuang di tempat sampah yang sudah disediakan di luar ruang/lab.
4. Pengunjung wajib merapikan alat setelah digunakan.
5. Pengunjung tidak diperkenankan membawa alat keluar ruang/lab tanpa izin dari Teknisi dan Koordinator Lab.
6. Pengunjung wajib menjaga inventaris lab.
7. Jika terjadi kerusakan atau kehilangan alat, pengunjung wajib melapor kepada Teknisi dan Koordinator Lab.
"""

# Handler untuk perintah /start
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_names.pop(chat_id, None)  # Menghapus nama pengguna sebelumnya jika ada
    context.bot.send_message(
        chat_id,
        "Halo, selamat datang di bot CoE Smart System. Silakan masukkan nama pengguna Anda:"
    )

# Handler pesan untuk menangkap nama pengguna
def handle_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_name = update.message.text
    user_names[chat_id] = user_name  # Menyimpan nama pengguna berdasarkan ID chat

    context.bot.send_message(
        chat_id,
        f"Halo {user_name}, silakan pilih menu yang Anda inginkan:"
    )
    show_main_menu(update, context)

# Tampilkan menu utama
def show_main_menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Alat", callback_data='tools_menu')],
        [InlineKeyboardButton("Tata Tertib", callback_data='rules')],
        [InlineKeyboardButton("Pemesanan Ruangan", callback_data='room_booking')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id,
        "Pilih menu utama:",
        reply_markup=reply_markup
    )

# Handler untuk pemilihan menu utama
def handle_main_menu_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == 'room_booking':
        show_room_booking_menu(update, context)
    elif data == 'rules':
        show_rules_menu(update, context)
    elif data == 'tools_menu':
        show_tools_menu(update, context)

# Tampilkan menu pemesanan ruangan
def show_room_booking_menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Link Form Peminjaman", url='http://ugm.id/formpenggunaanruanganSmartSystem')],  # Ganti dengan link form peminjaman Anda
        [InlineKeyboardButton("Kembali ke Menu Utama", callback_data='back_to_main')],
        [InlineKeyboardButton("Selesai", callback_data='finish')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id,
        "Menu Pemesanan Ruangan. Silakan pilih:",
        reply_markup=reply_markup
    )


# Tampilkan menu peraturan
def show_rules_menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Kembali ke Menu Utama", callback_data='back_to_main')],
        [InlineKeyboardButton("Keluar", callback_data='exit')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id,
        RULES_TEXT,
        reply_markup=reply_markup
    )

# Tampilkan menu peralatan
def show_tools_menu(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Mesin Brushing", callback_data='brushing_milling')],
        [InlineKeyboardButton("Mesin Through Hole Plating", callback_data='thp')],
        [InlineKeyboardButton("Unit paparan vakum", callback_data='hellas')],
        [InlineKeyboardButton("Mesin Splash Etching", callback_data='splash_etching')],
        [InlineKeyboardButton("Unit Pengolahan Air Limbah", callback_data='wwtu')],
        [InlineKeyboardButton("Mesin Laminasi Film Kering", callback_data='dfl')],
        [InlineKeyboardButton("Kembali ke Menu Utama", callback_data='back_to_main')],
        [InlineKeyboardButton("Selesai", callback_data='finish')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id,
        "Pilih peralatan yang ingin Anda pelajari:",
        reply_markup=reply_markup
    )

# Handler untuk pemilihan peralatan
def handle_tool_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == 'back_to_main':
        show_main_menu(update, context)
        return
    elif data == 'finish' or data == 'exit':
        query.edit_message_text("Terima kasih telah menggunakan bot ini. Anda dapat memulai kembali dengan mengetik /start.")
        return

    keyboard = [
        [InlineKeyboardButton("Deskripsi Alat", callback_data=f"{data}_description")],
        [InlineKeyboardButton("Panduan Alat (YouTube)", callback_data=f"{data}_guide")],
        [InlineKeyboardButton("Lokasi Alat (Peta)", callback_data=f"{data}_location")],
        [InlineKeyboardButton("Kembali ke Daftar Alat", callback_data='tools_menu')],
        [InlineKeyboardButton("Selesai", callback_data='finish')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        f"Anda memilih {data.replace('_', ' ').title()}. Pilih opsi di bawah ini:",
        reply_markup=reply_markup
    )

# Handler untuk deskripsi, panduan, dan lokasi
def handle_option_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    # Deskripsi alat
    descriptions = {
        'brushing_milling_description': (
            "Mesin penyikat profesional yang dirancang untuk digunakan dalam produksi seri kecil dan laboratorium. Mesin penyikat pemrosesan basah berkualitas tinggi untuk produksi PCB dengan harga murah adalah pilihan yang tepat! Buktinya adalah Bungard RBM 300. Adik perempuan kami yang lebih kecil dari RBM 402 ini dibuat sekecil mungkin tetapi tidak pada kualitas, ketahanan, dan detail presisi tinggi.\n"
            " \n"
            " \n"            
            "Fitur:\n"
            "a. RBM 300 memiliki sikat berosilasi dengan perangkat penggantian cepat\n"
            "b. Frekuensi osilasi dan kecepatan transportasi adalah variabel stepless\n"
            "c. Penyesuaian ketinggian paralel. Berbeda dengan penyesuaian ketinggian satu sisi, Anda akan memperoleh hasil penyikatan yang merata dalam jangka panjang hanya dengan penyesuaian ketinggian paralel dua sisi\n"
            "d. Mesin dilengkapi dengan sikat akhir yang digunakan sebelum laminasi. Tersedia berbagai sikat"
        ),
        'thp_description': (
            "Mesin dari seri COMPACTA ini dirancang untuk memenuhi tuntutan metalisasi langsung profesional. Mesin ini dapat menangani papan hingga 210 x 300 mm² dan memiliki 5 tangki perawatan (pembersihan - pra-celup - katalis - intensifier - tangki cadangan) dan satu tangki pelapisan galvanik, "
            "Dua tangki perawatan dikontrol secara termostatik dan dilengkapi dengan pemanas teflon. Pergerakan bak pada semua tangki dilakukan dengan motor DCgear. Kecepatan langkah adalah variabel stepless. "
            "Tangki pelapisan galvanik dilengkapi dengan injeksi udara terintegrasi dan penyearah teregulasi stepless. Volt- dan Amperemeter menunjukkan nilai listrik saat ini. Penekanan khusus diberikan pada teknik pembilasan yang unik. Pembilasan kaskade ganda dan pembilasan semprot, yang terakhir diaktifkan melalui sakelar kaki dan katup magnetik, merupakan bagian integral dari COMPACTA 30. "
        ),
        'hellas_description': (
            "Unit pemaparan vakum presisi untuk pemaparan kontak dua sisi dari bahan dasar yang dilapisi foto, film cetak, dan banyak lagi"
            "Dengan unit vakum Hellas, Anda dapat memproses semua produk fotosensitif dengan sensitivitas spektral dalam rentang UV dekat (360-400nm)"
            "Produk-produk ini terutama PCB yang dilapisi foto positif atau negatif, pelat cetak yang terbuat dari nilon, aluminium, baja, dan diazo serta film transfer."
            " \n"
            " \n"
            "Fitur:\n"
            "- 2 x 6 tabung UV superaktinik, masing-masing 18 W\n"
            "- Reflektor khusus untuk undercut minimum\n"
            "- Tampilan emisi cahaya analog\n"
            "- Permukaan paparan bawah dari kaca khusus 8 mm\n"
            "- Area paparan atas dari foil mylar terstruktur dalam bingkai yang kokoh dan area kerja 570 x 300 mm yang cocok untuk PCB garis halus\n"
            "- Vakum bebas perawatan (>60%) dengan tampilan pengukur, peringkat kontinu 1380 l/jam\n"
            "- Timer digital 1 detik - 9 menit 59 detik dengan hitungan mundur, pengaturan ulang otomatis, dan beeper\n"
            "- Kipas pendingin internal memungkinkan proses pemaparan atau pemanggangan dalam waktu lama"
        ),
        'splash_etching_description': (
            "Mesin splash Etching, dikenal sebagai Splash Center/Splash Center XL, adalah mesin etsa laboratorium dengan pembilasan "
            "statis dan semprot, tangki pengembang terintegrasi, tangki cadangan untuk pelapisan kimia, dan pengering tekan. Cocok untuk PCB dua sisi, "
            "dengan alur kerja yang ergonomis dan bersih serta hambatan kimia yang rendah. Alur kerja umum:\n\n"
            "1. Tangki 1 (kompartemen semprot) untuk etsa\n"
            "2. Tangki 2 dan 3 untuk pembilasan\n"
            "3. Tangki 4 (dengan pompa sentrifugal) untuk pengembangan\n"
            "4. Tangki 5 untuk pelapisan\n\n"
            " \n"
            " \n"
            "Fitur:\n"
            "- 5 katup bola untuk menguras semua tangki, penutup terlindungi dari depan\n"
            "- Semua tangki dengan tutup\n"
            "- Baki tetes terintegrasi untuk semua tangki, dipasang sekitar 120 mm di atas tanah\n"
            "- Pengering peras mekanis terintegrasi"
        ),
        'wwtu_description': (
            "Sistem pengolahan air limbah modern ini. Ionex merupakan pabrik modern dan kompak untuk mengolah air bilasan yang berasal dari mesin etsa atau pelapisan lubang tembus dari laboratorium PCB."
            " Menawarkan 4 varian dasar, yang berbeda dalam hal keluaran air bilasan dan kapasitas ion. Tipe A dan B dilengkapi dengan pra-filter katun, dua kolom kation, dan kolom netralisasi pH. Tipe KA dan KB memiliki tiga kolom pertukaran ion."
            " Kolom kation berwarna merah, ketika diisi dengan ion besi dan biru/hijau, ketika diisi dengan ion tembaga. Pemuatan kolom anion dapat diuji dengan mengukur konduktansi air yang dibersihkan."
            " \n"
            " \n"
            " Fitur:\n"
            "1. Untuk pasca perawatan etsa dan air bilas galvanik\n"
            "2. Penghapusan padatan dan semua logam berat dengan kebutuhan oksigen kimia\n"
            "3. Bak penampung terpadu berkapasitas 110 l (A/KA) atau 220 l (B/KB) untuk menampung air bilasan\n"
            "4. Perubahan warna yang signifikan saat diisi dengan logam\n"
            "5. Penanganan dan pengoperasian yang mudah serta regenerasi resin pertukaran ion oleh pemasok atau pengguna dengan biaya rendah\n"
            "6. Netralisasi pH tambahan dan pembuangan ke saluran pembuangan"
        ),
        'dfl_description': (
            "Dry Film Laminator adalah laminator film kering yang dibuat khusus untuk perusahaan kecil, sekolah, departemen penelitian dan pengembangan."
            " Semua laminasi komersial untuk pembuatan PCB dan teknik etsa cetakan dapat diproses. Berkat kontrol tekanan yang dapat disesuaikan dan kecepatan laminasi yang dapat disesuaikan, aplikasi masker solder juga dapat dilakukan tanpa masalah."
            " Mesin ini juga digunakan dengan sangat sukses dalam bidang aplikasi lain seperti WAFER MASKING dan produksi SMT STENCIL atau PENGERJAAN LOGAM."
            " \n"
            " \n"
            " Fitur:\n"
            "- Pemasangan rol resist mudah dan cepat dengan semua diameter kumparan umum\n"
            "- Meja saluran masuk yang dapat dilepas untuk memudahkan akses ke gulungan resistan bawah\n"
            "- Kecepatan laminasi dapat disesuaikan tanpa batas\n"
            "- Rol laminasi berpemanas listrik dengan distribusi suhu yang seragam\n"
            "- Rol pengangkut terpisah untuk pengangkutan laminasi tanpa kusut\n"
            "- Pengaturan digital dan pembacaan suhu laminasi\n"
            "- Tekanan laminasi yang dapat disesuaikan secara manual\n"
            "- Untuk semua film kering umum yang resistan dengan diameter inti 3 dan 5 inci\n"
            "- Cocok untuk aplikasi masker solder"
        ),
    }

    # Link panduan YouTube
    youtube_links = {
        'brushing_milling_guide': 'https://youtu.be/LF5Ssw5IagI?si=i5Y_wf22s8Up2ZUJ',
        'thp_guide': 'https://youtu.be/Ex6f8f0ONDY?si=k7drPhmzKJ13jX7G',
        'hellas_guide': 'https://youtu.be/tHK9b2zqM_s?feature=shared',
        'splash_etching_guide': 'https://youtu.be/4r6z7Hq61ic?si=9gPJwwRnrKSEOBg9',
        'wwtu_guide': 'https://youtu.be/-usoUvP31x8?feature=shared',
        'dfl_guide': 'https://youtu.be/-EeWD3-y4N4?si=SoEH5o3nIxWnO6P7'
    }

    # File gambar lokasi
    image_files = {
        'brushing_milling_location': os.path.join(UPLOAD_DIR, 'brushing_milling.png'),
        'thp_location': os.path.join(UPLOAD_DIR, 'thp.png'),
        'hellas_location': os.path.join(UPLOAD_DIR, 'hellas.png'),
        'splash_etching_location': os.path.join(UPLOAD_DIR, 'splash_etching.png'),
        'wwtu_location': os.path.join(UPLOAD_DIR, 'wwtu.png'),
        'dfl_location': os.path.join(UPLOAD_DIR, 'dfl.png')
    }

    chat_id = query.message.chat_id

    # Kirim deskripsi alat
    if data.endswith('_description'):
        description = descriptions.get(data)
        if description:
            context.bot.send_message(chat_id, description)
        else:
            context.bot.send_message(chat_id, "Deskripsi untuk alat ini belum tersedia.")

    # Kirim link panduan YouTube
    elif data.endswith('_guide'):
        link = youtube_links.get(data)
        if link:
            context.bot.send_message(chat_id, f"Panduan YouTube dapat dilihat di sini: {link}")
        else:
            context.bot.send_message(chat_id, "Panduan untuk alat ini belum tersedia.")

    # Kirim gambar lokasi alat
    elif data.endswith('_location'):
        image_path = image_files.get(data)
        if image_path and os.path.exists(image_path):
            context.bot.send_photo(chat_id, open(image_path, 'rb'))
        else:
            context.bot.send_message(chat_id, "Gambar lokasi untuk alat ini belum tersedia.")

# Fungsi utama
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(CallbackQueryHandler(handle_main_menu_selection, pattern='^(rules|room_booking|tools_menu)$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_tool_selection, pattern='^(brushing_milling|thp|hellas|splash_etching|wwtu|dfl|back_to_main|finish|exit)$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_option_selection, pattern='.*_(description|guide|location)$'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()