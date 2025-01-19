from django.http import HttpResponse ,FileResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import *
import tempfile

def generate_pdf(transaction,expenses,additems):
    html_string=render_to_string('pdf_template.html',{
        'context1':transaction,
        'context2':expenses,
        'context3':additems
    })

    with tempfile.NamedTemporaryFile(delete=False,suffix='.pdf') as output:
        HTML(string=html_string).write_pdf(output.name)
        return output.name

def download_pdf(request):
    transaction=Transactions.objects.all()
    expenses=Expenses.objects.all()
    additems=AddItem.objects.all()

    pdf_path=generate_pdf(transaction,expenses,additems)

    response = FileResponse(open(pdf_path, 'rb'), as_attachment=True, filename='statement.pdf')
    return response