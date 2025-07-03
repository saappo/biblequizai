from flask import render_template, request, redirect, url_for, flash, session, jsonify, make_response, get_flashed_messages
from flask_login import login_required, current_user, login_user, AnonymousUserMixin
from models import User, Quiz, Question, UserResponse, Suggestion, db, ContactMessage
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)

# Define sample questions if not already defined
SAMPLE_QUESTIONS = {
    'Easy': [
        {
            'text': 'Who built the ark?',
            'options': ['Noah', 'Moses', 'Abraham', 'David'],
            'correct_answer': 'Noah',
            'category': 'Old Testament',
            'explanation': 'Noah was commanded by God to build an ark to save his family and animals from the flood. (Genesis 6-9)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+6-9&version=NIV'
        },
        {
            'text': 'How many disciples did Jesus have?',
            'options': ['10', '12', '13', '14'],
            'correct_answer': '12',
            'category': 'New Testament',
            'explanation': 'Jesus chose twelve disciples to be His closest followers. (Matthew 10:1-4)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+10%3A1-4&version=NIV'
        },
        {
            'text': 'Who was the first man created by God?',
            'options': ['Adam', 'Eve', 'Noah', 'Abraham'],
            'correct_answer': 'Adam',
            'category': 'Old Testament',
            'explanation': 'Adam was the first human created by God from the dust of the ground. (Genesis 2:7)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+2%3A7&version=NIV'
        },
        {
            'text': 'What was the first miracle Jesus performed?',
            'options': ['Walking on water', 'Turning water into wine', 'Feeding 5000', 'Raising Lazarus'],
            'correct_answer': 'Turning water into wine',
            'category': 'New Testament',
            'explanation': 'Jesus turned water into wine at the wedding in Cana, His first recorded miracle. (John 2:1-11)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+2%3A1-11&version=NIV'
        },
        {
            'text': "Who was thrown into the lion's den?",
            'options': ['David', 'Daniel', 'Joseph', 'Jonah'],
            'correct_answer': 'Daniel',
            'category': 'Old Testament',
            'explanation': 'Daniel was thrown into the lion\'s den for praying to God, but God protected him. (Daniel 6)',
            'reference': 'https://www.biblegateway.com/passage/?search=Daniel+6&version=NIV'
        },
        {
            'text': "What was the name of Jesus' mother?",
            'options': ['Mary', 'Elizabeth', 'Sarah', 'Rebecca'],
            'correct_answer': 'Mary',
            'category': 'New Testament',
            'explanation': 'Mary was chosen by God to be the mother of Jesus. (Luke 1:26-38)',
            'reference': 'https://www.biblegateway.com/passage/?search=Luke+1%3A26-38&version=NIV'
        },
        {
            'text': 'Which book comes first in the Bible?',
            'options': ['Genesis', 'Exodus', 'Matthew', 'Psalms'],
            'correct_answer': 'Genesis',
            'category': 'Old Testament',
            'explanation': 'Genesis is the first book of the Bible, describing creation and early history. (Genesis 1:1)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+1%3A1&version=NIV'
        },
        {
            'text': 'Who was the first king of Israel?',
            'options': ['Saul', 'David', 'Solomon', 'Samuel'],
            'correct_answer': 'Saul',
            'category': 'Old Testament',
            'explanation': 'Saul was anointed by Samuel as the first king of Israel. (1 Samuel 10:1)',
            'reference': 'https://www.biblegateway.com/passage/?search=1+Samuel+10%3A1&version=NIV'
        },
        {
            'text': 'What was the name of the place where Jesus was born?',
            'options': ['Bethlehem', 'Nazareth', 'Jerusalem', 'Galilee'],
            'correct_answer': 'Bethlehem',
            'category': 'New Testament',
            'explanation': 'Jesus was born in Bethlehem, fulfilling prophecy. (Luke 2:1-7)',
            'reference': 'https://www.biblegateway.com/passage/?search=Luke+2%3A1-7&version=NIV'
        },
        {
            'text': 'How many books are in the New Testament?',
            'options': ['27', '39', '66', '73'],
            'correct_answer': '27',
            'category': 'General',
            'explanation': 'The New Testament contains 27 books, from Matthew to Revelation.',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+1&version=NIV'
        },
        {
            'text': 'Who was the first person to die in the Bible?',
            'options': ['Abel', 'Cain', 'Adam', 'Eve'],
            'correct_answer': 'Abel',
            'category': 'Old Testament',
            'explanation': 'Abel was killed by his brother Cain, making him the first person to die. (Genesis 4:8)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+4%3A8&version=NIV'
        },
        {
            'text': 'What was the name of the garden where Adam and Eve lived?',
            'options': ['Garden of Eden', 'Garden of Gethsemane', 'Garden of Paradise', 'Garden of Heaven'],
            'correct_answer': 'Garden of Eden',
            'category': 'Old Testament',
            'explanation': 'Adam and Eve lived in the Garden of Eden until they disobeyed God. (Genesis 2:8)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+2%3A8&version=NIV'
        },
        {
            'text': 'Who was the father of Isaac?',
            'options': ['Abraham', 'Noah', 'Moses', 'David'],
            'correct_answer': 'Abraham',
            'category': 'Old Testament',
            'explanation': 'Abraham was the father of Isaac, the child of promise. (Genesis 21:1-3)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+21%3A1-3&version=NIV'
        },
        {
            'text': 'What was the name of Isaac\'s wife?',
            'options': ['Rebecca', 'Sarah', 'Rachel', 'Leah'],
            'correct_answer': 'Rebecca',
            'category': 'Old Testament',
            'explanation': 'Rebecca became Isaac\'s wife and the mother of Jacob and Esau. (Genesis 24:67)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+24%3A67&version=NIV'
        },
        {
            'text': 'Who was the father of Jacob?',
            'options': ['Isaac', 'Abraham', 'Noah', 'Moses'],
            'correct_answer': 'Isaac',
            'category': 'Old Testament',
            'explanation': 'Isaac was the father of Jacob, who later became Israel. (Genesis 25:24-26)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+25%3A24-26&version=NIV'
        },
        {
            'text': 'How many sons did Jacob have?',
            'options': ['10', '11', '12', '13'],
            'correct_answer': '12',
            'category': 'Old Testament',
            'explanation': 'Jacob had 12 sons who became the fathers of the 12 tribes of Israel. (Genesis 35:22-26)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+35%3A22-26&version=NIV'
        },
        {
            'text': 'Who was sold into slavery by his brothers?',
            'options': ['Joseph', 'Benjamin', 'Judah', 'Reuben'],
            'correct_answer': 'Joseph',
            'category': 'Old Testament',
            'explanation': 'Joseph was sold into slavery by his jealous brothers. (Genesis 37:28)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+37%3A28&version=NIV'
        },
        {
            'text': 'Who was the baby found in a basket in the river?',
            'options': ['Moses', 'Aaron', 'Joshua', 'Caleb'],
            'correct_answer': 'Moses',
            'category': 'Old Testament',
            'explanation': 'Moses was found in a basket in the Nile River by Pharaoh\'s daughter. (Exodus 2:1-10)',
            'reference': 'https://www.biblegateway.com/passage/?search=Exodus+2%3A1-10&version=NIV'
        },
        {
            'text': 'What was the name of Moses\' brother?',
            'options': ['Aaron', 'Joshua', 'Caleb', 'Miriam'],
            'correct_answer': 'Aaron',
            'category': 'Old Testament',
            'explanation': 'Aaron was Moses\' brother and the first high priest of Israel. (Exodus 4:14)',
            'reference': 'https://www.biblegateway.com/passage/?search=Exodus+4%3A14&version=NIV'
        },
        {
            'text': 'How many plagues did God send on Egypt?',
            'options': ['7', '9', '10', '12'],
            'correct_answer': '10',
            'category': 'Old Testament',
            'explanation': 'God sent 10 plagues on Egypt to convince Pharaoh to let the Israelites go. (Exodus 7-12)',
            'reference': 'https://www.biblegateway.com/passage/?search=Exodus+7-12&version=NIV'
        },
        {
            'text': 'What was the first plague?',
            'options': ['Water to blood', 'Frogs', 'Gnats', 'Flies'],
            'correct_answer': 'Water to blood',
            'category': 'Old Testament',
            'explanation': 'The first plague was turning the Nile River water into blood. (Exodus 7:14-24)',
            'reference': 'https://www.biblegateway.com/passage/?search=Exodus+7%3A14-24&version=NIV'
        },
        {
            'text': 'Who was the first king of Israel after Saul?',
            'options': ['David', 'Solomon', 'Samuel', 'Jonathan'],
            'correct_answer': 'David',
            'category': 'Old Testament',
            'explanation': 'David became king after Saul and was known as a man after God\'s own heart. (1 Samuel 16:13)',
            'reference': 'https://www.biblegateway.com/passage/?search=1+Samuel+16%3A13&version=NIV'
        },
        {
            'text': 'Who was David\'s son who became king?',
            'options': ['Solomon', 'Absalom', 'Adonijah', 'Amnon'],
            'correct_answer': 'Solomon',
            'category': 'Old Testament',
            'explanation': 'Solomon was David\'s son who became king and was known for his wisdom. (1 Kings 1:39)',
            'reference': 'https://www.biblegateway.com/passage/?search=1+Kings+1%3A39&version=NIV'
        },
        {
            'text': 'Who built the first temple in Jerusalem?',
            'options': ['Solomon', 'David', 'Hezekiah', 'Josiah'],
            'correct_answer': 'Solomon',
            'category': 'Old Testament',
            'explanation': 'Solomon built the first temple in Jerusalem for the worship of God. (1 Kings 6:1)',
            'reference': 'https://www.biblegateway.com/passage/?search=1+Kings+6%3A1&version=NIV'
        },
        {
            'text': 'Who was the prophet who was swallowed by a big fish?',
            'options': ['Jonah', 'Elijah', 'Elisha', 'Isaiah'],
            'correct_answer': 'Jonah',
            'category': 'Old Testament',
            'explanation': 'Jonah was swallowed by a great fish when he tried to run from God. (Jonah 1:17)',
            'reference': 'https://www.biblegateway.com/passage/?search=Jonah+1%3A17&version=NIV'
        },
        {
            'text': 'Who was the prophet who was taken to heaven in a chariot?',
            'options': ['Elijah', 'Elisha', 'Isaiah', 'Jeremiah'],
            'correct_answer': 'Elijah',
            'category': 'Old Testament',
            'explanation': 'Elijah was taken up to heaven in a whirlwind with a chariot of fire. (2 Kings 2:11)',
            'reference': 'https://www.biblegateway.com/passage/?search=2+Kings+2%3A11&version=NIV'
        },
        {
            'text': 'Who was the prophet who was thrown into a fiery furnace?',
            'options': ['Shadrach, Meshach, and Abednego', 'Daniel', 'Jeremiah', 'Ezekiel'],
            'correct_answer': 'Shadrach, Meshach, and Abednego',
            'category': 'Old Testament',
            'explanation': 'Shadrach, Meshach, and Abednego were thrown into a fiery furnace but God protected them. (Daniel 3:20-25)',
            'reference': 'https://www.biblegateway.com/passage/?search=Daniel+3%3A20-25&version=NIV'
        },
        {
            'text': 'Who was the angel who appeared to Mary?',
            'options': ['Gabriel', 'Michael', 'Raphael', 'Uriel'],
            'correct_answer': 'Gabriel',
            'category': 'New Testament',
            'explanation': 'The angel Gabriel appeared to Mary to tell her she would give birth to Jesus. (Luke 1:26-38)',
            'reference': 'https://www.biblegateway.com/passage/?search=Luke+1%3A26-38&version=NIV'
        },
        {
            'text': 'Who was the first person to see the baby Jesus?',
            'options': ['The shepherds', 'The wise men', 'Simeon', 'Anna'],
            'correct_answer': 'The shepherds',
            'category': 'New Testament',
            'explanation': 'The shepherds were the first to see the baby Jesus after the angels told them. (Luke 2:8-20)',
            'reference': 'https://www.biblegateway.com/passage/?search=Luke+2%3A8-20&version=NIV'
        },
        {
            'text': 'Who were the first people to visit Jesus after His birth?',
            'options': ['The wise men', 'The shepherds', 'Simeon and Anna', 'Herod'],
            'correct_answer': 'The wise men',
            'category': 'New Testament',
            'explanation': 'The wise men from the east came to visit Jesus and brought gifts. (Matthew 2:1-12)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+2%3A1-12&version=NIV'
        },
        {
            'text': 'What gifts did the wise men bring to Jesus?',
            'options': ['Gold, frankincense, and myrrh', 'Silver, gold, and jewels', 'Food, water, and clothes', 'Books, scrolls, and oil'],
            'correct_answer': 'Gold, frankincense, and myrrh',
            'category': 'New Testament',
            'explanation': 'The wise men brought gold, frankincense, and myrrh as gifts to Jesus. (Matthew 2:11)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+2%3A11&version=NIV'
        },
        {
            'text': 'Who was Jesus\' earthly father?',
            'options': ['Joseph', 'God', 'David', 'Abraham'],
            'correct_answer': 'Joseph',
            'category': 'New Testament',
            'explanation': 'Joseph was Jesus\' earthly father, though Jesus was conceived by the Holy Spirit. (Matthew 1:18-25)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+1%3A18-25&version=NIV'
        },
        {
            'text': 'Who was the first disciple Jesus called?',
            'options': ['Andrew', 'Peter', 'John', 'James'],
            'correct_answer': 'Andrew',
            'category': 'New Testament',
            'explanation': 'Andrew was the first disciple Jesus called, and he brought his brother Peter to Jesus. (John 1:35-42)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+1%3A35-42&version=NIV'
        },
        {
            'text': 'Who was the disciple who betrayed Jesus?',
            'options': ['Judas Iscariot', 'Peter', 'Thomas', 'Philip'],
            'correct_answer': 'Judas Iscariot',
            'category': 'New Testament',
            'explanation': 'Judas Iscariot betrayed Jesus for thirty pieces of silver. (Matthew 26:14-16)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+26%3A14-16&version=NIV'
        },
        {
            'text': 'Who was the disciple who doubted Jesus\' resurrection?',
            'options': ['Thomas', 'Peter', 'John', 'Andrew'],
            'correct_answer': 'Thomas',
            'category': 'New Testament',
            'explanation': 'Thomas doubted Jesus\' resurrection until he saw Jesus with his own eyes. (John 20:24-29)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+20%3A24-29&version=NIV'
        },
        {
            'text': 'Who was the first person to see Jesus after His resurrection?',
            'options': ['Mary Magdalene', 'Peter', 'John', 'The disciples'],
            'correct_answer': 'Mary Magdalene',
            'category': 'New Testament',
            'explanation': 'Mary Magdalene was the first person to see Jesus after His resurrection. (John 20:11-18)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+20%3A11-18&version=NIV'
        },
        {
            'text': 'How many people did Jesus feed with 5 loaves and 2 fish?',
            'options': ['3000', '4000', '5000', '6000'],
            'correct_answer': '5000',
            'category': 'New Testament',
            'explanation': 'Jesus fed 5000 men (plus women and children) with 5 loaves and 2 fish. (Matthew 14:13-21)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+14%3A13-21&version=NIV'
        },
        {
            'text': 'Who was the woman who washed Jesus\' feet with her tears?',
            'options': ['Mary Magdalene', 'Mary of Bethany', 'A sinful woman', 'The Samaritan woman'],
            'correct_answer': 'A sinful woman',
            'category': 'New Testament',
            'explanation': 'A sinful woman washed Jesus\' feet with her tears and dried them with her hair. (Luke 7:36-50)',
            'reference': 'https://www.biblegateway.com/passage/?search=Luke+7%3A36-50&version=NIV'
        },
        {
            'text': 'Who was the woman Jesus met at the well?',
            'options': ['The Samaritan woman', 'Mary Magdalene', 'Mary of Bethany', 'The Canaanite woman'],
            'correct_answer': 'The Samaritan woman',
            'category': 'New Testament',
            'explanation': 'Jesus met a Samaritan woman at the well and told her about living water. (John 4:1-42)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+4%3A1-42&version=NIV'
        },
        {
            'text': 'Who was the man Jesus raised from the dead after 4 days?',
            'options': ['Lazarus', 'Jairus\' daughter', 'The widow\'s son', 'The centurion\'s servant'],
            'correct_answer': 'Lazarus',
            'category': 'New Testament',
            'explanation': 'Jesus raised Lazarus from the dead after he had been in the tomb for 4 days. (John 11:1-44)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+11%3A1-44&version=NIV'
        },
        {
            'text': 'Who was the Roman governor who sentenced Jesus to death?',
            'options': ['Pontius Pilate', 'Herod', 'Caiaphas', 'Annas'],
            'correct_answer': 'Pontius Pilate',
            'category': 'New Testament',
            'explanation': 'Pontius Pilate was the Roman governor who sentenced Jesus to death by crucifixion. (Matthew 27:11-26)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+27%3A11-26&version=NIV'
        },
        {
            'text': 'Who was the first Christian martyr?',
            'options': ['Stephen', 'James', 'Peter', 'Paul'],
            'correct_answer': 'Stephen',
            'category': 'New Testament',
            'explanation': 'Stephen was the first Christian martyr, stoned to death for his faith. (Acts 7:54-60)',
            'reference': 'https://www.biblegateway.com/passage/?search=Acts+7%3A54-60&version=NIV'
        },
        {
            'text': 'Who was the first Gentile to be baptized?',
            'options': ['Cornelius', 'Lydia', 'The Ethiopian eunuch', 'The Philippian jailer'],
            'correct_answer': 'Cornelius',
            'category': 'New Testament',
            'explanation': 'Cornelius was the first Gentile to be baptized, showing the gospel was for all people. (Acts 10)',
            'reference': 'https://www.biblegateway.com/passage/?search=Acts+10&version=NIV'
        },
        {
            'text': 'Who wrote the most books in the New Testament?',
            'options': ['Paul', 'John', 'Peter', 'Luke'],
            'correct_answer': 'Paul',
            'category': 'New Testament',
            'explanation': 'Paul wrote 13 books of the New Testament, more than any other author.',
            'reference': 'https://www.biblegateway.com/passage/?search=Romans+1&version=NIV'
        },
        {
            'text': 'How many books are in the entire Bible?',
            'options': ['66', '73', '77', '81'],
            'correct_answer': '66',
            'category': 'General',
            'explanation': 'The Bible contains 66 books total: 39 in the Old Testament and 27 in the New Testament.',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+1&version=NIV'
        },
        {
            'text': 'What is the shortest verse in the Bible?',
            'options': ['Jesus wept', 'Rejoice always', 'Pray continually', 'Love one another'],
            'correct_answer': 'Jesus wept',
            'category': 'New Testament',
            'explanation': '"Jesus wept" (John 11:35) is the shortest verse in the Bible.',
            'reference': 'https://www.biblegateway.com/passage/?search=John+11%3A35&version=NIV'
        },
        {
            'text': 'What is the longest book in the Bible?',
            'options': ['Psalms', 'Genesis', 'Isaiah', 'Jeremiah'],
            'correct_answer': 'Psalms',
            'category': 'Old Testament',
            'explanation': 'Psalms is the longest book in the Bible with 150 chapters.',
            'reference': 'https://www.biblegateway.com/passage/?search=Psalms+1&version=NIV'
        },
        {
            'text': 'What is the shortest book in the Bible?',
            'options': ['2 John', '3 John', 'Jude', 'Philemon'],
            'correct_answer': '2 John',
            'category': 'New Testament',
            'explanation': '2 John is the shortest book in the Bible with only 13 verses.',
            'reference': 'https://www.biblegateway.com/passage/?search=2+John+1&version=NIV'
        },
        {
            'text': 'Who was the first person to be baptized in the New Testament?',
            'options': ['Jesus', 'John the Baptist', 'Peter', 'Andrew'],
            'correct_answer': 'Jesus',
            'category': 'New Testament',
            'explanation': 'Jesus was baptized by John the Baptist, marking the beginning of His ministry. (Matthew 3:13-17)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+3%3A13-17&version=NIV'
        },
        {
            'text': 'Who was the first person to recognize Jesus as the Messiah?',
            'options': ['Peter', 'John', 'Andrew', 'Simon'],
            'correct_answer': 'Peter',
            'category': 'New Testament',
            'explanation': 'Peter was the first to recognize Jesus as the Messiah, the Son of the living God. (Matthew 16:16)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+16%3A16&version=NIV'
        },
        {
            'text': 'Who was the first person to be healed by Jesus?',
            'options': ['A leper', 'A blind man', 'A paralyzed man', 'A woman with bleeding'],
            'correct_answer': 'A leper',
            'category': 'New Testament',
            'explanation': 'Jesus healed a leper, which was one of His first recorded healings. (Matthew 8:1-4)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+8%3A1-4&version=NIV'
        },
        {
            'text': 'Who was the first person to be raised from the dead by Jesus?',
            'options': ['Jairus\' daughter', 'The widow\'s son', 'Lazarus', 'The centurion\'s servant'],
            'correct_answer': 'Jairus\' daughter',
            'category': 'New Testament',
            'explanation': 'Jesus raised Jairus\' daughter from the dead, one of His first resurrection miracles. (Mark 5:21-43)',
            'reference': 'https://www.biblegateway.com/passage/?search=Mark+5%3A21-43&version=NIV'
        },
        {
            'text': 'Who was the first person to be called by Jesus to follow Him?',
            'options': ['Andrew and Simon Peter', 'James and John', 'Philip and Nathanael', 'Matthew'],
            'correct_answer': 'Andrew and Simon Peter',
            'category': 'New Testament',
            'explanation': 'Andrew and Simon Peter were the first disciples called by Jesus to follow Him. (Matthew 4:18-20)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+4%3A18-20&version=NIV'
        },
        {
            'text': 'Who was the first person to be sent out by Jesus to preach?',
            'options': ['The twelve disciples', 'The seventy-two', 'John the Baptist', 'Paul'],
            'correct_answer': 'The twelve disciples',
            'category': 'New Testament',
            'explanation': 'Jesus first sent out the twelve disciples to preach and heal. (Matthew 10:1-15)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+10%3A1-15&version=NIV'
        },
        {
            'text': 'Who was the first person to be converted after Jesus\' resurrection?',
            'options': ['The Ethiopian eunuch', 'Cornelius', 'Saul (Paul)', 'Lydia'],
            'correct_answer': 'The Ethiopian eunuch',
            'category': 'New Testament',
            'explanation': 'The Ethiopian eunuch was one of the first converts after Jesus\' resurrection. (Acts 8:26-40)',
            'reference': 'https://www.biblegateway.com/passage/?search=Acts+8%3A26-40&version=NIV'
        },
        {
            'text': 'Who was the first person to be baptized in the Holy Spirit?',
            'options': ['The disciples at Pentecost', 'Cornelius', 'The Samaritans', 'The Ephesians'],
            'correct_answer': 'The disciples at Pentecost',
            'category': 'New Testament',
            'explanation': 'The disciples were baptized with the Holy Spirit at Pentecost. (Acts 2:1-4)',
            'reference': 'https://www.biblegateway.com/passage/?search=Acts+2%3A1-4&version=NIV'
        },
        {
            'text': 'Who was the first person to be called a Christian?',
            'options': ['The disciples in Antioch', 'Paul', 'Peter', 'Barnabas'],
            'correct_answer': 'The disciples in Antioch',
            'category': 'New Testament',
            'explanation': 'The disciples were first called Christians in Antioch. (Acts 11:26)',
            'reference': 'https://www.biblegateway.com/passage/?search=Acts+11%3A26&version=NIV'
        },
        {
            'text': 'Who was the first person to be imprisoned for preaching about Jesus?',
            'options': ['Peter and John', 'Paul', 'Stephen', 'James'],
            'correct_answer': 'Peter and John',
            'category': 'New Testament',
            'explanation': 'Peter and John were the first to be imprisoned for preaching about Jesus. (Acts 4:1-3)',
            'reference': 'https://www.biblegateway.com/passage/?search=Acts+4%3A1-3&version=NIV'
        },
        {
            'text': 'Who was the first person to be shipwrecked while spreading the gospel?',
            'options': ['Paul', 'Peter', 'John', 'Barnabas'],
            'correct_answer': 'Paul',
            'category': 'New Testament',
            'explanation': 'Paul experienced shipwrecks while spreading the gospel. (2 Corinthians 11:25)',
            'reference': 'https://www.biblegateway.com/passage/?search=2+Corinthians+11%3A25&version=NIV'
        },
        {
            'text': 'Who was the first person to write about Jesus\' life?',
            'options': ['Mark', 'Matthew', 'Luke', 'John'],
            'correct_answer': 'Mark',
            'category': 'New Testament',
            'explanation': 'Mark is believed to be the first to write a Gospel about Jesus\' life.',
            'reference': 'https://www.biblegateway.com/passage/?search=Mark+1&version=NIV'
        },
        {
            'text': 'Who was the first person to see the risen Jesus?',
            'options': ['Mary Magdalene', 'Peter', 'John', 'The disciples'],
            'correct_answer': 'Mary Magdalene',
            'category': 'New Testament',
            'explanation': 'Mary Magdalene was the first person to see Jesus after His resurrection. (John 20:11-18)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+20%3A11-18&version=NIV'
        },
        {
            'text': 'Who was the first person to be healed on the Sabbath?',
            'options': ['A man with a withered hand', 'A blind man', 'A paralyzed man', 'A woman with bleeding'],
            'correct_answer': 'A man with a withered hand',
            'category': 'New Testament',
            'explanation': 'Jesus healed a man with a withered hand on the Sabbath. (Mark 3:1-6)',
            'reference': 'https://www.biblegateway.com/passage/?search=Mark+3%3A1-6&version=NIV'
        },
        {
            'text': 'Who was the first person to be called by name by Jesus?',
            'options': ['Simon Peter', 'Andrew', 'John', 'James'],
            'correct_answer': 'Simon Peter',
            'category': 'New Testament',
            'explanation': 'Jesus called Simon by name and gave him the name Peter. (John 1:42)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+1%3A42&version=NIV'
        },
        {
            'text': 'Who was the first person to be given the keys to the kingdom?',
            'options': ['Peter', 'John', 'James', 'Andrew'],
            'correct_answer': 'Peter',
            'category': 'New Testament',
            'explanation': 'Jesus gave Peter the keys to the kingdom of heaven. (Matthew 16:19)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+16%3A19&version=NIV'
        },
        {
            'text': 'Who was the first person to be told to "follow me" by Jesus?',
            'options': ['Andrew and Simon Peter', 'James and John', 'Philip', 'Matthew'],
            'correct_answer': 'Andrew and Simon Peter',
            'category': 'New Testament',
            'explanation': 'Jesus first said "Follow me" to Andrew and Simon Peter. (Matthew 4:19)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+4%3A19&version=NIV'
        },
        {
            'text': 'Who was the first person to be given authority to cast out demons?',
            'options': ['The twelve disciples', 'The seventy-two', 'Peter', 'Paul'],
            'correct_answer': 'The twelve disciples',
            'category': 'New Testament',
            'explanation': 'Jesus gave the twelve disciples authority to cast out demons. (Matthew 10:1)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+10%3A1&version=NIV'
        },
        {
            'text': 'Who was the first person to be told to "go and sin no more"?',
            'options': ['The woman caught in adultery', 'The paralyzed man', 'The blind man', 'The leper'],
            'correct_answer': 'The woman caught in adultery',
            'category': 'New Testament',
            'explanation': 'Jesus told the woman caught in adultery to "go and sin no more." (John 8:11)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+8%3A11&version=NIV'
        },
        {
            'text': 'Who was the first person to be told to "take up your cross"?',
            'options': ['The disciples', 'Peter', 'John', 'James'],
            'correct_answer': 'The disciples',
            'category': 'New Testament',
            'explanation': 'Jesus told His disciples to take up their cross and follow Him. (Matthew 16:24)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+16%3A24&version=NIV'
        },
        {
            'text': 'Who was the first person to be told to "love your enemies"?',
            'options': ['The disciples', 'The crowds', 'The Pharisees', 'The Sadducees'],
            'correct_answer': 'The disciples',
            'category': 'New Testament',
            'explanation': 'Jesus told His disciples to love their enemies in the Sermon on the Mount. (Matthew 5:44)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+5%3A44&version=NIV'
        },
        {
            'text': 'Who was the first person to be told to "turn the other cheek"?',
            'options': ['The disciples', 'The crowds', 'The Pharisees', 'The Sadducees'],
            'correct_answer': 'The disciples',
            'category': 'New Testament',
            'explanation': 'Jesus told His disciples to turn the other cheek in the Sermon on the Mount. (Matthew 5:39)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+5%3A39&version=NIV'
        },
        {
            'text': 'Who was the first person to be told to "pray for those who persecute you"?',
            'options': ['The disciples', 'The crowds', 'The Pharisees', 'The Sadducees'],
            'correct_answer': 'The disciples',
            'category': 'New Testament',
            'explanation': 'Jesus told His disciples to pray for those who persecute them. (Matthew 5:44)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+5%3A44&version=NIV'
        },
        {
            'text': 'Who was the first person to be told to "forgive seventy times seven"?',
            'options': ['Peter', 'John', 'James', 'Andrew'],
            'correct_answer': 'Peter',
            'category': 'New Testament',
            'explanation': 'Jesus told Peter to forgive seventy times seven times. (Matthew 18:21-22)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+18%3A21-22&version=NIV'
        },
        {
            'text': 'Who was the first person to be told to "sell everything and give to the poor"?',
            'options': ['The rich young ruler', 'Zacchaeus', 'The widow', 'The tax collector'],
            'correct_answer': 'The rich young ruler',
            'category': 'New Testament',
            'explanation': 'Jesus told the rich young ruler to sell everything and give to the poor. (Matthew 19:21)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+19%3A21&version=NIV'
        },
        {
            'text': 'Who was the first person to be told to "be born again"?',
            'options': ['Nicodemus', 'The Samaritan woman', 'The disciples', 'The crowds'],
            'correct_answer': 'Nicodemus',
            'category': 'New Testament',
            'explanation': 'Jesus told Nicodemus that he must be born again. (John 3:3)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+3%3A3&version=NIV'
        },
        {
            'text': 'Who was the first person to be told to "drink living water"?',
            'options': ['The Samaritan woman', 'The disciples', 'The crowds', 'Nicodemus'],
            'correct_answer': 'The Samaritan woman',
            'category': 'New Testament',
            'explanation': 'Jesus told the Samaritan woman about living water. (John 4:10)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+4%3A10&version=NIV'
        },
        {
            'text': 'Who was the first person to be told to "eat the bread of life"?',
            'options': ['The crowds', 'The disciples', 'The Pharisees', 'The Sadducees'],
            'correct_answer': 'The crowds',
            'category': 'New Testament',
            'explanation': 'Jesus told the crowds that He is the bread of life. (John 6:35)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+6%3A35&version=NIV'
        },
        {
            'text': 'Who was the first person to be told to "walk in the light"?',
            'options': ['The disciples', 'The crowds', 'The Pharisees', 'The Sadducees'],
            'correct_answer': 'The disciples',
            'category': 'New Testament',
            'explanation': 'Jesus told His disciples to walk in the light. (John 8:12)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+8%3A12&version=NIV'
        },
        {
            'text': 'Who was the first person to be told to "abide in the vine"?',
            'options': ['The disciples', 'The crowds', 'The Pharisees', 'The Sadducees'],
            'correct_answer': 'The disciples',
            'category': 'New Testament',
            'explanation': 'Jesus told His disciples to abide in Him, the true vine. (John 15:4)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+15%3A4&version=NIV'
        },
        {
            'text': 'Who was the first person to be told to "love one another"?',
            'options': ['The disciples', 'The crowds', 'The Pharisees', 'The Sadducees'],
            'correct_answer': 'The disciples',
            'category': 'New Testament',
            'explanation': 'Jesus told His disciples to love one another as He loved them. (John 13:34)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+13%3A34&version=NIV'
        },
        {
            'text': 'Who was the first person to be told to "go and make disciples"?',
            'options': ['The eleven disciples', 'The crowds', 'The Pharisees', 'The Sadducees'],
            'correct_answer': 'The eleven disciples',
            'category': 'New Testament',
            'explanation': 'Jesus told the eleven disciples to go and make disciples of all nations. (Matthew 28:19)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+28%3A19&version=NIV'
        },
        {
            'text': 'Who was the first person to be told to "wait for the Holy Spirit"?',
            'options': ['The disciples', 'The crowds', 'The Pharisees', 'The Sadducees'],
            'correct_answer': 'The disciples',
            'category': 'New Testament',
            'explanation': 'Jesus told His disciples to wait for the Holy Spirit in Jerusalem. (Acts 1:4-5)',
            'reference': 'https://www.biblegateway.com/passage/?search=Acts+1%3A4-5&version=NIV'
        }
    ],
    'Medium': [
        {
            'text': "What was the name of Abraham's wife?",
            'options': ['Sarah', 'Rebecca', 'Rachel', 'Leah'],
            'correct_answer': 'Sarah',
            'category': 'Old Testament',
            'explanation': 'Sarah was Abraham\'s wife and the mother of Isaac. (Genesis 17:15-19)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+17%3A15-19&version=NIV'
        },
        {
            'text': "Who interpreted Pharaoh's dreams in Egypt?",
            'options': ['Joseph', 'Moses', 'Daniel', 'Aaron'],
            'correct_answer': 'Joseph',
            'category': 'Old Testament',
            'explanation': "Joseph interpreted Pharaoh's dreams, predicting seven years of plenty and seven years of famine. (Genesis 41)",
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+41&version=NIV'
        },
        {
            'text': "Which prophet confronted King David about his sin with Bathsheba?",
            'options': ['Nathan', 'Samuel', 'Elijah', 'Elisha'],
            'correct_answer': 'Nathan',
            'category': 'Old Testament',
            'explanation': "Nathan confronted David and told him the parable of the rich man and the poor man. (2 Samuel 12)",
            'reference': 'https://www.biblegateway.com/passage/?search=2+Samuel+12&version=NIV'
        },
        {
            'text': "Who was the Roman governor who sentenced Jesus to be crucified?",
            'options': ['Pilate', 'Herod', 'Caesar', 'Felix'],
            'correct_answer': 'Pilate',
            'category': 'New Testament',
            'explanation': "Pontius Pilate was the Roman governor who authorized Jesus' crucifixion. (Matthew 27:24-26)",
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+27%3A24-26&version=NIV'
        },
        {
            'text': "Who wrote the Book of Revelation?",
            'options': ['John', 'Paul', 'Peter', 'James'],
            'correct_answer': 'John',
            'category': 'New Testament',
            'explanation': "The apostle John wrote the Book of Revelation while exiled on Patmos. (Revelation 1:1,9)",
            'reference': 'https://www.biblegateway.com/passage/?search=Revelation+1%3A1,9&version=NIV'
        },
        {
            'text': "What was Paul's name before his conversion?",
            'options': ['Saul', 'Simon', 'Barnabas', 'Silas'],
            'correct_answer': 'Saul',
            'category': 'New Testament',
            'explanation': "Paul was known as Saul before his encounter with Jesus on the road to Damascus. (Acts 9:1-19)",
            'reference': 'https://www.biblegateway.com/passage/?search=Acts+9%3A1-19&version=NIV'
        },
        {
            'text': "What is the longest chapter in the Bible?",
            'options': ['Psalm 119', 'Psalm 23', 'Genesis 1', 'Matthew 5'],
            'correct_answer': 'Psalm 119',
            'category': 'Old Testament',
            'explanation': "Psalm 119 is the longest chapter in the Bible with 176 verses.",
            'reference': 'https://www.biblegateway.com/passage/?search=Psalm+119&version=NIV'
        },
        {
            'text': "Who was the father of King Solomon?",
            'options': ['David', 'Saul', 'Samuel', 'Jesse'],
            'correct_answer': 'David',
            'category': 'Old Testament',
            'explanation': "King Solomon was the son of King David and Bathsheba. (2 Samuel 12:24)",
            'reference': 'https://www.biblegateway.com/passage/?search=2+Samuel+12%3A24&version=NIV'
        },
        {
            'text': "What city's walls fell after the Israelites marched around it?",
            'options': ['Jericho', 'Ai', 'Bethel', 'Jerusalem'],
            'correct_answer': 'Jericho',
            'category': 'Old Testament',
            'explanation': "The walls of Jericho fell after the Israelites marched around them for seven days. (Joshua 6)",
            'reference': 'https://www.biblegateway.com/passage/?search=Joshua+6&version=NIV'
        },
        {
            'text': "How many people were saved on Noah's Ark?",
            'options': ['8', '2', '12', '40'],
            'correct_answer': '8',
            'category': 'Old Testament',
            'explanation': "Noah, his wife, his three sons, and their wives (8 people) were saved on the Ark. (Genesis 7:13)",
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+7%3A13&version=NIV'
        },
        {
            'text': "Which Gospel contains the Sermon on the Mount?",
            'options': ['Matthew', 'Mark', 'Luke', 'John'],
            'correct_answer': 'Matthew',
            'category': 'New Testament',
            'explanation': "The Sermon on the Mount is found in Matthew chapters 5-7.",
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+5-7&version=NIV'
        },
        {
            'text': 'How many days was Jonah in the belly of the fish?',
            'options': ['1', '2', '3', '4'],
            'correct_answer': '3',
            'category': 'Old Testament',
            'explanation': 'Jonah was in the belly of the great fish for three days and three nights. (Jonah 1:17)',
            'reference': 'https://www.biblegateway.com/passage/?search=Jonah+1%3A17&version=NIV'
        },
        {
            'text': 'Who denied Jesus three times?',
            'options': ['Peter', 'John', 'James', 'Andrew'],
            'correct_answer': 'Peter',
            'category': 'New Testament',
            'explanation': 'Peter denied knowing Jesus three times before the rooster crowed. (Luke 22:54-62)',
            'reference': 'https://www.biblegateway.com/passage/?search=Luke+22%3A54-62&version=NIV'
        },
        {
            'text': 'What was the name of the river where Jesus was baptized?',
            'options': ['Jordan', 'Nile', 'Euphrates', 'Tigris'],
            'correct_answer': 'Jordan',
            'category': 'New Testament',
            'explanation': 'Jesus was baptized by John the Baptist in the Jordan River. (Matthew 3:13-17)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+3%3A13-17&version=NIV'
        },
        {
            'text': 'Who was the father of John the Baptist?',
            'options': ['Zechariah', 'Joseph', 'Eli', 'Joachim'],
            'correct_answer': 'Zechariah',
            'category': 'New Testament',
            'explanation': 'Zechariah was a priest and the father of John the Baptist. (Luke 1:5-25)',
            'reference': 'https://www.biblegateway.com/passage/?search=Luke+1%3A5-25&version=NIV'
        },
        {
            'text': 'What was the name of the mountain where Moses received the Ten Commandments?',
            'options': ['Mount Sinai', 'Mount Horeb', 'Mount Ararat', 'Mount Moriah'],
            'correct_answer': 'Mount Sinai',
            'category': 'Old Testament',
            'explanation': 'Moses received the Ten Commandments from God on Mount Sinai. (Exodus 19-20)',
            'reference': 'https://www.biblegateway.com/passage/?search=Exodus+19-20&version=NIV'
        },
        {
            'text': 'How many days was Jesus in the tomb before His resurrection?',
            'options': ['1', '2', '3', '4'],
            'correct_answer': '3',
            'category': 'New Testament',
            'explanation': 'Jesus was in the tomb for three days before rising from the dead. (Matthew 12:40)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+12%3A40&version=NIV'
        },
        {
            'text': 'What was the name of the prophet who was taken to heaven in a chariot of fire?',
            'options': ['Elijah', 'Elisha', 'Isaiah', 'Jeremiah'],
            'correct_answer': 'Elijah',
            'category': 'Old Testament',
            'explanation': 'Elijah was taken up to heaven in a whirlwind with a chariot of fire. (2 Kings 2:11)',
            'reference': 'https://www.biblegateway.com/passage/?search=2+Kings+2%3A11&version=NIV'
        },
        {
            'text': 'What was the name of the place where Jesus was crucified?',
            'options': ['Golgotha', 'Gethsemane', 'Bethlehem', 'Nazareth'],
            'correct_answer': 'Golgotha',
            'category': 'New Testament',
            'explanation': 'Jesus was crucified at Golgotha, also called the Place of the Skull. (John 19:17-18)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+19%3A17-18&version=NIV'
        },
        {
            'text': 'What was the name of the high priest who questioned Jesus?',
            'options': ['Caiaphas', 'Annas', 'Pilate', 'Herod'],
            'correct_answer': 'Caiaphas',
            'category': 'New Testament',
            'explanation': 'Caiaphas was the high priest who led the questioning of Jesus before His crucifixion. (Matthew 26:57-68)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+26%3A57-68&version=NIV'
        },
        {
            'text': "Who interpreted Pharaoh's dreams in Egypt?",
            'options': ['Joseph', 'Moses', 'Daniel', 'Aaron'],
            'correct_answer': 'Joseph',
            'category': 'Old Testament',
            'explanation': 'Joseph interpreted Pharaoh\'s dreams, predicting seven years of plenty and seven years of famine. (Genesis 41)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+41&version=NIV'
        },
        {
            'text': 'Which prophet confronted King David about his sin with Bathsheba?',
            'options': ['Nathan', 'Samuel', 'Elijah', 'Elisha'],
            'correct_answer': 'Nathan',
            'category': 'Old Testament',
            'explanation': 'Nathan confronted David and told him the parable of the rich man and the poor man. (2 Samuel 12)',
            'reference': 'https://www.biblegateway.com/passage/?search=2+Samuel+12&version=NIV'
        },
        {
            'text': 'Who was the Roman governor who sentenced Jesus to be crucified?',
            'options': ['Pilate', 'Herod', 'Caesar', 'Felix'],
            'correct_answer': 'Pilate',
            'category': 'New Testament',
            'explanation': 'Pontius Pilate was the Roman governor who authorized Jesus\' crucifixion. (Matthew 27:24-26)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+27%3A24-26&version=NIV'
        },
        {
            'text': 'Who wrote the Book of Revelation?',
            'options': ['John', 'Paul', 'Peter', 'James'],
            'correct_answer': 'John',
            'category': 'New Testament',
            'explanation': 'The apostle John wrote the Book of Revelation while exiled on Patmos. (Revelation 1:1,9)',
            'reference': 'https://www.biblegateway.com/passage/?search=Revelation+1%3A1,9&version=NIV'
        },
        {
            'text': "What was Paul's name before his conversion?",
            'options': ['Saul', 'Simon', 'Barnabas', 'Silas'],
            'correct_answer': 'Saul',
            'category': 'New Testament',
            'explanation': 'Paul was known as Saul before his encounter with Jesus on the road to Damascus. (Acts 9:1-19)',
            'reference': 'https://www.biblegateway.com/passage/?search=Acts+9%3A1-19&version=NIV'
        },
        {
            'text': 'What is the longest chapter in the Bible?',
            'options': ['Psalm 119', 'Psalm 23', 'Genesis 1', 'Matthew 5'],
            'correct_answer': 'Psalm 119',
            'category': 'Old Testament',
            'explanation': 'Psalm 119 is the longest chapter in the Bible with 176 verses.',
            'reference': 'https://www.biblegateway.com/passage/?search=Psalm+119&version=NIV'
        },
        {
            'text': 'Who was the father of King Solomon?',
            'options': ['David', 'Saul', 'Samuel', 'Jesse'],
            'correct_answer': 'David',
            'category': 'Old Testament',
            'explanation': 'King Solomon was the son of King David and Bathsheba. (2 Samuel 12:24)',
            'reference': 'https://www.biblegateway.com/passage/?search=2+Samuel+12%3A24&version=NIV'
        },
        {
            'text': 'What city\'s walls fell after the Israelites marched around it?',
            'options': ['Jericho', 'Ai', 'Bethel', 'Jerusalem'],
            'correct_answer': 'Jericho',
            'category': 'Old Testament',
            'explanation': 'The walls of Jericho fell after the Israelites marched around them for seven days. (Joshua 6)',
            'reference': 'https://www.biblegateway.com/passage/?search=Joshua+6&version=NIV'
        },
        {
            'text': "How many people were saved on Noah's Ark?",
            'options': ['8', '2', '12', '40'],
            'correct_answer': '8',
            'category': 'Old Testament',
            'explanation': 'Noah, his wife, his three sons, and their wives (8 people) were saved on the Ark. (Genesis 7:13)',
            'reference': 'https://www.biblegateway.com/passage/?search=Genesis+7%3A13&version=NIV'
        },
        {
            'text': 'Which Gospel contains the Sermon on the Mount?',
            'options': ['Matthew', 'Mark', 'Luke', 'John'],
            'correct_answer': 'Matthew',
            'category': 'New Testament',
            'explanation': 'The Sermon on the Mount is found in Matthew chapters 5-7.',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+5-7&version=NIV'
        }
    ],
    'Hard': [
        {
            'text': 'How many years did the Israelites wander in the wilderness?',
            'options': ['30', '40', '50', '60'],
            'correct_answer': '40',
            'category': 'Old Testament',
            'explanation': 'The Israelites wandered in the wilderness for 40 years before entering the Promised Land. (Numbers 14:33-34)',
            'reference': 'https://www.biblegateway.com/passage/?search=Numbers+14%3A33-34&version=NIV'
        },
        {
            "text": "What is the shortest verse in the Bible?",
            "options": ["Jesus wept", "God is love", "Rejoice always", "Pray without ceasing"],
            "correct_answer": "Jesus wept",
            "explanation": "John 11:35 is the shortest verse in most English translations.",
            "reference": "https://www.biblegateway.com/passage/?search=John+11%3A35",
            "category": "New Testament"
        },
        {
            "text": "What Old Testament book contains the story of Samson?",
            "options": ["Judges", "Joshua", "1 Samuel", "Numbers"],
            "correct_answer": "Judges",
            "explanation": "Samson’s story is found in Judges 13–16.",
            "reference": "https://www.biblegateway.com/passage/?search=Judges+13-16",
            "category": "Old Testament"
        },
        {
            "text": "Who had a vision of a valley of dry bones?",
            "options": ["Ezekiel", "Isaiah", "Jeremiah", "Daniel"],
            "correct_answer": "Ezekiel",
            "explanation": "Ezekiel saw the valley of dry bones in a vision. (Ezekiel 37)",
            "reference": "https://www.biblegateway.com/passage/?search=Ezekiel+37",
            "category": "Old Testament"
        },
        {
            "text": "Which king saw the writing on the wall?",
            "options": ["Belshazzar", "Nebuchadnezzar", "Darius", "Cyrus"],
            "correct_answer": "Belshazzar",
            "explanation": "Belshazzar saw the mysterious writing on the wall. (Daniel 5)",
            "reference": "https://www.biblegateway.com/passage/?search=Daniel+5",
            "category": "Old Testament"
        },
        {
            "text": "Who was the mother of Samuel the prophet?",
            "options": ["Hannah", "Rachel", "Leah", "Rebekah"],
            "correct_answer": "Hannah",
            "explanation": "Hannah prayed for a son and gave birth to Samuel. (1 Samuel 1)",
            "reference": "https://www.biblegateway.com/passage/?search=1+Samuel+1",
            "category": "Old Testament"
        },
        {
            "text": "What Jewish festival commemorates the events in the Book of Esther?",
            "options": ["Purim", "Passover", "Hanukkah", "Tabernacles"],
            "correct_answer": "Purim",
            "explanation": "Purim celebrates the deliverance of the Jews as recorded in Esther.",
            "reference": "https://www.biblegateway.com/passage/?search=Esther+9",
            "category": "Old Testament"
        },
        {
            "text": "Which disciple doubted Jesus' resurrection until he saw Him?",
            "options": ["Thomas", "Peter", "Philip", "Andrew"],
            "correct_answer": "Thomas",
            "explanation": "Thomas is known as 'Doubting Thomas' because he demanded proof. (John 20:24–29)",
            "reference": "https://www.biblegateway.com/passage/?search=John+20%3A24-29",
            "category": "New Testament"
        },
        {
            "text": "Which prophet married a prostitute as a symbol of Israel’s unfaithfulness?",
            "options": ["Hosea", "Amos", "Joel", "Malachi"],
            "correct_answer": "Hosea",
            "explanation": "Hosea’s marriage to Gomer symbolized Israel's spiritual adultery. (Hosea 1)",
            "reference": "https://www.biblegateway.com/passage/?search=Hosea+1",
            "category": "Old Testament"
        },
        {
            "text": "Which disciple was a tax collector?",
            "options": ["Matthew", "James", "Simon", "Bartholomew"],
            "correct_answer": "Matthew",
            "explanation": "Matthew was a former tax collector. (Matthew 9:9)",
            "reference": "https://www.biblegateway.com/passage/?search=Matthew+9%3A9",
            "category": "New Testament"
        },
        {
            "text": "What New Testament book quotes the Old Testament the most?",
            "options": ["Matthew", "Romans", "Hebrews", "Revelation"],
            "correct_answer": "Matthew",
            "explanation": "Matthew frequently references Old Testament prophecy.",
            "reference": "https://www.biblegateway.com/passage/?search=Matthew+1",
            "category": "New Testament"
        },
        {
            "text": "How many chapters are in the book of Psalms?",
            "options": ["150", "100", "120", "180"],
            "correct_answer": "150",
            "explanation": "Psalms has 150 chapters—the most of any book in the Bible.",
            "reference": "https://www.biblegateway.com/passage/?search=Psalm+1",
            "category": "Old Testament"
        },
        {
            "text": "Who fell asleep and fell out of a window while Paul was preaching?",
            "options": ["Eutychus", "Tychicus", "Barnabas", "Silas"],
            "correct_answer": "Eutychus",
            "explanation": "Eutychus fell from a window and was revived by Paul. (Acts 20:9)",
            "reference": "https://www.biblegateway.com/passage/?search=Acts+20%3A9",
            "category": "New Testament"
        },
        {
            "text": "Which Old Testament figure was known for his patience?",
            "options": ["Job", "Moses", "Noah", "David"],
            "correct_answer": "Job",
            "explanation": "Job remained faithful through intense suffering. (Job 1–2)",
            "reference": "https://www.biblegateway.com/passage/?search=Job+1",
            "category": "Old Testament"
        },
        {
            "text": "What language was most of the Old Testament originally written in?",
            "options": ["Hebrew", "Greek", "Aramaic", "Latin"],
            "correct_answer": "Hebrew",
            "explanation": "Most of the Old Testament was written in Hebrew.",
            "reference": "https://en.wikipedia.org/wiki/Hebrew_Bible",
            "category": "General Knowledge"
        },
        {
            "text": "Who had a vision of a statue with a gold head and iron feet?",
            "options": ["Nebuchadnezzar", "Daniel", "Belshazzar", "Cyrus"],
            "correct_answer": "Nebuchadnezzar",
            "explanation": "Nebuchadnezzar had the dream which Daniel interpreted. (Daniel 2)",
            "reference": "https://www.biblegateway.com/passage/?search=Daniel+2",
            "category": "Old Testament"
        },
        {
            "text": "Who was Paul's companion on his first missionary journey?",
            "options": ["Barnabas", "Silas", "Timothy", "John Mark"],
            "correct_answer": "Barnabas",
            "explanation": "Barnabas accompanied Paul on his first mission trip. (Acts 13:2)",
            "reference": "https://www.biblegateway.com/passage/?search=Acts+13%3A2",
            "category": "New Testament"
        },
        {
            "text": "Who was the first king of the divided northern kingdom of Israel?",
            "options": ["Jeroboam", "Rehoboam", "Ahab", "Jehu"],
            "correct_answer": "Jeroboam",
            "explanation": "Jeroboam ruled the northern tribes after the kingdom split. (1 Kings 12)",
            "reference": "https://www.biblegateway.com/passage/?search=1+Kings+12",
            "category": "Old Testament"
        },
        {
            "text": "In which epistle is the 'armor of God' described?",
            "options": ["Ephesians", "Galatians", "Philippians", "Colossians"],
            "correct_answer": "Ephesians",
            "explanation": "Paul describes the armor of God in Ephesians 6.",
            "reference": "https://www.biblegateway.com/passage/?search=Ephesians+6",
            "category": "New Testament"
        },
        {
            "text": "Which king ordered the massacre of infants in Bethlehem?",
            "options": ["Herod", "Caesar", "Pilate", "Nero"],
            "correct_answer": "Herod",
            "explanation": "King Herod ordered the massacre to kill baby Jesus. (Matthew 2:16)",
            "reference": "https://www.biblegateway.com/passage/?search=Matthew+2%3A16",
            "category": "New Testament"
        },
        {
            "text": "Who is the 'weeping prophet' known for his laments?",
            "options": ["Jeremiah", "Ezekiel", "Isaiah", "Micah"],
            "correct_answer": "Jeremiah",
            "explanation": "Jeremiah is called the weeping prophet. (Jeremiah 9:1)",
            "reference": "https://www.biblegateway.com/passage/?search=Jeremiah+9%3A1",
            "category": "Old Testament"
        },
        {
            'text': 'Who was the first martyr of the Christian church?',
            'options': ['Stephen', 'James', 'Peter', 'Paul'],
            'correct_answer': 'Stephen',
            'category': 'New Testament',
            'explanation': 'Stephen was the first Christian martyr, stoned to death for his faith. (Acts 7:54-60)',
            'reference': 'https://www.biblegateway.com/passage/?search=Acts+7%3A54-60&version=NIV'
        },
        {
            'text': 'What was the name of the place where Jesus prayed before His arrest?',
            'options': ['Gethsemane', 'Golgotha', 'Bethlehem', 'Nazareth'],
            'correct_answer': 'Gethsemane',
            'category': 'New Testament',
            'explanation': 'Jesus prayed in the Garden of Gethsemane before His arrest. (Matthew 26:36-46)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+26%3A36-46&version=NIV'
        },
        {
            'text': 'Who was the first Gentile to be baptized?',
            'options': ['Cornelius', 'Lydia', 'The Ethiopian eunuch', 'The Philippian jailer'],
            'correct_answer': 'Cornelius',
            'category': 'New Testament',
            'explanation': 'Cornelius was the first Gentile to be baptized, showing the gospel was for all people. (Acts 10)',
            'reference': 'https://www.biblegateway.com/passage/?search=Acts+10&version=NIV'
        },
        {
            'text': 'What was the name of the mountain where Jesus gave the Sermon on the Mount?',
            'options': ['Mount of Olives', 'Mount Sinai', 'Mount Horeb', 'Mount Ararat'],
            'correct_answer': 'Mount of Olives',
            'category': 'New Testament',
            'explanation': 'Jesus gave the Sermon on the Mount, teaching His disciples. (Matthew 5-7)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+5-7&version=NIV'
        },
        {
            'text': 'Who was the first person to see Jesus after His resurrection?',
            'options': ['Mary Magdalene', 'Peter', 'John', 'The disciples'],
            'correct_answer': 'Mary Magdalene',
            'category': 'New Testament',
            'explanation': 'Mary Magdalene was the first person to see Jesus after His resurrection. (John 20:11-18)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+20%3A11-18&version=NIV'
        },
        {
            'text': 'What was the name of the place where Jesus was tempted by Satan?',
            'options': ['The wilderness', 'The temple', 'The mountain', 'The desert'],
            'correct_answer': 'The wilderness',
            'category': 'New Testament',
            'explanation': 'Jesus was tempted by Satan in the wilderness for 40 days. (Matthew 4:1-11)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+4%3A1-11&version=NIV'
        },
        {
            'text': 'Who was the first person to be baptized by John the Baptist?',
            'options': ['Jesus', 'Peter', 'Andrew', 'John'],
            'correct_answer': 'Jesus',
            'category': 'New Testament',
            'explanation': 'Jesus was baptized by John the Baptist in the Jordan River. (Matthew 3:13-17)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+3%3A13-17&version=NIV'
        },
        {
            'text': 'What was the name of the place where Jesus performed His first miracle?',
            'options': ['Cana', 'Bethlehem', 'Nazareth', 'Jerusalem'],
            'correct_answer': 'Cana',
            'category': 'New Testament',
            'explanation': 'Jesus performed His first miracle at a wedding in Cana, turning water into wine. (John 2:1-11)',
            'reference': 'https://www.biblegateway.com/passage/?search=John+2%3A1-11&version=NIV'
        },
        {
            'text': 'Who was the first person to recognize Jesus as the Messiah?',
            'options': ['Peter', 'John', 'Andrew', 'Simon'],
            'correct_answer': 'Peter',
            'category': 'New Testament',
            'explanation': 'Peter was the first to recognize Jesus as the Messiah, the Son of the living God. (Matthew 16:16)',
            'reference': 'https://www.biblegateway.com/passage/?search=Matthew+16%3A16&version=NIV'
        }
    ]
}

