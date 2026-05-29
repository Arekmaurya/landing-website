from django.db import models

class ClinicInformation(models.Model):
    """Stores all contact info, location map, hours, socials, and notification settings."""
    address = models.TextField(default="123 Medical Arcade, Suite 400, Metropolis, NY 10001")
    phone = models.CharField(max_length=50, default="+1 (555) 123-4567")
    whatsapp = models.CharField(max_length=50, default="+1 (555) 123-4567")
    
    # Working hours
    weekdays_working_hours = models.CharField(max_length=100, default="Mon - Fri: 8:00 AM - 6:00 PM")
    saturday_working_hours = models.CharField(max_length=100, default="Sat: 9:00 AM - 2:00 PM")
    sunday_working_hours = models.CharField(max_length=100, default="Sun: Closed")
    
    # Map Link
    map_link = models.TextField(default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3022.6175407386008!2d-73.98782292346985!3d40.74844047138767!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c259a9b3117469%3A0xd134e199a405a163!2sEmpire%20State%20Building!5e0!3m2!1sen!2sus!4v1713374240000!5m2!1sen!2sus")
    
    # Social links
    facebook_url = models.CharField(max_length=255, blank=True, default="https://facebook.com")
    twitter_url = models.CharField(max_length=255, blank=True, default="https://twitter.com")
    instagram_url = models.CharField(max_length=255, blank=True, default="https://instagram.com")
    linkedin_url = models.CharField(max_length=255, blank=True, default="https://linkedin.com")
    
    # Notification method
    NOTIFICATION_CHOICES = [
        ('email', 'Email only'),
        ('whatsapp', 'WhatsApp only'),
        ('both', 'Both Email and WhatsApp'),
    ]
    notification_method = models.CharField(
        max_length=15,
        choices=NOTIFICATION_CHOICES,
        default='both'
    )

    class Meta:
        verbose_name = "Clinic Information"
        verbose_name_plural = "Clinic Information"

    def __str__(self):
        return "Clinic Information Configuration"


class Credential(models.Model):
    """Doctor credentials and qualifications list."""
    text = models.CharField(max_length=255)
    order = models.IntegerField(default=0, help_text="Lower numbers appear first")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text


class Review(models.Model):
    """Patient testimonials/reviews."""
    name = models.CharField(max_length=100)
    initial = models.CharField(max_length=10, blank=True, help_text="Fallback avatar initials if image is missing")
    stars = models.PositiveIntegerField(default=5, choices=[(i, f"{i} Stars") for i in range(1, 6)])
    quote = models.TextField()
    image = models.ImageField(upload_to="patients/", blank=True, null=True, help_text="Optional patient photo avatar")

    def __str__(self):
        return f"{self.name} - {self.stars} Stars"


class Appointment(models.Model):
    """Patient appointment booking records."""
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=20)
    contact = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.contact} ({self.created_at.strftime('%Y-%b-%d')})"
