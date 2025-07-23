import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from ...models.interview import Interview, Question, Answer, InterviewEvaluation

class InterviewService:
    def __init__(self):
        self.interviews = {}  # 临时存储，之后会替换为数据库

    def generate_interview_id(self) -> str:
        """生成唯一的面试ID"""
        return f"AI-{datetime.now().strftime('%Y%m')}-{str(uuid.uuid4())[:8]}"

    def get_upcoming_interview(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        获取用户即将开始的面试
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict: 面试信息，如果没有则返回None
        """
        # 查找最近的待开始面试
        upcoming = None
        for interview_id, interview in self.interviews.items():
            if (interview['user_id'] == user_id and 
                interview['status'] == 'scheduled' and
                (not upcoming or interview['start_time'] < upcoming['start_time'])):
                upcoming = interview.copy()
                upcoming['id'] = interview_id
                
        if upcoming:
            return {
                'id': upcoming['id'],
                'company': upcoming['company'],
                'position': upcoming['position'],
                'time': upcoming['start_time'].isoformat(),
                'status': upcoming['status']
            }
        return None

    def get_interview_statistics(self, user_id: str) -> Dict[str, int]:
        """
        获取用户的面试统计信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict: 统计信息
        """
        stats = {
            'total': 0,
            'completed': 0,
            'upcoming': 0,
            'failed': 0
        }
        
        for interview in self.interviews.values():
            if interview['user_id'] == user_id:
                stats['total'] += 1
                if interview['status'] == 'completed':
                    stats['completed'] += 1
                    if interview.get('final_score', 0) < 60:
                        stats['failed'] += 1
                elif interview['status'] == 'scheduled':
                    stats['upcoming'] += 1
                    
        return stats

    def get_interview_history(
        self, 
        user_id: str, 
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """
        获取面试历史记录
        
        Args:
            user_id: 用户ID
            status: 面试状态筛选
            start_date: 开始日期
            end_date: 结束日期
            page: 页码
            page_size: 每页数量
            
        Returns:
            Dict: 分页的面试历史记录
        """
        # 筛选符合条件的面试记录
        filtered_interviews = []
        for interview_id, interview in self.interviews.items():
            if interview['user_id'] != user_id:
                continue
                
            if status and interview['status'] != status:
                continue
                
            if start_date and interview['start_time'] < start_date:
                continue
                
            if end_date and interview['start_time'] > end_date:
                continue
                
            interview_data = {
                'id': interview_id,
                'start_time': interview['start_time'].isoformat(),
                'end_time': interview.get('end_time', '').isoformat() if interview.get('end_time') else None,
                'position': interview['position'],
                'company': interview['company'],
                'type': interview.get('type', 'online'),
                'status': interview['status']
            }
            
            # 添加评估信息
            if interview.get('evaluations'):
                latest_eval = interview['evaluations'][-1]
                interview_data['evaluation'] = {
                    'overall_rating': latest_eval.get('score', 0),
                    'technical_rating': latest_eval.get('technical_score', 0),
                    'communication_rating': latest_eval.get('communication_score', 0),
                    'strengths': latest_eval.get('strengths', []),
                    'weaknesses': latest_eval.get('weaknesses', []),
                    'feedback': latest_eval.get('comment', '')
                }
            
            # 添加录像信息
            if interview.get('recording_url'):
                interview_data['recording'] = interview['recording_url']
                
            filtered_interviews.append(interview_data)
            
        # 排序：按开始时间倒序
        filtered_interviews.sort(key=lambda x: x['start_time'], reverse=True)
        
        # 分页
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        return {
            'total': len(filtered_interviews),
            'items': filtered_interviews[start_idx:end_idx]
        }

    def start_interview(self, user_id: str, position: str, company: str) -> str:
        """
        开始一个新的面试会话
        
        Args:
            user_id: 用户ID
            position: 面试职位
            company: 面试公司
            
        Returns:
            str: 面试ID
        """
        interview_id = self.generate_interview_id()
        
        self.interviews[interview_id] = {
            'user_id': user_id,
            'position': position,
            'company': company,
            'start_time': datetime.now(),
            'status': 'in_progress',
            'questions': [],
            'answers': [],
            'evaluations': [],
            'final_score': None,
            'type': 'online'
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

    def add_question(self, interview_id: str, question: str, tips: str = None, difficulty: str = 'medium') -> None:
        """
        添加面试问题
        
        Args:
            interview_id: 面试ID
            question: 问题内容
            tips: 问题提示
            difficulty: 难度级别
        """
        if interview_id not in self.interviews:
            raise Exception('面试ID不存在')
            
        interview = self.interviews[interview_id]
        if interview['status'] != 'in_progress':
            raise Exception('面试已结束')
            
        interview['questions'].append({
            'id': str(uuid.uuid4()),
            'question': question,
            'tips': tips,
            'difficulty': difficulty,
            'time': datetime.now()
        })

    def add_answer(self, interview_id: str, question_id: str, answer: str) -> Dict[str, Any]:
        """
        添加答案并返回评估结果
        
        Args:
            interview_id: 面试ID
            question_id: 问题ID
            answer: 答案内容
            
        Returns:
            Dict: 答案评估结果
        """
        if interview_id not in self.interviews:
            raise Exception('面试ID不存在')
            
        interview = self.interviews[interview_id]
        if interview['status'] != 'in_progress':
            raise Exception('面试已结束')
            
        # 添加答案
        interview['answers'].append({
            'question_id': question_id,
            'answer': answer,
            'time': datetime.now()
        })

        # 生成评估结果（这里是模拟的评估逻辑，实际应该调用AI模型）
        evaluation = {
            'overall_score': 85,
            'completeness': 90,
            'expression': 80,
            'comments': '回答结构清晰，论述有理有据。',
            'suggestions': [
                '可以多举一些具体的例子',
                '建议控制答题时间在2-3分钟内'
            ]
        }
        
        return evaluation

    def add_evaluation(
        self, 
        interview_id: str, 
        aspect: str, 
        score: float, 
        technical_score: float,
        communication_score: float,
        strengths: List[str],
        weaknesses: List[str],
        comment: str
    ) -> None:
        """
        添加评估
        
        Args:
            interview_id: 面试ID
            aspect: 评估方面
            score: 总体评分
            technical_score: 技术能力评分
            communication_score: 沟通能力评分
            strengths: 优势列表
            weaknesses: 待改进项列表
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
            'technical_score': technical_score,
            'communication_score': communication_score,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'comment': comment,
            'time': datetime.now()
        })

# 创建服务实例
interview_service = InterviewService() 