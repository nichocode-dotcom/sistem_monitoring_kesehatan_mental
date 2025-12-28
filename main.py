import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from database import MoodTracker, SmartJournal, HabitManager, AnalyticsDashboard

MOOD_THEMES = {
    "Zen Forest": {
        "bg": "#E8F8F5", "sidebar": "#148F77", "card": "#FFFFFF", 
        "text": "#148F77", "btn": "#48C9B0", "btn_hover": "#1ABC9C",
        "description": "Warna hijau ini hadir sebagai ruang napas untuk meredam gemuruh di hatimu, mengajakmu pulang ke ketenangan alam saat energimu berada di titik terendah."
    },
    "Serenity Blue": {
        "bg": "#EBF5FB", "sidebar": "#2874A6", "card": "#FFFFFF", 
        "text": "#2874A6", "btn": "#5DADE2", "btn_hover": "#3498DB",
        "description": "Biru ini adalah jangkar bagi pikiranmu yang berisik, memberikan rasa aman dan stabilitas untuk menenangkan jiwamu yang sedang dilanda ketidakpastian."
    },
    "Morning Mist (Gray)": { 
        "bg": "#F8F9F9", "sidebar": "#455A64", "card": "#FFFFFF", 
        "text": "#37474F", "btn": "#9BA9B0", "btn_hover": "#7F9096",
        "description": "Mengusung warna abu-abu netral untuk memberikan kesan bersih dan objektif sebagai ruang kosong bagi pengguna dalam menjernihkan pikiran."
    },
    "Warm Sunset": {
        "bg": "#FEF5E7", "sidebar": "#AF601A", "card": "#FFFFFF", 
        "text": "#AF601A", "btn": "#F39C12", "btn_hover": "#D68910",
        "description": "Warna jingga yang hangat ini adalah pelukan visual yang meyakinkanmu bahwa di balik rasa lelah dan sedih, selalu ada harapan baru yang akan terbit esok hari."
    },
    "Healing Rose": {
        "bg": "#FFF0F5", "sidebar": "#DB7093", "card": "#FFFFFF",    
        "text": "#C71585", "btn": "#FFB6C1", "btn_hover": "#FF69B4",
        "description": "Warna merah muda yang lembut ini adalah simbol kasih sayang untuk dirimu sendiri, meyakinkanmu bahwa setiap luka sedang berproses menjadi kekuatan baru yang lebih indah."
    },
    "Joyful Berry": {
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
        
        self.main_container = ctk.CTkFrame(self, corner_radius=0)
        self.main_container.pack(fill="both", expand=True)
        
        self.show_login()

    def refresh_app_state(self):
        if hasattr(self, 'current_user_id') and self.current_user_id is not None:
            current_battery = self.logic_dash.hitung_mental_battery(self.current_user_id)
        else:
            current_battery = 0 
        if current_battery == 0:
            theme_key = "Morning Mist (Gray)"
        elif current_battery <= 20: 
            theme_key = "Zen Forest"
        elif current_battery <= 40: 
            theme_key = "Serenity Blue"
        elif current_battery <= 60: 
            theme_key = "Healing Rose"
        elif current_battery <= 80: 
            theme_key = "Warm Sunset"
        else: 
            theme_key = "Joyful Berry"
        self.mental_battery = current_battery
        self.theme_name = theme_key
        self.theme = MOOD_THEMES[self.theme_name]
        
        try:
            self.current_quote = self.logic_dash.get_contextual_quote(self.mental_battery)
        except:
            self.current_quote = ("Tetap melangkah, hari ini milikmu", "ZenMood")

    def apply_current_theme(self):
        self.configure(fg_color=self.theme["bg"])
        self.main_container.configure(fg_color=self.theme["bg"])
        
        if hasattr(self, 'sidebar'):
            self.sidebar.configure(fg_color=self.theme["sidebar"])
            
            if hasattr(self, 'nav_buttons'):
                for btn in self.nav_buttons:
                    btn.configure(
                        fg_color=self.theme["btn_hover"], 
                        hover_color=self.theme["btn"])
            
            if hasattr(self, 'btn_logout'):
                 self.btn_logout.configure(
                     fg_color=self.theme["btn_hover"], 
                     hover_color=self.theme["btn"])

    def clear_screen(self):
        for widget in self.main_container.winfo_children(): 
            widget.destroy()
        if hasattr(self, 'sidebar'):
            del self.sidebar

    def clear_content_frame(self):
        if hasattr(self, 'content_area'):
            for widget in self.content_area.winfo_children():
                widget.destroy()

#================= REGISTER =================
    def show_register(self):
        self.clear_screen()
        self.refresh_app_state() 
        self.apply_current_theme()

        reg_container = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius=15, width=900, height=550, border_width=0)
        reg_container.place(relx=0.5, rely=0.5, anchor="center")
        reg_container.pack_propagate(False)

        left_brand_frame = ctk.CTkFrame(reg_container, fg_color=self.theme["sidebar"], corner_radius=0, width=400)
        left_brand_frame.pack(side="left", fill="y")
        left_brand_frame.pack_propagate(False)
        ctk.CTkFrame(left_brand_frame, fg_color=self.theme["sidebar"], width=50, corner_radius=0).pack(side="right", fill="y")
        ctk.CTkLabel(left_brand_frame, text="ZENMOOD🌿\nJOIN\nOUR\nJOURNEY", font=("Century Gothic", 35, "bold"), text_color="white", justify="left").place(relx=0.1, rely=0.3)
        ctk.CTkLabel(left_brand_frame, text="Mulai langkah sehatmu hari ini", font=("Century Gothic", 14), text_color="white").place(relx=0.1, rely=0.6)

        right_form_frame = ctk.CTkFrame(reg_container, fg_color="white", corner_radius=0)
        right_form_frame.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(right_form_frame, text="Buat Akun Baru", font=("Century Gothic", 28, "bold"), text_color=self.theme["text"]).pack(pady=(60, 5), padx=100, anchor="w")
        ctk.CTkLabel(right_form_frame, text="Lengkapi data diri anda", font=("Century Gothic", 13), text_color=self.theme["text"]).pack(pady=(0, 10), padx=100, anchor="w")
        
        ctk.CTkLabel(right_form_frame, text="USERNAME", font=("Arial", 10, "bold"), text_color=self.theme["text"]).pack(padx=100, anchor="w")
        self.ent_reg_user = ctk.CTkEntry(right_form_frame, width=350, height=40, corner_radius=20, 
                                         fg_color="#F2F4F4", text_color="black", border_width=1, border_color="#cbd5e0")
        self.ent_reg_user.pack(pady=(5, 15), padx=100, anchor="w")

        def toggle_eye(entry_widget, btn_widget):
            if btn_widget.cget("text") == "◉": 
                entry_widget.configure(show="") 
                btn_widget.configure(text="○")  
            else:
                entry_widget.configure(show="*") 
                btn_widget.configure(text="◉")   

        ctk.CTkLabel(right_form_frame, text="PASSWORD", font=("Arial", 10, "bold"), text_color=self.theme["text"]).pack(padx=100, anchor="w")
        
        pass_frame1 = ctk.CTkFrame(right_form_frame, fg_color="transparent", width=350, height=40)
        pass_frame1.pack(pady=(5, 15), padx=100, anchor="w")
        pass_frame1.pack_propagate(False)

        self.ent_reg_pass = ctk.CTkEntry(pass_frame1, width=350, height=40, corner_radius=20, show="*", 
                                         fg_color="#F2F4F4", text_color="black", border_width=1, border_color="#cbd5e0")
        self.ent_reg_pass.place(relx=0, rely=0, relwidth=1, relheight=1)

        btn_eye1 = ctk.CTkButton(pass_frame1, text="◉", width=20, height=20,  corner_radius=0, border_width=0, fg_color="#F2F4F4", hover_color="#E0E0E0", 
                                 text_color="grey", font=("Arial", 18, "bold"))
        btn_eye1.configure(command=lambda: toggle_eye(self.ent_reg_pass, btn_eye1))
        btn_eye1.place(relx=0.9, rely=0.5, anchor="center")

        ctk.CTkLabel(right_form_frame, text="KONFIRMASI PASSWORD", font=("Arial", 10, "bold"), text_color=self.theme["text"]).pack(padx=100, anchor="w")
        
        pass_frame2 = ctk.CTkFrame(right_form_frame, fg_color="transparent", width=350, height=40)
        pass_frame2.pack(pady=(5, 20), padx=100, anchor="w")
        pass_frame2.pack_propagate(False)

        self.ent_reg_confirm = ctk.CTkEntry(pass_frame2, width=350, height=40, corner_radius=20, show="*", 
                                            fg_color="#F2F4F4", text_color="black", border_width=1, border_color="#cbd5e0")
        self.ent_reg_confirm.place(relx=0, rely=0, relwidth=1, relheight=1)

        btn_eye2 = ctk.CTkButton(pass_frame2, text="◉", width=20, height=20,  corner_radius=0, border_width=0, fg_color="#F2F4F4", hover_color="#E0E0E0", 
                                 text_color="grey", font=("Arial", 18, "bold"))
        btn_eye2.configure(command=lambda: toggle_eye(self.ent_reg_confirm, btn_eye2))
        btn_eye2.place(relx=0.9, rely=0.5, anchor="center")

        btn_register = ctk.CTkButton(right_form_frame, text="DAFTAR SEKARANG", command=self.process_register, 
                                     fg_color=self.theme["sidebar"], hover_color=self.theme["btn_hover"], 
                                     height=40, width=350, corner_radius=20, font=("Arial", 13, "bold"))
        btn_register.pack(pady=10, padx=100, anchor="w")

        btn_back = ctk.CTkButton(right_form_frame, text="Kembali ke Login", font=("Arial", 11, "bold"), 
                                 fg_color="transparent", hover_color=self.theme["btn_hover"], 
                                 text_color=self.theme["sidebar"], command=self.show_login, width=350)
        btn_back.pack(pady=5, padx=100, anchor="w")

    def process_register(self):
        user = self.ent_reg_user.get().strip()
        pwd = self.ent_reg_pass.get().strip()
        confirm_pwd =self.ent_reg_confirm.get().strip()

        if not user or not pwd or not confirm_pwd:
            return messagebox.showwarning("Peringatan", "Semua kolom harus diisi dengan benar!")
        
        if pwd != confirm_pwd:
            return messagebox.showerror("Error", "Konfirmasi password tidak cocok!\nCek kembali password Anda.")

        try:
            sukses, pesan = self.db.registrasi_user(user, pwd)
            if sukses:
                messagebox.showinfo("Berhasil", pesan)
                self.show_login()
            else:
                messagebox.showerror("Gagal", pesan)
        except AttributeError:
            messagebox.showerror("Error", "Fungsi registrasi belum ada di database.py!")

#================= LOGIN =================
    def show_login(self):
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
        ctk.CTkLabel(left_brand_frame, text="Tenang Fokus Terkendali", 
                     font=("Century Gothic", 14), text_color="white").place(relx=0.1, rely=0.6)

        right_form_frame = ctk.CTkFrame(login_container, fg_color="white", corner_radius=0)
        right_form_frame.pack(side="right", fill="both", expand=True)

        ctk.CTkLabel(right_form_frame, text="Selamat Datang", 
                     font=("Century Gothic", 28, "bold"), text_color=self.theme["text"]).pack(pady=(80, 5), padx=100, anchor="w")
        ctk.CTkLabel(right_form_frame, text="Silakan login akun pengguna", 
                     font=("Century Gothic", 13), text_color=self.theme["text"]).pack(pady=(0, 10), padx=100, anchor="w")
        
        ctk.CTkLabel(right_form_frame, text="USERNAME", font=("Arial", 10, "bold"), text_color=self.theme["text"]).pack(padx=100, anchor="w")
        self.ent_user = ctk.CTkEntry(right_form_frame, width=350, height=40, corner_radius=20, 
                                     fg_color="#F2F4F4", text_color="black", border_width=2, border_color=self.theme["btn"])
        self.ent_user.pack(pady=(5, 20), padx=100, anchor="w")

        ctk.CTkLabel(right_form_frame, text="PASSWORD", font=("Arial", 10, "bold"), text_color=self.theme["text"]).pack(padx=100, anchor="w")
        
        pass_frame = ctk.CTkFrame(right_form_frame, fg_color="transparent", width=350, height=40)
        pass_frame.pack(pady=(5, 50), padx=100, anchor="w")
        pass_frame.pack_propagate(False) # Agar ukuran wadah tidak menyusut

        self.ent_pass = ctk.CTkEntry(pass_frame, width=350, height=40, corner_radius=20, show="*", 
                                     fg_color="#F2F4F4", text_color="black", border_width=2, border_color=self.theme["btn"])

        self.ent_pass.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.is_pass_visible = False
        
        def toggle_password():
            if self.is_pass_visible:
                self.ent_pass.configure(show="*")
                btn_eye.configure(text="◉") 
                self.is_pass_visible = False
            else:
                self.ent_pass.configure(show="") 
                btn_eye.configure(text="○") 
                self.is_pass_visible = True
                
        btn_eye = ctk.CTkButton(pass_frame, text="◉", width=20, height=20, border_width=0, corner_radius=0,
                                
                                fg_color="#F2F4F4", 
                                
                                hover_color="#E0E0E0", 
                                
                                text_color="grey", font=("Segoe UI Emoji", 16),
                                command=toggle_password)
        
        btn_eye.place(relx=0.9, rely=0.5, anchor="center")
        
        btn_login = ctk.CTkButton(right_form_frame, text="LOGIN", command=self.process_login, 
                                  fg_color=self.theme["sidebar"], hover_color=self.theme["btn_hover"], 
                                  height=40, width=350, corner_radius=20, font=("Arial", 13, "bold"))
        btn_login.pack(pady=0, padx=100, anchor="w")
        
        register_frame = ctk.CTkFrame(right_form_frame, fg_color="transparent")
        register_frame.pack(padx=100, anchor="w")
        
        ctk.CTkLabel(register_frame, text="Belum punya akun?", font=("Arial", 11), text_color=self.theme["text"]).pack(side="left")
        
        btn_reg = ctk.CTkButton(register_frame, text="Daftar di sini", font=("Arial", 11, "bold"),
                                fg_color="transparent", hover_color=self.theme["btn_hover"], height=25, width=80,
                                text_color=self.theme["text"], command=self.show_register)
        btn_reg.pack(side="left", pady=30)

    def process_login(self):
        username = self.ent_user.get().strip()
        password = self.ent_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Gagal", "Username dan password harus diisi.")
            return

        sukses,hasil = self.db.check_login(username, password)
        if sukses:
            self.current_user_id = hasil
            self.current_user = username
            self.setup_main_ui()
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah.")

    def logout(self):
        if self.current_user_id is None:
            self.show_login()
            return

        fitur_aplikasi = [self.logic_mood, self.logic_journal, self.logic_habit, self.logic_dash]
        laporan_gabungan = ""
        
        for fitur in fitur_aplikasi:
            try:
                laporan_gabungan += fitur.generate_laporan_harian(self.current_user_id) + "\n\n"
            except Exception:
                continue

        self.show_report_popup(laporan_gabungan)
        
    def show_report_popup(self, isi_laporan):
        popup = ctk.CTkToplevel(self)
        popup.title("Laporan Aktivitas Harian")
        popup.geometry("550x520")
        popup.resizable(False, False)
        
        popup.transient(self) 
        popup.grab_set()      
        popup.configure(fg_color=self.theme["bg"]) 

        card = ctk.CTkFrame(popup, fg_color=self.theme["card"], corner_radius=20)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(card, text="🌙 Laporan Aktivitas", 
                     font=("Century Gothic", 24, "bold"), 
                     text_color=self.theme["text"]).pack(pady=(25, 5))
        
        ctk.CTkLabel(card, text="Sebelum istirahat, inilah hasil aktivitasmu hari ini: ", 
                     font=("Arial", 12), text_color="grey").pack(pady=(0, 20))

        scroll_area = ctk.CTkScrollableFrame(card, fg_color="#F9F9F9", corner_radius=15)
        scroll_area.pack(fill="both", expand=True, padx=20, pady=5)
        
        ctk.CTkLabel(scroll_area, text=isi_laporan, 
                     font=("Arial", 13), text_color="#555555", 
                     justify="left", wraplength=350).pack(anchor="w", padx=10, pady=10)

        def confirm_logout():
            popup.destroy()       
            self.current_user = None
            self.current_user_id = None
            self.show_login()     

        ctk.CTkButton(card, text="Siap Istirahat 😴", command=confirm_logout,
                      fg_color=self.theme["btn_hover"], text_color="white", hover_color=self.theme["btn"],
                      font=("Century Gothic", 14, "bold"), 
                      height=45, corner_radius=15).pack(fill="x", padx=30, pady=25)
        
#================= SIDEBAR =================
    def setup_main_ui(self):
        self.clear_screen()
        self.refresh_app_state()
        
        self.sidebar = ctk.CTkFrame(self.main_container, width=240, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(self.sidebar, text="ZenMood🌿", font=("Century Gothic", 22, "bold"), text_color="white").pack(pady=40)
        
        self.nav_buttons = [] 
        
        menu_items = [
            ("🏠 Dashboard", self.show_dashboard), 
            ("🙂 Mood Track", self.show_mood), 
            ("📝 Journaling", self.show_jurnal), 
            ("✅ Habit Log", self.show_habit)
        ]

        for text, cmd in menu_items:
            btn = ctk.CTkButton(self.sidebar, text=text, corner_radius=15, command=cmd, 
                                font=("Century Gothic", 14, "bold"),
                                fg_color=self.theme["btn"], 
                                text_color="white", anchor="w", height=50, 
                                hover_color=self.theme["btn_hover"])
            btn.pack(fill="x", padx=30, pady=5)
            self.nav_buttons.append(btn)

        ctk.CTkLabel(self.sidebar, text="").pack(fill="both", expand=True)

        self.btn_logout = ctk.CTkButton(self.sidebar, text="Logout", command=self.logout, 
                                   fg_color=self.theme["btn"], text_color="white", 
                                   hover_color=self.theme["btn_hover"], height=50, 
                                   font=("Arial", 12, "bold"), corner_radius=15)
        self.btn_logout.pack(fill="x", padx=30, pady=20)
        
        self.content_area = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_area.pack(side="right", fill="both", expand=True, padx=30, pady=20)
        
        self.apply_current_theme() 
        
        self.show_dashboard()

# ================= DASHBOARD  =================
    def show_dashboard(self):
        self.clear_content_frame()
        self.refresh_app_state()
        self.apply_current_theme()

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

        main_stats_container = ctk.CTkFrame(self.content_area, fg_color="transparent")
        main_stats_container.pack(fill="both", expand=True)

        left_column = ctk.CTkFrame(main_stats_container, fg_color="transparent")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))

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

        theme_desc = ctk.CTkLabel(card_bat, text=self.theme["description"], font=("Arial", 12, "italic"), text_color=self.theme["text"],wraplength=350, justify="left")
        theme_desc.pack(padx=25, anchor="w", pady=(0, 15))

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

        card_jur = ctk.CTkFrame(main_stats_container, fg_color=self.theme["card"], corner_radius=25)
        card_jur.pack(side="right", fill="both", expand=True, padx=(10, 0))

        ctk.CTkLabel(card_jur, text="📝 Jurnal Terbaru", 
                     font=("Arial", 16, "bold"), text_color=self.theme["text"]).pack(padx=25, pady=(20,10), anchor="w")

        journal_scroll = ctk.CTkScrollableFrame(card_jur, fg_color="transparent")
        journal_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        try:
            res_jurnal = self.logic_journal.get_jurnal_harian(self.current_user_id) 
            if res_jurnal:
                for idx, jurnal in enumerate(res_jurnal):
                    preview_frame = ctk.CTkFrame(journal_scroll, fg_color="#F9F9F9", corner_radius=15)
                    preview_frame.pack(fill="x", pady=(0, 10), padx=5)
                    
                    top_row = ctk.CTkFrame(preview_frame, fg_color="transparent")
                    top_row.pack(fill="x", padx=15, pady=(15, 5))

                    judul_text = jurnal[0] if jurnal[0] else "Tanpa Judul"
                    if len(judul_text) > 25: judul_text = judul_text[:25] + "..."
                    
                    ctk.CTkLabel(top_row, text=f"{idx+1}. {judul_text}", 
                                 font=("Arial", 12, "bold"), 
                                 text_color=self.theme["text"]).pack(side="left")

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

                    if jurnal[1]:
                        txt_preview = (jurnal[1][:60] + '...') if len(jurnal[1]) > 60 else jurnal[1]
                        ctk.CTkLabel(preview_frame, text=txt_preview, font=("Arial", 10), 
                                     text_color=self.theme["text"], wraplength=280, justify="left").pack(anchor="w", padx=15, pady=(0, 15))
            else:
                ctk.CTkLabel(journal_scroll, text="Belum ada cerita hari ini.", 
                             font=("Arial", 12, "italic"), text_color=self.theme["text"]).pack(pady=50)
        except Exception as e:
            print(f"DEBUG ERROR: {e}")
            ctk.CTkLabel(journal_scroll, text="Gagal memuat data.").pack(pady=50)
        
        card_q = ctk.CTkFrame(self.content_area, fg_color=self.theme["card"], corner_radius=25)
        card_q.pack(fill="x", pady=20, ipady=10)

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