class GuestUser(AnonymousUserMixin):
    is_guest = True
    username = "Guest"

def register_routes(app):
    @app.route('/')
    def home():
        return redirect(url_for('welcome'))

    @app.route('/health')
    def health_check():
        """Simple health check endpoint for Render"""
        return {'status': 'healthy', 'message': 'Bible Quiz AI is running on Render!'}

    @app.route('/submit', methods=['GET', 'POST'])
    def submit_suggestion():
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')
            location = request.form.get('location')
            
            if not title or not content:
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('submit_suggestion'))
            
            suggestion = Suggestion(
                title=title,
                content=content,
                location=location,
                user_id=current_user.id if current_user.is_authenticated else None
            )
            
            db.session.add(suggestion)
            db.session.commit()
            
            flash('Thank you for your suggestion!', 'success')
            return redirect(url_for('home'))
        
        return render_template('submit.html')

    @app.route('/suggestions')
    def view_suggestions():
        suggestions = Suggestion.query.filter_by(status='approved').order_by(Suggestion.created_at.desc()).all()
        return render_template('suggestions.html', suggestions=suggestions)

    @app.route('/admin')
    @login_required
    def admin():
        if not current_user.is_admin:
            flash('Access denied', 'error')
            return redirect(url_for('home'))
        
        suggestions = Suggestion.query.order_by(Suggestion.created_at.desc()).all()
        return render_template('admin.html', suggestions=suggestions)

    @app.route('/admin/suggestion/<int:id>/<action>')
    @login_required
    def admin_action(id, action):
        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 403
        
        suggestion = Suggestion.query.get_or_404(id)
        if action == 'approve':
            suggestion.status = 'approved'
        elif action == 'reject':
            suggestion.status = 'rejected'
        
        db.session.commit()
        return redirect(url_for('admin'))

    @app.route('/admin/generate-questions', methods=['POST'])
    @login_required
    def admin_generate_questions():
        """Admin route to manually trigger question generation"""
        if not current_user.is_admin:
            flash('Access denied', 'error')
            return redirect(url_for('home'))
        
        try:
            from question_generator import generate_daily_questions
            success = generate_daily_questions()
            if success:
                flash('Questions generated successfully!', 'success')
            else:
                flash('Error generating questions. Check the logs for details.', 'error')
        except Exception as e:
            logger.error(f"Error in manual question generation: {str(e)}")
            flash('Error generating questions. Check the logs for details.', 'error')
        
        return redirect(url_for('admin'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        logger.debug('Accessing login page')
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            user = User.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password', 'error')
        
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        logger.debug('Accessing register page')
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
                return redirect(url_for('register'))
            
            new_user = User(
                email=email,
                password_hash=generate_password_hash(password)
            )
            
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                logger.error(f'Error during registration: {str(e)}')
                db.session.rollback()
                flash('An error occurred during registration', 'error')
        
        return render_template('register.html')

    @app.route('/dashboard')
    def dashboard():
        logger.debug('Accessing dashboard')
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            return redirect(url_for('login'))
        
        return render_template('dashboard.html', user=user)

    @app.route('/quiz/<difficulty>', methods=['GET', 'POST'])
    def take_quiz(difficulty):
        logger.debug(f'Accessing quiz with difficulty {difficulty}')
        if difficulty not in ['Easy', 'Medium', 'Hard']:
            flash('Invalid difficulty level', 'error')
            return redirect(url_for('home'))
        
        if request.method == 'POST':
            try:
                answer = request.form.get('answer')
                if not answer:
                    flash('Please select an answer', 'error')
                    return redirect(url_for('take_quiz', difficulty=difficulty))
                
                if 'answers' not in session:
                    session['answers'] = []
                session['answers'].append(answer)
                session.modified = True
                
                logger.info(f"Answer submitted for difficulty {difficulty}")
                
                if len(session['answers']) >= len(session['questions']):
                    logger.info("Quiz completed, redirecting to results")
                    return redirect(url_for('results'))
                
                current_question = session['questions'][len(session['answers'])]
                return render_template('quiz.html',
                                    question=current_question,
                                    difficulty=difficulty,
                                    current_question=len(session['answers']) + 1,
                                    total_questions=len(session['questions']))
            except Exception as e:
                logger.error(f"Error in quiz submission: {str(e)}")
                flash('An error occurred. Please try again.', 'error')
                return redirect(url_for('home'))
        
        try:
            if 'questions' not in session or 'difficulty' not in session or session['difficulty'] != difficulty:
                # Get questions from database based on difficulty
                questions = Question.query.filter_by(difficulty=difficulty).order_by(db.func.random()).limit(5).all()
                if not questions:
                    flash('No questions available for this difficulty level', 'error')
                    return redirect(url_for('home'))
                
                # Convert questions to session-friendly format
                session_questions = []
                for q in questions:
                    session_questions.append({
                        'text': q.text,
                        'options': q.options,
                        'correct_answer': q.correct_answer,
                        'category': q.category if hasattr(q, 'category') else 'General'
                    })
                
                session['questions'] = session_questions
                session['answers'] = []
                session['difficulty'] = difficulty
                session.modified = True
                logger.info(f"New quiz initialized with {len(session_questions)} questions")
            
            current_question_index = len(session.get('answers', []))
            if current_question_index >= len(session['questions']):
                return redirect(url_for('results'))
                
            current_question = session['questions'][current_question_index]
            return render_template('quiz.html',
                                question=current_question,
                                difficulty=difficulty,
                                current_question=current_question_index + 1,
                                total_questions=len(session['questions']))
        except Exception as e:
            logger.error(f"Error in quiz initialization: {str(e)}")
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('home'))

    @app.route('/results')
    def results():
        if 'questions' not in session or 'answers' not in session:
            flash('No quiz in progress', 'error')
            return redirect(url_for('home'))
        
        try:
            correct_answers = sum(1 for q, a in zip(session['questions'], session['answers'])
                                if a == q['correct_answer'])
            total_questions = len(session['questions'])
            score = int((correct_answers / total_questions) * 100)
            
            questions = []
            for q, a in zip(session['questions'], session['answers']):
                questions.append({
                    'text': q['text'],
                    'user_answer': a,
                    'correct_answer': q['correct_answer']
                })
            
            session.pop('questions', None)
            session.pop('answers', None)
            session.pop('difficulty', None)
            
            return render_template('results.html',
                                score=score,
                                correct_answers=correct_answers,
                                total_questions=total_questions,
                                questions=questions)
        except Exception as e:
            logger.error(f"Error in results calculation: {str(e)}")
            flash('An error occurred while calculating results.', 'error')
            return redirect(url_for('home'))

    @app.route('/logout')
    def logout():
        logger.debug('User logging out')
        session.clear()
        return redirect(url_for('home'))

    @app.errorhandler(404)
    def not_found_error(error):
        logger.error(f'404 error: {str(error)}')
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'500 error: {str(error)}')
        db.session.rollback()
        return render_template('500.html'), 500

    @app.route('/welcome')
    def welcome():
        return render_template('welcome.html')

    @app.route('/public-quiz/<difficulty>', methods=['GET', 'POST'])
    def public_quiz(difficulty):
        """Non-login-required quiz route with feedback and scoring"""
        logger.debug(f'Accessing public quiz with difficulty {difficulty}')
        
        if difficulty not in ['Easy', 'Medium', 'Hard']:
            flash('Invalid difficulty level', 'error')
            return redirect(url_for('welcome'))

        # Navigation (next/prev) logic
        next_q = request.args.get('next', type=int)
        prev_q = request.args.get('prev', type=int)

        # Handle navigation from template
        if next_q:
            current_idx = len(session['answers'])
            if current_idx < len(session['questions']):
                # Move to next question
                pass
            else:
                # Quiz completed, go to results
                return redirect(url_for('public_quiz_results'))
            show_feedback = False
        elif prev_q:
            current_idx = max(0, len(session['answers']) - 1)
            if session['answers']:
                session['answers'].pop()
                session['start_times'].pop()
                session.modified = True
            show_feedback = False
        else:
            # Initialize session data if not present
            if 'questions' not in session or 'answers' not in session or 'score' not in session:
                session['questions'] = []
                session['answers'] = []
                session['difficulty'] = difficulty
                session['score'] = 0
                session['start_times'] = []  # Track start time for each question
                session.modified = True

            # Start a new quiz on GET (if no questions or navigation)
            if request.method == 'GET' and not next_q and not prev_q:
                session.clear()
                questions = random.sample(SAMPLE_QUESTIONS[difficulty], min(5, len(SAMPLE_QUESTIONS[difficulty])))
                session['questions'] = questions
                session['answers'] = []
                session['difficulty'] = difficulty
                session['score'] = 0
                session['start_times'] = [datetime.utcnow().timestamp()]  # Start time for Q1
                session.modified = True
                current_idx = 0
                show_feedback = False
            else:
                # Navigation: next/prev
                current_idx = len(session['answers']) if not prev_q else len(session['answers']) - 1
                show_feedback = False

        # Handle answer submission
        if request.method == 'POST':
            answer = request.form.get('answer')
            if not answer:
                flash('Please select an answer', 'error')
                return redirect(url_for('public_quiz', difficulty=difficulty))
            # Calculate time taken for this question
            now = datetime.utcnow().timestamp()
            start_time = session['start_times'][-1] if session['start_times'] else now
            time_taken = max(1, int(now - start_time))  # At least 1 second
            
            # New scoring system based on difficulty
            if difficulty == 'Easy':
                max_points = 12  # 12 points per question = 60 total for 5 questions
            elif difficulty == 'Medium':
                max_points = 18  # 18 points per question = 90 total for 5 questions
            else:  # Hard
                max_points = 24  # 24 points per question = 120 total for 5 questions
            
            # Bonus for quick answers (optional - you can remove this if you want flat scoring)
            # Give full points for answers under 10 seconds, slight penalty for slower answers
            if time_taken <= 10:
                points = max_points
            else:
                # Small penalty for taking longer than 10 seconds
                penalty = min(3, (time_taken - 10) // 5)  # Max 3 point penalty
                points = max(max_points - penalty, max_points // 2)  # At least half points
            # Get current question
            current_idx = len(session['answers'])
            current_question = session['questions'][current_idx]
            is_correct = (answer == current_question['correct_answer'])
            if is_correct:
                session['score'] += points
            session['answers'].append(answer)
            session['start_times'].append(now)
            session.modified = True
            show_feedback = True
            # If last question, show feedback but don't redirect yet
            # User will click "Finish Quiz" to go to results
        else:
            # Not POST: get current question
            current_question = session['questions'][current_idx]

        # Prepare template variables
        user_answer = session['answers'][-1] if show_feedback and session['answers'] else None
        progress_percent = int(((current_idx+1)/len(session['questions']))*100)
        
        # Add explanation and reference to question object if not present
        if 'explanation' not in current_question:
            current_question['explanation'] = f"This question tests your knowledge of {difficulty.lower()} biblical concepts. Study the relevant passages to deepen your understanding."
        if 'reference' not in current_question:
            current_question['reference'] = "https://www.biblegateway.com/"
            
        # Calculate max score based on difficulty
        if difficulty == 'Easy':
            max_score = len(session['questions']) * 12  # 60 total for 5 questions
        elif difficulty == 'Medium':
            max_score = len(session['questions']) * 18  # 90 total for 5 questions
        else:  # Hard
            max_score = len(session['questions']) * 24  # 120 total for 5 questions
            
        return render_template('quiz.html',
            question=current_question,
            difficulty=difficulty,
            current_question=current_idx+1,
            total_questions=len(session['questions']),
            show_feedback=show_feedback,
            user_answer=user_answer,
            score=session.get('score', 0),
            max_score=max_score,
            progress_percent=progress_percent
        )

    @app.route('/public-quiz-results')
    def public_quiz_results():
        """Results page for non-login-required quiz"""
        if 'questions' not in session or 'answers' not in session:
            flash('No quiz in progress', 'error')
            return redirect(url_for('welcome'))
        
        try:
            # Get the actual score points from session
            actual_score = session.get('score', 0)
            total_questions = len(session['questions'])
            difficulty = session.get('difficulty', 'Easy')
            
            # Calculate max score based on difficulty
            if difficulty == 'Easy':
                max_score = total_questions * 12  # 60 total for 5 questions
            elif difficulty == 'Medium':
                max_score = total_questions * 18  # 90 total for 5 questions
            else:  # Hard
                max_score = total_questions * 24  # 120 total for 5 questions
                
            correct_answers = sum(1 for q, a in zip(session['questions'], session['answers'])
                                if a == q['correct_answer'])
            accuracy = int((correct_answers / total_questions) * 100)
            
            questions = []
            for q, a in zip(session['questions'], session['answers']):
                questions.append({
                    'text': q['text'],
                    'user_answer': a,
                    'correct_answer': q['correct_answer']
                })
            
            session.pop('questions', None)
            session.pop('answers', None)
            session.pop('difficulty', None)
            session.pop('score', None)
            
            return render_template('results.html',
                                score=actual_score,
                                max_score=max_score,
                                accuracy=accuracy,
                                correct_answers=correct_answers,
                                total_questions=total_questions,
                                questions=questions)
        except Exception as e:
            logger.error(f"Error in public quiz results calculation: {str(e)}")
            flash('An error occurred while calculating results.', 'error')
            return redirect(url_for('welcome'))

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        # Clear any quiz-related session data
        session.pop('questions', None)
        session.pop('answers', None)
        session.pop('difficulty', None)
        
        if request.method == 'POST':
            try:
                logger.info("Processing contact form submission")
                name = request.form.get('name')
                email = request.form.get('email')
                subject = request.form.get('subject')
                message = request.form.get('message')
                
                logger.info(f"Form data received - Name: {name}, Email: {email}, Subject: {subject}")
                
                if not all([name, email, subject, message]):
                    logger.warning("Missing required fields in contact form")
                    flash('All fields are required', 'error')
                    return redirect(url_for('contact'))
                
                try:
                    # Create and save the contact message using the model
                    logger.info("Creating new ContactMessage object")
                    contact_message = ContactMessage(
                        name=name,
                        email=email,
                        subject=subject,
                        message=message
                    )
                    logger.info("Adding contact message to database session")
                    db.session.add(contact_message)
                    
                    # Log the current database state
                    logger.info(f"Database URI: {db.engine.url}")
                    logger.info(f"Database tables: {db.engine.table_names()}")
                    
                    try:
                        logger.info("Attempting to commit database transaction")
                        db.session.commit()
                        logger.info("Contact message saved successfully")
                    except Exception as commit_error:
                        logger.error(f"Error during commit: {str(commit_error)}", exc_info=True)
                        db.session.rollback()
                        raise
                    
                    flash('Thank you for your message! We will get back to you soon.', 'success')
                    return redirect(url_for('welcome'))
                except Exception as db_error:
                    logger.error(f"Database error in contact form submission: {str(db_error)}", exc_info=True)
                    db.session.rollback()
                    raise
            except Exception as e:
                logger.error(f"Error in contact form submission: {str(e)}", exc_info=True)
                flash('An error occurred while sending your message. Please try again.', 'error')
                return redirect(url_for('contact'))
        
        # Clear any existing flash messages before rendering the contact form
        get_flashed_messages()
        
        return render_template('contact.html')

    @app.route('/play-as-guest')
    def play_as_guest():
        # Create a guest user with a temporary email
        guest = User(email="guest@temp.com", is_guest=True)
        guest.set_password("guest_password")
        db.session.add(guest)
        db.session.commit()
        login_user(guest)
        return redirect(url_for('welcome')) 