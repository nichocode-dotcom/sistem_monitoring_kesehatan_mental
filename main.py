import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from database import MoodTracker, SmartJournal, HabitManager, AnalyticsDashboard

MOOD_THEMES = {
    "Marah (Zen Forest)": {
        "bg": "#E8F8F5", "sidebar": "#148F77", "card": "#FFFFFF", 
        "text": "#148F77", "btn": "#48C9B0", "btn_hover": "#1ABC9C",
        "description": "Warna hijau ini hadir sebagai ruang napas untuk meredam gemuruh di hatimu, mengajakmu pulang ke ketenangan alam saat energimu berada di titik terendah."
    },
    "Cemas (Serenity Blue)": {
        "bg": "#EBF5FB", "sidebar": "#2874A6", "card": "#FFFFFF", 
        "text": "#2874A6", "btn": "#5DADE2", "btn_hover": "#3498DB",
        "description": "Biru ini adalah jangkar bagi pikiranmu yang berisik, memberikan rasa aman dan stabilitas untuk menenangkan jiwamu yang sedang dilanda ketidakpastian."
    },
    "Morning Mist (Gray)": { 
        "bg": "#F8F9F9", "sidebar": "#455A64", "card": "#FFFFFF", 
        "text": "#37474F", "btn": "#9BA9B0", "btn_hover": "#7F9096",
        "description": "Warna merah muda yang lembut ini adalah simbol kasih sayang untuk dirimu sendiri, meyakinkanmu bahwa setiap luka sedang berproses menjadi kekuatan baru yang lebih indah."
    },
    "Sedih (Warm Sunset)": {
        "bg": "#FEF5E7", "sidebar": "#AF601A", "card": "#FFFFFF", 
        "text": "#AF601A", "btn": "#F39C12", "btn_hover": "#D68910",
        "description": "Warna jingga yang hangat ini adalah pelukan visual yang meyakinkanmu bahwa di balik rasa lelah dan sedih, selalu ada harapan baru yang akan terbit esok hari."
    },
    "Pulih (Healing Rose)": {
        "bg": "#FFF0F5", "sidebar": "#DB7093", "card": "#FFFFFF",    
        "text": "#C71585", "btn": "#FFB6C1", "btn_hover": "#FF69B4",
        "description": "Warna merah muda yang lembut ini adalah simbol kasih sayang untuk dirimu sendiri, meyakinkanmu bahwa setiap luka sedang berproses menjadi kekuatan baru yang lebih indah."
    },
    "Senang (Joyful Berry)": {
        "bg": "#F5EEF8", "sidebar": "#9B59B6", "card": "#FFFFFF", 
        "text": "#633974", "btn": "#BF98CF", "btn_hover": "#B587C9",
        "description": "Ungu berry yang ceria ini adalah perayaan atas cahaya di dalam dirimu, memancarkan energi kreatif dan kepuasan karena kamu telah berhasil merawat dirimu dengan baik."
    }
}
class ZenMoodApp(ctk.CTk):
    def __init__(self):
        super().__init__() 
        self.title("ZenMood - Personal Mental Health Tracker")
        self.after(0, lambda: self.state('zoomed'))
        
        self.logic_dash = AnalyticsDashboard()
        self.logic_journal = SmartJournal()
        self.logic_mood = MoodTracker()
        self.logic_habit = HabitManager()
        
        self.db = self.logic_dash.db_manager
        self.mental_battery = 0
        self.current_user_id = None
        self.current_user = None
        
        # Setup Container Utama (Kosong)
        self.main_container = ctk.CTkFrame(self, corner_radius=0)
        self.main_container.pack(fill="both", expand=True)
        
        # Mulai dengan Halaman Login
        self.show_login()

    # ================= 2. HELPER (BANTUAN) =================
    # --- [FUNGSI UPDATE STATUS BATERAI & TEMA TERINTEGRASI] ---
    def refresh_app_state(self):
        """Menghitung baterai berdasarkan user yang login dan menentukan tema warna"""
        
        # 1. Ambil data baterai (hanya jika user sudah login)
        if hasattr(self, 'current_user_id') and self.current_user_id is not None:
            current_battery = self.logic_dash.hitung_mental_battery(self.current_user_id)
        else:
            current_battery = 0 

        if current_battery == 0:
            theme_key = "Morning Mist (Gray)"
        elif current_battery <= 20: 
            theme_key = "Marah (Zen Forest)"
        elif current_battery <= 40: 
            theme_key = "Cemas (Serenity Blue)"
        elif current_battery <= 60: 
            theme_key = "Pulih (Healing Rose)"
        elif current_battery <= 80: 
            theme_key = "Sedih (Warm Sunset)"
        else: 
            theme_key = "Senang (Joyful Berry)"
        # 3. Simpan ke variabel state aplikasi
        self.mental_battery = current_battery
        self.theme_name = theme_key
        self.theme = MOOD_THEMES[self.theme_name]
        
        # 4. Ambil Quote (Gunakan try-except agar aman jika DB quotes bermasalah)
        try:
            self.current_quote = self.logic_dash.get_contextual_quote(self.mental_battery)
        except:
            self.current_quote = ("Tetap melangkah, hari ini milikmu", "ZenMood")

    def apply_current_theme(self):
        # 1. Background Utama
        self.configure(fg_color=self.theme["bg"])
        self.main_container.configure(fg_color=self.theme["bg"])
        
        # 2. Sidebar Background
        if hasattr(self, 'sidebar'):
            self.sidebar.configure(fg_color=self.theme["sidebar"])
            
            # 3. Update Warna Tombol Navigasi (Dashboard - Habit)
            if hasattr(self, 'nav_buttons'):
                for btn in self.nav_buttons:
                    btn.configure(
                        fg_color=self.theme["btn_hover"], 
                        hover_color=self.theme["btn"]
                    )
            
            # 4. [FIX] Update Tombol Keluar
            if hasattr(self, 'btn_logout'):
                 self.btn_logout.configure(
                     # fg_color biarkan transparent atau btn_hover (sesuai selera)
                     fg_color=self.theme["btn_hover"], 
                     # hover_color ambil dari tema (agar serasi dengan tombol lain)
                     hover_color=self.theme["btn"]
                 )

    def clear_screen(self):
        """Hapus semua widget layar utama (dipakai saat login/logout)"""
        for widget in self.main_container.winfo_children(): 
            widget.destroy()
        # Hapus referensi sidebar jika ada
        if hasattr(self, 'sidebar'):
            del self.sidebar

    def clear_content_frame(self):
        """Hapus isi konten kanan saja (dipakai saat navigasi menu)"""
        if hasattr(self, 'content_area'):
            for widget in self.content_area.winfo_children():
                widget.destroy()

    # ================= 3. AUTHENTICATION (LOGIN/LOGOUT) =================
    def show_login(self):
        self.clear_screen()
        self.refresh_app_state() 
        self.apply_current_theme()

        login_container = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15, width=900, height=550, border_width=0)
        login_container.place(relx=0.5, rely=0.5, anchor="center")
        login_container.pack_propagate(False)

        # KIRI: Branding
        left_brand_frame = ctk.CTkFrame(login_container, fg_color=self.theme["sidebar"], corner_radius=0, width=400)
        left_brand_frame.pack(side="left", fill="y")
        left_brand_frame.pack_propagate(False)
        
        ctk.CTkFrame(left_brand_frame, fg_color=self.theme["sidebar"], width=50, corner_radius=0).pack(side="right", fill="y")

        ctk.CTkLabel(left_brand_frame, text="ZENMOOD🌿\nOPTIMIZE\nYOUR\nMOOD", 
                     font=("Century Gothic", 35, "bold"), text_color="white", justify="left").place(relx=0.1, rely=0.3)
        ctk.CTkLabel(left_brand_frame, text="Tenang Fokus Terkendali", 
                     font=("Century Gothic", 14), text_color="white").place(relx=0.1, rely=0.6)

        # KANAN: Form
        right_form_frame = ctk.CTkFrame(login_container, fg_color="white", corner_radius=0)
        right_form_frame.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(right_form_frame, text="Selamat Datang", 
                     font=("Century Gothic", 28, "bold"), text_color=self.theme["text"]).pack(pady=(80, 5), padx=100, anchor="w")
        ctk.CTkLabel(right_form_frame, text="Silakan login akun pengguna", 
                     font=("Century Gothic", 13), text_color=self.theme["text"]).pack(pady=(0, 40), padx=100, anchor="w")
        
        ctk.CTkLabel(right_form_frame, text="USERNAME", font=("Arial", 10, "bold"), text_color=self.theme["text"]).pack(padx=100, anchor="w")
        self.ent_user = ctk.CTkEntry(right_form_frame, width=350, height=40, corner_radius=20, 
                                     fg_color="#F2F4F4", text_color="black", border_width=1, border_color="#cbd5e0")
        self.ent_user.pack(pady=(5, 20), padx=100, anchor="w")

        ctk.CTkLabel(right_form_frame, text="PASSWORD", font=("Arial", 10, "bold"), text_color=self.theme["text"]).pack(padx=100, anchor="w")
        self.ent_pass = ctk.CTkEntry(right_form_frame, width=350, height=40, corner_radius=20, show="*", 
                                     fg_color="#F2F4F4", text_color="black", border_width=1, border_color="#cbd5e0")
        self.ent_pass.pack(pady=(5, 30), padx=100, anchor="w")
        
        btn_login = ctk.CTkButton(right_form_frame, text="LOGIN", command=self.process_login, 
                                  fg_color=self.theme["sidebar"], hover_color=self.theme["btn_hover"], 
                                  height=45, width=350, corner_radius=20, font=("Arial", 13, "bold"))
        btn_login.pack(pady=30, padx=100, anchor="w")

        ctk.CTkLabel(right_form_frame, text="v1.0 • ZenMood Production", font=("Arial", 10), text_color="#D5DBDB").pack(side="bottom", pady=20)

    def process_login(self):
        username = self.ent_user.get().strip()
        password = self.ent_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Gagal", "Username dan password harus diisi.")
            return

        user = self.db.check_login(username, password)
        if user:
            self.current_user_id = user[0]
            self.current_user = username
            self.setup_main_ui()
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah.")

    def logout(self):
        self.current_user = None
        self.current_user_id = None
        self.show_login()

    def setup_main_ui(self):
        """Membangun kerangka Sidebar dan Content Area"""
        self.clear_screen()
        self.refresh_app_state()
        
        # A. SIDEBAR
        self.sidebar = ctk.CTkFrame(self.main_container, width=240, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(self.sidebar, text="ZenMood🌿", font=("Century Gothic", 22, "bold"), text_color="white").pack(pady=40)
        
        self.nav_buttons = [] # [FIX] List untuk menyimpan tombol agar bisa diubah warnanya nanti
        
        menu_items = [
            ("🏠 Dashboard", self.show_dashboard), 
            ("🙂 Mood Track", self.show_mood), 
            ("📝 Journaling", self.show_jurnal), 
            ("✅ Habit Log", self.show_habit)
        ]

        for text, cmd in menu_items:
            # Menggunakan warna btn_hover dari tema agar serasi
            btn = ctk.CTkButton(self.sidebar, text=text, corner_radius=15, command=cmd, 
                                font=("Century Gothic", 14, "bold"),
                                fg_color=self.theme["btn"], 
                                text_color="white", anchor="w", height=50, 
                                hover_color=self.theme["btn_hover"])
            btn.pack(fill="x", padx=30, pady=5)
            self.nav_buttons.append(btn)  # Simpan referensi tombol

        # Spacer untuk mendorong tombol Keluar ke bawah
        ctk.CTkLabel(self.sidebar, text="").pack(fill="both", expand=True)

        self.btn_logout = ctk.CTkButton(self.sidebar, text="Logout", command=self.logout, 
                                   fg_color=self.theme["btn"], text_color="white", 
                                   hover_color=self.theme["btn_hover"], height=50, 
                                   font=("Arial", 12, "bold"), corner_radius=15)
        self.btn_logout.pack(fill="x", padx=30, pady=20)
        
        # B. CONTENT AREA
        self.content_area = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_area.pack(side="right", fill="both", expand=True, padx=30, pady=20)
        
        # [PENTING] Panggil ini TERAKHIR agar semua warna tombol ter-update sesuai tema saat ini
        self.apply_current_theme() 
        
        # C. TAMPILKAN DASHBOARD AWAL
        self.show_dashboard()

# ================= 5. FITUR: DASHBOARD (NO EMPTY SPACE)    =================
    def show_dashboard(self):
        self.clear_content_frame()
        self.refresh_app_state()
        self.apply_current_theme()

        # --- [A. BAGIAN HEADER / BINGKAI ATAS] ---
        header_bingkai = ctk.CTkFrame(self.content_area, fg_color=self.theme["btn"], corner_radius=20)
        header_bingkai.pack(fill="x", pady=(0, 15), ipady=10)

        salam_frame = ctk.CTkFrame(header_bingkai, fg_color="transparent")
        salam_frame.pack(side="left", padx=25, pady=10)
        
        ctk.CTkLabel(salam_frame, text=f"Hai, {self.current_user}!", 
                     font=("Century Gothic", 28, "bold"), 
                     text_color="white").pack(anchor="w")
        
        ctk.CTkLabel(salam_frame, text="Selamat datang di ZenMood, semoga harimu menyenangkan!", 
                     font=("Century Gothic", 14), 
                     text_color="white").pack(anchor="w")
        
        date_container = ctk.CTkFrame(header_bingkai, fg_color="transparent")
        date_container.pack(side="right", padx=25, pady=10)
        
        ctk.CTkLabel(date_container, text=f"📅",
                     font=("Segoe UI Emoji", 24),
                     text_color="white").pack(side="left", padx=(0,8), pady=(0,3))
        
        tgl_str = datetime.now().strftime("%A, %d %B %Y")
        ctk.CTkLabel(date_container, text=tgl_str, 
                     font=("Century Gothic", 14, "bold"), 
                     text_color="white").pack(side="left", padx=0)

        # --- [B. BAGIAN TENGAH: STATISTIK (FULL FILL)] ---
        # Menggunakan expand=True agar container ini mengambil sisa ruang yang ada
        main_stats_container = ctk.CTkFrame(self.content_area, fg_color="transparent")
        main_stats_container.pack(fill="both", expand=True)

        # -- KOLOM KIRI (Baterai & Habit) --
        left_column = ctk.CTkFrame(main_stats_container, fg_color="transparent")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # 1. Card Baterai Mental (Tinggi disesuaikan agar proporsional)
        card_bat = ctk.CTkFrame(left_column, fg_color=self.theme["card"], corner_radius=25)
        card_bat.pack(fill="both", expand=True, pady=(0, 10), ipady=10)
        
        ctk.CTkLabel(card_bat, text="🔋 Kondisi Mental", 
                     font=("Arial", 15, "bold"), text_color=self.theme["text"]).pack(padx=25, pady=(15,5), anchor="w")
        
        prog_bat = ctk.CTkProgressBar(card_bat, height=25, corner_radius=10, 
                                      progress_color=self.theme["btn"], fg_color="#F0F0F0")
        prog_bat.set(self.mental_battery / 100)
        prog_bat.pack(padx=25, pady=10, fill="x")
        
        ctk.CTkLabel(card_bat, text=f"Persentase Saat Ini: {int(self.mental_battery)}%", 
                     font=("Arial", 14, "bold"), text_color=self.theme["text"]).pack(padx=25, anchor="w")

        ctk.CTkLabel(card_bat, text=f"Tema: {self.theme_name}", 
                    font=("Arial", 10, "italic"), wraplength=350, justify="left" ,text_color=self.theme["text"]).pack(padx=25, anchor="w")

        # 2. Label Deskripsi Tema (dengan wrap)
        theme_desc = ctk.CTkLabel(card_bat,
                                text=self.theme["description"],  # PERBAIKAN: dari self.theme['description']
                                font=("Arial", 12, "italic"),
                                text_color=self.theme["text"],
                                wraplength=350, 
                                justify="left")
        theme_desc.pack(padx=25, anchor="w", pady=(0, 15))

        # 2. Card Habit Progress (Kotak Habit Sekarang Mengisi Sisa Ruang Bawah)
        habits = self.logic_habit.get_habits_harian(self.current_user_id)
        total_habit = len(habits)
        done_habit = sum([1 for h in habits if h[3] == 1])
        progress_val = done_habit / total_habit if total_habit > 0 else 0

        card_hab = ctk.CTkFrame(left_column, fg_color=self.theme["btn"], corner_radius=25)
        card_hab.pack(fill="both", expand=True, ipady=10)

        ctk.CTkLabel(card_hab, text="✅ Progres Pencapaian Habit Anda Hari Ini!", 
                     font=("Arial", 15, "bold"), text_color="white").pack(padx=25, pady=(15, 5), anchor="w")
        
        ctk.CTkLabel(card_hab, text=f"{done_habit} dari {total_habit} Selesai", 
                     font=("Century Gothic", 20, "bold"), text_color="white").pack(padx=25, anchor="w")

        prog_hab = ctk.CTkProgressBar(card_hab, height=20, corner_radius=10, 
                                      progress_color="white", fg_color=self.theme["btn_hover"])
        prog_hab.set(progress_val)
        prog_hab.pack(padx=25, pady=15, fill="x")


        # -- KOLOM KANAN: Jurnal (Full Height Sejajar Kiri) --
        card_jur = ctk.CTkFrame(main_stats_container, fg_color=self.theme["card"], corner_radius=25)
        card_jur.pack(side="right", fill="both", expand=True, padx=(10, 0))

        ctk.CTkLabel(card_jur, text="📝 Jurnal Terbaru", 
                     font=("Arial", 16, "bold"), text_color=self.theme["text"]).pack(padx=25, pady=(20,10), anchor="w")

        # [PERBAIKAN] Buat Scrollable Frame DULUAN di sini (agar variabelnya dikenali di blok else/except)
        journal_scroll = ctk.CTkScrollableFrame(card_jur, fg_color="transparent")
        journal_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        try:
            res_jurnal = self.logic_journal.get_jurnal_harian(self.current_user_id) 
            
            if res_jurnal:
                for idx, jurnal in enumerate(res_jurnal):
                    # Frame Kartu Jurnal
                    preview_frame = ctk.CTkFrame(journal_scroll, fg_color="#F9F9F9", corner_radius=15)
                    preview_frame.pack(fill="x", pady=(0, 10), padx=5)
                    
                    # --- HEADER BARIS ---
                    top_row = ctk.CTkFrame(preview_frame, fg_color="transparent")
                    top_row.pack(fill="x", padx=15, pady=(15, 5))

                    judul_text = jurnal[0] if jurnal[0] else "Tanpa Judul"
                    if len(judul_text) > 25: judul_text = judul_text[:25] + "..."
                    
                    ctk.CTkLabel(top_row, text=f"{idx+1}. {judul_text}", 
                                 font=("Arial", 12, "bold"), 
                                 text_color=self.theme["text"]).pack(side="left")

                    # --- TOMBOL LIHAT ---
                    btn_lihat = ctk.CTkFrame(top_row, fg_color=self.theme["btn_hover"], corner_radius=15, cursor="hand2", width=80, height=30) 
                    btn_lihat.pack(side="right")
                    btn_lihat.pack_propagate(False)

                    def on_click_lihat(event, j=jurnal):
                        self.tampilkan_detail_inline(j)

                    content_frame = ctk.CTkFrame(btn_lihat, fg_color="transparent")
                    content_frame.place(relx=0.5, rely=0.5, anchor="center")

                    icon_lbl = ctk.CTkLabel(content_frame, text="👁️", font=("Segoe UI Emoji", 12), text_color="white")
                    icon_lbl.pack(side="left", padx=(0, 3)) 
                    text_lbl = ctk.CTkLabel(content_frame, text="Lihat", font=("Arial", 11, "bold"), text_color="white")
                    text_lbl.pack(side="left")

                    # Hover Logic
                    def make_hover(btn_target):
                        def on_enter(e): btn_target.configure(fg_color=self.theme["btn"]) 
                        def on_leave(e): btn_target.configure(fg_color=self.theme["btn_hover"])
                        return on_enter, on_leave

                    enter_func, leave_func = make_hover(btn_lihat)
                    widgets_to_bind = [btn_lihat, content_frame, icon_lbl, text_lbl]
                    for w in widgets_to_bind:
                        w.bind("<Button-1>", on_click_lihat)
                        w.bind("<Enter>", enter_func)
                        w.bind("<Leave>", leave_func)

                    # Preview Teks
                    if jurnal[1]:
                        txt_preview = (jurnal[1][:60] + '...') if len(jurnal[1]) > 60 else jurnal[1]
                        ctk.CTkLabel(preview_frame, text=txt_preview, font=("Arial", 10), 
                                     text_color="grey", wraplength=280, justify="left").pack(anchor="w", padx=15, pady=(0, 15))
            else:
                # [SUKSES] Sekarang ini aman karena journal_scroll sudah ada
                ctk.CTkLabel(journal_scroll, text="Belum ada cerita hari ini.", 
                             font=("Arial", 12, "italic"), text_color="grey").pack(pady=50)
        except Exception as e:
            print(f"DEBUG ERROR: {e}")
            # [SUKSES] Ini juga aman
            ctk.CTkLabel(journal_scroll, text="Gagal memuat data.").pack(pady=50)
        
        card_q = ctk.CTkFrame(self.content_area, fg_color=self.theme["card"], corner_radius=25)
        card_q.pack(fill="x", pady=20, ipady=10)

        # AMBIL QUOTE BARU setiap kali dashboard ditampilkan
        try:
            quote_data = self.logic_dash.get_contextual_quote(self.mental_battery)
            quote_text = quote_data[0]
            quote_author = quote_data[1]
        except:
            quote_text = "Tetap melangkah, hari ini milikmu."
            quote_author = "ZenMood"

        ctk.CTkLabel(card_q, text=f'"{quote_text}"', font=("Century Gothic", 16), 
                    text_color=self.theme["text"], wraplength=800).pack(padx=20, pady=(30, 5))
        ctk.CTkLabel(card_q, text=f"— {quote_author}", font=("Arial", 13, "bold"), text_color=self.theme["text"]).pack(pady=(0, 15))
    # ================= 6. FITUR: MOOD TRACKER =================
    def show_mood(self):
        self.clear_content_frame()
        
        header_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        date_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        date_container.pack(side="right", padx=25, pady=10)
        
        ctk.CTkLabel(header_frame, text="Bagaimana Perasaan Anda hari ini?", font=("Century Gothic", 26, "bold"), text_color=self.theme["text"]).pack(anchor="w")
        ctk.CTkLabel(header_frame, text="Semoga kamu baik-baik saja ya, aku yakin semuanya bisa terhandle dengan baik.", font=("Century Gothic", 14), text_color=self.theme["text"]).pack(anchor="w")
        
        ctk.CTkLabel(date_container, text=f"📅", font=("Segoe UI Emoji", 24), text_color=self.theme["text"]).pack(side="left", padx=(0,8), pady=(0,3))
        
        tgl_str = datetime.now().strftime("%A, %d %B %Y")
        ctk.CTkLabel(date_container, text=tgl_str, font=("Arial", 12, "bold"), text_color=self.theme["text"]).pack(side="right", pady=10)

        # Container
        card = ctk.CTkFrame(self.content_area, fg_color=self.theme["card"], corner_radius=25)
        card.pack(fill="both", expand=True, ipadx=20, ipady=20)

        ctk.CTkLabel(card, text="Pilih Emosi:", font=("Arial", 14, "bold"), text_color=self.theme["text"]).pack(anchor="w", pady=(10, 15), padx=20)
        
        emosi_grid = ctk.CTkFrame(card, fg_color="transparent")
        emosi_grid.pack(fill="x", padx=20)

        self.var_emosi = ctk.IntVar(value=0)
        self.btns_mood = [] 

        def select_mood_visual(selected_id, btn_widget):
            self.var_emosi.set(selected_id)
            for btn in self.btns_mood:
                btn.configure(fg_color="transparent", border_width=2, text_color=self.theme["text"])
            btn_widget.configure(fg_color=self.theme["btn"], border_width=0, text_color="white")

        data_emosi = self.logic_mood.get_daftar_emosi() 
        for idx, (eid, nama, ikon, skor) in enumerate(data_emosi):
            btn = ctk.CTkButton(emosi_grid, text=f"{ikon}\n{nama}", font=("Arial", 15, "bold"), 
                                fg_color="#F9F9F9", border_color=self.theme["btn"], border_width=2,
                                text_color=self.theme["text"], corner_radius=15, height=80, width=150, hover_color=self.theme["btn_hover"])
            btn.configure(command=lambda i=eid, b=btn: select_mood_visual(i, b))
            btn.grid(row=idx//3, column=idx%3, padx=10, pady=10, sticky="ew")
            emosi_grid.grid_columnconfigure(idx%3, weight=1)
            self.btns_mood.append(btn)

        # Input Aktivitas
        ctk.CTkLabel(card, text="Apa aktivitas utamamu?", font=("Arial", 14, "bold"), text_color=self.theme["text"]).pack(anchor="w", pady=(30, 10), padx=20)
        self.ent_aktivitas = ctk.CTkEntry(card, height=50, placeholder_text="Ceritakan singkat aktivitasmu...", font=("Arial", 13), text_color=self.theme["text"], border_width=2, border_color=self.theme["btn"], fg_color="#F9F9F9", corner_radius=15)
        self.ent_aktivitas.pack(fill="x", padx=20)

        # Tombol Simpan
        ctk.CTkButton(card, text="SIMPAN", command=self.simpan_mood_action, text_color="white",
                      fg_color=self.theme["btn_hover"], hover_color=self.theme["btn"], 
                      height=50, font=("Century Gothic", 14, "bold"), corner_radius=25).pack(pady=(30, 10), padx=20)

    def simpan_mood_action(self):
        if not self.var_emosi.get():
            messagebox.showwarning("Info", "Pilih emosi dulu!")
            return
        msg = self.logic_mood.simpan_mood(self.current_user_id, self.var_emosi.get(), self.ent_aktivitas.get())
        self.refresh_app_state()
        self.apply_current_theme()
        self.show_dashboard()

    # ================= 7. FITUR: JURNAL =================
    
    
    
    def tampilkan_detail_jurnal_dashboard(self, jurnal_data):
        """Wrapper untuk menampilkan detail jurnal dari dashboard"""
        self.tampilkan_detail_inline(jurnal_data)   
        
        
        
    def tampilkan_detail_inline(self, jurnal_data):
        """Tampilkan detail jurnal langsung di area konten"""
        judul, isi = jurnal_data
        
        # 1. Bersihkan content area
        for widget in self.content_area.winfo_children():
            widget.destroy()
            
        # 2. Buat frame untuk detail jurnal
        detail_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        detail_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # --- ISI KONTEN DETAIL ---
        # Header Detail
        header = ctk.CTkFrame(detail_frame, fg_color=self.theme["sidebar"], corner_radius=35)
        header.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(header, text=judul if judul else "Tanpa Judul", corner_radius=15,
                    font=("Arial", 16, "bold"), text_color="white").pack(side="left", padx=20, pady=15)
        
        # Tombol Kembali ke Dashboard
        ctk.CTkButton(header, text="← Kembali", text_color="white", font=("Arial", 12, "bold"), corner_radius=35, width=50, fg_color=self.theme["btn_hover"], hover_color=self.theme["btn"]  
                      , command=self.show_dashboard).pack(side="right", padx=50)
        
        # Area Teks
        text_area = ctk.CTkTextbox(detail_frame, text_color=self.theme["text"] ,font=("Arial", 13), fg_color= self.theme["card"], corner_radius=35,)
        text_area.pack(fill="both", expand=True)
        text_area.insert("1.0", isi)
        text_area.configure(state="disabled") # Agar tidak bisa diedit
            
       
    
    def show_jurnal(self): 
        self.clear_content_frame()
        
        # 1. Header & Tanggal
        header_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        date_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        date_container.pack(side="right", padx=25, pady=10)
        
        ctk.CTkLabel(header_frame, text="Ruang Bercerita", font=("Century Gothic", 26, "bold"), text_color=self.theme["text"]).pack(anchor="w")
        ctk.CTkLabel(header_frame, text="Silahkan sampaikan semua keluh kesahmu disini, tidak perlu khawatir ZenMood siap mendengarkan kok.", font=("Century Gothic", 14), text_color=self.theme["text"]).pack(anchor="w")
        
        ctk.CTkLabel(date_container, text=f"📅", font=("Segoe UI Emoji", 24), text_color=self.theme["text"]).pack(side="left", padx=(0,8), pady=(0,3))
        
        tgl_str = datetime.now().strftime("%A, %d %B %Y")
        ctk.CTkLabel(date_container, text=tgl_str, font=("Arial", 12, "bold"), text_color=self.theme["text"]).pack(side="right", pady=10)

        # 2. Container Utama (Card)
        card = ctk.CTkFrame(self.content_area, fg_color=self.theme["card"], corner_radius=20)
        card.pack(fill="both", expand=True, ipadx=10, ipady=10)

        # --- A. Prompt (Ide Tulisan) - WARNA DINAMIS ---
        # Menggunakan self.theme["bg"] agar senada dengan background utama tapi tetap di dalam card
        prompt_frame = ctk.CTkFrame(card, fg_color=self.theme["bg"], corner_radius=15)
        prompt_frame.pack(fill="x", padx=20, pady=(20, 10)) 
        
        self.lbl_prompt = ctk.CTkLabel(prompt_frame, text=f"💡 {self.logic_journal.get_prompt_acak()}", 
                                       font=("Arial", 13, "italic"), text_color=self.theme["text"]) # Text color juga ikut tema
        self.lbl_prompt.pack(side="left", padx=15, pady=10)
        
        # Tombol Ganti dengan warna tema
        ctk.CTkButton(prompt_frame, text="🔄 Ganti", width=60, height=25, 
                      fg_color=self.theme["btn_hover"], text_color="white",
                      font=("Arial", 11, "bold"), hover_color=self.theme["btn"],
                      command=lambda: self.lbl_prompt.configure(text=f"💡 {self.logic_journal.get_prompt_acak()}")).pack(side="right", padx=10)

        # --- B. Input Judul ---
        self.ent_judul = ctk.CTkEntry(card, placeholder_text="Beri judul cerita hari ini...", 
                                      height=45, font=("Arial", 14, "bold"), text_color=self.theme["text"],
                                      border_width=2, border_color=self.theme["btn"], fg_color="#F9F9F9", corner_radius=10)
        self.ent_judul.pack(fill="x", padx=20, pady=(5, 10))

        # --- C. Rating Bintang (Presisi) ---
        rating_container = ctk.CTkFrame(card, fg_color="transparent")
        rating_container.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(rating_container, text="Rating Harimu:", font=("Arial", 12, "bold"), text_color=self.theme["text"]).pack(side="left", padx=(5, 10))
        
        self.var_rating = ctk.IntVar(value=0)
        self.star_buttons = []

        def set_rating(score):
            self.var_rating.set(score)
            for i, btn in enumerate(self.star_buttons):
                # Gunakan warna tema untuk bintang aktif agar serasi
                active_color = self.theme["btn"] 
                btn.configure(text_color="#FFC107" if i < score else "#E0E0E0") 

        for i in range(1, 6):
            btn = ctk.CTkButton(rating_container, text="★", width=30, height=30, 
                                font=("Arial", 28), fg_color="transparent", hover_color="#FAFAFA", 
                                text_color="#E0E0E0", anchor="center")
            btn.configure(command=lambda x=i: set_rating(x))
            btn.pack(side="left", padx=0)
            self.star_buttons.append(btn)

        # --- D. Text Area (Isi Catatan) ---
        self.txt_isi = ctk.CTkTextbox(card,  font=("Arial", 13), fg_color="#FAFAFA", text_color=self.theme["text"],
                                      border_width=2, border_color=self.theme["btn"], corner_radius=10)
        self.txt_isi.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        placeholder_msg = "Silahkan isi ceritamu hari ini..."
        
        def on_focus_in(event):
            current_text = self.txt_isi.get("0.0", "end-1c")
            if current_text == placeholder_msg:
                self.txt_isi.delete("0.0", "end")
                self.txt_isi.configure(text_color=self.theme["text"]) # Warna teks normal (Hitam/Tema)

        # Fungsi saat ditinggalkan (Kembalikan placeholder jika kosong)
        def on_focus_out(event):
            current_text = self.txt_isi.get("0.0", "end-1c").strip()
            if current_text == "":
                self.txt_isi.insert("0.0", placeholder_msg)
                self.txt_isi.configure(text_color="grey") # Warna teks redup (Placeholder)

        # Inisialisasi Awal
        self.txt_isi.insert("0.0", placeholder_msg)
        self.txt_isi.configure(text_color="grey")

        # Pasang (Bind) Event ke Textbox
        self.txt_isi.bind("<FocusIn>", on_focus_in)
        self.txt_isi.bind("<FocusOut>", on_focus_out)

        # --- E. Tombol Simpan ---
        ctk.CTkButton(card, text="SIMPAN TULISAN", command=self.simpan_jurnal_action, text_color="white",
                      font=("Century Gothic", 13, "bold"), height=45, width=200, corner_radius=20,
                      fg_color=self.theme["btn_hover"], hover_color=self.theme["btn"]).pack(anchor="e", padx=20, pady=(0, 20))

    def simpan_jurnal_action(self ):
        isi_raw = self.txt_isi.get("1.0", "end").strip()
        placeholder_msg = "Silahkan isi ceritamu hari ini..." # Harus sama persis

        # Validasi: Jika kosong ATAU masih berisi placeholder -> Tolak
        if not isi_raw or isi_raw == placeholder_msg: 
            return messagebox.showwarning("Info", "Isi jurnal tidak boleh kosong.")
        
        if self.var_rating.get() == 0: 
            return messagebox.showwarning("Info", "Beri rating dulu!")
        
        judul = self.ent_judul.get().strip()
        rating = self.var_rating.get()
        
        
        try:
            # Simpan ke Database
            msg=self.logic_journal.simpan_jurnal(self.current_user_id, judul, isi_raw, rating)
          
            
            self.refresh_app_state()
            self.apply_current_theme() # Pastikan tema tetap terjaga
            self.show_dashboard()
            
        except:
            # HANYA JIKA ERROR, tampilkan pesan error
             messagebox.showerror("Error", f"Terjadi kesalahan tak terduga:\n{msg}")
  

    # ================= 8. FITUR: HABIT =================
    def show_habit(self):
        for w in self.content_area.winfo_children(): w.destroy()
        
        header_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        date_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        date_container.pack(side="right", padx=25, pady=10)
        
        ctk.CTkLabel(header_frame, text="Aktivitas Harian", font=("Century Gothic", 26, "bold"), text_color=self.theme["text"]).pack(anchor="w")
        ctk.CTkLabel(header_frame, text="Silahkan capai habit harianmu, semoga bisa terselesaikan dengan baik!", font=("Century Gothic", 14), text_color=self.theme["text"]).pack(anchor="w")
        
        ctk.CTkLabel(date_container, text=f"📅", font=("Segoe UI Emoji", 24), text_color=self.theme["text"]).pack(side="left", padx=(0,8), pady=(0,3))
        
        tgl_str = datetime.now().strftime("%A, %d %B %Y")
        ctk.CTkLabel(date_container, text=tgl_str, font=("Arial", 12, "bold"), text_color=self.theme["text"]).pack(side="right", pady=10)
        # Ambil Data Habit
        habits = self.logic_habit.get_habits_harian(self.current_user_id)
        
        if not habits:
            empty_frame = ctk.CTkFrame(self.content_area, fg_color=self.theme["card"], corner_radius=20)
            empty_frame.pack(fill="both", expand=True, pady=20)
            ctk.CTkLabel(empty_frame, text="🌱", font=("Arial", 60)).pack(pady=(100, 10))
            ctk.CTkLabel(empty_frame, text="Belum ada habit.", text_color=self.theme["text"]).pack()
            return

        # 2. Hero Section: Progress Bar Harian
        total_habit = len(habits)
        done_habit = sum([1 for h in habits if h[3] == 1])
        progress_val = done_habit / total_habit if total_habit > 0 else 0

        # Card Background (Warna Tema Saat Ini - Konsisten)
        hero_card = ctk.CTkFrame(self.content_area, fg_color=self.theme["btn"], corner_radius=20)
        hero_card.pack(fill="x", pady=(0, 20), ipady=10)
        
        # Teks Ringkasan
        hero_left = ctk.CTkFrame(hero_card, fg_color="transparent")
        hero_left.pack(side="left", padx=25)
        ctk.CTkLabel(hero_left, text="Progres Hari Ini", font=("Arial", 14), text_color="white").pack(anchor="w")
        ctk.CTkLabel(hero_left, text=f"{done_habit} dari {total_habit} Selesai", font=("Century Gothic", 22, "bold"), text_color="white").pack(anchor="w")
        
        # Progress Bar Visual
        hero_right = ctk.CTkFrame(hero_card, fg_color="transparent")
        hero_right.pack(side="right", padx=25, fill="x", expand=True)
        
        # Warna Track menggunakan btn_hover agar 'tone-on-tone' dengan background
        prog_bar = ctk.CTkProgressBar(hero_right, height=15, corner_radius=10, 
                                      progress_color="white", 
                                      fg_color=self.theme["btn_hover"]) 
        prog_bar.set(progress_val)
        prog_bar.pack(fill="x", pady=15)

        # 3. List Habit Cards
        scroll_frame = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)

        def get_icon(nama):
            n = nama.lower()
            if "susu" in n: return "🥛"       # Cek Susu dulu sebelum Minum biasa
            if "sayur" in n: return "🥗"      # Cek Sayur dulu sebelum Makan biasa
            if "buah" in n: return "🍎"       # Cek Buah
            if "air" in n: return "💧"        # Cek Air
            
            # --- CEK YANG UMUM ---
            if "minum" in n: return "💧"      # Default minum (selain susu)
            if "makan" in n: return "🍽️"      # Default makan (selain sayur/buah)
            
            # --- CEK YANG LAIN ---
            if "tidur" in n or "bangun" in n: return "🛌"
            if "buku" in n or "baca" in n or "belajar" in n: return "📚"
            if "lari" in n or "jalan" in n or "gym" in n or "olahraga" in n or "jogging" in n: return "🏃"
            if "sosmed" in n or "hp" in n or "screen" in n or "fokus" in n: return "📵"
            if "skin" in n or "wajah" in n or "masker" in n or "rawat" in n: return "🧖"
            return "✨"

        for h in habits:
            h_id, nama, target, status = h
            
            card_color = "#E8F5E9" if status == 1 else self.theme["card"]
            
            row = ctk.CTkFrame(scroll_frame, fg_color=card_color, corner_radius=15, border_width=2, border_color=self.theme["btn"])
            row.pack(fill="x", pady=5, ipady=5)
            
            # Ikon
            ctk.CTkLabel(row, text=get_icon(nama), font=("Arial", 24), text_color=self.theme["text"]).pack(side="left", padx=(20, 10))
            
            info_box = ctk.CTkFrame(row, fg_color="transparent")
            info_box.pack(side="left", fill="both", expand=True, pady=10)
            
            font_nama = ("Arial", 14, "bold") 
            
            # text_col = "#333" if status == 0 else "grey"
            
            ctk.CTkLabel(info_box, text=nama, font=font_nama, text_color=self.theme["text"]).pack(anchor="w")
            ctk.CTkLabel(info_box, text=f"Target: {target}", font=("Arial", 12), text_color=self.theme["text"]).pack(anchor="w")

            # --- CHECKBOX LOGIC ---
            def on_check(hid=h_id, val_var=None):
                self.logic_habit.toggle_habit(self.current_user_id,hid, val_var.get())
                self.refresh_app_state()
                self.apply_current_theme()
                self.show_habit()

            var = ctk.IntVar(value=status)
            
            cb = ctk.CTkCheckBox(row, text="Selesai", text_color=self.theme["text"], variable=var, onvalue=1, offvalue=0,
                                 command=lambda i=h_id, v=var: on_check(i, v),
                                 font=("Arial", 12, "bold"), border_color=self.theme["text"],
                                 fg_color=self.theme["btn"], hover_color=self.theme["btn_hover"],
                                 checkmark_color="white")
            cb.pack(side="right", padx=20)

if __name__ == "__main__":
    app = ZenMoodApp()
    app.mainloop()