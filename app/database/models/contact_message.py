from datetime import datetime
from enum import Enum
from app.database import db

class MessageStatus(Enum):
    UNREAD = 'Unread'
    READ = 'Read'
    REPLIED = 'Replied'

class ContactMessage(db.Model):
    """Stores messages submitted via the Contact page."""
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum(MessageStatus), default=MessageStatus.UNREAD, nullable=False)

    def __repr__(self):
        return f"<ContactMessage {self.id} {self.email}>"
