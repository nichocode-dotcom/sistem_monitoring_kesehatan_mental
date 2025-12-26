import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="serinity_fix.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.seed_master_data()
        self.seed_users()

    def create_tables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS master_user (id_user INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS master_emosi (
            id_emosi INTEGER PRIMARY KEY AUTOINCREMENT, nama TEXT, ikon TEXT, skor INTEGER)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS master_habit (
            id_habit INTEGER PRIMARY KEY AUTOINCREMENT, nama TEXT, target_harian TEXT)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS master_template (
            id_template INTEGER PRIMARY KEY AUTOINCREMENT, pertanyaan TEXT)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS master_quotes (
            id_quote INTEGER PRIMARY KEY AUTOINCREMENT, 
            isi TEXT, 
            penulis TEXT,
            kategori TEXT)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS trans_mood (
            id INTEGER PRIMARY KEY AUTOINCREMENT, id_user INTEGER, tanggal TEXT, jam TEXT, id_emosi INTEGER, aktivitas_note TEXT)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS trans_jurnal (
            id INTEGER PRIMARY KEY AUTOINCREMENT, id_user INTEGER, tanggal TEXT, judul TEXT, isi_teks TEXT, skor_analisis REAL, rating_user INTEGER)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS trans_habit (
            id INTEGER PRIMARY KEY AUTOINCREMENT, id_user INTEGER, tanggal TEXT, id_habit INTEGER, status INTEGER)""")
        
        self.conn.commit()
        
    def seed_users(self):
        users = [
            ("n", "1"),
            ("fadhlur", "456"),
            ("salsa", "789")
        ]

        for u in users:
            self.cursor.execute(
                "SELECT 1 FROM master_user WHERE username=?",
                (u[0],)
            )
            if not self.cursor.fetchone():
                self.cursor.execute(
                    "INSERT INTO master_user (username, password) VALUES (?, ?)",
                    u
                )

        self.conn.commit()
        
    def check_login(self, username, password):
        self.cursor.execute(
            "SELECT id_user FROM master_user WHERE username=? AND password=?",
            (username, password)
        )
        return self.cursor.fetchone()

    def seed_master_data(self):
        self.cursor.execute("SELECT count(*) FROM master_emosi")
        if self.cursor.fetchone()[0] == 0:
            emosi = [('Sangat Bahagia', '🤩', 5), ('Senang', '🙂', 3), ('Biasa Aja', '😐', 0),
                     ('Cemas/Gelisah', '😟', -3), ('Sangat Sedih', '😭', -5), ('Marah', '😡', -4)]
            self.cursor.executemany("INSERT INTO master_emosi (nama, ikon, skor) VALUES (?,?,?)", emosi)

            # aktivitas = [('Tidur Cukup', 'Fisik'), ('Olahraga', 'Fisik'), ('Tugas Kuliah', 'Kerja'), 
            #              ('Main Sosmed', 'Hiburan'), ('Bertengkar', 'Sosial'), ('Jalan-jalan', 'Hiburan')]
            # self.cursor.executemany("INSERT INTO master_aktivitas (nama, kategori) VALUES (?,?)", aktivitas)

            habits = [('Minum Air 2L', '2 Liter'), ('Meditasi', '10 Menit'), ('Waktu Tidur', '7-8 Jam'), 
                     ('Baca Buku', '15 Menit'), ('Jogging Pagi', '30 Menit'),
                     ('Makan Buah', '1 Porsi'), ('Makan Sayur', '1 Porsi'), ('Minum Susu', '1-2 Gelas'), ('No Sosmed', '1 Jam'), ('Skincare', 'Malam')]
            self.cursor.executemany("INSERT INTO master_habit (nama, target_harian) VALUES (?,?)", habits)

            templates = [
                ('Apa yang kamu syukuri hari ini?',), 
                ('Apa hal berat yang berhasil kamu lewati?',), 
                ('Bagaimana perasaanmu saat bangun tidur?',),  # <--- Dulu lupa koma disini
                ('Ceritakan momen menyenangkan yang kamu alami hari ini.',),
                ('Apa tantangan terbesar yang kamu hadapi hari ini?',), 
                ('Siapa orang yang membuat harimu lebih baik?',), # <--- Dulu lupa koma disini
                ('Apa hal kecil yang membuatmu tersenyum hari ini?',), 
                ('Bagaimana kamu merawat dirimu sendiri hari ini?',),
                ('Apa tujuan utama yang ingin kamu capai minggu ini?',), 
                ('Ceritakan sesuatu yang baru yang kamu pelajari hari ini.',),
                ('Apa yang bisa kamu lakukan besok untuk membuat harimu lebih baik?',), 
                ('Bagaimana kamu mengatasi stres hari ini?',),
                ('Apa hal positif yang bisa kamu ambil dari pengalaman sulit hari ini?',), 
                ('Ceritakan tentang momen kebahagiaan sederhana yang kamu alami.',),
                ('Apa satu hal yang ingin kamu ubah tentang rutinitas harianmu?',)
            ]
            
            self.cursor.executemany("INSERT INTO master_template (pertanyaan) VALUES (?)", templates)

            quotes = [
                # Support (Untuk Baterai < 40%)
                ('Tidak apa-apa untuk istirahat sejenak. Dunia bisa menunggu.', 'ZenMood', 'support'),
                ('Menangis itu valid. Keluarkan saja.', 'ZenMood', 'support'),
                ('Kamu lebih kuat dari yang kamu kira, tapi sekarang waktunya pulih.', 'ZenMood', 'support'),
                ('Hari ini berat, dan itu fakta. Kamu tidak lemah karenanya.', 'ZenMood', 'support'),
                ('Berhenti sebentar bukan berarti menyerah.', 'ZenMood', 'support'),
                ('Kalau napas terasa sesak, pelan-pelan saja. Tidak perlu buru-buru sembuh.', 'ZenMood', 'support'),
                ('Kalau hari ini cuma sanggup bertahan, itu sudah cukup.', 'ZenMood', 'support'),
                ('Ada luka yang nggak minta disembuhkan cepat-cepat.', 'ZenMood', 'support'),
                ('Kamu capek bukan karena lemah, tapi karena terlalu lama kuat.', 'ZenMood', 'support'),
                ('Diam juga bentuk bertahan hidup.', 'ZenMood', 'support'),
                ('Hari ini kamu boleh nggak punya jawaban.', 'ZenMood', 'support'),

                # Motivasi (Untuk Baterai 40% - 70%)
                ('Satu langkah kecil tetaplah langkah maju.', 'Serinity', 'motivasi'),
                ('Fokus pada apa yang bisa kamu kendalikan.', 'Serinity', 'motivasi'),
                ('Kesulitan hari ini adalah kekuatan di masa depan.', 'Serinity', 'motivasi'),
                ('Kamu tidak harus sempurna untuk tetap melangkah.', 'Serinity', 'motivasi'),
                ('Progress pelan lebih baik daripada diam di tempat.', 'Serinity', 'motivasi'),
                ('Tidak semua hari harus produktif, tapi hari ini masih berarti.', 'Serinity', 'motivasi'),
                ('Pelan bukan berarti mundur.', 'Serinity', 'motivasi'),
                ('Kamu masih berjalan, meski sambil ragu.', 'Serinity', 'motivasi'),
                ('Nggak apa-apa kalau langkahmu kecil, asal tetap milikmu.', 'Serinity', 'motivasi'),
                ('Hari ini mungkin biasa, tapi kamu tetap hadir.', 'Serinity', 'motivasi'),
                ('Kamu belajar, bahkan saat merasa tersesat.', 'Serinity', 'motivasi'),

                # Apresiasi (Untuk Baterai > 70%)
                ('Pertahankan energimu, kamu melakukan hal hebat!', 'Stain', 'apresiasi'),
                ('Jangan lupa berbagi senyum hari ini.', 'Stain', 'apresiasi'),
                ('Nikmati momen ini, kamu pantas mendapatkannya.', 'Stain', 'apresiasi'),
                ('Kamu datang sejauh ini, itu bukan kebetulan.', 'Stain', 'apresiasi'),
                ('Energi kamu hari ini hangat. Gunakan dengan bijak.', 'Stain', 'apresiasi'),
                ('Bangga itu boleh. Hari ini kamu layak merasa begitu.', 'Stain', 'apresiasi'),
                ('Tenangmu hari ini terasa nyata.', 'Stain', 'apresiasi'),
                ('Kamu nggak sekadar bertahan—kamu hidup.', 'Stain', 'apresiasi'),
                ('Ada cahaya kecil di caramu menjalani hari.', 'Stain', 'apresiasi'),
                ('Energi ini hasil dari proses panjang. Hormati itu.', 'Stain', 'apresiasi'),
                ('Hari ini kamu selaras dengan dirimu sendiri.', 'Stain', 'apresiasi')
            ]

            self.cursor.executemany("INSERT INTO master_quotes (isi, penulis, kategori) VALUES (?,?,?)", quotes)
            self.conn.commit()

class FiturKesehatan:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.conn = self.db_manager.conn
        self.cursor = self.db_manager.cursor

class MoodTracker(FiturKesehatan):
    def get_daftar_emosi(self):
        self.cursor.execute("SELECT * FROM master_emosi")
        return self.cursor.fetchall()
    
    # def get_daftar_aktivitas(self):
    #     self.cursor.execute("SELECT * FROM master_aktivitas")
    #     return self.cursor.fetchall()

    def simpan_mood(self, id_user, id_emosi, note_aktivitas):
        tgl = datetime.now().strftime("%Y-%m-%d")
        jam = datetime.now().strftime("%H:%M")
        try:
            self.cursor.execute("INSERT INTO trans_mood (id_user, tanggal, jam, id_emosi, aktivitas_note) VALUES (?,?,?,?,?)",
                                (id_user, tgl, jam, id_emosi, note_aktivitas))
            self.conn.commit()
            return "Mood berhasil dicatat!"
        except Exception as e: 
            return str(e)

class SmartJournal(FiturKesehatan):
    def get_prompt_acak(self):
        self.cursor.execute("SELECT pertanyaan FROM master_template ORDER BY RANDOM() LIMIT 1")
        res = self.cursor.fetchone()
        return res[0] if res else "Tulis apa saja..."

    def analisis_sentimen_sederhana(self, teks):
        kata_positif = ['senang', 'bersyukur', 'bahagia', 'tenang', 'semangat', 'berhasil', 'bagus', 'cinta', 'suka',
                        'gembira', 'riang', 'puas', 'bangga', 'lega', 'nyaman', 
                        'kagum', 'hebat', 'keren', 'damai', 'ceria', 'antusias', 
                        'takjub', 'terpesona', 'sayang', 'menikmati', 'seru', 'asik',
                        'berharap', 'semoga', 'ingin', 'berdoa', 'impian', 'cita-cita', 
                        'yakin', 'niat', 'optimis', 'percaya']
        
        kata_negatif = ['sedih', 'marah', 'kecewa', 'takut', 'cemas', 
                        'gagal', 'benci', 'lelah', 'capek', 'sakit',
                        'kesal', 'jengkel', 'dongkol', 'murung', 'gelisah', 'panik', 
                        'frustrasi', 'depresi', 'hancur', 'menderita', 'sengsara', 
                        'hampa', 'sepi', 'dendam', 'muak', 'jijik', 'nyesek',
                        'bingung', 'bimbang', 'ragu', 'gundah', 'resah', 'dilema', 
                        'tersesat', 'buntu', 'pasrah', 'overthinking',
                        'minder', 'malu', 'bodoh', 'jelek', 'iri', 'beban', 'payah',
                        'rindu', 'kangen', 'kepikiran', 'terbayang', 'homesick', 
                        'kesepian', 'kenangan', 'teringat']
        skor = 0
        words = teks.lower().split()
        for w in words:
            if w in kata_positif: skor += 2
            if w in kata_negatif: skor -= 2
        return max(min(skor, 5), -5)

    def simpan_jurnal(self, id_user, judul, isi, rating_user=None):
        """Simpan jurnal dengan rating user opsional"""
        tgl = datetime.now().strftime("%Y-%m-%d")
        
        
        
        # 1. Analisis sentimen otomatis (skor AI)
        skor_ai = self.analisis_sentimen_sederhana(isi)
        
        # 2. Jika ada rating user, konversi dari skala 1-5 ke -5 sampai +5
        if rating_user and 1 <= rating_user <= 5:
            # Konversi: 1 -> -5, 3 -> 0, 5 -> +5
            skor_user = (rating_user - 3) * 2.5
            # Gabungkan skor AI dan rating user (rata-rata)
            skor_final = (skor_ai + skor_user) / 2
        else:
            skor_final = skor_ai
        
        # 3. Simpan ke database (termasuk rating_user jika ada)
        self.cursor.execute("""
            INSERT INTO trans_jurnal (id_user, tanggal, judul, isi_teks, skor_analisis, rating_user) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_user, tgl, judul, isi, skor_final, rating_user))
        
        self.conn.commit()
    
        
        # # 4. Return pesan sukses
        if rating_user:
            return f"Jurnal tersimpan! "
        else:
            return f"Jurnal tersimpan! Skor analisis: {skor_final:.1f}"

    def get_jurnal_harian(self, id_user):
        tgl = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("SELECT judul, isi_teks FROM trans_jurnal WHERE tanggal=? AND id_user=? ORDER BY id DESC", 
                           (tgl, id_user))
        return self.cursor.fetchall()

