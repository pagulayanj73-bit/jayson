import customtkinter as ctk
import sqlite3
import csv
from tkinter import messagebox, filedialog


class ReportsWindow:
    def __init__(self, parent=None):
        self.app = ctk.CTkToplevel(parent) if parent else ctk.CTk()

        self.app.title("School Clinic - Reports")
        self.app.geometry("1100x750")
        self.app.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.app.configure(fg_color="#EAF4FF")

        header = ctk.CTkFrame(
            self.app,
            height=120,
            corner_radius=0,
            fg_color="#1565C0"
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="📊  CLINIC REPORTS",
            font=("Arial", 30, "bold"),
            text_color="white"
        ).pack(pady=(25, 3))

        ctk.CTkLabel(
            header,
            text="Clinic Records and Dispensing History",
            font=("Arial", 15),
            text_color="#DDEEFF"
        ).pack()

        summary_frame = ctk.CTkFrame(
            self.app,
            corner_radius=18,
            fg_color="white"
        )
        summary_frame.pack(
            pady=15,
            padx=35,
            fill="x"
        )

        ctk.CTkLabel(
            summary_frame,
            text="SYSTEM SUMMARY",
            font=("Arial", 20, "bold"),
            text_color="#1565C0"
        ).pack(pady=(15, 5))

        self.summary_label = ctk.CTkLabel(
            summary_frame,
            text="",
            font=("Arial", 14),
            text_color="#34536B",
            justify="left"
        )
        self.summary_label.pack(pady=(0, 15))

        report_frame = ctk.CTkFrame(
            self.app,
            corner_radius=18,
            fg_color="white"
        )
        report_frame.pack(
            pady=(0, 15),
            padx=35,
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            report_frame,
            text="CLINIC RECORDS",
            font=("Arial", 20, "bold"),
            text_color="#1565C0"
        ).pack(pady=(15, 5))

        self.report_text = ctk.CTkTextbox(
            report_frame,
            height=390,
            corner_radius=10,
            font=("Arial", 12)
        )
        self.report_text.pack(
            padx=20,
            pady=5,
            fill="both",
            expand=True
        )

        button_frame = ctk.CTkFrame(
            report_frame,
            fg_color="transparent"
        )
        button_frame.pack(pady=(5, 15))

        ctk.CTkButton(
            button_frame,
            text="🔄 REFRESH REPORT",
            width=180,
            height=42,
            corner_radius=9,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            font=("Arial", 13, "bold"),
            command=self.load_report
        ).grid(row=0, column=0, padx=8)

        ctk.CTkButton(
            button_frame,
            text="📁 EXPORT CSV",
            width=180,
            height=42,
            corner_radius=9,
            fg_color="#1565C0",
            hover_color="#0D47A1",
            font=("Arial", 13, "bold"),
            command=self.export_csv
        ).grid(row=0, column=1, padx=8)

        self.load_report()

        if not parent:
            self.app.mainloop()

    def get_data(self):
        connection = sqlite3.connect("clinic.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                patient_id,
                first_name,
                last_name,
                patient_type,
                contact_number
            FROM patients
            ORDER BY patient_id
        """)
        patients = cursor.fetchall()

        cursor.execute("""
            SELECT
                consultation_id,
                patient_id,
                consultation_date,
                symptoms,
                diagnosis,
                treatment
            FROM consultations
            ORDER BY consultation_id DESC
        """)
        consultations = cursor.fetchall()

        cursor.execute("""
            SELECT
                medicine_id,
                medicine_name,
                category,
                quantity,
                unit,
                expiration_date
            FROM medicines
            ORDER BY medicine_id
        """)
        medicines = cursor.fetchall()

        cursor.execute("""
            SELECT
                dt.transaction_id,
                dt.patient_id,
                p.first_name,
                p.last_name,
                dt.medicine_id,
                m.medicine_name,
                dt.quantity_dispensed,
                m.unit,
                dt.dispensing_date
            FROM dispensing_transactions dt
            JOIN patients p
                ON dt.patient_id = p.patient_id
            JOIN medicines m
                ON dt.medicine_id = m.medicine_id
            ORDER BY dt.transaction_id DESC
        """)
        dispensing = cursor.fetchall()

        connection.close()

        return patients, consultations, medicines, dispensing

    def load_report(self):
        try:
            (
                patients,
                consultations,
                medicines,
                dispensing
            ) = self.get_data()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Unable to load report:\n\n{error}"
            )
            return

        self.summary_label.configure(
            text=(
                f"Total Patients: {len(patients)}     |     "
                f"Consultations: {len(consultations)}     |     "
                f"Medicines: {len(medicines)}     |     "
                f"Dispensing Transactions: {len(dispensing)}"
            )
        )

        self.report_text.delete("1.0", "end")

        self.report_text.insert(
            "end",
            "=== PATIENT RECORDS ===\n\n"
        )

        if patients:
            for patient in patients:
                (
                    patient_id,
                    first_name,
                    last_name,
                    patient_type,
                    contact
                ) = patient

                self.report_text.insert(
                    "end",
                    f"Patient ID: {patient_id}\n"
                    f"Name: {first_name} {last_name}\n"
                    f"Type: {patient_type}\n"
                    f"Contact: {contact or 'N/A'}\n"
                    f"{'-' * 70}\n"
                )
        else:
            self.report_text.insert(
                "end",
                "No patient records found.\n"
            )

        self.report_text.insert(
            "end",
            "\n=== CONSULTATION RECORDS ===\n\n"
        )

        if consultations:
            for record in consultations:
                (
                    consultation_id,
                    patient_id,
                    consultation_date,
                    symptoms,
                    diagnosis,
                    treatment
                ) = record

                self.report_text.insert(
                    "end",
                    f"Consultation ID: {consultation_id}\n"
                    f"Patient ID: {patient_id}\n"
                    f"Date: {consultation_date}\n"
                    f"Symptoms: {symptoms or 'N/A'}\n"
                    f"Diagnosis: {diagnosis or 'N/A'}\n"
                    f"Treatment: {treatment or 'N/A'}\n"
                    f"{'-' * 70}\n"
                )
        else:
            self.report_text.insert(
                "end",
                "No consultation records found.\n"
            )

        self.report_text.insert(
            "end",
            "\n=== MEDICINE INVENTORY ===\n\n"
        )

        if medicines:
            for medicine in medicines:
                (
                    medicine_id,
                    name,
                    category,
                    quantity,
                    unit,
                    expiration
                ) = medicine

                self.report_text.insert(
                    "end",
                    f"Medicine ID: {medicine_id}\n"
                    f"Medicine: {name}\n"
                    f"Category: {category or 'N/A'}\n"
                    f"Stock: {quantity} {unit or ''}\n"
                    f"Expiration: {expiration or 'N/A'}\n"
                    f"{'-' * 70}\n"
                )
        else:
            self.report_text.insert(
                "end",
                "No medicine records found.\n"
            )

        self.report_text.insert(
            "end",
            "\n=== DISPENSING HISTORY ===\n\n"
        )

        if dispensing:
            for transaction in dispensing:
                (
                    transaction_id,
                    patient_id,
                    first_name,
                    last_name,
                    medicine_id,
                    medicine_name,
                    quantity,
                    unit,
                    dispensing_date
                ) = transaction

                self.report_text.insert(
                    "end",
                    f"Transaction ID: {transaction_id}\n"
                    f"Patient: {first_name} {last_name} "
                    f"(ID: {patient_id})\n"
                    f"Medicine: {medicine_name} "
                    f"(ID: {medicine_id})\n"
                    f"Quantity Dispensed: {quantity} {unit or ''}\n"
                    f"Date: {dispensing_date}\n"
                    f"{'-' * 70}\n"
                )
        else:
            self.report_text.insert(
                "end",
                "No dispensing transactions found.\n"
            )

    def export_csv(self):
        try:
            (
                patients,
                consultations,
                medicines,
                dispensing
            ) = self.get_data()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Unable to export report:\n\n{error}"
            )
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Clinic Report",
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        try:
            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "PATIENT RECORDS"
                ])

                writer.writerow([
                    "Patient ID",
                    "First Name",
                    "Last Name",
                    "Patient Type",
                    "Contact Number"
                ])

                writer.writerows(patients)

                writer.writerow([])
                writer.writerow([
                    "CONSULTATION RECORDS"
                ])

                writer.writerow([
                    "Consultation ID",
                    "Patient ID",
                    "Date",
                    "Symptoms",
                    "Diagnosis",
                    "Treatment"
                ])

                writer.writerows(consultations)

                writer.writerow([])
                writer.writerow([
                    "MEDICINE INVENTORY"
                ])

                writer.writerow([
                    "Medicine ID",
                    "Medicine Name",
                    "Category",
                    "Quantity",
                    "Unit",
                    "Expiration Date"
                ])

                writer.writerows(medicines)

                writer.writerow([])
                writer.writerow([
                    "DISPENSING HISTORY"
                ])

                writer.writerow([
                    "Transaction ID",
                    "Patient ID",
                    "Patient Name",
                    "Medicine ID",
                    "Medicine Name",
                    "Quantity",
                    "Unit",
                    "Dispensing Date"
                ])

                for transaction in dispensing:
                    (
                        transaction_id,
                        patient_id,
                        first_name,
                        last_name,
                        medicine_id,
                        medicine_name,
                        quantity,
                        unit,
                        dispensing_date
                    ) = transaction

                    writer.writerow([
                        transaction_id,
                        patient_id,
                        f"{first_name} {last_name}",
                        medicine_id,
                        medicine_name,
                        quantity,
                        unit,
                        dispensing_date
                    ])

            messagebox.showinfo(
                "Export Successful",
                "Clinic report exported successfully!"
            )

        except Exception as error:
            messagebox.showerror(
                "Export Error",
                f"Unable to export report:\n\n{error}"
            )


if __name__ == "__main__":
    ReportsWindow()