import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from database import MoodTracker, SmartJournal, HabitManager, AnalyticsDashboard

MOOD_THEMES = {
    "Marah (Zen Forest)": {
        "bg": "#E8F8F5", "sidebar": "#148F77", "card": "#FFFFFF", 
        "text": "#148F77", "btn": "#48C9B0", "btn_hover": "#1ABC9C"
    },
    "Cemas (Serenity Blue)": {
        "bg": "#EBF5FB", "sidebar": "#2874A6", "card": "#FFFFFF", 
        "text": "#2874A6", "btn": "#5DADE2", "btn_hover": "#3498DB"
    },
    "Morning Mist (Gray)": { 
        "bg": "#F2F4F4", "sidebar": "#37474F", "card": "#FFFFFF", 
        "text": "#263238", "btn": "#90A4AE", "btn_hover": "#78909C"
    },
    "Sedih (Warm Sunset)": {
        "bg": "#FEF5E7", "sidebar": "#AF601A", "card": "#FFFFFF", 
        "text": "#AF601A", "btn": "#F39C12", "btn_hover": "#D68910"
    },
    "Senang (Joyful Berry)": {
        "bg": "#F5EEF8", "sidebar": "#D7BDE2", "card": "#FFFFFF", 
        "text": "#633974", "btn": "#AF7AC5", "btn_hover": "#9B59B6"
    }
}

