from django.core.management.base import BaseCommand
from app.models import UserProfile

class Command(BaseCommand):
    help = 'Update profile pictures with UI Avatars'

    def handle(self, *args, **options):
        profiles = UserProfile.objects.all()
        
        for profile in profiles:
            # Create URL-safe name
            name = f"{profile.first_name}+{profile.last_name}"
            avatar_url = f"https://ui-avatars.com/api/?name={name}&background=random&size=256"
            
            # Update profile picture field
            profile.profile_picture = avatar_url
            profile.save()
            
            self.stdout.write(f"Updated avatar for {profile.first_name} {profile.last_name}")