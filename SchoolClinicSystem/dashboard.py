
import customtkinter as ctk
import sqlite3
from tkinter import messagebox


class DashboardWindow:
    def __init__(self):
        self.app = ctk.CTk()

        self.app.title("School Clinic Management System")
        self.app.geometry("1100x700")
        self.app.resizable(False, False)

        # Theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.app.configure(fg_color="#EAF4FF")

        # =========================
        # GET DATABASE STATISTICS
        # =========================
        total_patients, total_consultations, total_medicines, low_stock = (
            self.get_statistics()
        )

        # =========================
        # SIDEBAR
        # =========================
        sidebar = ctk.CTkFrame(
            self.app,
            width=250,
            corner_radius=0,
            fg_color="#1565C0"
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo = ctk.CTkLabel(
            sidebar,
            text="🏥",
            font=("Arial", 42)
        )
        logo.pack(pady=(45, 5))

        clinic_label = ctk.CTkLabel(
            sidebar,
            text="SCHOOL CLINIC",
            font=("Arial", 22, "bold"),
            text_color="white"
        )
        clinic_label.pack()

        system_label = ctk.CTkLabel(
            sidebar,
            text="Management System",
            font=("Arial", 13),
            text_color="#DDEEFF"
        )
        system_label.pack(pady=(0, 45))

        patient_button = ctk.CTkButton(
            sidebar,
            text="👤  Patient Visits",
            width=210,
            height=45,
            corner_radius=10,
            fg_color="#0D47A1",
            hover_color="#08306B",
            anchor="w",
            command=self.open_patient_visits
        )
        patient_button.pack(pady=7)

        medicine_button = ctk.CTkButton(
            sidebar,
            text="💊  Medicine Inventory",
            width=210,
            height=45,
            corner_radius=10,
            fg_color="#0D47A1",
            hover_color="#08306B",
            anchor="w",
            command=self.open_medicine_inventory
        )
        medicine_button.pack(pady=7)

        consultation_button = ctk.CTkButton(
            sidebar,
            text="📋  Consultation History",
            width=210,
            height=45,
            corner_radius=10,
            fg_color="#0D47A1",
            hover_color="#08306B",
            anchor="w",
            command=self.open_consultation
        )
        consultation_button.pack(pady=7)

        report_button = ctk.CTkButton(
            sidebar,
            text="📊  Reports",
            width=210,
            height=45,
            corner_radius=10,
            fg_color="#0D47A1",
            hover_color="#08306B",
            anchor="w",
            command=self.open_reports
        )
        report_button.pack(pady=7)

        # =========================
        # LOG OUT BUTTON
        # =========================
        logout_button = ctk.CTkButton(
            sidebar,
            text="🚪  Log Out",
            width=210,
            height=45,
            corner_radius=10,
            fg_color="#B71C1C",
            hover_color="#8E0000",
            anchor="w",
            command=self.logout
        )
        logout_button.pack(side="bottom", pady=25)

        # =========================
        # MAIN CONTENT
        # =========================
        content = ctk.CTkFrame(
            self.app,
            corner_radius=0,
            fg_color="#EAF4FF"
        )
        content.pack(side="right", fill="both", expand=True)

        welcome = ctk.CTkLabel(
            content,
            text="Welcome to the Clinic Dashboard",
            font=("Arial", 30, "bold"),
            text_color="#123B66"
        )
        welcome.pack(anchor="w", padx=45, pady=(50, 5))

        subtitle = ctk.CTkLabel(
            content,
            text=(
                "Manage patients, consultations, medicines, "
                "and clinic reports."
            ),
            font=("Arial", 16),
            text_color="#55708A"
        )
        subtitle.pack(anchor="w", padx=45, pady=(0, 35))

        # =========================
        # STATISTICS CARDS
        # =========================
        cards_frame = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )
        cards_frame.pack(fill="x", padx=40)

        self.create_card(
            cards_frame, "👤", str(total_patients),
            "Total Patients", 0
        )

        self.create_card(
            cards_frame, "📋", str(total_consultations),
            "Consultations", 1
        )

        self.create_card(
            cards_frame, "💊", str(total_medicines),
            "Medicines", 2
        )

        self.create_card(
            cards_frame, "⚠️", str(low_stock),
            "Low Stock", 3
        )

        # =========================
        # INFORMATION PANEL
        # =========================
        info = ctk.CTkFrame(
            content,
            corner_radius=18,
            fg_color="white"
        )
        info.pack(fill="x", padx=45, pady=40)

        info_title = ctk.CTkLabel(
            info,
            text="Clinic Management System",
            font=("Arial", 21, "bold"),
            text_color="#1565C0"
        )
        info_title.pack(anchor="w", padx=25, pady=(25, 5))

        info_text = ctk.CTkLabel(
            info,
            text=(
                "Use the navigation menu to manage patient visits, "
                "consultation records, medicine inventory, and reports."
            ),
            font=("Arial", 15),
            text_color="#55708A",
            justify="left"
        )
        info_text.pack(anchor="w", padx=25, pady=(0, 25))

        self.app.mainloop()

    # =========================
    # DATABASE STATISTICS
    # =========================
    def get_statistics(self):
        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM patients")
        total_patients = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM consultations")
        total_consultations = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM medicines")
        total_medicines = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM medicines WHERE quantity <= 5"
        )
        low_stock = cursor.fetchone()[0]

        connection.close()

        return (
            total_patients,
            total_consultations,
            total_medicines,
            low_stock
        )

    # =========================
    # DASHBOARD CARDS
    # =========================
    def create_card(self, parent, icon, number, title, column):
        card = ctk.CTkFrame(
            parent,
            width=150,
            height=150,
            corner_radius=18,
            fg_color="white"
        )
        card.grid(row=0, column=column, padx=6)
        card.grid_propagate(False)

        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=("Arial", 25)
        )
        icon_label.pack(pady=(15, 0))

        number_label = ctk.CTkLabel(
            card,
            text=number,
            font=("Arial", 26, "bold"),
            text_color="#1565C0"
        )
        number_label.pack()

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 12),
            text_color="#55708A"
        )
        title_label.pack(pady=2)

    # =========================
    # NAVIGATION
    # =========================
    def open_patient_visits(self):
        from patient_visits import PatientVisitsWindow
        PatientVisitsWindow()

    def open_medicine_inventory(self):
        from medicine_inventory import MedicineInventoryWindow
        MedicineInventoryWindow()

    def open_consultation(self):
        from consultation import ConsultationWindow
        ConsultationWindow()

    def open_reports(self):
        from reports import ReportsWindow
        ReportsWindow(self.app)

    # =========================
    # LOG OUT
    # =========================
    def logout(self):
        should_logout = messagebox.askyesno(
            "Confirm Log Out",
            "Are you sure you want to log out?",
            parent=self.app
        )

        if not should_logout:
            return

        self.app.destroy()

        from login import LoginWindow
        LoginWindow()


if __name__ == "__main__":
    DashboardWindow()