class ZenMoodApp(ctk.CTk):
    def __init__(self):
        super().__init__() 
        self.title("ZenMood - Personal Mental Health Tracker")
        self.after(0, lambda: self.state('zoomed'))
        # from database import DatabaseManager 
        # self.db_manager = DatabaseManager()
    

        

        # 2. Oper 'self.db_manager' ke semua kelas logika
        # Agar mereka memakai satu koneksi yang sama dan tidak bentrok (Locking)
        self.logic_dash = AnalyticsDashboard()
        self.logic_journal = SmartJournal()
        self.logic_mood = MoodTracker()
        self.logic_habit = HabitManager()
        
        # Alias untuk pengecekan login
        # self.db = self.db_manager 
        self.db = self.logic_dash.db_manager
        self.mental_battery = 0
        self.current_user_id = None
        
        # Setup UI
        self.main_container = ctk.CTkFrame(self, corner_radius=0)
        self.main_container.pack(fill="both", expand=True)
        self.show_login()

    def refresh_app_state(self):
        """Menghitung baterai harian dan menentukan tema"""
        
        if hasattr(self, 'current_user_id') and self.current_user_id is not None:
                # Jika sudah login, masukkan self.current_user_id ke dalam fungsi
            self.mental_battery = self.logic_dash.hitung_mental_battery(self.current_user_id)
        else:
        #     # Jika belum login (saat aplikasi baru buka), set default 0
            self.mental_battery = 0
        # self.self.mental_battery = self.logic_dash.hitung_self.mental_battery()
        
        if self.mental_battery == 0:
            # self.self.mental_battery = 0
            self.theme_name = "Morning Mist (Gray)"
        elif self.mental_battery <= 20: 
            self.theme_name = "Marah (Zen Forest)"
        elif self.mental_battery <= 40: 
            self.theme_name = "Cemas (Serenity Blue)"
        elif self.mental_battery <= 60: 
            self.theme_name = "Morning Mist (Gray)"
        elif self.mental_battery <= 80: 
            self.theme_name = "Sedih (Warm Sunset)"
        else: 
            self.theme_name = "Senang (Joyful Berry)"
            
        self.theme = MOOD_THEMES[self.theme_name]
        self.current_quote = self.logic_dash.get_contextual_quote(self.mental_battery)
        
    def show_login(self):
        """Menampilkan form login split-screen dengan sudut bulat yang benar"""
        self.clear_screen()
        self.refresh_app_state() 
        self.apply_current_theme()

        login_container = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15, width=900, height=550, border_width=0)
        login_container.place(relx=0.5, rely=0.5, anchor="center")
        login_container.pack_propagate(False)

        left_brand_frame = ctk.CTkFrame(login_container, fg_color=self.theme["sidebar"], corner_radius=0, width=400)
        left_brand_frame.pack(side="left", fill="y")
        left_brand_frame.pack_propagate(False)
        
        ctk.CTkFrame(left_brand_frame, fg_color=self.theme["sidebar"], width=50, corner_radius=0).pack(side="right", fill="y")

        ctk.CTkLabel(left_brand_frame, text="ZENMOOD🌿\nOPTIMIZE\nYOUR\nMOOD", 
                     font=("Century Gothic", 35, "bold"), text_color="white", justify="left").place(relx=0.1, rely=0.3)
        
        ctk.CTkLabel(left_brand_frame, text="Tenang Fokus Terkendali.", 
                     font=("Century Gothic", 14), text_color="white").place(relx=0.1, rely=0.6)

        right_form_frame = ctk.CTkFrame(login_container, fg_color="white", corner_radius=0)
        right_form_frame.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(right_form_frame, text="Selamat Datang", 
                     font=("Century Gothic", 28, "bold"), text_color=self.theme["text"]).pack(pady=(80, 5), padx=50, anchor="w")
        ctk.CTkLabel(right_form_frame, text="Silakan login akun pengguna", 
                     font=("Century Gothic", 13), text_color="grey").pack(pady=(0, 40), padx=50, anchor="w")
        
        ctk.CTkLabel(right_form_frame, text="USERNAME", font=("Arial", 10, "bold"), text_color="grey").pack(padx=50, anchor="w")
        self.ent_user = ctk.CTkEntry(
            right_form_frame, placeholder_text="", width=350, height=40, 
            corner_radius=10, fg_color="#F2F4F4", text_color="black", border_width=1, border_color="#cbd5e0"
        )
        self.ent_user.pack(pady=(5, 20), padx=50, anchor="w")

        ctk.CTkLabel(right_form_frame, text="PASSWORD", font=("Arial", 10, "bold"), text_color="grey").pack(padx=50, anchor="w")
        self.ent_pass = ctk.CTkEntry(
            right_form_frame, placeholder_text="", width=350, height=40, 
            corner_radius=10, show="*", fg_color="#F2F4F4", text_color="black", border_width=1, border_color="#cbd5e0"
        )
        self.ent_pass.pack(pady=(5, 30), padx=50, anchor="w")
        
        btn_login = ctk.CTkButton(
            right_form_frame, text="LOGIN SYSTEM", command=self.process_login, 
            fg_color=self.theme["sidebar"], hover_color=self.theme["btn_hover"], 
            height=45, width=350, corner_radius=10, font=("Arial", 13, "bold")
        )
        btn_login.pack(pady=30, padx=50, anchor="w")

        ctk.CTkLabel(right_form_frame, text="v1.0 • ZenMood Production", 
                     font=("Arial", 10), text_color="#D5DBDB").pack(side="bottom", pady=20)
        
        # --- [FUNGSI PROSES LOGIN] ---
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
    
    def setup_main_ui(self):
        """Membangun struktur Sidebar dan Area Konten Dashboard"""
        self.clear_screen()
        self.refresh_app_state()
        self.apply_current_theme()    \

            # Sidebar Dinamis
        self.sidebar = ctk.CTkFrame(self.main_container, width=240, corner_radius=0, fg_color=self.theme["sidebar"])
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(self.sidebar, text="ZenMood", font=("Century Gothic", 22, "bold"), text_color="white").pack(pady=40)
        
        menu_items = [("🏠 Dashboard", self.show_dashboard), ("🙂 Mood Track", self.show_mood), 
                      ("📝 Journaling", self.show_jurnal), ("✅ Habit Log", self.show_habit), ("⚙️ Data Master", None)]
        
        for text, cmd in menu_items:
            btn = ctk.CTkButton(self.sidebar, text=text, command=cmd, fg_color="transparent", 
                                text_color="white", anchor="w", height=50, hover_color=self.theme["btn"])
            btn.pack(fill="x", padx=10, pady=5)

        spacer = ctk.CTkLabel(self.sidebar, text="")
        spacer.pack(fill="both", expand=True)

        btn_logout = ctk.CTkButton(self.sidebar, text="🚪 Keluar", command=self.logout, 
                                   fg_color="transparent", text_color="#FF5252", 
                                   hover_color="#FFCDD2", height=50, font=("Arial", 12, "bold"), corner_radius=15)
        btn_logout.pack(fill="x", padx=20, pady=20)

        self.content_area = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_area.pack(side="right", fill="both", expand=True, padx=30, pady=20)
        self.show_dashboard()

    # # --- [FUNGSI KELUAR APLIKASI / LOGOUT] ---
    # def logout(self):
    #     """Reset sesi user dan kembali ke layar login"""
    #     self.current_user = None
    #     self.after(100, self.show_login)

    def apply_current_theme(self):
        self.configure(fg_color=self.theme["bg"])
        self.main_container.configure(fg_color=self.theme["bg"])
        if hasattr(self, 'sidebar'):
            self.sidebar.configure(fg_color=self.theme["sidebar"])

    def clear_screen(self):
        for widget in self.main_container.winfo_children(): 
            widget.destroy()
        if hasattr(self, 'sidebar'):
            del self.sidebar

