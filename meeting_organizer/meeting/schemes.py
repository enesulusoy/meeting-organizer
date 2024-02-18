from meeting_organizer import ma


class MeetingSchema(ma.Schema):
    class Meta:
        fields = ('id', 'meeting_subject', 'start_time', 'end_time', 'date', 'participants')