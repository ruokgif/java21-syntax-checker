"""
PDF Generator for Java 21 Syntax Checker Documentation Package
Generates 20 high-quality, professional, academic PDF documents in documentation/
Zero external dependencies (uses pure Python standard library to emit valid PDF 1.4).
"""

import os
import sys
import re

class PDFBuilder:
    def __init__(self, title, doc_num, category="Course-Based Project Documentation"):
        self.doc_title = title
        self.doc_num = doc_num
        self.category = category
        self.pages = []  # list of byte strings (page content streams)
        self.current_stream = []
        
        # Dimensions & Margins (Points: 72 points = 1 inch)
        self.width = 612.0   # 8.5 in (Letter)
        self.height = 792.0  # 11.0 in
        self.margin_x = 50.0
        self.margin_top = 54.0
        self.margin_bottom = 54.0
        self.content_width = self.width - (2 * self.margin_x)  # 512 pt
        
        self.y = self.height - self.margin_top
        self.page_count = 0
        self._start_new_page()

    def _start_new_page(self):
        self.page_count += 1
        self.y = self.height - self.margin_top
        self.current_stream = []

    def _flush_page(self):
        # Add header and footer to current page stream
        hf_stream = []
        
        # Header (Only on page > 1)
        if self.page_count > 1:
            hf_stream.append("q")
            hf_stream.append("0.1 0.2 0.35 rg")  # Dark navy
            hf_stream.append(f"BT /F2 8.5 Tf {self.margin_x} {self.height - 36} Td ({self._escape_pdf(self.doc_num + ': ' + self.doc_title)}) Tj ET")
            hf_stream.append("0.7 0.7 0.75 RG 0.5 w")
            hf_stream.append(f"{self.margin_x} {self.height - 42} m {self.width - self.margin_x} {self.height - 42} l S")
            hf_stream.append("Q")
            
        # Footer (On all pages)
        hf_stream.append("q")
        hf_stream.append("0.7 0.7 0.75 RG 0.5 w")
        hf_stream.append(f"{self.margin_x} {self.margin_bottom - 12} m {self.width - self.margin_x} {self.margin_bottom - 12} l S")
        hf_stream.append("0.35 0.4 0.45 rg")
        hf_stream.append(f"BT /F1 8 Tf {self.margin_x} {self.margin_bottom - 24} Td (Java 21 Syntax Checker | GNU Flex & Bison LALR\\(1\\)) Tj ET")
        hf_stream.append(f"BT /F2 8 Tf {self.width - self.margin_x - 60} {self.margin_bottom - 24} Td (Page {self.page_count}) Tj ET")
        hf_stream.append("Q")
        
        full_content = "\n".join(hf_stream) + "\n" + "\n".join(self.current_stream)
        self.pages.append(full_content.encode('latin1', 'replace'))

    def check_space(self, needed_pts):
        if self.y - needed_pts < self.margin_bottom:
            self._flush_page()
            self._start_new_page()
            if self.page_count > 1:
                self.y = self.height - self.margin_top - 10

    def _escape_pdf(self, text):
        return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

    def add_title_header(self, subtitle="Compiler Design Course-Based Project"):
        self.check_space(95)
        # Decorative Title Box
        box_top = self.y
        box_h = 75
        
        cmds = [
            "q",
            # Navy Banner Background
            "0.05 0.18 0.35 rg",
            f"{self.margin_x} {box_top - box_h} {self.content_width} {box_h} re f",
            # Gold/Cyan Accent left bar
            "0.1 0.6 0.85 rg",
            f"{self.margin_x} {box_top - box_h} 6 {box_h} re f",
            # Category text
            "0.85 0.92 1.0 rg",
            f"BT /F2 9 Tf {self.margin_x + 16} {box_top - 18} Td ({self._escape_pdf(self.category.upper())} | {self._escape_pdf(self.doc_num)}) Tj ET",
            # Title text
            "1 1 1 rg",
            f"BT /F2 16 Tf {self.margin_x + 16} {box_top - 40} Td ({self._escape_pdf(self.doc_title)}) Tj ET",
            # Subtitle text
            "0.8 0.85 0.9 rg",
            f"BT /F1 9.5 Tf {self.margin_x + 16} {box_top - 58} Td ({self._escape_pdf(subtitle)}) Tj ET",
            "Q"
        ]
        self.current_stream.append("\n".join(cmds))
        self.y -= (box_h + 20)

    def add_heading_1(self, text):
        self.check_space(38)
        cmds = [
            "q",
            # Heading bar
            "0.08 0.25 0.45 rg",
            f"{self.margin_x} {self.y - 15} 3 14 re f",
            f"BT /F2 12.5 Tf {self.margin_x + 8} {self.y - 13} Td ({self._escape_pdf(text)}) Tj ET",
            "0.8 0.85 0.9 RG 0.75 w",
            f"{self.margin_x} {self.y - 18} m {self.width - self.margin_x} {self.y - 18} l S",
            "Q"
        ]
        self.current_stream.append("\n".join(cmds))
        self.y -= 28

    def add_heading_2(self, text):
        self.check_space(28)
        cmds = [
            "q",
            "0.15 0.3 0.5 rg",
            f"BT /F2 10.5 Tf {self.margin_x} {self.y - 10} Td ({self._escape_pdf(text)}) Tj ET",
            "Q"
        ]
        self.current_stream.append("\n".join(cmds))
        self.y -= 18

    def add_heading_3(self, text):
        self.check_space(22)
        cmds = [
            "q",
            "0.25 0.35 0.45 rg",
            f"BT /F2 9.5 Tf {self.margin_x} {self.y - 9} Td ({self._escape_pdf(text)}) Tj ET",
            "Q"
        ]
        self.current_stream.append("\n".join(cmds))
        self.y -= 15

    def _wrap_text(self, text, font_size=9.5, max_width=None, font_type='F1'):
        if max_width is None:
            max_width = self.content_width
        
        char_w = 0.52 * font_size if font_type in ['F1', 'F2'] else 0.6 * font_size
        max_chars = max(10, int(max_width / char_w))
        
        words = text.split(' ')
        lines = []
        curr = []
        curr_len = 0
        
        for w in words:
            w_len = len(w)
            if curr and (curr_len + 1 + w_len) > max_chars:
                lines.append(' '.join(curr))
                curr = [w]
                curr_len = w_len
            else:
                curr.append(w)
                curr_len += (w_len + (1 if curr_len > 0 else 0))
        if curr:
            lines.append(' '.join(curr))
        return lines

    def add_paragraph(self, text, space_after=8, font_size=9.2, leading=13.0, color=(0.15, 0.18, 0.22)):
        lines = self._wrap_text(text, font_size=font_size, max_width=self.content_width)
        needed = (len(lines) * leading) + space_after
        self.check_space(needed)
        
        cmds = ["q", f"{color[0]} {color[1]} {color[2]} rg"]
        for line in lines:
            self.y -= leading
            cmds.append(f"BT /F1 {font_size} Tf {self.margin_x} {self.y} Td ({self._escape_pdf(line)}) Tj ET")
        cmds.append("Q")
        self.current_stream.append("\n".join(cmds))
        self.y -= space_after

    def add_bullet(self, text, prefix="•", level=1, font_size=9.0, leading=12.5):
        indent = self.margin_x + (level * 14)
        bullet_w = 12
        text_w = self.content_width - (level * 14) - bullet_w
        lines = self._wrap_text(text, font_size=font_size, max_width=text_w)
        
        needed = (len(lines) * leading) + 4
        self.check_space(needed)
        
        cmds = [
            "q",
            "0.1 0.4 0.7 rg",
            f"BT /F2 {font_size} Tf {indent} {self.y - leading} Td ({self._escape_pdf(prefix)}) Tj ET",
            "0.15 0.18 0.22 rg"
        ]
        
        first = True
        for line in lines:
            self.y -= leading
            x_pos = indent + bullet_w
            cmds.append(f"BT /F1 {font_size} Tf {x_pos} {self.y} Td ({self._escape_pdf(line)}) Tj ET")
        cmds.append("Q")
        self.current_stream.append("\n".join(cmds))
        self.y -= 4

    def add_callout(self, text, title="KEY POINT", style="info"):
        lines = self._wrap_text(text, font_size=8.8, max_width=self.content_width - 24)
        leading = 12.0
        box_h = (len(lines) * leading) + 26
        self.check_space(box_h + 8)
        
        # Colors based on style
        if style == "info":
            bg = "0.94 0.97 1.0"
            border = "0.1 0.5 0.8"
            title_color = "0.05 0.3 0.55"
        elif style == "success":
            bg = "0.93 0.98 0.95"
            border = "0.15 0.65 0.35"
            title_color = "0.08 0.45 0.2"
        elif style == "warning":
            bg = "1.0 0.96 0.93"
            border = "0.85 0.4 0.1"
            title_color = "0.6 0.25 0.05"
        else: # note
            bg = "0.96 0.96 0.97"
            border = "0.4 0.45 0.5"
            title_color = "0.2 0.25 0.3"
            
        cmds = [
            "q",
            # Background
            f"{bg} rg",
            f"{self.margin_x} {self.y - box_h} {self.content_width} {box_h} re f",
            # Left bar
            f"{border} rg",
            f"{self.margin_x} {self.y - box_h} 4 {box_h} re f",
            # Title
            f"{title_color} rg",
            f"BT /F2 8.5 Tf {self.margin_x + 12} {self.y - 14} Td ({self._escape_pdf(title)}) Tj ET",
            # Content
            "0.15 0.2 0.25 rg"
        ]
        
        curr_y = self.y - 26
        for line in lines:
            cmds.append(f"BT /F1 8.8 Tf {self.margin_x + 12} {curr_y} Td ({self._escape_pdf(line)}) Tj ET")
            curr_y -= leading
            
        cmds.append("Q")
        self.current_stream.append("\n".join(cmds))
        self.y -= (box_h + 8)

    def add_code_block(self, code_text, font_size=7.5, leading=10.5):
        raw_lines = code_text.strip().split('\n')
        wrapped_lines = []
        for rl in raw_lines:
            # Wrap long code lines
            if len(rl) > 85:
                wrapped_lines.append(rl[:85])
                wrapped_lines.append("  " + rl[85:])
            else:
                wrapped_lines.append(rl)
                
        box_h = (len(wrapped_lines) * leading) + 14
        self.check_space(box_h + 8)
        
        cmds = [
            "q",
            # Dark code background
            "0.12 0.14 0.18 rg",
            f"{self.margin_x} {self.y - box_h} {self.content_width} {box_h} re f",
            # Border
            "0.25 0.3 0.38 RG 0.5 w",
            f"{self.margin_x} {self.y - box_h} {self.content_width} {box_h} re S",
            # Code text
            "0.85 0.9 0.95 rg"
        ]
        
        curr_y = self.y - 10
        for line in wrapped_lines:
            cmds.append(f"BT /F3 {font_size} Tf {self.margin_x + 10} {curr_y} Td ({self._escape_pdf(line)}) Tj ET")
            curr_y -= leading
            
        cmds.append("Q")
        self.current_stream.append("\n".join(cmds))
        self.y -= (box_h + 8)

    def add_table(self, headers, rows, col_ratios=None):
        num_cols = len(headers)
        if col_ratios is None:
            col_widths = [self.content_width / num_cols] * num_cols
        else:
            total_ratio = sum(col_ratios)
            col_widths = [(r / total_ratio) * self.content_width for r in col_ratios]
            
        # Estimate height
        header_h = 20
        row_h = 16
        total_h = header_h + (len(rows) * row_h)
        self.check_space(min(total_h, 120))
        
        cmds = ["q"]
        
        # Header background
        cmds.append("0.08 0.22 0.4 rg")
        cmds.append(f"{self.margin_x} {self.y - header_h} {self.content_width} {header_h} re f")
        
        # Header text
        cmds.append("1 1 1 rg")
        x_off = self.margin_x
        for i, h in enumerate(headers):
            cmds.append(f"BT /F2 8.5 Tf {x_off + 6} {self.y - 13} Td ({self._escape_pdf(h)}) Tj ET")
            x_off += col_widths[i]
            
        self.y -= header_h
        
        # Rows
        for r_idx, row in enumerate(rows):
            self.check_space(row_h + 4)
            # Alternating background
            if r_idx % 2 == 1:
                cmds.append("0.95 0.97 0.99 rg")
                cmds.append(f"{self.margin_x} {self.y - row_h} {self.content_width} {row_h} re f")
                
            # Row bottom border
            cmds.append("0.85 0.88 0.92 RG 0.5 w")
            cmds.append(f"{self.margin_x} {self.y - row_h} m {self.width - self.margin_x} {self.y - row_h} l S")
            
            # Cell text
            cmds.append("0.15 0.18 0.22 rg")
            x_off = self.margin_x
            for c_idx, cell in enumerate(row):
                cell_str = str(cell)
                # truncate if too long
                max_ch = int(col_widths[c_idx] / 5.0)
                if len(cell_str) > max_ch:
                    cell_str = cell_str[:max_ch-3] + "..."
                cmds.append(f"BT /F1 8.2 Tf {x_off + 6} {self.y - 11} Td ({self._escape_pdf(cell_str)}) Tj ET")
                x_off += col_widths[c_idx]
                
            self.y -= row_h
            
        cmds.append("Q")
        self.current_stream.append("\n".join(cmds))
        self.y -= 10

    def add_viva_qa(self, q_num, question, answer, viva_bullet):
        self.check_space(65)
        # Question Title
        cmds = [
            "q",
            "0.08 0.25 0.45 rg",
            f"BT /F2 9.5 Tf {self.margin_x} {self.y - 10} Td ({self._escape_pdf(f'Q{q_num}: {question}')}) Tj ET",
            "Q"
        ]
        self.current_stream.append("\n".join(cmds))
        self.y -= 16
        
        # Answer
        self.add_paragraph(f"Answer: {answer}", space_after=4, font_size=8.8, leading=12.0)
        
        # Viva bullet callout
        bullet_text = f"Viva Bullet: \"{viva_bullet}\""
        self.add_callout(bullet_text, title="EXAMINER KEY PHRASE", style="note")
        self.y -= 4

    def save(self, filepath):
        self._flush_page()
        
        # Construct PDF 1.4 objects
        objects = []
        
        # 1: Catalog
        objects.append("<< /Type /Catalog /Pages 2 0 R >>")
        
        # 2: Pages Collection
        kids = " ".join([f"{3 + i*2} 0 R" for i in range(len(self.pages))])
        objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(self.pages)} >>")
        
        # Font Objects
        # F1: Helvetica, F2: Helvetica-Bold, F3: Courier, F4: Courier-Bold
        font_f1 = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
        font_f2 = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"
        font_f3 = "<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>"
        font_f4 = "<< /Type /Font /Subtype /Type1 /BaseFont /Courier-Bold >>"
        
        f1_obj_idx = 3 + (len(self.pages) * 2)
        f2_obj_idx = f1_obj_idx + 1
        f3_obj_idx = f2_obj_idx + 1
        f4_obj_idx = f3_obj_idx + 1
        
        # Add Page objects and Content stream objects
        for p_idx, p_stream in enumerate(self.pages):
            content_obj_idx = 4 + (p_idx * 2)
            page_obj = (
                f"<< /Type /Page /Parent 2 0 R "
                f"/MediaBox [0 0 {self.width} {self.height}] "
                f"/Contents {content_obj_idx} 0 R "
                f"/Resources << /Font << /F1 {f1_obj_idx} 0 R /F2 {f2_obj_idx} 0 R /F3 {f3_obj_idx} 0 R /F4 {f4_obj_idx} 0 R >> >> >>"
            )
            objects.append(page_obj)
            
            # Content Stream Object
            stream_obj = f"<< /Length {len(p_stream)} >>\nstream\n" + p_stream.decode('latin1') + "\nendstream"
            objects.append(stream_obj)
            
        # Append fonts
        objects.append(font_f1)
        objects.append(font_f2)
        objects.append(font_f3)
        objects.append(font_f4)
        
        # Write PDF binary
        with open(filepath, "wb") as f:
            f.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
            offsets = []
            
            for i, obj in enumerate(objects):
                offsets.append(f.tell())
                obj_str = f"{i+1} 0 obj\n{obj}\nendobj\n"
                f.write(obj_str.encode('latin1'))
                
            xref_pos = f.tell()
            f.write(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode('latin1'))
            for off in offsets:
                f.write(f"{off:010d} 00000 n \n".encode('latin1'))
                
            trailer = f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n"
            f.write(trailer.encode('latin1'))
            
        print(f"[SUCCESS] Generated: {filepath} ({len(self.pages)} pages)")

print("PDFBuilder module ready.")
