from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import Donation, Receipt
from stories.models import Story
from .forms import DonationForm
import uuid
import os


@login_required
def make_donation(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES, story=story)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.story = story
            donation.save()
            
            messages.success(request, 'Donation submitted successfully! It will be verified by admin.')
            return redirect('donor_dashboard')
    else:
        form = DonationForm(story=story)
    
    context = {
        'form': form,
        'story': story,
    }
    return render(request, 'donations/make_donation.html', context)


@login_required
def admin_donation_verification(request):
    # Only accessible to admin users
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin access required.')
        return redirect('home')
    
    pending_donations = Donation.objects.filter(status='pending').order_by('-donation_date')
    
    context = {
        'pending_donations': pending_donations,
    }
    return render(request, 'donations/admin_donation_verification.html', context)


@login_required
def verify_donation(request, donation_id):
    # Only accessible to admin users
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin access required.')
        return redirect('home')
    
    donation = get_object_or_404(Donation, id=donation_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['confirmed', 'rejected']:
            # Handle changing from confirmed to rejected or vice versa
            old_status = donation.status
            donation.status = status
            donation.save()
            
            # Update story's collected amount based on status changes
            if old_status == 'confirmed' and status == 'rejected':
                # Donation was confirmed but is now rejected, subtract amount
                donation.story.collected_amount -= donation.amount
                donation.story.save()
            elif old_status == 'rejected' and status == 'confirmed':
                # Donation was rejected but is now confirmed, add amount
                donation.story.collected_amount += donation.amount
                donation.story.save()
            elif old_status != 'confirmed' and status == 'confirmed':
                # Donation is newly confirmed, add amount
                donation.story.collected_amount += donation.amount
                donation.story.save()
            
            # Generate receipt only when donation is confirmed for the first time
            if status == 'confirmed' and not hasattr(donation, 'receipt'):
                generate_receipt(donation)
            
            messages.success(request, f'Donation status updated to {donation.get_status_display()}.')
        else:
            messages.error(request, 'Invalid status selected.')
        
        return redirect('admin_donation_verification')
    
    context = {
        'donation': donation,
    }
    return render(request, 'donations/verify_donation.html', context)


def generate_receipt(donation):
    """Generate a receipt for a confirmed donation"""
    # Create receipt number
    receipt_number = f"RCP-{uuid.uuid4().hex[:8].upper()}"
    
    # Create receipt object
    receipt = Receipt.objects.create(
        donation=donation,
        receipt_number=receipt_number
    )
    
    # Generate PDF receipt
    pdf_filename = f"receipt_{receipt_number}.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'receipts', pdf_filename)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    
    # Create PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story_pdf = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.darkblue
    )
    title = Paragraph('Donation Receipt', title_style)
    story_pdf.append(title)
    story_pdf.append(Spacer(1, 20))
    
    # Donation details
    details = [
        f'<b>Receipt Number:</b> {receipt_number}',
        f'<b>Donor Name:</b> {donation.donor.get_full_name() or donation.donor.username}',
        f'<b>Story Name:</b> {donation.story.title}',
        f'<b>Amount:</b> ${donation.amount}',
        f'<b>Date:</b> {donation.donation_date.strftime("%Y-%m-%d %H:%M:%S")}',
        f'<b>Transaction ID:</b> {donation.transaction_id or "N/A"}',
    ]
    
    for detail in details:
        p = Paragraph(detail, styles['Normal'])
        story_pdf.append(p)
        story_pdf.append(Spacer(1, 12))
    
    # Footer
    footer = Paragraph('Thank you for your generous donation!', styles['Normal'])
    story_pdf.append(Spacer(1, 50))
    story_pdf.append(footer)
    
    # Build PDF
    doc.build(story_pdf)
    
    # Save PDF path to receipt object
    receipt.pdf_file.name = f'receipts/{pdf_filename}'
    receipt.save()
    
    return receipt


@login_required
def download_receipt(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    
    # Only allow donor or admin to download receipt
    if donation.donor != request.user and request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if not hasattr(donation, 'receipt'):
        messages.error(request, 'Receipt not available for this donation.')
        return redirect('donor_dashboard')
    
    receipt = donation.receipt
    
    if not receipt.pdf_file:
        messages.error(request, 'Receipt file not found.')
        return redirect('donor_dashboard')
    
    # Serve the PDF file
    file_path = os.path.join(settings.MEDIA_ROOT, receipt.pdf_file.name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    else:
        raise Http404('Receipt file not found')