# ================= MOOD TRACKER =================
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

        ctk.CTkLabel(card, text="Apa aktivitas utamamu?", font=("Arial", 14, "bold"), text_color=self.theme["text"]).pack(anchor="w", pady=(30, 10), padx=20)
        self.ent_aktivitas = ctk.CTkEntry(card, height=50, placeholder_text="Ceritakan singkat aktivitasmu...", font=("Arial", 13), text_color=self.theme["text"], border_width=2, border_color=self.theme["btn"], fg_color="#F9F9F9", corner_radius=15)
        self.ent_aktivitas.pack(fill="x", padx=20)

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

# ================= JURNAL =================
    def tampilkan_detail_jurnal_dashboard(self, jurnal_data):
        self.tampilkan_detail_inline(jurnal_data)   
        
    def tampilkan_detail_inline(self, jurnal_data):
        judul, isi = jurnal_data

        for widget in self.content_area.winfo_children():
            widget.destroy()
            
        detail_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        detail_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        header = ctk.CTkFrame(detail_frame, fg_color=self.theme["sidebar"], corner_radius=35)
        header.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(header, text=judul if judul else "Tanpa Judul", corner_radius=15,
                    font=("Arial", 16, "bold"), text_color="white").pack(side="left", padx=20, pady=15)
        
        ctk.CTkButton(header, text="← Kembali", text_color="white", font=("Arial", 12, "bold"), corner_radius=35, width=50, fg_color=self.theme["btn_hover"], hover_color=self.theme["btn"]  
                      , command=self.show_dashboard).pack(side="right", padx=50)
        
        text_area = ctk.CTkTextbox(detail_frame, text_color=self.theme["text"] ,font=("Arial", 13), fg_color= self.theme["card"], corner_radius=35,)
        text_area.pack(fill="both", expand=True)
        text_area.insert("1.0", isi)
        text_area.configure(state="disabled")
            
    def show_jurnal(self): 
        self.clear_content_frame()
        
        header_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        date_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        date_container.pack(side="right", padx=25, pady=10)
        
        ctk.CTkLabel(header_frame, text="Ruang Bercerita", font=("Century Gothic", 26, "bold"), text_color=self.theme["text"]).pack(anchor="w")
        ctk.CTkLabel(header_frame, text="Silahkan sampaikan semua keluh kesahmu disini, tidak perlu khawatir ZenMood siap mendengarkan kok.", font=("Century Gothic", 14), text_color=self.theme["text"]).pack(anchor="w")
        
        ctk.CTkLabel(date_container, text=f"📅", font=("Segoe UI Emoji", 24), text_color=self.theme["text"]).pack(side="left", padx=(0,8), pady=(0,3))
        
        tgl_str = datetime.now().strftime("%A, %d %B %Y")
        ctk.CTkLabel(date_container, text=tgl_str, font=("Arial", 12, "bold"), text_color=self.theme["text"]).pack(side="right", pady=10)

        card = ctk.CTkFrame(self.content_area, fg_color=self.theme["card"], corner_radius=20)
        card.pack(fill="both", expand=True, ipadx=10, ipady=10)

        prompt_frame = ctk.CTkFrame(card, fg_color=self.theme["bg"], corner_radius=15)
        prompt_frame.pack(fill="x", padx=20, pady=(20, 10)) 
        
        self.lbl_prompt = ctk.CTkLabel(prompt_frame, text=f"💡 {self.logic_journal.get_prompt_acak()}", 
                                       font=("Arial", 13, "italic"), text_color=self.theme["text"]) 
        self.lbl_prompt.pack(side="left", padx=15, pady=10)
        
        ctk.CTkButton(prompt_frame, text="🔄 Ganti", width=60, height=25, 
                      fg_color=self.theme["btn_hover"], text_color="white",
                      font=("Arial", 11, "bold"), hover_color=self.theme["btn"],
                      command=lambda: self.lbl_prompt.configure(text=f"💡 {self.logic_journal.get_prompt_acak()}")).pack(side="right", padx=10)

        self.ent_judul = ctk.CTkEntry(card, placeholder_text="Beri judul cerita hari ini...", 
                                      height=45, font=("Arial", 14, "bold"), text_color=self.theme["text"],
                                      border_width=2, border_color=self.theme["btn"], fg_color="#F9F9F9", corner_radius=10)
        self.ent_judul.pack(fill="x", padx=20, pady=(5, 10))

        rating_container = ctk.CTkFrame(card, fg_color="transparent")
        rating_container.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(rating_container, text="Rating Harimu:", font=("Arial", 12, "bold"), text_color=self.theme["text"]).pack(side="left", padx=(5, 10))
        
        self.var_rating = ctk.IntVar(value=0)
        self.star_buttons = []

        def set_rating(score):
            self.var_rating.set(score)
            for i, btn in enumerate(self.star_buttons):
                active_color = self.theme["btn"] 
                btn.configure(text_color="#FFC107" if i < score else "#E0E0E0") 

        for i in range(1, 6):
            btn = ctk.CTkButton(rating_container, text="★", width=30, height=30, 
                                font=("Arial", 28), fg_color="transparent", hover_color="#FAFAFA", 
                                text_color="#E0E0E0", anchor="center")
            btn.configure(command=lambda x=i: set_rating(x))
            btn.pack(side="left", padx=0)
            self.star_buttons.append(btn)

        self.txt_isi = ctk.CTkTextbox(card,  font=("Arial", 13), fg_color="#FAFAFA", text_color=self.theme["text"],
                                      border_width=2, border_color=self.theme["btn"], corner_radius=10)
        self.txt_isi.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        placeholder_msg = "Silahkan isi ceritamu hari ini..."
        
        def on_focus_in(event):
            current_text = self.txt_isi.get("0.0", "end-1c")
            if current_text == placeholder_msg:
                self.txt_isi.delete("0.0", "end")
                self.txt_isi.configure(text_color=self.theme["text"])

        def on_focus_out(event):
            current_text = self.txt_isi.get("0.0", "end-1c").strip()
            if current_text == "":
                self.txt_isi.insert("0.0", placeholder_msg)
                self.txt_isi.configure(text_color="grey")

        self.txt_isi.insert("0.0", placeholder_msg)
        self.txt_isi.configure(text_color="grey")

        self.txt_isi.bind("<FocusIn>", on_focus_in)
        self.txt_isi.bind("<FocusOut>", on_focus_out)

        ctk.CTkButton(card, text="SIMPAN TULISAN", command=self.simpan_jurnal_action, text_color="white",
                      font=("Century Gothic", 13, "bold"), height=45, width=200, corner_radius=20,
                      fg_color=self.theme["btn_hover"], hover_color=self.theme["btn"]).pack(anchor="e", padx=20, pady=(0, 20))

    def simpan_jurnal_action(self ):
        isi_raw = self.txt_isi.get("1.0", "end").strip()
        placeholder_msg = "Silahkan isi ceritamu hari ini..." 

        if not isi_raw or isi_raw == placeholder_msg: 
            return messagebox.showwarning("Info", "Isi jurnal tidak boleh kosong.")
        
        if self.var_rating.get() == 0: 
            return messagebox.showwarning("Info", "Beri rating dulu!")
        
        judul = self.ent_judul.get().strip()
        rating = self.var_rating.get()
        
        try:
            msg=self.logic_journal.simpan_jurnal(self.current_user_id, judul, isi_raw, rating)
            self.refresh_app_state()
            self.apply_current_theme() 
            self.show_dashboard()
        except:
             messagebox.showerror("Error", f"Terjadi kesalahan tak terduga:\n{msg}")