# # --- [GUI: HALAMAN LOGIN MODERN DENGAN CORNER RADIUS SEMPURNA] ---
#     def show_login(self):
#         """Menampilkan form login split-screen dengan sudut bulat yang benar"""
#         self.clear_screen()
#         self.refresh_app_state() 
#         self.apply_current_theme()

#         login_container = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15, width=900, height=550, border_width=0)
#         login_container.place(relx=0.5, rely=0.5, anchor="center")
#         login_container.pack_propagate(False)

#         left_brand_frame = ctk.CTkFrame(login_container, fg_color=self.theme["sidebar"], corner_radius=0, width=400)
#         left_brand_frame.pack(side="left", fill="y")
#         left_brand_frame.pack_propagate(False)
        
#         ctk.CTkFrame(left_brand_frame, fg_color=self.theme["sidebar"], width=50, corner_radius=0).pack(side="right", fill="y")

#         ctk.CTkLabel(left_brand_frame, text="ZENMOOD🌿\nOPTIMIZE\nYOUR\nMOOD", 
#                      font=("Century Gothic", 35, "bold"), text_color="white", justify="left").place(relx=0.1, rely=0.3)
        
#         ctk.CTkLabel(left_brand_frame, text="Tenang Fokus Terkendali.", 
#                      font=("Century Gothic", 14), text_color="white").place(relx=0.1, rely=0.6)

#         right_form_frame = ctk.CTkFrame(login_container, fg_color="white", corner_radius=0)
#         right_form_frame.pack(side="right", fill="both", expand=True)

#         ctk.CTkLabel(right_form_frame, text="Selamat Datang", 
#                      font=("Century Gothic", 28, "bold"), text_color=self.theme["text"]).pack(pady=(80, 5), padx=50, anchor="w")
#         ctk.CTkLabel(right_form_frame, text="Silakan login akun pengguna", 
#                      font=("Century Gothic", 13), text_color="grey").pack(pady=(0, 40), padx=50, anchor="w")
        
#         ctk.CTkLabel(right_form_frame, text="USERNAME", font=("Arial", 10, "bold"), text_color="grey").pack(padx=50, anchor="w")
#         self.ent_user = ctk.CTkEntry(
#             right_form_frame, placeholder_text="", width=350, height=40, 
#             corner_radius=10, fg_color="#F2F4F4", text_color="black", border_width=1, border_color="#cbd5e0"
#         )
#         self.ent_user.pack(pady=(5, 20), padx=50, anchor="w")

#         ctk.CTkLabel(right_form_frame, text="PASSWORD", font=("Arial", 10, "bold"), text_color="grey").pack(padx=50, anchor="w")
#         self.ent_pass = ctk.CTkEntry(
#             right_form_frame, placeholder_text="", width=350, height=40, 
#             corner_radius=10, show="*", fg_color="#F2F4F4", text_color="black", border_width=1, border_color="#cbd5e0"
#         )
#         self.ent_pass.pack(pady=(5, 30), padx=50, anchor="w")
        
#         btn_login = ctk.CTkButton(
#             right_form_frame, text="LOGIN SYSTEM", command=self.process_login, 
#             fg_color=self.theme["sidebar"], hover_color=self.theme["btn_hover"], 
#             height=45, width=350, corner_radius=10, font=("Arial", 13, "bold")
#         )
#         btn_login.pack(pady=30, padx=50, anchor="w")

