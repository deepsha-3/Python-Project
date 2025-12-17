from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

# Receipt data
DATA = [
    ["Started Date", "Course", "Time", "Amount"],
    ["05/01/2026", "Full Stack Development", "1 year", "10,000/-"],
    ["16/11/2025", "Coding Classes", "6 months", "5,000/-"],
    ["12/12/2025", "Basic Computer Classes", " 3 months", "3000/-"],
   
  
]

# Create PDF document
pdf = SimpleDocTemplate("receipt.pdf", pagesize=A4)

# Title style
styles = getSampleStyleSheet()
title_style = styles["Heading1"]
title_style.alignment = 1  # Center alignment

title = Paragraph("Tech_With_Dee", title_style)

# Table style
style = TableStyle([
    ("BOX", (0, 0), (-1, -1), 1, colors.black),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ("FONTSIZE", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
])

# Create table with column widths
table = Table(DATA, colWidths=[100, 200, 100, 100], style=style)

# Build PDF
pdf.build([title, table])
