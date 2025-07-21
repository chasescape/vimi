import uuid
from datetime import datetime
from typing import Dict, Any
from ...models.interview import Interview, Question, Answer, Evaluation

class InterviewService:
    def __init__(self):
        self.interviews = {}  # 临时存储，之后会替换为数据库

    def generate_interview_id(self) -> str:
        """生成唯一的面试ID"""
        return f"AI-{datetime.now().strftime('%Y%m')}-{str(uuid.uuid4())[:8]}"

    def start_interview(self, user_id: str, position: str) -> str:
        """
        开始一个新的面试会话
        
        Args:
            user_id: 用户ID
            position: 面试职位
            
        Returns:
            str: 面试ID
        """
        interview_id = self.generate_interview_id()
        
        self.interviews[interview_id] = {
            'user_id': user_id,
            'position': position,
            'start_time': datetime.now(),
            'status': 'in_progress',
            'questions': [],
            'answers': [],
            'evaluations': [],
            'final_score': None
        }
        
        return interview_id

    def end_interview(self, interview_id: str) -> None:
        """
        结束面试会话
        
        Args:
            interview_id: 面试ID
        """
        if interview_id not in self.interviews:
            raise Exception('面试ID不存在')
            
        interview = self.interviews[interview_id]
        interview['status'] = 'completed'
        interview['end_time'] = datetime.now()
        
        # 计算最终评分
        if interview['evaluations']:
            scores = [eval['score'] for eval in interview['evaluations']]
            interview['final_score'] = sum(scores) / len(scores)

    def get_interview_result(self, interview_id: str) -> Dict[str, Any]:
        """
        获取面试结果
        
        Args:
            interview_id: 面试ID
            
        Returns:
            Dict: 面试结果详情
        """
        if interview_id not in self.interviews:
            raise Exception('面试ID不存在')
            
        interview = self.interviews[interview_id]
        
        if interview['status'] != 'completed':
            raise Exception('面试尚未结束')
            
        return {
            'interview_id': interview_id,
            'user_id': interview['user_id'],
            'position': interview['position'],
            'start_time': interview['start_time'].isoformat(),
            'end_time': interview['end_time'].isoformat(),
            'duration': (interview['end_time'] - interview['start_time']).total_seconds(),
            'questions_count': len(interview['questions']),
            'final_score': interview['final_score'],
            'evaluations': interview['evaluations']
        }

    def add_question(self, interview_id: str, question: str) -> None:
        """
        添加面试问题
        
        Args:
            interview_id: 面试ID
            question: 问题内容
        """
        if interview_id not in self.interviews:
            raise Exception('面试ID不存在')
            
        interview = self.interviews[interview_id]
        if interview['status'] != 'in_progress':
            raise Exception('面试已结束')
            
        interview['questions'].append({
            'question': question,
            'time': datetime.now()
        })

    def add_answer(self, interview_id: str, answer: str) -> None:
        """
        添加答案
        
        Args:
            interview_id: 面试ID
            answer: 答案内容
        """
        if interview_id not in self.interviews:
            raise Exception('面试ID不存在')
            
        interview = self.interviews[interview_id]
        if interview['status'] != 'in_progress':
            raise Exception('面试已结束')
            
        interview['answers'].append({
            'answer': answer,
            'time': datetime.now()
        })

    def add_evaluation(self, interview_id: str, aspect: str, score: float, comment: str) -> None:
        """
        添加评估
        
        Args:
            interview_id: 面试ID
            aspect: 评估方面（如：专业能力、沟通能力等）
            score: 评分（0-100）
            comment: 评语
        """
        if interview_id not in self.interviews:
            raise Exception('面试ID不存在')
            
        interview = self.interviews[interview_id]
        if interview['status'] != 'in_progress':
            raise Exception('面试已结束')
            
        interview['evaluations'].append({
            'aspect': aspect,
            'score': score,
            'comment': comment,
            'time': datetime.now()
        })

# 创建服务实例
interview_service = InterviewService() 