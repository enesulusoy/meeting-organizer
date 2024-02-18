import os
from datetime import datetime
from flask import request, jsonify, Blueprint, render_template
from flask.views import MethodView
from meeting_organizer import db, app, ValidationError
from meeting_organizer.meeting.models import Meeting
from meeting_organizer.meeting.schemes import MeetingSchema

template_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'templates')
meeting = Blueprint('meeting', __name__)

meeting_schema = MeetingSchema()
meetings_schema = MeetingSchema(many=True)

@meeting.route('/')
@meeting.route('/home')
def home():
    return render_template('home.html')


class MeetingView(MethodView):
    def get(self, id=None):
        if id is None:
            page = request.args.get('page', 1, type=int)
            per_page = 10
            meetings = Meeting.query.paginate(page=page, per_page=per_page, error_out=False)
            if not meetings.items:
                return jsonify({"error": "No meetings found"}), 404
            return jsonify({
                "meetings": meetings_schema.dump(meetings.items),
                "total_pages": meetings.pages,
                "current_page": meetings.page,
                "total_meetings": meetings.total
            }), 200
            
        else:
            meeting = Meeting.query.get(id)
            if not meeting:
                return jsonify({"error": "Meeting not found"}), 404
            
            return jsonify(meeting_schema.dump(meeting)), 200
    
    def post(self):
        data = request.json
        data["date"] = datetime.strptime(data['date'], '%Y-%m-%d').date()
        data["start_time"] = datetime.strptime(data['start_time'] + ':00', '%H:%M:%S').time()
        data["end_time"] = datetime.strptime(data['end_time'] + ':00', '%H:%M:%S').time()
        try:
            meeting_dto = meeting_schema.load(data)
            meeting = Meeting(**meeting_dto)
            db.session.add(meeting)
            db.session.commit()
            return jsonify(meeting_schema.dump(meeting)), 201
        
        except ValidationError as err:
            db.session.rollback()
            return jsonify({"error": str(err)}), 400
        
    def put(self, id):
        meeting = Meeting.query.get(id)
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 404
        
        data = request.json
        data["date"] = datetime.strptime(data['date'], '%Y-%m-%d').date()
        data["start_time"] = datetime.strptime(data['start_time'] + ':00', '%H:%M:%S').time()
        data["end_time"] = datetime.strptime(data['end_time'] + ':00', '%H:%M:%S').time()
        try:
            meeting_dto = meeting_schema.load(data)
            meeting.meeting_subject = meeting_dto.get('meeting_subject', meeting.meeting_subject)
            meeting.start_time = meeting_dto.get('start_time', meeting.start_time)
            meeting.end_time = meeting_dto.get('end_time', meeting.end_time)
            meeting.date = meeting_dto.get('date', meeting.date)
            meeting.participants = meeting_dto.get('participants', meeting.participants)
            db.session.commit()
            return jsonify(meeting_schema.dump(meeting)), 200
        
        except ValidationError as err:
            db.session.rollback()
            return jsonify({"error": err.messages}), 400
    
    def delete(self, id):
        meeting = Meeting.query.get(id)
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 404
        
        db.session.delete(meeting)
        db.session.commit()
        return jsonify({"message": "Meeting deleted"}), 200
    
    
meeting_view =  MeetingView.as_view('meeting_view')
app.add_url_rule(
    '/meetings/', view_func=meeting_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/meetings/<int:id>', view_func=meeting_view, methods=['GET', 'PUT', 'DELETE']
)