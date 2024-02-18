from meeting_organizer import db

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_subject = db.Column(db.String(255))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    date = db.Column(db.Date)
    participants = db.Column(db.String(500))

    def __init__(self, meeting_subject, date, start_time, end_time, participants):
        self.meeting_subject = meeting_subject
        self.start_time = start_time
        self.end_time = end_time
        self.date = date
        self.participants = participants

    def __repr__(self):
        return '<Product %d>' % self.id
