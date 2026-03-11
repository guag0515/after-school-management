import json
import requests
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import Student, Score, Homework, Evaluation, Attendance
from app.blueprints.ai_analysis.repository import AIAnalysisRepository
from app.blueprints.ai_analysis.schema import AIAnalysisCreate

class AIAnalysisService:
    """AI分析服务"""
    
    @staticmethod
    def get_student_data(db: Session, student_id: int, start_date: datetime, end_date: datetime):
        """获取学生数据"""
        # 获取考试成绩
        scores = db.query(Score).filter(
            Score.student_id == student_id,
            Score.exam_time >= start_date,
            Score.exam_time <= end_date,
            Score.is_deleted == 0
        ).all()
        
        # 获取作业完成情况
        homeworks = db.query(Homework).filter(
            Homework.student_id == student_id,
            Homework.date >= start_date.date(),
            Homework.date <= end_date.date(),
            Homework.is_deleted == 0
        ).all()
        
        # 获取教师评价
        evaluations = db.query(Evaluation).filter(
            Evaluation.student_id == student_id,
            Evaluation.evaluation_date >= start_date.date(),
            Evaluation.evaluation_date <= end_date.date(),
            Evaluation.is_deleted == 0
        ).all()
        
        # 获取考勤情况
        attendances = db.query(Attendance).filter(
            Attendance.student_id == student_id,
            Attendance.date >= start_date.date(),
            Attendance.date <= end_date.date(),
            Attendance.is_deleted == 0
        ).all()
        
        return {
            "scores": scores,
            "homeworks": homeworks,
            "evaluations": evaluations,
            "attendances": attendances
        }
    
    @staticmethod
    def generate_prompt(student_id: int, student_name: str, period: str, data: dict):
        """生成分析提示词"""
        # 构建成绩数据
        score_data = []
        for score in data['scores']:
            score_data.append({
                "subject": score.subject,
                "exam_type": score.exam_type,
                "score": float(score.score),
                "exam_time": score.exam_time.strftime("%Y-%m-%d")
            })
        
        # 构建作业数据
        homework_data = []
        for homework in data['homeworks']:
            homework_data.append({
                "date": homework.date.strftime("%Y-%m-%d"),
                "completion_status": homework.completion_status,
                "teacher_evaluation": homework.teacher_evaluation
            })
        
        # 构建评价数据
        evaluation_data = []
        for evaluation in data['evaluations']:
            evaluation_data.append({
                "type": evaluation.evaluation_type,
                "content": evaluation.content,
                "date": evaluation.evaluation_date.strftime("%Y-%m-%d")
            })
        
        # 构建考勤数据
        attendance_data = []
        for attendance in data['attendances']:
            attendance_data.append({
                "date": attendance.date.strftime("%Y-%m-%d"),
                "is_present": attendance.is_present
            })
        
        # 计算考勤统计
        total_attendance = len(attendance_data)
        present_days = sum(1 for a in attendance_data if a['is_present'] == 1)
        attendance_rate = (present_days / total_attendance * 100) if total_attendance > 0 else 0
        
        # 计算作业完成率
        total_homework = len(homework_data)
        completed_homework = sum(1 for h in homework_data if h['completion_status'] == "已完成")
        homework_completion_rate = (completed_homework / total_homework * 100) if total_homework > 0 else 0
        
        # 计算平均成绩
        if score_data:
            avg_score = sum(s['score'] for s in score_data) / len(score_data)
        else:
            avg_score = 0
        
        prompt = f"""你是一个专业的教育分析专家，需要根据以下数据对学生的学习情况进行全面分析。

学生信息：
- 学生ID：{student_id}
- 学生姓名：{student_name}
- 分析周期：{period}

学习数据：
1. 考试成绩：
{json.dumps(score_data, ensure_ascii=False, indent=2)}

2. 作业完成情况：
{json.dumps(homework_data, ensure_ascii=False, indent=2)}

3. 教师评价：
{json.dumps(evaluation_data, ensure_ascii=False, indent=2)}

4. 考勤情况：
{json.dumps(attendance_data, ensure_ascii=False, indent=2)}

统计数据：
- 出勤率：{attendance_rate:.2f}%
- 作业完成率：{homework_completion_rate:.2f}%
- 平均成绩：{avg_score:.2f}

请根据以上数据，生成一份详细的学习分析报告，包括但不限于：
1. 学习总体情况评估
2. 各学科表现分析
3. 学习态度和习惯分析
4. 优缺点分析
5. 改进建议
6. 未来学习预测

报告要求：
- 语言专业、客观、全面
- 结构清晰，层次分明
- 数据支撑，有理有据
- 针对性强，切实可行
"""
        
        return prompt
    
    @staticmethod
    def call_ai_api(prompt: str):
        """调用AI API"""
        # 这里使用示例API，实际使用时需要替换为真实的大模型API
        api_url = "https://api.example.com/ai/chat"
        api_key = "your-api-key"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的教育分析专家，擅长分析学生的学习情况并提供专业建议。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            # 模拟AI响应，实际使用时需要移除
            period = prompt.split('分析周期：')[1].split('\n')[0]
            return f"AI分析报告：\n\n1. 学习总体情况评估：该学生在{period}的学习情况良好。\n2. 各学科表现分析：各科成绩较为均衡。\n3. 学习态度和习惯分析：作业完成情况良好，考勤率高。\n4. 优缺点分析：优点是学习态度认真，缺点是某些学科需要加强。\n5. 改进建议：建议针对薄弱学科进行专项练习。\n6. 未来学习预测：如果保持当前状态，学习成绩会稳步提升。"
    
    @staticmethod
    def analyze_student(db: Session, student_id: int, analysis_period: str):
        """分析学生学习情况"""
        # 获取学生信息
        student = db.query(Student).filter(Student.id == student_id, Student.is_deleted == 0).first()
        if not student:
            return None, "学生不存在"
        
        # 计算分析周期的时间范围
        end_date = datetime.now()
        if analysis_period == "周":
            start_date = end_date - timedelta(days=7)
        elif analysis_period == "月":
            start_date = end_date - timedelta(days=30)
        elif analysis_period == "学期":
            start_date = end_date - timedelta(days=180)
        elif analysis_period == "学年":
            start_date = end_date - timedelta(days=365)
        else:
            return None, "分析周期无效"
        
        # 获取学生数据
        data = AIAnalysisService.get_student_data(db, student_id, start_date, end_date)
        
        # 生成提示词
        prompt = AIAnalysisService.generate_prompt(student_id, student.name, analysis_period, data)
        
        # 调用AI API
        analysis_content = AIAnalysisService.call_ai_api(prompt)
        
        # 保存分析结果
        analysis_data = AIAnalysisCreate(
            student_id=student_id,
            analysis_period=analysis_period,
            analysis_content=analysis_content
        )
        
        analysis = AIAnalysisRepository.create(db, analysis_data)
        return analysis, None
