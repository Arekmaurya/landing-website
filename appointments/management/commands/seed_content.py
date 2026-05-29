import json
import os
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from appointments.models import ClinicInformation, Credential, Review

class Command(BaseCommand):
    help = 'Seeds database models from the existing content.json file'

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        content_path = os.path.join(base_dir, 'data', 'content.json')
        
        if not os.path.exists(content_path):
            self.stdout.write(self.style.WARNING("No content.json found to seed from."))
            return
            
        with open(content_path, 'r') as f:
            content = json.load(f)
            
        # 1. Seed ClinicInformation
        contact = content.get('contact', {})
        working_hours = contact.get('working_hours', {})
        socials = contact.get('socials', {})
        
        clinic, created = ClinicInformation.objects.get_or_create(id=1)
        clinic.address = contact.get('address', '')
        clinic.phone = contact.get('phone', '')
        clinic.whatsapp = contact.get('whatsapp', '')
        clinic.weekdays_working_hours = working_hours.get('weekdays', '')
        clinic.saturday_working_hours = working_hours.get('saturday', '')
        clinic.sunday_working_hours = working_hours.get('sunday', '')
        clinic.map_link = contact.get('map_link', '')
        clinic.facebook_url = socials.get('facebook', '')
        clinic.twitter_url = socials.get('twitter', '')
        clinic.instagram_url = socials.get('instagram', '')
        clinic.linkedin_url = socials.get('linkedin', '')
        clinic.notification_method = content.get('notification_method', 'both')
        clinic.save()
        self.stdout.write(self.style.SUCCESS("Successfully seeded ClinicInformation."))
        
        # 2. Seed Credentials
        # Clear existing ones to prevent duplicates if run twice
        Credential.objects.all().delete()
        for order, text in enumerate(content.get('credentials', [])):
            Credential.objects.create(text=text, order=order)
        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {Credential.objects.count()} Credentials."))
        
        # 3. Seed Reviews
        Review.objects.all().delete()
        for review_data in content.get('reviews', []):
            name = review_data.get('name', '')
            initial = review_data.get('initial', '')
            stars = review_data.get('stars', 5)
            quote = review_data.get('quote', '')
            delay = review_data.get('delay', '0.1s')
            image_url = review_data.get('image', '')
            
            review = Review.objects.create(
                name=name,
                initial=initial,
                stars=stars,
                quote=quote
            )
            
            # Download remote images if present to local media storage
            if image_url and image_url.startswith('http'):
                try:
                    self.stdout.write(f"Downloading review photo for {name}...")
                    response = requests.get(image_url, timeout=10)
                    response.raise_for_status()
                    
                    filename = f"{name.lower().replace(' ', '_')}.jpg"
                    review.image.save(filename, ContentFile(response.content), save=True)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Failed to fetch image for {name}: {e}"))
            
        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {Review.objects.count()} Reviews."))
