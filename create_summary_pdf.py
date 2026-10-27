import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

pdf_filename = "Java21_Syntax_Checker_Project_Summary.pdf"

# Printable area: 8.5 x 11 inches. Margins: 0.35 in left/right, 0.35 in top/bottom
doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=letter,
    leftMargin=0.38 * inch,
    rightMargin=0.38 * inch,
    topMargin=0.35 * inch,
    bottomMargin=0.35 * inch
)

styles = getSampleStyleSheet()

primary_color = colors.HexColor('#142a4a')    # Navy
accent_color = colors.HexColor('#00805a')     # Green
dark_neutral = colors.HexColor('#1f2328')     # Charcoal
light_bg = colors.HexColor('#f6f8fa')         # Cool gray
border_color = colors.HexColor('#d0d7de')     # GitHub border gray

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=21,
    textColor=primary_color,
    alignment=1,
    spaceAfter=2
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=12,
    textColor=colors.HexColor('#57606a'),
    alignment=1,
    spaceAfter=6
)

h1_style = ParagraphStyle(
    'Heading1_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10.5,
    leading=13,
    textColor=primary_color,
    spaceBefore=5,
    spaceAfter=3
)

body_style = ParagraphStyle(
    'Body_Custom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8.3,
    leading=11.2,
    textColor=dark_neutral,
    spaceAfter=3.5
)

bullet_style = ParagraphStyle(
    'Bullet_Custom',
    parent=body_style,
    leftIndent=12,
    firstLineIndent=-8,
    spaceAfter=2.5
)

table_header_style = ParagraphStyle(
    'TH_Style',
    fontName='Helvetica-Bold',
    fontSize=8,
    leading=10,
    textColor=colors.white,
    alignment=0
)

table_body_style = ParagraphStyle(
    'TB_Style',
    fontName='Helvetica',
    fontSize=7.5,
    leading=9.8,
    textColor=dark_neutral
)

table_bold_style = ParagraphStyle(
    'TB_Bold_Style',
    fontName='Helvetica-Bold',
    fontSize=7.5,
    leading=9.8,
    textColor=primary_color
)

story = []

# Header
story.append(Paragraph('Java 21 Syntax Checker & Web Application', title_style))
story.append(Paragraph('Course-Based Project (CBP) Executive Summary &middot; Department of Computer Science', subtitle_style))
story.append(HRFlowable(width='100%', thickness=1.2, color=primary_color, spaceAfter=5))

# 1. Project Overview
story.append(Paragraph('1. What is this Project? (In Simple Words)', h1_style))
p1 = (
    'Just like a spell-checker in Microsoft Word catches spelling and grammar mistakes in English before you send a document, '
    'this project is an automated <b>Syntax Checker for Java 21</b>. It reads any Java program and immediately verifies '
    'whether the code follows the official grammar and structure rules of the Java language.'
)
p2 = (
    'If the code is 100% correct, it displays a green <b>SUCCESS: Valid Java Syntax</b> banner. If there is a mistake '
    '(such as a missing semicolon, unclosed curly brace, or misplaced keyword), it instantly pinpoints the <b>exact line number</b> '
    'and the <b>offending symbol</b> that caused the problem, allowing the programmer to fix it in seconds.'
)
story.append(Paragraph(p1, body_style))
story.append(Paragraph(p2, body_style))

# 2. How it works
story.append(Paragraph('2. How Does It Work? (The 3 Simple Stages)', h1_style))
s1 = '<b>Stage 1: The Word Reader (Lexical Analyzer / Flex):</b> Reads your Java code character by character and groups them into recognized \"tokens\" (keywords like <i>class</i>, symbols like <i>{</i>, variable names, and numbers). It tracks exact line and column numbers throughout.'
s2 = '<b>Stage 2: The Grammar Checker (Parser / Bison):</b> Checks whether those tokens appear in a valid, legal order according to Java 21 grammar rules. If a rule is violated, it immediately stops and reports the exact line.'
s3 = '<b>Stage 3: The User Interface (Web & Desktop):</b> Users can write code or upload files either on an interactive website (accessible from any web browser or phone) or on a local desktop application.'
story.append(Paragraph('&bull; ' + s1, bullet_style))
story.append(Paragraph('&bull; ' + s2, bullet_style))
story.append(Paragraph('&bull; ' + s3, bullet_style))

# 3. Technology Stack Table
story.append(Paragraph('3. Technology Stack Table', h1_style))

