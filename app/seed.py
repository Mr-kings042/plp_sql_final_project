from app.database import SessionLocal
from app import models

def create_sample_publishers():
    """Create 10 sample publishers if they don't exist"""
    db = SessionLocal()
    try:
        # Check if publishers already exist
        existing_count = db.query(models.Publisher).count()
        if existing_count > 0:
            return
        
        publishers_data = [
            {
                "name": "Penguin Random House",
                "address": "1745 Broadway, New York, NY 10019, USA",
                "website": "https://www.penguinrandomhouse.com"
            },
            {
                "name": "HarperCollins Publishers",
                "address": "195 Broadway, New York, NY 10007, USA", 
                "website": "https://www.harpercollins.com"
            },
            {
                "name": "Macmillan Publishers",
                "address": "120 Broadway, New York, NY 10271, USA",
                "website": "https://us.macmillan.com"
            },
            {
                "name": "Simon & Schuster",
                "address": "1230 Avenue of the Americas, New York, NY 10020, USA",
                "website": "https://www.simonandschuster.com"
            },
            {
                "name": "Hachette Book Group",
                "address": "1290 Avenue of the Americas, New York, NY 10104, USA",
                "website": "https://www.hachettebookgroup.com"
            },
            {
                "name": "Scholastic Corporation",
                "address": "557 Broadway, New York, NY 10012, USA",
                "website": "https://www.scholastic.com"
            },
            {
                "name": "Oxford University Press",
                "address": "198 Madison Avenue, New York, NY 10016, USA",
                "website": "https://global.oup.com"
            },
            {
                "name": "Cambridge University Press",
                "address": "1 Liberty Plaza, New York, NY 10006, USA",
                "website": "https://www.cambridge.org"
            },
            {
                "name": "Wiley",
                "address": "111 River Street, Hoboken, NJ 07030, USA",
                "website": "https://www.wiley.com"
            },
            {
                "name": "Pearson Education",
                "address": "221 River Street, Hoboken, NJ 07030, USA",
                "website": "https://www.pearson.com"
            }
        ]
        
        for publisher_data in publishers_data:
            publisher = models.Publisher(**publisher_data)
            db.add(publisher)
        
        db.commit()
        print("✅ Created 10 sample publishers successfully!")
        
    except Exception as e:
        print(f"❌ Error creating publishers: {e}")
        db.rollback()
    finally:
        db.close()
