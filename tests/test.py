from fpdf import FPDF 


# PDF-Objekt erstellen
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Willkommen zu Python PDF Erstellung!", ln=True, align='C')

# PDF speichern
pdf.output("example.pdf")