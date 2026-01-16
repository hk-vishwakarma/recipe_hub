from faker import Faker
import random
from recipes.models import Recipe, Feedback  # adjust import based on your app name

def feedback_generate():
    fake = Faker()

    # Feedback templates by rating
    feedback_by_rating = {
        5: [
            "Absolutely loved it! Will make again.",
            "This recipe is amazing, everyone enjoyed it!",
            "Perfect dish, super easy to follow and delicious!",
            "Fantastic flavor and texture, highly recommended!",
            "I’m very impressed, came out exactly as described.",
            "Delicious and easy to make, my family loved it!",
            "One of the best recipes I’ve tried recently!",
            "Came out perfect, will definitely add to my weekly menu.",
            "Flavor was incredible, everyone asked for seconds!",
            "A new favorite recipe, simple and tasty!"
        ],
        4: [
            "Really good recipe, just added a bit more salt.",
            "Tasty and easy to make, will try again with slight tweaks.",
            "Enjoyed it, but I would adjust the seasoning next time.",
            "Great recipe, worked well, my family liked it.",
            "Pretty good, just a little bland for my taste.",
            "Nice recipe, easy to follow, will cook again.",
            "Turned out great, but I would try a different spice mix next time.",
            "Simple and flavorful, but could be slightly better.",
            "Liked it overall, will recommend to friends.",
            "Good balance of flavors, satisfied with the result."
        ],
        3: [
            "It was okay, nothing special but edible.",
            "Average taste, I might try a different recipe next time.",
            "Recipe turned out fine, but I expected more flavor.",
            "Not bad, but could be improved with some changes.",
            "It worked, but I think the dish was too bland.",
            "Decent recipe, nothing outstanding.",
            "Followed instructions, but flavor wasn’t amazing.",
            "Edible, but I probably wouldn’t make it often.",
            "Fine for a quick meal, but not memorable.",
            "The recipe was okay, could use better seasoning."
        ]
        
    }

    # Generate fake feedbacks with variations
    recipes = Recipe.objects.all()

    for recipe in recipes:
        num_feedbacks = random.randint(3, 10)  # random number of feedbacks per recipe
        for _ in range(num_feedbacks):
            rating = random.randint(3, 5)
            comment = random.choice(feedback_by_rating[rating])


            Feedback.objects.create(
                recipe=recipe,
                name=fake.name(),
                rating=rating,
                comment=comment
            )

    print("Realistic fake feedback generated successfully!")
    return