# ================= HABIT =================
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
        habits = self.logic_habit.get_habits_harian(self.current_user_id)
        
        if not habits:
            empty_frame = ctk.CTkFrame(self.content_area, fg_color=self.theme["card"], corner_radius=20)
            empty_frame.pack(fill="both", expand=True, pady=20)
            ctk.CTkLabel(empty_frame, text="🌱", font=("Arial", 60)).pack(pady=(100, 10))
            ctk.CTkLabel(empty_frame, text="Belum ada habit.", text_color=self.theme["text"]).pack()
            return

        total_habit = len(habits)
        done_habit = sum([1 for h in habits if h[3] == 1])
        progress_val = done_habit / total_habit if total_habit > 0 else 0

        hero_card = ctk.CTkFrame(self.content_area, fg_color=self.theme["btn"], corner_radius=20)
        hero_card.pack(fill="x", pady=(0, 20), ipady=10)
        
        hero_left = ctk.CTkFrame(hero_card, fg_color="transparent")
        hero_left.pack(side="left", padx=25)
        ctk.CTkLabel(hero_left, text="Progres Hari Ini", font=("Arial", 14), text_color="white").pack(anchor="w")
        ctk.CTkLabel(hero_left, text=f"{done_habit} dari {total_habit} Selesai", font=("Century Gothic", 22, "bold"), text_color="white").pack(anchor="w")
        
        hero_right = ctk.CTkFrame(hero_card, fg_color="transparent")
        hero_right.pack(side="right", padx=25, fill="x", expand=True)
        
        prog_bar = ctk.CTkProgressBar(hero_right, height=15, corner_radius=10, 
                                      progress_color="white", 
                                      fg_color=self.theme["btn_hover"]) 
        prog_bar.set(progress_val)
        prog_bar.pack(fill="x", pady=15)

        scroll_frame = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True)

        def get_icon(nama):
            n = nama.lower()
            if "susu" in n: return "🥛"      
            if "sayur" in n: return "🥗"    
            if "buah" in n: return "🍎"    
            if "air" in n: return "💧"   
            
            if "minum" in n: return "💧"    
            if "makan" in n: return "🍽️"     
            
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
            
            ctk.CTkLabel(row, text=get_icon(nama), font=("Arial", 24), text_color=self.theme["text"]).pack(side="left", padx=(20, 10))
            
            info_box = ctk.CTkFrame(row, fg_color="transparent")
            info_box.pack(side="left", fill="both", expand=True, pady=10)
            
            font_nama = ("Arial", 14, "bold") 
            
            ctk.CTkLabel(info_box, text=nama, font=font_nama, text_color=self.theme["text"]).pack(anchor="w")
            ctk.CTkLabel(info_box, text=f"Target: {target}", font=("Arial", 12), text_color=self.theme["text"]).pack(anchor="w")

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