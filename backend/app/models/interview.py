from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from . import Base

class Interview(Base):
    __tablename__ = 'interviews'

    id = Column(String(50), primary_key=True)
    user_id = Column(String(50), ForeignKey('users.id'), nullable=False)
    position = Column(String(100), nullable=False)
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime)
    status = Column(String(20), nullable=False, default='in_progress')
    final_score = Column(Float)

    # 关联
    questions = relationship('Question', back_populates='interview')
    answers = relationship('Answer', back_populates='interview')
    evaluations = relationship('Evaluation', back_populates='interview')
    user = relationship('User', back_populates='interviews')

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    interview_id = Column(String(50), ForeignKey('interviews.id'), nullable=False)
    content = Column(Text, nullable=False)
    time = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # 关联
    interview = relationship('Interview', back_populates='questions')
    answer = relationship('Answer', back_populates='question', uselist=False)

class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    interview_id = Column(String(50), ForeignKey('interviews.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    content = Column(Text, nullable=False)
    time = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # 关联
    interview = relationship('Interview', back_populates='answers')
    question = relationship('Question', back_populates='answer')

class Evaluation(Base):
    __tablename__ = 'evaluations'

    id = Column(Integer, primary_key=True)
    interview_id = Column(String(50), ForeignKey('interviews.id'), nullable=False)
    aspect = Column(String(50), nullable=False)
    score = Column(Float, nullable=False)
    comment = Column(Text)
    time = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # 关联
    interview = relationship('Interview', back_populates='evaluations') 