from sqlalchemy.orm import Session
from app.models import Student, Parent
from app.blueprints.student.schema import StudentCreate, StudentUpdate, ParentCreate
from app.utils import hash_password

class StudentRepository:
    @staticmethod
    def create(db: Session, student_data: StudentCreate) -> Student:
        """创建学生"""
        db_student = Student(
            name=student_data.name,
            gender=student_data.gender,
            class_=student_data.class_,
            service_type=student_data.service_type,
            parent1_phone=student_data.parent1_phone,
            parent2_phone=student_data.parent2_phone
        )
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    
    @staticmethod
    def get_by_id(db: Session, student_id: int) -> Student:
        """根据ID获取学生"""
        return db.query(Student).filter(Student.id == student_id, Student.is_deleted == 0).first()
    
    @staticmethod
    def get_list(db: Session, skip: int = 0, limit: int = 10, **filters) -> tuple:
        """获取学生列表"""
        query = db.query(Student).filter(Student.is_deleted == 0)
        
        # 应用过滤条件
        if filters.get('name'):
            query = query.filter(Student.name.like(f"%{filters['name']}%"))
        if filters.get('class_'):
            query = query.filter(Student.class_ == filters['class_'])
        if filters.get('service_type'):
            query = query.filter(Student.service_type == filters['service_type'])
        
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return total, items
    
    @staticmethod
    def update(db: Session, student_id: int, student_data: StudentUpdate) -> Student:
        """更新学生"""
        db_student = StudentRepository.get_by_id(db, student_id)
        if db_student:
            update_data = student_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_student, field, value)
            db.commit()
            db.refresh(db_student)
        return db_student
    
    @staticmethod
    def delete(db: Session, student_id: int) -> bool:
        """删除学生（软删除）"""
        db_student = StudentRepository.get_by_id(db, student_id)
        if db_student:
            db_student.is_deleted = 1
            db.commit()
            return True
        return False

class ParentRepository:
    @staticmethod
    def create(db: Session, parent_data: ParentCreate) -> Parent:
        """创建家长"""
        db_parent = Parent(
            student_id=parent_data.student_id,
            phone=parent_data.phone,
            password=hash_password(parent_data.password),
            relation=parent_data.relation
        )
        db.add(db_parent)
        db.commit()
        db.refresh(db_parent)
        return db_parent
    
    @staticmethod
    def get_by_id(db: Session, parent_id: int) -> Parent:
        """根据ID获取家长"""
        return db.query(Parent).filter(Parent.id == parent_id, Parent.is_deleted == 0).first()
    
    @staticmethod
    def get_by_phone(db: Session, phone: str) -> Parent:
        """根据手机号获取家长"""
        return db.query(Parent).filter(Parent.phone == phone, Parent.is_deleted == 0).first()
