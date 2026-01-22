from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(report_data, output_file):
    doc = SimpleDocTemplate(output_file)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>AI Media Plan Recommendation</b>", styles["Title"]))
    story.append(Paragraph(f"Client: {report_data['client']}", styles["Normal"]))
    story.append(Paragraph(f"Platform: {report_data['platform']}", styles["Normal"]))
    story.append(Paragraph(f"Time Band: {report_data['time_band']}", styles["Normal"]))
    story.append(Paragraph(f"Expected ROI: {report_data['expected_roi']}", styles["Normal"]))
    story.append(Paragraph("<br/>", styles["Normal"]))
    story.append(Paragraph("<b>Explanation</b>", styles["Heading2"]))
    story.append(Paragraph(report_data["explanation"], styles["Normal"]))

    doc.build(story)
