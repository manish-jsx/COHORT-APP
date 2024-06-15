from django.core.management.base import BaseCommand
from api.models import Course, Module, Notebook, Video, UserProgress, User
from faker import Faker
import random


class Command(BaseCommand):
    help = "Seed the database with realistic data for a 30-day data science cohort"

    def handle(self, *args, **options):
        fake = Faker()

        # Courses (One course for the entire cohort)
        course = Course.objects.create(
            title="30-Day Data Science Bootcamp",
            description="An immersive course to master essential data science skills in 30 days."
        )

        # Modules (One for each day of the cohort)
        modules = []
        for day in range(1, 31):
            module_title = f"Day {day}: {fake.random_element(['Data Exploration', 'Data Preprocessing', 'Regression Analysis', 'Classification', 'Time Series', 'Clustering', 'Natural Language Processing', 'Deep Learning'])}"
            module_content = f"""
**Introduction**

In today's module, we will explore {module_title}.
*Subtopics covered:*
    * Topic 1: ...
    * Topic 2: ...
    * Topic 3: ...

**Key Concepts:**
    *Concept 1*: {fake.paragraph()}
    *Concept 2*: {fake.paragraph()}

**Hands-On Exercise:**
We'll work on a practical project to apply what we learned.

**Additional Resources:**
    * Blog Post: {fake.url()}
    * Tutorial: {fake.url()}
            """
            module = Module.objects.create(
                course=course,
                title=module_title,
                content=module_content,
                order=day  # Set order sequentially
            )
            modules.append(module)  # Store the modules for later use

        # Notebooks and Videos (Varying number per module, up to 3 each)
        notebook_titles = [
            "Data Cleaning with Pandas", 
            "Exploratory Data Analysis (EDA) in Python", 
            "Building a Linear Regression Model",
            "Hyperparameter Tuning",
            # Add more notebook titles as needed
        ]

        video_titles = [
            "Introduction to Data Visualization",
            "Decision Trees Explained",
            "Implementing a Neural Network",
            "Feature Engineering Techniques",
            # Add more video titles as needed
        ]

        for module in modules:
            for _ in range(random.randint(1, 3)):  # 1 to 3 notebooks per module
                Notebook.objects.create(
                    module=module,
                    title=fake.random_element(notebook_titles),
                    # file=f'notebooks/{fake.file_name(extension="ipynb")}',  # Placeholder for actual files
                )

            for _ in range(random.randint(1, 3)):  # 1 to 3 videos per module
                Video.objects.create(
                    module=module,
                    title=fake.random_element(video_titles),
                    url=fake.url()
                )

        # Sample Users and Progress
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.user_name(),
                password='testpassword',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email()
            )
            # Randomly assign completed modules for each user
            completed_modules = random.sample(modules, random.randint(0, 15))  # Up to 15 modules completed
            for module in completed_modules:
                UserProgress.objects.create(
                    user=user,
                    module=module,
                    completed=True
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database'))