table_data = [
    [
        Paragraph('Component', table_header_style),
        Paragraph('Technology Used', table_header_style),
        Paragraph('What It Does in Simple Words', table_header_style)
    ],
    [
        Paragraph('Lexical Analyzer (Lexer)', table_bold_style),
        Paragraph('GNU Flex 2.6', table_body_style),
        Paragraph('Scans code text and breaks it into recognizable tokens (words, symbols, operators) while tracking exact line numbers.', table_body_style)
    ],
    [
        Paragraph('Syntax Parser', table_bold_style),
        Paragraph('GNU Bison (LALR-1)', table_body_style),
        Paragraph('Verifies that the tokens follow official Java 21 grammar rules and pinpoints errors if grammar is broken.', table_body_style)
    ],
    [
        Paragraph('Native Engine Core', table_bold_style),
        Paragraph('C99 / GCC', table_body_style),
        Paragraph('Compiles the generated parser into a lightning-fast native binary (< 1 ms parsing execution time).', table_body_style)
    ],
    [
        Paragraph('Web Server Backend', table_bold_style),
        Paragraph('Python Flask & Gunicorn', table_body_style),
        Paragraph('Handles web requests, processes file uploads safely, and sends syntax results back to the browser.', table_body_style)
    ],
    [
        Paragraph('Web Frontend', table_bold_style),
        Paragraph('HTML5, CSS3, CodeMirror', table_body_style),
        Paragraph('Modern browser interface featuring a code editor with syntax highlighting, sample loader, and line error markers.', table_body_style)
    ],
    [
        Paragraph('Desktop GUI', table_bold_style),
        Paragraph('Python Tkinter', table_body_style),
        Paragraph('Alternative local desktop application with syntax error highlighting and line-number gutter.', table_body_style)
    ],
    [
        Paragraph('Containerization & Cloud', table_bold_style),
        Paragraph('Docker & Render Cloud', table_body_style),
        Paragraph('Packages the entire project into a self-contained container and hosts it live on the web for 24/7 public access.', table_body_style)
    ],
]

col_widths = [1.5 * inch, 1.5 * inch, 4.74 * inch]
tech_table = Table(table_data, colWidths=col_widths, repeatRows=1)
tech_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), primary_color),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, border_color),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg]),
    ('TOPPADDING', (0, 0), (-1, -1), 2.5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
]))
story.append(tech_table)

# 4. Key Highlights & Supported Java 21 Features
story.append(Paragraph('4. Key Features & Supported Java 21 Constructs', h1_style))
f1 = '<b>Modern Java 21 Support:</b> Validates advanced Java 21 features including Record Patterns deconstruction, Switch expressions with When-guards, Sealed classes/interfaces, Multi-dimensional array initializers, and Text blocks.'
f2 = '<b>Dual Access:</b> Works both as a responsive Web Application (accessible on mobile, tablet, or desktop) and as a standalone desktop application.'
f3 = '<b>Interactive Diagnostics:</b> Clicking \"Jump to Line\" in the web UI automatically scrolls the code editor directly to the offending line.'
f4 = '<b>Drag & Drop Upload:</b> Users can drop any .java file directly into the browser editor and modify it before checking.'
f5 = '<b>100% Automated Test Coverage:</b> Thoroughly verified across 109 automated tests (62 parser grammar tests, 19 web API tests, and 28 GUI integration tests) with a 100% pass rate.'
story.append(Paragraph('&bull; ' + f1, bullet_style))
story.append(Paragraph('&bull; ' + f2, bullet_style))
story.append(Paragraph('&bull; ' + f3, bullet_style))
story.append(Paragraph('&bull; ' + f4, bullet_style))
story.append(Paragraph('&bull; ' + f5, bullet_style))

# 5. Deployment Summary
story.append(Paragraph('5. Live Cloud Deployment on Render', h1_style))
dep_text = (
    'The application is fully containerized using a lightweight Linux <b>Docker</b> image and deployed on <b>Render Cloud</b> '
    'directly from GitHub (<code>ruokgif/java21-syntax-checker</code>). On Render, the Docker container automatically compiles '
    'the native C parser and starts the high-performance Gunicorn web server, providing a public URL accessible worldwide without '
    'requiring users to install any software.'
)
story.append(Paragraph(dep_text, body_style))

doc.build(story)

with open(pdf_filename, 'rb') as f:
    text = f.read().decode('latin1', errors='ignore')
pages = re.findall(r'/Type\s*/Page\b', text)
print("SUCCESS: PDF created at " + os.path.abspath(pdf_filename) + " | Total Pages: " + str(len(pages)))
