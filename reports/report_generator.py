from reports.ppt_template import create_ppt
from reports.pdf_generator import create_pdf

def generate_reports(report_data):
    create_ppt(report_data, "client_media_plan.pptx")
    create_pdf(report_data, "client_media_plan.pdf")

    return {
        "ppt": "client_media_plan.pptx",
        "pdf": "client_media_plan.pdf"
    }
