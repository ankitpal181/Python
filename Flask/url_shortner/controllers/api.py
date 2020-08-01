import random, string
from system import db
from models.urls import Url
from controllers.logger import LoggerController as logger

class APIController():
    def __init__(self):
        self.long_url = ""
        self.short_url = ""
    
    def createUrl(self):
        url = Url.query.filter_by(long_url=self.long_url).first()
        if url:
            return "Url already exists"
        short_url = "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=8))
        short_url = self.long_url[:self.long_url.find("/")] + "/" + short_url
        url = Url(long_url=self.long_url, short_url=short_url)
        db.session.add(url)
        db.session.commit()
        return short_url

    def readUrl(self, return_type="long"):
        if return_type == "short":
            url = Url.query.filter_by(long_url=self.long_url).first()
            if url:
                return url.short_url
        else:
            url = Url.query.filter_by(short_url=self.short_url).first()
            if url:
                return url.long_url
        return None

    def updateUrl(self):
        url = Url.query.filter_by(long_url=self.long_url).first()
        if url:
            short_url = "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=8))
            short_url = self.long_url[:self.long_url.find("/")] + "/" + short_url
            url.short_url = short_url
            db.session.commit()
            return short_url
        return "Url does not exists"

    def deleteUrl(self):
        url = Url.query.filter_by(long_url=self.long_url).first()
        if url:
            db.session.delete(url)
            db.session.commit()
        return "Url does not exists"