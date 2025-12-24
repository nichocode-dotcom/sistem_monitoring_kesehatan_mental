import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="serenity_log.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.seed_master_data()

    def create_tables(self):
        # --- 5 DATA MASTER (REFERENSI) ---
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS master_emosi (
            id_emosi INTEGER PRIMARY KEY AUTOINCREMENT, 
            nama TEXT, 
            ikon TEXT, 
            skor INTEGER)""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS master_aktivitas (
            id_aktivitas INTEGER PRIMARY KEY AUTOINCREMENT, 
            nama TEXT, 
            kategori TEXT)""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS master_habit (
            id_habit INTEGER PRIMARY KEY AUTOINCREMENT, 
            nama TEXT, 
            target_harian TEXT)""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS master_template (
            id_template INTEGER PRIMARY KEY AUTOINCREMENT, 
            pertanyaan TEXT)""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS master_quotes (
            id_quote INTEGER PRIMARY KEY AUTOINCREMENT, 
            isi TEXT, 
            penulis TEXT)""")

        # --- 3 DATA TRANSAKSI (KEGIATAN HARIAN) ---
        # 1. Transaksi Mood
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS trans_mood (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            tanggal TEXT, 
            jam TEXT, 
            id_emosi INTEGER, 
            aktivitas_note TEXT)""")

        # 2. Transaksi Jurnal
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS trans_jurnal (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            tanggal TEXT, 
            judul TEXT, 
            isi_teks TEXT, 
            skor_analisis INTEGER)""")

        # 3. Transaksi Habit Log
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS trans_habit (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            tanggal TEXT, 
            id_habit INTEGER, 
            status INTEGER)""")
        
        self.conn.commit()

    def seed_master_data(self):
        # Isi data awal jika tabel kosong
        self.cursor.execute("SELECT count(*) FROM master_emosi")
        if self.cursor.fetchone()[0] == 0:
            emosi = [
                ('Sangat Bahagia', '🤩', 5), ('Senang', '🙂', 3), ('Biasa Aja', '😐', 0),
                ('Cemas/Gelisah', '😟', -3), ('Sangat Sedih', '😭', -5), ('Marah', '😡', -4)
            ]
            self.cursor.executemany("INSERT INTO master_emosi (nama, ikon, skor) VALUES (?,?,?)", emosi)

            aktivitas = [('Tidur Cukup', 'Fisik'), ('Olahraga', 'Fisik'), ('Tugas Kuliah', 'Kerja'), 
                         ('Main Sosmed', 'Hiburan'), ('Bertengkar', 'Sosial'), ('Jalan-jalan', 'Hiburan')]
            self.cursor.executemany("INSERT INTO master_aktivitas (nama, kategori) VALUES (?,?)", aktivitas)

            habits = [('Minum Air 2L', '2 Liter'), ('Meditasi', '10 Menit'), ('Tidur < Jam 11', '8 Jam'), ('Baca Buku', '15 Menit')]
            self.cursor.executemany("INSERT INTO master_habit (nama, target_harian) VALUES (?,?)", habits)

            templates = [('Apa yang kamu syukuri hari ini?',), ('Apa hal berat yang berhasil kamu lewati?',), ('Bagaimana perasaanmu saat bangun tidur?',)]
            self.cursor.executemany("INSERT INTO master_template (pertanyaan) VALUES (?)", templates)

            quotes = [('Kamu lebih kuat dari yang kamu kira.', 'Unknown'), ('Istirahat itu produktif.', 'Serenity'), ('Satu langkah kecil tetaplah langkah maju.', 'Anonim')]
            self.cursor.executemany("INSERT INTO master_quotes (isi, penulis) VALUES (?,?)", quotes)
            
            self.conn.commit()

# --- PARENT CLASS FITUR ---
class FiturKesehatan:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.conn = self.db_manager.conn
        self.cursor = self.db_manager.cursor

# --- CHILD CLASSES (LOGIKA APLIKASI) ---

class MoodTracker(FiturKesehatan):
    def get_daftar_emosi(self):
        self.cursor.execute("SELECT * FROM master_emosi")
        return self.cursor.fetchall()
    
    def get_daftar_aktivitas(self):
        self.cursor.execute("SELECT * FROM master_aktivitas")
        return self.cursor.fetchall()

    def simpan_mood(self, id_emosi, note_aktivitas):
        tgl = datetime.now().strftime("%Y-%m-%d")
        jam = datetime.now().strftime("%H:%M")
        try:
            self.cursor.execute("INSERT INTO trans_mood (tanggal, jam, id_emosi, aktivitas_note) VALUES (?,?,?,?)",
                                (tgl, jam, id_emosi, note_aktivitas))
            self.conn.commit()
            return "Mood berhasil dicatat!"
        except Exception as e: return str(e)

