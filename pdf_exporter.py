from fpdf import FPDF

def export_to_pdf(title, node, change_type, summary, pre, procedure, rollback, post, approvals):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, title, align='C')

    def add_section(header, content):
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(0, 10, header, ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 10, content)

    add_section("Node Type", node)
    add_section("Change Type", change_type)
    add_section("Summary", summary)
    add_section("Pre-Checks", pre)
    add_section("Procedure", procedure)
    add_section("Rollback Plan", rollback)
    add_section("Post-Checks", post)
    add_section("Approvals", approvals)

    file_path = f"{title.replace(' ', '_')}.pdf"
    pdf.output(file_path)
