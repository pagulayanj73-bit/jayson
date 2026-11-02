import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from datetime import date


class ConsultationWindow:
    def __init__(self):
        self.app = ctk.CTk()

        self.app.title("School Clinic - Consultation Records")
        self.app.geometry("1100x720")
        self.app.resizable(False, False)

        # Theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.app.configure(fg_color="#EAF4FF")

        self.selected_consultation_id = None

        # =========================
        # HEADER
        # =========================

        header = ctk.CTkFrame(
            self.app,
            height=120,
            corner_radius=0,
            fg_color="#1565C0"
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="📋  CONSULTATION RECORDS",
            font=("Arial", 30, "bold"),
            text_color="white"
        )
        title.pack(pady=(25, 3))

        subtitle = ctk.CTkLabel(
            header,
            text="Patient Consultation and Visit History",
            font=("Arial", 15),
            text_color="#DDEEFF"
        )
        subtitle.pack()

        # =========================
        # FORM CARD
        # =========================

        form_frame = ctk.CTkFrame(
            self.app,
            corner_radius=18,
            fg_color="white"
        )
        form_frame.pack(
            pady=20,
            padx=35,
            fill="x"
        )

        form_title = ctk.CTkLabel(
            form_frame,
            text="CONSULTATION INFORMATION",
            font=("Arial", 20, "bold"),
            text_color="#1565C0"
        )
        form_title.grid(
            row=0,
            column=0,
            columnspan=4,
            pady=(18, 10)
        )

        # Patient ID
        ctk.CTkLabel(
            form_frame,
            text="Patient ID",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=1,
            column=0,
            padx=15,
            pady=8
        )

        self.patient_id_entry = ctk.CTkEntry(
            form_frame,
            width=210,
            height=38,
            corner_radius=8,
            placeholder_text="Enter Patient ID"
        )
        self.patient_id_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=8
        )

        # Date
        ctk.CTkLabel(
            form_frame,
            text="Date",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=1,
            column=2,
            padx=15,
            pady=8
        )

        self.date_entry = ctk.CTkEntry(
            form_frame,
            width=210,
            height=38,
            corner_radius=8
        )
        self.date_entry.grid(
            row=1,
            column=3,
            padx=10,
            pady=8
        )

        self.date_entry.insert(
            0,
            str(date.today())
        )

        # Symptoms
        ctk.CTkLabel(
            form_frame,
            text="Symptoms",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=2,
            column=0,
            padx=15,
            pady=8
        )

        self.symptoms_entry = ctk.CTkEntry(
            form_frame,
            width=210,
            height=38,
            corner_radius=8,
            placeholder_text="Enter symptoms"
        )
        self.symptoms_entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=8
        )

        # Diagnosis
        ctk.CTkLabel(
            form_frame,
            text="Diagnosis",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=2,
            column=2,
            padx=15,
            pady=8
        )

        self.diagnosis_entry = ctk.CTkEntry(
            form_frame,
            width=210,
            height=38,
            corner_radius=8,
            placeholder_text="Enter diagnosis"
        )
        self.diagnosis_entry.grid(
            row=2,
            column=3,
            padx=10,
            pady=8
        )

        # Treatment
        ctk.CTkLabel(
            form_frame,
            text="Treatment",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=3,
            column=0,
            padx=15,
            pady=8
        )

        self.treatment_entry = ctk.CTkEntry(
            form_frame,
            width=210,
            height=38,
            corner_radius=8,
            placeholder_text="Enter treatment"
        )
        self.treatment_entry.grid(
            row=3,
            column=1,
            padx=10,
            pady=8
        )

        # =========================
        # BUTTONS
        # =========================

        button_frame = ctk.CTkFrame(
            form_frame,
            fg_color="transparent"
        )
        button_frame.grid(
            row=4,
            column=0,
            columnspan=4,
            pady=(12, 20)
        )

        ctk.CTkButton(
            button_frame,
            text="ADD RECORD",
            width=150,
            height=40,
            corner_radius=9,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            font=("Arial", 13, "bold"),
            command=self.add_consultation
        ).grid(
            row=0,
            column=0,
            padx=6
        )

        ctk.CTkButton(
            button_frame,
            text="UPDATE",
            width=150,
            height=40,
            corner_radius=9,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            font=("Arial", 13, "bold"),
            command=self.update_consultation
        ).grid(
            row=0,
            column=1,
            padx=6
        )

        ctk.CTkButton(
            button_frame,
            text="DELETE",
            width=150,
            height=40,
            corner_radius=9,
            fg_color="#C62828",
            hover_color="#8E0000",
            font=("Arial", 13, "bold"),
            command=self.delete_consultation
        ).grid(
            row=0,
            column=2,
            padx=6
        )

        ctk.CTkButton(
            button_frame,
            text="CLEAR",
            width=150,
            height=40,
            corner_radius=9,
            fg_color="#607D8B",
            hover_color="#455A64",
            font=("Arial", 13, "bold"),
            command=self.clear_fields
        ).grid(
            row=0,
            column=3,
            padx=6
        )

        # =========================
        # CONSULTATION HISTORY
        # =========================

        list_frame = ctk.CTkFrame(
            self.app,
            corner_radius=18,
            fg_color="white"
        )
        list_frame.pack(
            pady=(0, 20),
            padx=35,
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            list_frame,
            text="CONSULTATION HISTORY",
            font=("Arial", 20, "bold"),
            text_color="#1565C0"
        ).pack(pady=(15, 8))

        self.consultation_list = ctk.CTkTextbox(
            list_frame,
            height=185,
            corner_radius=10,
            font=("Arial", 12)
        )
        self.consultation_list.pack(
            padx=20,
            pady=5,
            fill="both",
            expand=True
        )

        # =========================
        # SELECT RECORD
        # =========================

        select_frame = ctk.CTkFrame(
            list_frame,
            fg_color="transparent"
        )
        select_frame.pack(pady=(5, 15))

        ctk.CTkLabel(
            select_frame,
            text="Consultation ID:",
            font=("Arial", 13, "bold"),
            text_color="#34536B"
        ).grid(
            row=0,
            column=0,
            padx=8
        )

        self.consultation_id_entry = ctk.CTkEntry(
            select_frame,
            width=170,
            height=38,
            corner_radius=8,
            placeholder_text="Consultation ID"
        )
        self.consultation_id_entry.grid(
            row=0,
            column=1,
            padx=8
        )

        ctk.CTkButton(
            select_frame,
            text="SELECT RECORD",
            width=160,
            height=38,
            corner_radius=9,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            command=self.select_consultation
        ).grid(
            row=0,
            column=2,
            padx=8
        )

        self.load_consultations()

        self.app.mainloop()

    # =========================
    # ADD CONSULTATION
    # =========================

    def add_consultation(self):
        patient_id = self.patient_id_entry.get().strip()
        consultation_date = self.date_entry.get().strip()
        symptoms = self.symptoms_entry.get().strip()
        diagnosis = self.diagnosis_entry.get().strip()
        treatment = self.treatment_entry.get().strip()

        if not patient_id:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the Patient ID."
            )
            return

        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT patient_id FROM patients WHERE patient_id = ?",
            (patient_id,)
        )

        patient = cursor.fetchone()

        if patient is None:
            connection.close()

            messagebox.showerror(
                "Patient Not Found",
                "The Patient ID does not exist."
            )
            return

        cursor.execute("""
            INSERT INTO consultations
            (
                patient_id,
                consultation_date,
                symptoms,
                diagnosis,
                treatment
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            patient_id,
            consultation_date,
            symptoms,
            diagnosis,
            treatment
        ))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Consultation record added successfully!"
        )

        self.clear_fields()
        self.load_consultations()

    # =========================
    # LOAD CONSULTATIONS
    # =========================

    def load_consultations(self):
        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                c.consultation_id,
                c.patient_id,
                p.first_name,
                p.last_name,
                c.consultation_date,
                c.symptoms,
                c.diagnosis,
                c.treatment
            FROM consultations c
            JOIN patients p
                ON c.patient_id = p.patient_id
            ORDER BY c.consultation_id DESC
        """)

        records = cursor.fetchall()
        connection.close()

        self.consultation_list.delete(
            "1.0",
            "end"
        )

        if not records:
            self.consultation_list.insert(
                "end",
                "No consultation records yet."
            )
            return

        for record in records:
            (
                consultation_id,
                patient_id,
                first_name,
                last_name,
                consultation_date,
                symptoms,
                diagnosis,
                treatment
            ) = record

            self.consultation_list.insert(
                "end",
                f"Consultation ID: {consultation_id}\n"
                f"Patient ID: {patient_id}\n"
                f"Patient: {first_name} {last_name}\n"
                f"Date: {consultation_date}\n"
                f"Symptoms: {symptoms}\n"
                f"Diagnosis: {diagnosis}\n"
                f"Treatment: {treatment}\n"
                f"{'-' * 70}\n"
            )

    # =========================
    # SELECT CONSULTATION
    # =========================

    def select_consultation(self):
        consultation_id = (
            self.consultation_id_entry
            .get()
            .strip()
        )

        if not consultation_id:
            messagebox.showwarning(
                "Missing ID",
                "Please enter a Consultation ID."
            )
            return

        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                patient_id,
                consultation_date,
                symptoms,
                diagnosis,
                treatment
            FROM consultations
            WHERE consultation_id = ?
        """, (consultation_id,))

        record = cursor.fetchone()
        connection.close()

        if record is None:
            messagebox.showerror(
                "Not Found",
                "Consultation ID not found."
            )
            return

        self.selected_consultation_id = consultation_id

        self.patient_id_entry.delete(0, "end")
        self.patient_id_entry.insert(0, record[0])

        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, record[1])

        self.symptoms_entry.delete(0, "end")
        self.symptoms_entry.insert(0, record[2] or "")

        self.diagnosis_entry.delete(0, "end")
        self.diagnosis_entry.insert(0, record[3] or "")

        self.treatment_entry.delete(0, "end")
        self.treatment_entry.insert(0, record[4] or "")

        messagebox.showinfo(
            "Record Selected",
            f"Consultation ID {consultation_id} selected."
        )

    # =========================
    # UPDATE CONSULTATION
    # =========================

    def update_consultation(self):
        if self.selected_consultation_id is None:
            messagebox.showwarning(
                "No Record Selected",
                "Please select a consultation record first."
            )
            return

        patient_id = self.patient_id_entry.get().strip()
        consultation_date = self.date_entry.get().strip()
        symptoms = self.symptoms_entry.get().strip()
        diagnosis = self.diagnosis_entry.get().strip()
        treatment = self.treatment_entry.get().strip()

        if not patient_id:
            messagebox.showwarning(
                "Missing Information",
                "Patient ID is required."
            )
            return

        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT patient_id FROM patients WHERE patient_id = ?",
            (patient_id,)
        )

        if cursor.fetchone() is None:
            connection.close()

            messagebox.showerror(
                "Patient Not Found",
                "The Patient ID does not exist."
            )
            return

        cursor.execute("""
            UPDATE consultations
            SET patient_id = ?,
                consultation_date = ?,
                symptoms = ?,
                diagnosis = ?,
                treatment = ?
            WHERE consultation_id = ?
        """, (
            patient_id,
            consultation_date,
            symptoms,
            diagnosis,
            treatment,
            self.selected_consultation_id
        ))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Consultation record updated successfully!"
        )

        self.clear_fields()
        self.load_consultations()

    # =========================
    # DELETE CONSULTATION
    # =========================

    def delete_consultation(self):
        if self.selected_consultation_id is None:
            messagebox.showwarning(
                "No Record Selected",
                "Please select a consultation record first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this consultation?"
        )

        if not confirm:
            return

        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM consultations
            WHERE consultation_id = ?
        """, (self.selected_consultation_id,))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Deleted",
            "Consultation record deleted successfully!"
        )

        self.clear_fields()
        self.load_consultations()

    # =========================
    # CLEAR
    # =========================

    def clear_fields(self):
        self.patient_id_entry.delete(0, "end")
        self.consultation_id_entry.delete(0, "end")

        self.date_entry.delete(0, "end")
        self.date_entry.insert(
            0,
            str(date.today())
        )

        self.symptoms_entry.delete(0, "end")
        self.diagnosis_entry.delete(0, "end")
        self.treatment_entry.delete(0, "end")

        self.selected_consultation_id = None


if __name__ == "__main__":
    ConsultationWindow()