class HabitManager(FiturKesehatan):
    def get_habits_harian(self, id_user):
        self.cursor.execute("SELECT * FROM master_habit")
        master = self.cursor.fetchall()
        tgl = datetime.now().strftime("%Y-%m-%d")
        hasil = []
        for h in master: 
            self.cursor.execute("SELECT status FROM trans_habit WHERE tanggal=? AND id_habit=? AND id_user=?", 
                               (tgl, h[0], id_user))
            stat = self.cursor.fetchone()
            is_done = stat[0] if stat else 0
            hasil.append((h[0], h[1], h[2], is_done))
        return hasil

    def toggle_habit(self, id_user, id_habit, nilai_baru):
        tgl = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("SELECT id FROM trans_habit WHERE tanggal=? AND id_habit=? AND id_user=?", 
                           (tgl, id_habit, id_user))
        ada = self.cursor.fetchone()
        if ada:
            self.cursor.execute("UPDATE trans_habit SET status=? WHERE id=?", (nilai_baru, ada[0]))
        else:
            self.cursor.execute("INSERT INTO trans_habit (id_user, tanggal, id_habit, status) VALUES (?,?,?,?)", 
                               (id_user, tgl, id_habit, nilai_baru))
        self.conn.commit()

class AnalyticsDashboard(FiturKesehatan):
    def get_contextual_quote(self, battery_level):
        if battery_level < 40:
            kategori = 'support'
        elif battery_level < 75:
            kategori = 'motivasi'
        else:
            kategori = 'apresiasi'
            
        self.cursor.execute("SELECT isi, penulis FROM master_quotes WHERE kategori=? ORDER BY RANDOM() LIMIT 1", (kategori,))
        res = self.cursor.fetchone()
        return res if res else ("Tetap semangat!", "System")
    
    def get_habits_harian(self, id_user):
        """Ambil habits untuk user tertentu"""
        self.cursor.execute("SELECT * FROM master_habit")
        master = self.cursor.fetchall()
        tgl = datetime.now().strftime("%Y-%m-%d")
        hasil = []
        for h in master: 
            self.cursor.execute("SELECT status FROM trans_habit WHERE tanggal=? AND id_habit=? AND id_user=?", 
                               (tgl, h[0], id_user))
            stat = self.cursor.fetchone()
            is_done = stat[0] if stat else 0
            hasil.append((h[0], h[1], h[2], is_done))
        return hasil
    
    def hitung_mental_battery(self, id_user):
        tgl = datetime.now().strftime("%Y-%m-%d")
        
        # 1. Rata-rata Mood
        self.cursor.execute("""
            SELECT AVG(m.skor) FROM trans_mood t 
            JOIN master_emosi m ON t.id_emosi = m.id_emosi 
            WHERE t.tanggal = ? AND t.id_user = ?""", (tgl, id_user,))
        res_mood = self.cursor.fetchone()[0]
        score_mood = res_mood if res_mood is not None else None
        
        # 2. Rata-rata Jurnal
        self.cursor.execute("SELECT skor_analisis, rating_user FROM trans_jurnal WHERE tanggal = ? AND id_user = ?", 
                           (tgl, id_user))
        jurnal_data = self.cursor.fetchall()
        
        if jurnal_data:
            total_skor = 0
            for skor_ai, rating_user in jurnal_data:
                if rating_user is not None and 1 <= rating_user <= 5:
                    skor_user = (rating_user - 3) * 2.5
                    skor_jurnal = (skor_ai + skor_user) / 2
                else:
                    skor_jurnal = skor_ai
                total_skor += skor_jurnal
            
            score_jurnal = total_skor / len(jurnal_data)
        else:
            score_jurnal = None
        
        # 3. Habit
        habits = self.get_habits_harian(id_user)
        
        score_habit = None
        
        if habits:
            total_habit = len(habits)
            done_habit = sum([1 for h in habits if h[3] == 1])
            
            if total_habit > 0:
                persen = done_habit / total_habit
                score_habit = (persen * 10) - 5

        # --- LOGIKA PENENTUAN 0% ---
        if (score_mood is None and score_jurnal is None and score_habit is None):
            return 0 
        
        komponen = []
        if score_mood is not None: 
            komponen.append(score_mood)
        if score_jurnal is not None: 
            komponen.append(score_jurnal)
        if score_habit is not None: 
            komponen.append(score_habit)
        
        if not komponen:
            return 0
            
        avg_total = sum(komponen) / len(komponen)
        baterai = (avg_total + 5) * 10 
        
        return int(max(min(baterai, 100), 0))