#         ctk.CTkLabel(right_form_frame, text="v1.0 • ZenMood Production", 
#                      font=("Arial", 10), text_color="#D5DBDB").pack(side="bottom", pady=20)
        

        
#         # Sidebar Dinamis
#         self.sidebar = ctk.CTkFrame(self.main_container, width=240, corner_radius=0, fg_color=self.theme["sidebar"])
#         self.sidebar.pack(side="left", fill="y")
#         self.sidebar.pack_propagate(False)

#         ctk.CTkLabel(self.sidebar, text="ZenMood", font=("Century Gothic", 22, "bold"), text_color="white").pack(pady=40)
        
#         menu_items = [("🏠 Dashboard", self.show_dashboard), ("🙂 Mood Track", self.show_mood), 
#                       ("📝 Journaling", self.show_jurnal), ("✅ Habit Log", self.show_habit), ("⚙️ Data Master", None)]
        
#         for text, cmd in menu_items:
#             btn = ctk.CTkButton(self.sidebar, text=text, command=cmd, fg_color="transparent", 
#                                 text_color="white", anchor="w", height=50, hover_color=self.theme["btn"])
#             btn.pack(fill="x", padx=10, pady=5)

#         spacer = ctk.CTkLabel(self.sidebar, text="")
#         spacer.pack(fill="both", expand=True)

#         btn_logout = ctk.CTkButton(self.sidebar, text="🚪 Keluar", command=self.logout, 
#                                    fg_color="transparent", text_color="#FF5252", 
#                                    hover_color="#FFCDD2", height=50, font=("Arial", 12, "bold"), corner_radius=15)
#         btn_logout.pack(fill="x", padx=20, pady=20)

