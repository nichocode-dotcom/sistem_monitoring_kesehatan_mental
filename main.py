import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
from database import MoodTracker, SmartJournal, HabitManager, AnalyticsDashboard

# --- WARNA TEMA (CALMING PALETTE) ---
COLOR_PRIMARY = "#00695C"    # Teal Gelap
COLOR_ACCENT = "#4DB6AC"     # Teal Terang
COLOR_BG = "#E0F7FA"         # Cyan Sangat Muda
COLOR_WHITE = "#FFFFFF"
COLOR_TEXT = "#263238"

class SerenityLogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SerenityLog - Personal Mental Health Tracker")
        self.root.geometry("1000x650")
        self.root.configure(bg=COLOR_BG)

        # Inisialisasi Logika
        self.logic_mood = MoodTracker()
        self.logic_journal = SmartJournal()
        self.logic_habit = HabitManager()
        self.logic_dashboard = AnalyticsDashboard()

        self.setup_styles()
        self.setup_ui()
        self.show_dashboard() # Halaman pertama

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style Frame
        style.configure("Card.TFrame", background=COLOR_WHITE, relief="flat", borderwidth=0)
        style.configure("Main.TFrame", background=COLOR_BG)
        
        # Style Labels
        style.configure("H1.TLabel", background=COLOR_WHITE, foreground=COLOR_PRIMARY, font=("Segoe UI", 18, "bold"))
        style.configure("H2.TLabel", background=COLOR_WHITE, foreground=COLOR_TEXT, font=("Segoe UI", 12))
        style.configure("Body.TLabel", background=COLOR_WHITE, foreground=COLOR_TEXT, font=("Segoe UI", 10))
        
        # Style Buttons
        style.configure("Nav.TButton", font=("Segoe UI", 11), background=COLOR_PRIMARY, foreground=COLOR_WHITE, padding=10)
        style.map("Nav.TButton", background=[('active', COLOR_ACCENT)])
        
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), background=COLOR_ACCENT, foreground=COLOR_WHITE)

    def setup_ui(self):
        # 1. SIDEBAR NAVIGASI
        self.sidebar = tk.Frame(self.root, bg=COLOR_PRIMARY, width=220)
        self.sidebar.pack(side="left", fill="y")
        
        # Logo Area
        tk.Label(self.sidebar, text="SerenityLog", bg=COLOR_PRIMARY, fg=COLOR_WHITE, font=("Segoe UI", 20, "bold")).pack(pady=(30, 40))
        
        # Menu Buttons
        self.btn_dash = tk.Button(self.sidebar, text="🏠 Dashboard", command=self.show_dashboard, bg=COLOR_PRIMARY, fg=COLOR_WHITE, bd=0, font=("Segoe UI", 11), anchor="w", padx=20, pady=10, activebackground=COLOR_ACCENT)
        self.btn_dash.pack(fill="x")
        
        self.btn_mood = tk.Button(self.sidebar, text="🙂 Mood Check-In", command=self.show_mood, bg=COLOR_PRIMARY, fg=COLOR_WHITE, bd=0, font=("Segoe UI", 11), anchor="w", padx=20, pady=10, activebackground=COLOR_ACCENT)
        self.btn_mood.pack(fill="x")
        
        self.btn_jurnal = tk.Button(self.sidebar, text="📝 Jurnal Harian", command=self.show_jurnal, bg=COLOR_PRIMARY, fg=COLOR_WHITE, bd=0, font=("Segoe UI", 11), anchor="w", padx=20, pady=10, activebackground=COLOR_ACCENT)
        self.btn_jurnal.pack(fill="x")
        
        self.btn_habit = tk.Button(self.sidebar, text="✅ Habit Tracker", command=self.show_habit, bg=COLOR_PRIMARY, fg=COLOR_WHITE, bd=0, font=("Segoe UI", 11), anchor="w", padx=20, pady=10, activebackground=COLOR_ACCENT)
        self.btn_habit.pack(fill="x")

        # 2. MAIN CONTENT AREA
        self.content_area = ttk.Frame(self.root, style="Main.TFrame")
        self.content_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # --- HALAMAN 1: DASHBOARD ---
    def show_dashboard(self):
        self.clear_content()
        
        # Card Header
        header = ttk.Frame(self.content_area, style="Card.TFrame", padding=20)
        header.pack(fill="x", pady=(0, 20))
        ttk.Label(header, text="Dashboard Kesehatan Mental", style="H1.TLabel").pack(anchor="w")
        
        # Quote Hari Ini
        quote_data = self.logic_dashboard.get_daily_quote()
        quote_text = f'"{quote_data[0]}" - {quote_data[1]}' if quote_data else "Tetap semangat!"
        ttk.Label(header, text=quote_text, style="Body.TLabel", font=("Segoe UI", 11, "italic")).pack(anchor="w", pady=(5,0))

        # Mental Battery Section
        battery_frame = ttk.Frame(self.content_area, style="Card.TFrame", padding=30)
        battery_frame.pack(fill="both", expand=True)
        
        level = self.logic_dashboard.hitung_mental_battery()
        
        ttk.Label(battery_frame, text="🔋 Baterai Mental Hari Ini", style="H2.TLabel").pack(pady=(0, 15))
        
        # Visual Progress Bar Custom
        canvas = tk.Canvas(battery_frame, width=400, height=40, bg="#ecf0f1", highlightthickness=0)
        canvas.pack(pady=10)
        
        # Warna bar berubah sesuai level
        bar_color = "#e74c3c" if level < 30 else "#f1c40f" if level < 70 else "#2ecc71"
        canvas.create_rectangle(0, 0, 400 * (level/100), 40, fill=bar_color, width=0)
        
        ttk.Label(battery_frame, text=f"{int(level)}%", style="H1.TLabel", font=("Segoe UI", 24, "bold")).pack()
        
        status_msg = "Butuh istirahat, jangan memaksakan diri." if level < 40 else "Kondisi stabil, pertahankan!" if level < 80 else "Kondisi prima! Hari yang produktif."
        ttk.Label(battery_frame, text=status_msg, style="Body.TLabel").pack(pady=5)

    # --- HALAMAN 2: MOOD TRACKER ---
    def show_mood(self):
        self.clear_content()
        card = ttk.Frame(self.content_area, style="Card.TFrame", padding=30)
        card.pack(fill="both", expand=True)
        
        ttk.Label(card, text="Bagaimana perasaanmu saat ini?", style="H1.TLabel").pack(pady=(0, 20))
        
        # Grid Emosi
        frame_emoji = tk.Frame(card, bg=COLOR_WHITE)
        frame_emoji.pack(pady=10)
        
        self.var_emosi = tk.IntVar()
        emosi_list = self.logic_mood.get_daftar_emosi()
        
        for i, (eid, nama, ikon, skor) in enumerate(emosi_list):
            btn = tk.Radiobutton(frame_emoji, text=f"{ikon}\n{nama}", variable=self.var_emosi, value=eid, 
                                 indicatoron=0, width=12, height=3, bg="#f1f2f6", selectcolor=COLOR_ACCENT, font=("Segoe UI", 10))
            btn.grid(row=0, column=i, padx=5)

        ttk.Label(card, text="Apa aktivitas utamamu?", style="H2.TLabel").pack(pady=(20, 10))
        
        # Input Aktivitas (Text sederhana untuk prototype)
        self.ent_aktivitas = ttk.Entry(card, width=50, font=("Segoe UI", 11))
        self.ent_aktivitas.pack(ipady=5)
        ttk.Label(card, text="(Contoh: Tugas Kuliah, Main Game, Kurang Tidur)", style="Body.TLabel", foreground="grey").pack()

        def simpan():
            if not self.var_emosi.get():
                messagebox.showwarning("Info", "Pilih emosi dulu ya!")
                return
            res = self.logic_mood.simpan_mood(self.var_emosi.get(), self.ent_aktivitas.get())
            messagebox.showinfo("Sukses", res)
            self.show_dashboard()

        ttk.Button(card, text="SIMPAN MOOD", style="Action.TButton", command=simpan).pack(pady=30)

    # --- HALAMAN 3: JURNAL ---
    def show_jurnal(self):
        self.clear_content()
        card = ttk.Frame(self.content_area, style="Card.TFrame", padding=30)
        card.pack(fill="both", expand=True)
        
        ttk.Label(card, text="Ruang Bercerita", style="H1.TLabel").pack(anchor="w")
        
        # Prompt Otomatis
        prompt = self.logic_journal.get_prompt_acak()
        lbl_prompt = tk.Label(card, text=f"💡 Ide Tulisan: {prompt}", bg="#FFF3E0", fg="#E65100", padx=10, pady=5, font=("Segoe UI", 10, "italic"))
        lbl_prompt.pack(fill="x", pady=15)
        
        ttk.Label(card, text="Judul:", style="Body.TLabel").pack(anchor="w")
        ent_judul = ttk.Entry(card, width=60, font=("Segoe UI", 11))
        ent_judul.pack(fill="x", pady=(5, 15))
        
        ttk.Label(card, text="Isi Hati:", style="Body.TLabel").pack(anchor="w")
        txt_isi = scrolledtext.ScrolledText(card, height=10, font=("Segoe UI", 11), bd=1, relief="solid")
        txt_isi.pack(fill="both", expand=True, pady=5)
        
        def simpan():
            judul = ent_judul.get()
            isi = txt_isi.get("1.0", tk.END).strip()
            if not isi:
                messagebox.showwarning("Kosong", "Tulis sesuatu dulu yuk!")
                return
            
            res = self.logic_journal.simpan_jurnal(judul, isi)
            messagebox.showinfo("Tersimpan", res)
            self.show_dashboard()

        ttk.Button(card, text="SIMPAN CERITA", style="Action.TButton", command=simpan).pack(pady=10, anchor="e")

    # --- HALAMAN 4: HABIT ---
    def show_habit(self):
        self.clear_content()
        card = ttk.Frame(self.content_area, style="Card.TFrame", padding=30)
        card.pack(fill="both", expand=True)
        
        ttk.Label(card, text="Target Kebiasaan Hari Ini", style="H1.TLabel").pack(pady=(0, 20))
        
        # List Habit dengan Checkbox
        habits = self.logic_habit.get_habits_harian() # [(id, nama, target, status), ...]
        
        if not habits:
            ttk.Label(card, text="Belum ada data habit di Master Data.", style="Body.TLabel").pack()
            return

        self.check_vars = {} 
        
        for h in habits:
            h_id, nama, target, status = h
            var = tk.IntVar(value=status)
            self.check_vars[h_id] = var
            
            # Frame per baris agar rapi
            row = tk.Frame(card, bg=COLOR_WHITE)
            row.pack(fill="x", pady=5)
            
            # Logic update langsung saat di-klik
            def on_click(hid=h_id, v=var):
                self.logic_habit.toggle_habit(hid, v.get())

            cb = tk.Checkbutton(row, text=f"{nama} ({target})", variable=var, command=on_click, 
                                bg=COLOR_WHITE, font=("Segoe UI", 12), activebackground=COLOR_WHITE)
            cb.pack(side="left")

        ttk.Label(card, text="*Perubahan disimpan otomatis saat diklik.", style="Body.TLabel", foreground="grey").pack(pady=20)
        ttk.Button(card, text="Kembali ke Dashboard", command=self.show_dashboard).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SerenityLogApp(root)
    root.mainloop()