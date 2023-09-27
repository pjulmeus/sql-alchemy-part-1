
from models import db, User, Post
from app import app 

db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()


paul = User(first_name = "Paul", last_name = "Julmeus", image_url = "https://gweb-research-imagen.web.app/compositional/An%20oil%20painting%20of%20a%20British%20Shorthair%20cat%20wearing%20a%20cowboy%20hat%20and%20red%20shirt%20playing%20a%20guitar%20in%20a%20garden./0_.jpeg")
ketsia = User(first_name = "Ketsia", last_name = "Bell", image_url = "https://www.thespruce.com/thmb/c3znkzZgMeuvzBy4wH13jVllfUo=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/plants-with-big-flowers-4138211-hero-b10becb169064cc4b3c7967adc1b22e1.jpg")
laura = User(first_name = "Laura", last_name = "Merli", image_url = "https://images.rawpixel.com/image_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIyLTA1L2Zycm9zZV9mbG93ZXJfZ3JleV9mbG9yYWwtaW1hZ2Uta3liY3R3OWkuanBn.jpg")

db.session.add(paul)
db.session.add(ketsia)
db.session.add(laura)

db.session.commit()