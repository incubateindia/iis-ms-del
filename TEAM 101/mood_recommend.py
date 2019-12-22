from bs4 import BeautifulSoup as SOUP
import re
import requests as HTTP
import random
from flask import jsonify

class RecommendEmotion(object):

    def __init__(self,score):
        vocab = {}
        vocab['1'] = 'Happy'
        vocab['2'] = 'Calm'
        vocab['3'] = 'Sad'
        vocab['4'] = 'Fear'
        vocab['5'] = 'Angry'
        self.vocab  = vocab
        self.score = score

        self.movies_df  = {'Sad' : [['Hustlers','https://www.imdb.com/title/tt5503686/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BNjM5ZTNiNGMtMDA2OC00MDYyLWEyNzAtOWZmMzFlY2VmOWM4XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['The Lion King','https://www.imdb.com/title/tt6105098/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMjIwMjE1Nzc4NV5BMl5BanBnXkFtZTgwNDg4OTA1NzM@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['The Shawshank Redemption','https://www.imdb.com/title/tt0111161/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Gladiator','https://www.imdb.com/title/tt0172495/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMDliMmNhNDEtODUyOS00MjNlLTgxODEtN2U3NzIxMGVkZTA1L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['The Sky is Pink','https://www.imdb.com/title/tt8902990/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BNWQ5OTJjYTktMGNmYi00ZGMwLTlkYTgtODY3YWIxZDgyMzkwXkEyXkFqcGdeQXVyOTg4MzcyNzQ@._V1_UY98_CR0,0,67,98_AL_.jpg'],
        ['Pulp Fiction','https://www.imdb.com/title/tt0110912/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_UY98_CR0,0,67,98_AL_.jpg'],
        ['A Star is Born','https://www.imdb.com/title/tt1517451/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BNmE5ZmE3OGItNTdlNC00YmMxLWEzNjctYzAwOGQ5ODg0OTI0XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Goodfellas','https://www.imdb.com/title/tt0099685/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BY2NkZjEzMDgtN2RjYy00YzM1LWI4ZmQtMjIwYjFjNmI3ZGEwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Forrest Gump','https://www.imdb.com/title/tt0109830/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UY98_CR0,0,67,98_AL_.jpg']],
        'Anger' : [['Toy Story 4','https://www.imdb.com/title/tt1979376/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMTYzMDM4NzkxOV5BMl5BanBnXkFtZTgwNzM1Mzg2NzM@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['The Nightmare Before Christams','https://www.imdb.com/title/tt0107688/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BNWE4OTNiM2ItMjY4Ni00ZTViLWFiZmEtZGEyNGY2ZmNlMzIyXkEyXkFqcGdeQXVyMDU5NDcxNw@@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['The Karate Kid','https://www.imdb.com/title/tt0087538/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BNTkzY2YzNmYtY2ViMS00MThiLWFlYTEtOWQ1OTBiOGEwMTdhXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['The Golden Compass','https://www.imdb.com/title/tt0385752/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMTM2NDkxMjQxMV5BMl5BanBnXkFtZTYwNTMxMDM4._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Inside Out','https://www.imdb.com/title/tt2096673/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BOTgxMDQwMDk0OF5BMl5BanBnXkFtZTgwNjU5OTg2NDE@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Jumanji','https://www.imdb.com/title/tt0113497/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BZTk2ZmUwYmEtNTcwZS00YmMyLWFkYjMtNTRmZDA3YWExMjc2XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UY98_CR3,0,67,98_AL_.jpg'],
        ['Despicable Me 3','https://www.imdb.com/title/tt3469046/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BNjUyNzQ2MTg3Ml5BMl5BanBnXkFtZTgwNzE4NDM3MTI@._V1_UX67_CR0,0,67,98_AL_.jpg']],
        'Calm': [['Trap','https://www.imdb.com/title/tt0041983/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMTYxNDg4NDA3NF5BMl5BanBnXkFtZTcwMzY1MzcyMQ@@._V1_UY98_CR0,0,67,98_AL_.jpg'],
        ['Scarface','https://www.imdb.com/title/tt0023427/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BYmMxZTU2ZDUtM2Y1MS00ZWFmLWJlN2UtNzI0OTJiOTYzMTk3XkEyXkFqcGdeQXVyMjUxODE0MDY@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Sweet Smell of Success','https://www.imdb.com/title/tt0051036/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMjE5NTU3YWYtOWIxNi00YWZhLTg2NzktYzVjZWY5MDQ4NzVlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['The Big Heat','https://www.imdb.com/title/tt0045555/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMmY1YzRmZDgtMTU4NS00NTcwLWE3N2EtNDc0MTk1ODg2YTA2XkEyXkFqcGdeQXVyMTYzMTY1MjQ@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['The Killers','https://www.imdb.com/title/tt0038669/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BNGZmNmJhY2YtMjhjNy00YThhLTk5MWItNDU2NTZhNzg1MTYwXkEyXkFqcGdeQXVyMTMxMTY0OTQ@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['The Hitch-Hiker','https://www.imdb.com/title/tt0045877/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BNjM3NTY4OWYtNzkzNy00ZGZhLThkMmUtYjM4OTRlNmY0MWI2L2ltYWdlXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_UX67_CR0,0,67,98_AL_.jpg']],
        'Fear': [['The Peanut Butter Falcon','https://www.imdb.com/title/tt7339248/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BOWVmZGQ0MGYtMDI1Yy00MDkxLWJiYjQtMmZjZmQ0NDFmMDRhXkEyXkFqcGdeQXVyNjg3MDMxNzU@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Ford v Ferrari','https://www.imdb.com/title/tt1950186/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BYzcyZDNlNDktOWRhYy00ODQ5LTg1ODQtZmFmZTIyMjg2Yjk5XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Moneyball','https://www.imdb.com/title/tt1210166/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMjAxOTU3Mzc1M15BMl5BanBnXkFtZTcwMzk1ODUzNg@@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Remember the Titans','https://www.imdb.com/title/tt0210945/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BYThkMzgxNjEtMzFiOC00MTI0LWI5MDItNDVmYjA4NzY5MDQ2L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Dodgeball','https://www.imdb.com/title/tt0364725/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMTIwMzE2MjM4MV5BMl5BanBnXkFtZTYwNjA1OTY3._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Rocky','https://www.imdb.com/title/tt0075148/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMTY5MDMzODUyOF5BMl5BanBnXkFtZTcwMTQ3NTMyNA@@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['The Fighter','https://www.imdb.com/title/tt0964517/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMTM0ODk3MjM1MV5BMl5BanBnXkFtZTcwNzc1MDIwNA@@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Rush','https://www.imdb.com/title/tt1979320/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BOWEwODJmZDItYTNmZC00OGM4LThlNDktOTQzZjIzMGQxODA4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['SouthPaw','https://www.imdb.com/title/tt1798684/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMjI1MTcwODk0MV5BMl5BanBnXkFtZTgwMTgwMDM5NTE@._V1_UX67_CR0,0,67,98_AL_.jpg']],
        'Happy' : [['The Irishmen','https://www.imdb.com/title/tt1302006/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMGUyM2ZiZmUtMWY0OC00NTQ4LThkOGUtNjY2NjkzMDJiMWMwXkEyXkFqcGdeQXVyMzY0MTE3NzU@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Midsommar','https://www.imdb.com/title/tt8772262/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMzQxNzQzOTQwM15BMl5BanBnXkFtZTgwMDQ2NTcwODM@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Stuber','https://www.imdb.com/title/tt7734218/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BOGE1ZjFhYzAtYWM4ZC00NGI1LWFmYzMtZWRhZDhjMjE4YzBjXkEyXkFqcGdeQXVyODQzNTE3ODc@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Inception','https://www.imdb.com/title/tt1375666/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Blade Runner','https://www.imdb.com/title/tt1856101/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BNzA1Njg4NzYxOV5BMl5BanBnXkFtZTgwODk5NjU3MzI@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Glass','https://www.imdb.com/title/tt6823368/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BMTY1OTA2MjI5OV5BMl5BanBnXkFtZTgwNzkxMjU4NjM@._V1_UY98_CR1,0,67,98_AL_.jpg'],
        ['Hotel Mumbai','https://www.imdb.com/title/tt5461944/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BYTJlZWY2YjYtZGIxMy00MDEwLTliNzMtZGM3MDQ1NzlmNDY1XkEyXkFqcGdeQXVyNDY2MjcyOTQ@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Goodfellas','https://www.imdb.com/title/tt0099685/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BY2NkZjEzMDgtN2RjYy00YzM1LWI4ZmQtMjIwYjFjNmI3ZGEwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_UX67_CR0,0,67,98_AL_.jpg'],
        ['Forrest Gump','https://www.imdb.com/title/tt0109830/?ref_=adv_li_tt','https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_UY98_CR0,0,67,98_AL_.jpg']]
        }
        self.books_df = {'Sad' : [['What If?','https://whatareyoureadingtoday.com/science-can-be-cool-and-funny/','https://whatareyoureadingtoday.com/wp-content/uploads/2018/10/WhatIf2.jpg'],
        ['Hats and Doctors','https://whatareyoureadingtoday.com/short-stories-about-the-indian-middle-class/','https://whatareyoureadingtoday.com/wp-content/uploads/2018/09/Hats-and-Doctors.jpg'],
        ['Invitation to the Waltz','https://whatareyoureadingtoday.com/invitation-to-the-waltz-by-rosamond-lehmann/','https://whatareyoureadingtoday.com/wp-content/uploads/2017/10/Invitation-to-the-Waltz.jpg'],
        ['The Lost art of Keeping Secrets','https://whatareyoureadingtoday.com/the-lost-art-of-keeping-secrets/','https://whatareyoureadingtoday.com/wp-content/uploads/2017/10/The-Lost-Art-of-Keeping-Secrets.jpg']],
        'Anger':[['Mrs Funny Bone','https://whatareyoureadingtoday.com/you-go-girl/','https://whatareyoureadingtoday.com/wp-content/uploads/2019/08/Mrs-Funnybones.jpg'],
        ['The Domestic Goddess','https://whatareyoureadingtoday.com/had-a-tiring-day-well-heres-something-to-refresh-you/','https://whatareyoureadingtoday.com/wp-content/uploads/2019/05/The-Undomestic-Goddess.jpg'],
        ['The Lost art of Keeping Secrets','https://whatareyoureadingtoday.com/the-lost-art-of-keeping-secrets/','https://whatareyoureadingtoday.com/wp-content/uploads/2017/10/The-Lost-Art-of-Keeping-Secrets.jpg']],
        'Calm':[['A Visit from the Goon Squad','https://whatareyoureadingtoday.com/when-your-life-diverges-from-the-path-you-have-chosen/','https://whatareyoureadingtoday.com/wp-content/uploads/2018/07/A-Visit-from-the-Goon-Squad.jpg'],
        ['Litte Paris Bookshop','https://whatareyoureadingtoday.com/when-you-are-feeling-a-little-lost-on-this-crazy-journey-called-life/','https://whatareyoureadingtoday.com/wp-content/uploads/2018/07/The-Little-Paris-Bookshop.jpg'],
        ['Les Miserables','https://whatareyoureadingtoday.com/when-life-and-society-seem-to-have-reached-their-bleakest-points/','https://whatareyoureadingtoday.com/wp-content/uploads/2018/07/Les-Miserables.jpg'],
        ['The Forty Rules of Love','https://whatareyoureadingtoday.com/love-is-the-only-rule/','https://whatareyoureadingtoday.com/wp-content/uploads/2018/11/The-Forty-Rules-of-Love.jpg']],
        'Happy': [['Animal People','https://whatareyoureadingtoday.com/if-you-think-your-life-is-hard/','https://whatareyoureadingtoday.com/wp-content/uploads/2019/06/AnimalsPeople.jpg'],
        ['The House of Spirits','https://whatareyoureadingtoday.com/the-spirit-of-the-past/','https://whatareyoureadingtoday.com/wp-content/uploads/2019/08/The-House-of-the-Spirits.jpg'],
        ['Wonder IF I','https://whatareyoureadingtoday.com/wonder-if-i/','https://whatareyoureadingtoday.com/wp-content/uploads/2018/09/wonder.png']],
        'Fear':[['TIN MAN','https://whatareyoureadingtoday.com/almost-all-first-love-stories-are-tragic-but-this-one-is-beautiful-too/','https://whatareyoureadingtoday.com/wp-content/uploads/2019/07/Tin-Man.jpg'],
        ['The Shadow of the Wind','https://whatareyoureadingtoday.com/when-youve-finished-watching-the-final-season-of-got-and-are-looking-for-something-wildly-adventurous-and-mysterious/','https://whatareyoureadingtoday.com/wp-content/uploads/2019/05/The-Shadow.jpg'],
        ['Human Acts','https://whatareyoureadingtoday.com/when-you-feel-helpless-at-the-state-of-the-society/','https://whatareyoureadingtoday.com/wp-content/uploads/2018/09/Human-Acts.jpg']]        }

        self.blog_df = {'Happy': [['Erratic Wisdom','http://erraticwisdom.com/'],
        ['Philosophy and Life','http://www.markvernon.com/friendshiponline/dotclear/'],
        ['Will Wilkinson','http://www.markvernon.com/friendshiponline/dotclear/'],
        ['Talking Philosophy','http://blog.talkingphilosophy.com/'],
        ['Leiter Reports','http://leiterreports.typepad.com/blog/']],
        'Calm': [['Philosophy, etc','http://www.philosophyetc.net/'],
        ['Thoughts Arguments and Rants','http://tar.weatherson.org/'],
        ['Ancient Philosophy Society','http://www.ancientphilosophysociety.org/'],
        ['Unpolished Jade','http://unpolishedjade.wordpress.com/'],
        ['Philosopher Carnival','http://philosophycarnival.blogspot.com/']],
        'Angry' :[ ['The Splintered Mind','http://thesplinteredmind.blogspot.com/'],
        ['A Beautiful Revolution','http://www.abeautifulrevolution.com/blog/'],
        ['Beyond Blue','http://blog.beliefnet.com/beyondblue/'],
        ['Postpartum Progress','http://postpartumprogress.typepad.com/'],
        ['Furious Seasons','http://www.furiousseasons.com/']],
        'Fear' : [['105 Action Steps to Make you Bold and Successful','http://theboldlife.com/2013/10/105-action-steps-to-make-you-bold-brave-and-successful/'],
        ['How to create Fearless Future','http://theboldlife.com/2013/05/how-to-create-a-fearless-future/'],
        ['Love Versus Fear: A Moment by Moment Choice','http://theboldlife.com/2013/08/love-versus-fear-a-moment-by-moment-choice/'],
        ['You are a Risktaker','http://theboldlife.com/2013/06/the-bold-life-show-you-are-a-risktaker-video/'],
        ['Passing Judgement','http://theboldlife.com/2013/07/passing-judgment-just-like-me/']],
        'Sad': [['Storytime with John','http://storytimewithjohn.com/'],
        ['Multiple Momstrosity','http://multiplemomstrosity.blogspot.ca/'],
        ['Passive Aggressive Notes','http://www.passiveaggressivenotes.com/'],
        ['The Bloggess','http://thebloggess.com/'],
        ['Pleated-Jeans','http://www.pleated-jeans.com/']]}

        self.song_df = {'Sad': [['Hometown Glory','https://youtu.be/BW9Fzwuf43c'],
        ['Young and Beautiful','https://youtu.be/Te11UaHOHMQ'],
        ['The Call','https://youtu.be/oNsQewlFtEs'],
        ['I will Always Love You','https://youtu.be/3JWTaaS7LdU']],
        'Fear': [['Sweet Disposition','https://youtu.be/jxKjOOR9sPU'],
        ['Back to Black','https://youtu.be/TJAfLE39ZZ8'],
        ['With or Without You','https://youtu.be/imogyJJBYTo'],
        ['Fix You','https://youtu.be/hbJuEFs7-kU']],
        'Angry': [['Somebody that I used to Know','https://youtu.be/8UVNT4wvIGY'],
        ['You Found Me','https://youtu.be/jFg_8u87zT0'],
        ['My Immortal','https://youtu.be/5anLPw0Efmo'],
        ['Apologize','https://youtu.be/fm0T7_SGee4']],
        'Calm': [['How to Save a Life','https://youtu.be/cjVQ36NhbMk'],
        ['Let Go','https://youtu.be/r3Cg1wxgX6M'],
        ['May It Be','https://youtu.be/_8u4VLk0iTI'],
        ['Stay with Me','https://youtu.be/pB-5XG-DbAA']],
        'Happy' : [['Forever and Always','https://youtu.be/G0pbW-fUWLI'],
        ['Eleanor Rigby','https://youtu.be/ojpSiNZA5_0'],
        ['I will Remember You','https://youtu.be/nSz16ngdsG0'],
        ['Hallelujah','https://youtu.be/vEOZLQ3d1FI']]}


    def movies(self):
        movie_choice = random.sample(self.movies_df[self.vocab[self.score]],k=3) ## get the choice of movies
        return movie_choice ## returns in the format of [title,url,image]

    def books(self):
        books_choice = random.sample(self.books_df[self.vocab[self.score]],k=3) ## get the choice of movies
        return books_choice ## Title Url Image
       
    def blogs(self):
        blog_choice = random.sample(self.blog_df[self.vocab[self.score]],k=3) ## get the choice of movies
        return blog_choice ## Title Url Image

    def songs(self):
        song_choice = random.sample(self.song_df[self.vocab[self.score]],k=3) ## get the choice of movies
        return song_choice ## Title Url Image

    # def recommend(self,score):
    #     rec = RecommendEmotion(str(score))
    #     movies = rec.movies();
    #     movie_json = []
    #     for m in movies:
    #         for p in m:
    #             x = jsonify({
    #                 'name':p[0],
    #                 'url':p[1],
    #                 'img_url':p[2]
    #             })
    #             movie_json.append(x)
    #     print(movie_json)




if __name__ == '__main__':
    rec = RecommendEmotion('2')
    movies = rec.movies();
    print(movies)
    # movie_json = []
    # for m in movies:
    #     for p in m:
    #         x = jsonify({
    #             'name':p[0],
    #             'url':p[1],
    #             'img_url':p[2]
    #         })
    #         movie_json.append(x)
    # print(movie_json)
    # rec = RecommendEmotion('2')
    # print(rec.movies())
    # print(rec.movies(),rec.blogs(),rec.books(),rec.songs())