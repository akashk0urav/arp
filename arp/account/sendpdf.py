from django.http import HttpResponse ,FileResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import *
import tempfile
from django.conf import settings

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

from django.core.mail import EmailMessage

def send_monthly_statement(request):
    # Query the monthly data
    from datetime import date, timedelta
    today = date.today()
    start_date = today.replace(day=1)  # First day of the month
    end_date = today  # Today's date

    transactions = Transactions.objects.filter(sale_date__date__range=(start_date, end_date))
    expenses = Expenses.objects.filter(expenses_date__date__range=(start_date, end_date))
    add_items = AddItem.objects.filter(item_date__date__range=(start_date, end_date))

    # Generate the PDF
    pdf_path = generate_pdf(transactions, expenses, add_items)

    # Send the email
    subject = 'Subject with Attachment'
    message = 'Here is your attachment.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['arp.bajrangmenswear@gmail.com']

    email = EmailMessage(subject, message, from_email, recipient_list)
    email.attach_file(pdf_path)
    email.send()

    print("Monthly statement email sent successfully!")
    return HttpResponse("Monthly statement email sent successfully!")