class SmartJournal(FiturKesehatan):
    def get_prompt_acak(self):
        self.cursor.execute("SELECT pertanyaan FROM master_template ORDER BY RANDOM() LIMIT 1")
        res = self.cursor.fetchone()
        return res[0] if res else "Tulis apa saja..."

    def analisis_sentimen_sederhana(self, teks):
        # Logika analisis kata kunci
        kata_positif = ['senang', 'bersyukur', 'bahagia', 'tenang', 'semangat', 'berhasil', 'bagus', 'cinta', 'suka']
        kata_negatif = ['sedih', 'marah', 'kecewa', 'takut', 'cemas', 'gagal', 'benci', 'lelah', 'capek', 'sakit']
        
        skor = 0
        words = teks.lower().split()
        for w in words:
            if w in kata_positif: skor += 2
            if w in kata_negatif: skor -= 2
        
        # Batasi skor antara -5 sampai 5
        return max(min(skor, 5), -5)

    def simpan_jurnal(self, judul, isi):
        tgl = datetime.now().strftime("%Y-%m-%d")
        # Panggil fungsi analisis internal (Private logic simulation)
        skor = self.analisis_sentimen_sederhana(isi)
        
        self.cursor.execute("INSERT INTO trans_jurnal (tanggal, judul, isi_teks, skor_analisis) VALUES (?,?,?,?)",
                            (tgl, judul, isi, skor))
        self.conn.commit()
        return f"Jurnal Tersimpan. Skor Mood Terdeteksi: {skor}"

class HabitManager(FiturKesehatan):
    def get_habits_harian(self):
        # Ambil semua habit master
        self.cursor.execute("SELECT * FROM master_habit")
        master = self.cursor.fetchall()
        
        # Cek status hari ini
        tgl = datetime.now().strftime("%Y-%m-%d")
        hasil = []
        for h in master: # h = (id, nama, target)
            self.cursor.execute("SELECT status FROM trans_habit WHERE tanggal=? AND id_habit=?", (tgl, h[0]))
            stat = self.cursor.fetchone()
            is_done = stat[0] if stat else 0
            hasil.append((h[0], h[1], h[2], is_done)) # Return: ID, Nama, Target, Status(0/1)
        return hasil

    def toggle_habit(self, id_habit, nilai_baru):
        tgl = datetime.now().strftime("%Y-%m-%d")
        # Cek apakah sudah ada row hari ini
        self.cursor.execute("SELECT id FROM trans_habit WHERE tanggal=? AND id_habit=?", (tgl, id_habit))
        ada = self.cursor.fetchone()
        
        if ada:
            self.cursor.execute("UPDATE trans_habit SET status=? WHERE id=?", (nilai_baru, ada[0]))
        else:
            self.cursor.execute("INSERT INTO trans_habit (tanggal, id_habit, status) VALUES (?,?,?)", (tgl, id_habit, nilai_baru))
        self.conn.commit()

class AnalyticsDashboard(FiturKesehatan):
    def get_daily_quote(self):
        self.cursor.execute("SELECT isi, penulis FROM master_quotes ORDER BY RANDOM() LIMIT 1")
        return self.cursor.fetchone()

    def hitung_mental_battery(self):
        tgl = datetime.now().strftime("%Y-%m-%d")
        
        # 1. Rata-rata Mood (-5 s.d 5)
        self.cursor.execute("""
            SELECT AVG(m.skor) FROM trans_mood t 
            JOIN master_emosi m ON t.id_emosi = m.id_emosi 
            WHERE t.tanggal = ?""", (tgl,))
        res_mood = self.cursor.fetchone()[0]
        score_mood = res_mood if res_mood else 0
        
        # 2. Rata-rata Jurnal (-5 s.d 5)
        self.cursor.execute("SELECT AVG(skor_analisis) FROM trans_jurnal WHERE tanggal = ?", (tgl,))
        res_jurnal = self.cursor.fetchone()[0]
        score_jurnal = res_jurnal if res_jurnal else 0
        
        # 3. Persentase Habit (0 s.d 100 -> dikonversi ke skala 5)
        habits = HabitManager().get_habits_harian()
        if habits:
            done = sum([1 for h in habits if h[3] == 1])
            persen = done / len(habits) # 0.0 s.d 1.0
            score_habit = (persen * 10) - 5 # Konversi jadi range -5 s.d 5
        else:
            score_habit = 0
            
        # Rumus Baterai Mental (0 - 100%)
        # Rata-rata dari ketiga komponen, dipetakan ke 0-100
        avg_total = (score_mood + score_jurnal + score_habit) / 3
        # Mapping: -5 = 0%, 0 = 50%, +5 = 100%
        baterai = (avg_total + 5) * 10 
        
        return max(min(baterai, 100), 0) # Pastikan 0-100