#         self.content_area = ctk.CTkFrame(self.main_container, fg_color="transparent")
#         self.content_area.pack(side="right", fill="both", expand=True, padx=30, pady=20)
#         self.show_dashboard()

    # --- 1. DASHBOARD ---
    def show_dashboard(self):
        for w in self.content_area.winfo_children(): w.destroy()
        
        # Header (dengan tombol reset untuk testing)
        header = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(header, text=f"Halo, {self.current_user}!", 
                     font=("Century Gothic", 26, "bold"), text_color=self.theme["text"]).pack(side="left")
        def _confirm_reset():
            if messagebox.askyesno("Konfirmasi", "Hapus semua data hari ini? Ini akan mengembalikan baterai ke 0%."):
                self.reset_today_data()
        ctk.CTkButton(header, text="Reset Hari Ini", width=120, height=30, fg_color="#FF6B6B", hover_color="#FF8A8A", command=_confirm_reset).pack(side="right", padx=10)

        # Container Atas (Split Layout)
        top_container = ctk.CTkFrame(self.content_area, fg_color="transparent")
        top_container.pack(fill="x", expand=True)

        # -- KIRI: Baterai Mental --
        card_bat = ctk.CTkFrame(top_container, fg_color=self.theme["card"], corner_radius=25, height=200)
        card_bat.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(card_bat, text="🔋 Baterai Mental", font=("Arial", 14, "bold"), text_color=self.theme["text"]).pack(padx=20, pady=(20,10), anchor="w")
        
        prog = ctk.CTkProgressBar(card_bat, width=300, height=20, corner_radius=10, progress_color=self.theme["btn"])
        prog.set(self.self.mental_battery / 100)
        prog.pack(padx=20, pady=10, fill="x")
        
        ctk.CTkLabel(card_bat, text=f"{int(self.self.mental_battery)}% - {self.theme_name}", font=("Arial", 12), text_color="grey").pack(padx=20, anchor="w")

        # -- KANAN: List Jurnal --
        card_jur = ctk.CTkFrame(top_container, fg_color=self.theme["card"], corner_radius=25)
        card_jur.pack(side="right", fill="both", expand=True, padx=(10, 0))

        header_jur = ctk.CTkFrame(card_jur, fg_color="transparent")
        header_jur.pack(fill="x", padx=20, pady=(20,10))
        ctk.CTkLabel(header_jur, text="📝 Jurnal Terbaru", font=("Arial", 14, "bold"), text_color=self.theme["text"]).pack(side="left")
        ctk.CTkButton(header_jur, text="+ Baru", width=60, height=25, command=self.show_jurnal, fg_color=self.theme["btn"]).pack(side="right")

        list_jurnal = self.logic_journal.get_jurnal_harian() # Ambil 2 jurnal
        if list_jurnal:
            for j in list_jurnal:
                f_item = ctk.CTkFrame(card_jur, fg_color="#F9F9F9", corner_radius=10)
                f_item.pack(fill="x", padx=20, pady=5)
                ctk.CTkLabel(f_item, text=j[0], font=("Arial", 12, "bold"), text_color=self.theme["text"]).pack(anchor="w", padx=10, pady=(5,0))
                preview = (j[1][:40] + '...') if len(j[1]) > 40 else j[1]
                ctk.CTkLabel(f_item, text=preview, font=("Arial", 11), text_color="grey").pack(anchor="w", padx=10, pady=(0,5))
        else:
            ctk.CTkLabel(card_jur, text="Belum ada catatan hari ini.", text_color="grey").pack(pady=20)

        # -- BAWAH: Quote --
        card_q = ctk.CTkFrame(self.content_area, fg_color=self.theme["card"], corner_radius=25)
        card_q.pack(fill="x", pady=20, ipady=10)
        ctk.CTkLabel(card_q, text=f'"{self.current_quote[0]}"', font=("Century Gothic", 16, "italic"), 
                     text_color=self.theme["text"], wraplength=800).pack(pady=(15, 5))
        ctk.CTkLabel(card_q, text=f"— {self.current_quote[1]}", font=("Arial", 12), text_color="grey").pack()
        

    # --- 2. MOOD CHECK-IN (REVISI DESIGN) ---
    def show_mood(self):
        for w in self.content_area.winfo_children(): w.destroy()
        
        # 1. Header dengan Tanggal
        tgl_str = datetime.now().strftime("%A, %d %B %Y")
        header_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header_frame, text="Bagaimana Perasaanmu?", font=("Century Gothic", 26, "bold"), 
                     text_color=self.theme["text"]).pack(anchor="w")
        ctk.CTkLabel(header_frame, text=f"{tgl_str} — Check-in harianmu penting.", 
                     font=("Arial", 12), text_color="grey").pack(anchor="w")

        # Container Utama (Card Putih)
        card = ctk.CTkFrame(self.content_area, fg_color=self.theme["card"], corner_radius=25)
        card.pack(fill="both", expand=True, ipadx=20, ipady=20)

        # 2. Grid Emosi (Tombol Besar)
        ctk.CTkLabel(card, text="Pilih Emosi:", font=("Arial", 14, "bold"), text_color=self.theme["text"]).pack(anchor="w", pady=(10, 15), padx=20)
        
        emosi_grid = ctk.CTkFrame(card, fg_color="transparent")
        emosi_grid.pack(fill="x", padx=20)

        # Variable untuk menyimpan pilihan
        self.var_emosi = ctk.IntVar(value=0)
        self.btns_mood = [] # Simpan referensi tombol untuk ubah warna nanti

        # Logika visual saat tombol diklik
        def select_mood_visual(selected_id, btn_widget):
            self.var_emosi.set(selected_id)
            # Reset semua tombol ke warna default (transparent/outline)
            for btn in self.btns_mood:
                btn.configure(fg_color="transparent", border_width=2, text_color="grey")
            # Highlight tombol yang dipilih
            btn_widget.configure(fg_color=self.theme["btn"], border_width=0, text_color="white")

        # Loop membuat tombol grid
        data_emosi = self.logic_mood.get_daftar_emosi() # [(id, nama, ikon, skor), ...]
        
        for idx, (eid, nama, ikon, skor) in enumerate(data_emosi):
            # Custom Button
            btn = ctk.CTkButton(emosi_grid, text=f"{ikon}\n{nama}", font=("Arial", 14), 
                                fg_color="transparent", border_color=self.theme["btn"], border_width=2,
                                text_color="grey", corner_radius=15, height=80, width=150)
            
            # Menggunakan lambda agar setiap tombol ingat ID-nya masing-masing
            btn.configure(command=lambda i=eid, b=btn: select_mood_visual(i, b))
            
            # Grid layout (misal: 3 kolom)
            btn.grid(row=idx//3, column=idx%3, padx=10, pady=10, sticky="ew")
            emosi_grid.grid_columnconfigure(idx%3, weight=1) # Agar lebar rata
            self.btns_mood.append(btn)

        # 3. Input Aktivitas dengan Quick Tags
        ctk.CTkLabel(card, text="Apa aktivitas utamamu?", font=("Arial", 14, "bold"), text_color=self.theme["text"]).pack(anchor="w", pady=(30, 10), padx=20)
        
        self.ent_aktivitas = ctk.CTkEntry(card, height=50, placeholder_text="Ceritakan singkat aktivitasmu...", font=("Arial", 13), corner_radius=15)
        self.ent_aktivitas.pack(fill="x", padx=20)

        # Quick Tags (Tombol Cepat)
        tags_frame = ctk.CTkFrame(card, fg_color="transparent")
        tags_frame.pack(fill="x", padx=20, pady=10)
        
        tags = ["🎓 Kuliah", "💤 Tidur", "🎮 Main Game", "💻 Coding", "🏃 Olahraga", "🍔 Makan Enak"]
        
        def add_tag(tag_text):
            current = self.ent_aktivitas.get()
            new_text = f"{current}, {tag_text}" if current else tag_text
            self.ent_aktivitas.delete(0, "end")
            self.ent_aktivitas.insert(0, new_text.strip(", "))

        for t in tags:
            ctk.CTkButton(tags_frame, text=t, command=lambda x=t: add_tag(x), 
                          fg_color="#F0F0F0", text_color="#555", hover_color="#E0E0E0", 
                          height=30, width=60, corner_radius=15, font=("Arial", 11)).pack(side="left", padx=(0, 5))

        ctk.CTkButton(card, text="SIMPAN CHECK-IN", command=self.simpan_mood_action, 
                      fg_color=self.theme["btn"], hover_color=self.theme["btn_hover"], 
                      height=50, font=("Century Gothic", 14, "bold"), corner_radius=25).pack(pady=(30, 10), padx=20, fill="x")

    def simpan_mood_action(self):
        if not self.var_emosi.get():
            messagebox.showwarning("Info", "Pilih emosi dulu!")
            return
        msg = self.logic_mood.simpan_mood(self.var_emosi.get(), self.ent_aktivitas.get())
        messagebox.showinfo("Sukses", msg)
        self.refresh_app_state() # Update baterai
        self.apply_current_theme() # Update tema jika berubah
        self.show_dashboard()

    # --- 3. JURNAL ---
    def show_jurnal(self):
        for w in self.content_area.winfo_children(): w.destroy()
        
        # 1. Header & Tanggal
        tgl_str = datetime.now().strftime("%A, %d %B %Y")
        header_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(header_frame, text="Ruang Bercerita", font=("Century Gothic", 26, "bold"), text_color=self.theme["text"]).pack(side="left")
        ctk.CTkLabel(header_frame, text=tgl_str, font=("Arial", 12, "bold"), text_color="grey").pack(side="right", pady=10)

        # Container Utama
        card = ctk.CTkFrame(self.content_area, fg_color=self.theme["card"], corner_radius=20)
        card.pack(fill="both", expand=True, ipadx=20, ipady=20)

        # 2. Prompt (Ide Tulisan)
        prompt_frame = ctk.CTkFrame(card, fg_color="#F0F8FF", corner_radius=10)
        prompt_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        self.lbl_prompt = ctk.CTkLabel(prompt_frame, text=f"💡 {self.logic_journal.get_prompt_acak()}", 
                                       font=("Arial", 13, "italic"), text_color="#2E86C1")
        self.lbl_prompt.pack(side="left", padx=15, pady=10)
        
        ctk.CTkButton(prompt_frame, text="🔄 Ganti Topik", width=80, height=25, font=("Arial", 10), 
                      fg_color="#AED6F1", text_color="#1B4F72", hover_color="#85C1E9",
                      command=lambda: self.lbl_prompt.configure(text=f"💡 {self.logic_journal.get_prompt_acak()}")).pack(side="right", padx=10)

        # 3. Input Judul
        self.ent_judul = ctk.CTkEntry(card, placeholder_text="Beri judul untuk ceritamu hari ini...", 
                                      height=45, font=("Arial", 14, "bold"), border_width=0, fg_color="#F9F9F9")
        self.ent_judul.pack(fill="x", padx=10, pady=(0, 10))

        # --- FITUR BARU: RATING BINTANG ---
        rating_frame = ctk.CTkFrame(card, fg_color="transparent")
        rating_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkLabel(rating_frame, text="Rating harimu:", font=("Arial", 12), text_color="grey").pack(side="left", padx=(0,10))
        
        self.var_rating = ctk.IntVar(value=0) # Menyimpan nilai 1-5
        self.star_buttons = [] # Menyimpan objek tombol bintang

        def set_rating(score):
            self.var_rating.set(score)
            # Update warna visual bintang
            for i, btn in enumerate(self.star_buttons):
                # Jika index tombol < score, warnai Emas. Jika tidak, warnai Abu.
                if i < score:
                    btn.configure(text_color="#FFD700") # Warna Emas
                else:
                    btn.configure(text_color="#D3D3D3") # Warna Abu

        # Membuat 5 Bintang
        for i in range(1, 6):
            # Menggunakan karakter bintang Unicode (★)
            btn = ctk.CTkButton(rating_frame, text="★", width=30, height=30, 
                                font=("Arial", 24), fg_color="transparent", hover_color="#FAFAFA",
                                text_color="#D3D3D3", # Default abu-abu
                                command=lambda x=i: set_rating(x))
            btn.pack(side="left", padx=2)
            self.star_buttons.append(btn)

        # ----------------------------------

        # 4. Area Teks Utama
        self.txt_isi = ctk.CTkTextbox(card, font=("Arial", 13), fg_color="#FAFAFA", border_width=1, border_color="#E0E0E0", corner_radius=10)
        self.txt_isi.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        # 5. Footer & Simpan
        footer_frame = ctk.CTkFrame(card, fg_color="transparent")
        footer_frame.pack(fill="x", padx=10, pady=10)

        self.lbl_word_count = ctk.CTkLabel(footer_frame, text="0 kata", font=("Arial", 11), text_color="grey")
        self.lbl_word_count.pack(side="left")

        def update_word_count(event):
            text = self.txt_isi.get("1.0", "end").strip()
            count = len(text.split()) if text else 0
            self.lbl_word_count.configure(text=f"{count} kata")
        
        self.txt_isi.bind("<KeyRelease>", update_word_count)

        ctk.CTkButton(footer_frame, text="SIMPAN TULISAN", command=self.simpan_jurnal_action, 
                      font=("Century Gothic", 13, "bold"), height=40, width=150,
                      fg_color=self.theme["btn"], hover_color=self.theme["btn_hover"]).pack(side="right")

    def simpan_jurnal_action(self):
        judul = self.ent_judul.get()
        isi = self.txt_isi.get("1.0", "end").strip()
        rating = self.var_rating.get() # Ambil nilai bintang

        if not isi:
            messagebox.showwarning("Info", "Isi jurnal tidak boleh kosong.")
            return
        
        if rating == 0:
            messagebox.showwarning("Info", "Beri rating bintang dulu ya!")
            return

        # Kirim rating ke database
        msg = self.logic_journal.simpan_jurnal(judul, isi, rating)
        messagebox.showinfo("Sukses", msg)
        self.refresh_app_state()
        self.show_dashboard()

    # --- 4. HABIT TRACKER (WARNA KONSISTEN & TANPA CORETAN) ---
    def show_habit(self):
        for w in self.content_area.winfo_children(): w.destroy()
        
        # 1. Header & Tanggal
        tgl_str = datetime.now().strftime("%A, %d %B %Y")
        header_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(header_frame, text="Habit Tracker", font=("Century Gothic", 26, "bold"), text_color=self.theme["text"]).pack(side="left")
        ctk.CTkLabel(header_frame, text=tgl_str, font=("Arial", 12, "bold"), text_color="grey").pack(side="right", pady=10)

        # Ambil Data Habit
        habits = self.logic_habit.get_habits_harian()
        
        if not habits:
            empty_frame = ctk.CTkFrame(self.content_area, fg_color=self.theme["card"], corner_radius=20)
            empty_frame.pack(fill="both", expand=True, pady=20)
            ctk.CTkLabel(empty_frame, text="🌱", font=("Arial", 60)).pack(pady=(100, 10))
            ctk.CTkLabel(empty_frame, text="Belum ada habit.", text_color="grey").pack()
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
            if "air" in n or "minum" in n: return "💧"
            if "tidur" in n or "bangun" in n: return "🛌"
            if "buku" in n or "baca" in n or "belajar" in n: return "📚"
            if "lari" in n or "jalan" in n or "gym" in n or "olahraga" in n: return "🏃"
            return "✨"

        for h in habits:
            h_id, nama, target, status = h
            
            # Warna kartu: Putih jika belum, Hijau tipis jika selesai
            # Menggunakan kode hex manual untuk hijau tipis agar netral
            card_color = "#E8F5E9" if status == 1 else self.theme["card"]
            
            row = ctk.CTkFrame(scroll_frame, fg_color=card_color, corner_radius=15, border_width=1, border_color="#DDD")
            row.pack(fill="x", pady=5, ipady=5)
            
            # Ikon
            ctk.CTkLabel(row, text=get_icon(nama), font=("Arial", 24)).pack(side="left", padx=(20, 10))
            
            # Info (Nama & Target)
            info_box = ctk.CTkFrame(row, fg_color="transparent")
            info_box.pack(side="left", fill="both", expand=True, pady=10)
            
            # [PERBAIKAN FONT] Hapus "overstrike" agar tidak dicoret
            # Font tetap Bold baik sudah selesai atau belum agar terbaca jelas
            font_nama = ("Arial", 14, "bold") 
            
            # Warna teks jadi abu-abu jika selesai, hitam jika belum (pembeda visual pengganti coretan)
            text_col = "#333" if status == 0 else "grey"
            
            ctk.CTkLabel(info_box, text=nama, font=font_nama, text_color=text_col).pack(anchor="w")
            ctk.CTkLabel(info_box, text=f"Target: {target}", font=("Arial", 12), text_color="grey").pack(anchor="w")

            # --- CHECKBOX LOGIC ---
            def on_check(hid=h_id, val_var=None):
                self.logic_habit.toggle_habit(hid, val_var.get())
                
                # [PERBAIKAN] Hapus atau disable baris refresh_app_state() ini
                # self.refresh_app_state() 
                
                # Cukup refresh halaman ini saja, tema tetap menggunakan warna 'self.theme' yang lama
                self.show_habit()

            var = ctk.IntVar(value=status)
            
            cb = ctk.CTkCheckBox(row, text="Selesai", variable=var, onvalue=1, offvalue=0,
                                 command=lambda i=h_id, v=var: on_check(i, v),
                                 font=("Arial", 12, "bold"), 
                                 fg_color=self.theme["btn"], hover_color=self.theme["btn_hover"],
                                 checkmark_color="white")
            cb.pack(side="right", padx=20)

    # --- 5. DATA MASTER (Sederhana) ---
    def show_master(self):
        for w in self.content_area.winfo_children(): w.destroy()
        ctk.CTkLabel(self.content_area, text="Data Master (Read Only)", font=("Century Gothic", 24, "bold"), text_color=self.theme["text"]).pack(pady=20)
        
        tabview = ctk.CTkTabview(self.content_area, fg_color=self.theme["card"])
        tabview.pack(fill="both", expand=True)
        tabview.add("Emosi")
        tabview.add("Aktivitas")
        tabview.add("Habit")

        # Tab Emosi
        t_emosi = ctk.CTkTextbox(tabview.tab("Emosi"))
        t_emosi.pack(fill="both", expand=True)
        for e in self.logic_mood.get_daftar_emosi(): t_emosi.insert("end", f"{e[2]} {e[1]} (Skor: {e[3]})\n")
        
        t_akt = ctk.CTkTextbox(tabview.tab("Aktivitas"))
        t_akt.pack(fill="both", expand=True)
        for a in self.logic_mood.get_daftar_aktivitas(): t_akt.insert("end", f"- {a[1]} ({a[2]})\n")

        t_hab = ctk.CTkTextbox(tabview.tab("Habit"))
        t_hab.pack(fill="both", expand=True)
        for h in self.logic_habit.get_habits_harian(): t_hab.insert("end", f"- {h[1]} (Target: {h[2]})\n")

if __name__ == "__main__":
    app = ZenMoodApp()
    app.mainloop()