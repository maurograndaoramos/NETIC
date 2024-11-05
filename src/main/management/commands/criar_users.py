import random
import faker
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import UserProfile

class Command(BaseCommand):
    help = 'Cria 100 instâncias de usuário e perfil com dados aleatórios.'

    def handle(self, *args, **kwargs):
        print("Starting to create users and profiles...")
        fake = faker.Faker()
        cursos = [
            "Design de Comunicação e Marketing Digital",
            "Criação Musical, Produção e Técnicas de Som",
            "Design de Comunicação e Multimédia",
            "Fotografia Profissional",
            "Programação Web",
            "Realização, Cinema e TV",
            "Videojogos",
            "Concept Art",
            "Design Gráfico",
            "Fotografia",
            "Marketing Digital e Social Media",
            "Produção e Criação Musical Eletrónica",
            "Técnicas de Som"
        ]

        for i in range(100):
            # Generate user details
            username = fake.user_name()
            email = fake.unique.email()

            # Create user
            user = User.objects.create_user(username=username, email=email, password='123456')

            # Generate profile details
            first_name = fake.first_name()
            last_name = fake.last_name()
            curso_aleatorio = random.choice(cursos)
            sinopse = fake.sentence(nb_words=10)
            instagram = f"https://instagram.com/{username}"
            linkedin = f"https://linkedin.com/in/{username}"
            github = f"https://github.com/{username}"
            website = f"https://{username}.com/"
            descricao_longa = fake.text(max_nb_chars=300)

            print(f"Adding profile for user: {username}")

            # Create the profile with all fields
            UserProfile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                curso=curso_aleatorio,
                sinopse=sinopse,
                instagram=instagram,
                linkedin=linkedin,
                github=github,
                website=website,
                descricao_longa=descricao_longa,
            )

        print("Finished creating users and profiles.")
