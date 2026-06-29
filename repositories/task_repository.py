from sqlalchemy.orm import Session

from models.task import Task


class TaskRepository:

    def create_task(self, db: Session, title: str, description: str, user_id: int):
        task = Task(
            title=title,
            description=description,
            user_id=user_id,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def get_tasks(self, db: Session, user_id: int):
        return db.query(Task).filter(Task.user_id == user_id).all()

    def get_task_by_id(self, db: Session, task_id: int):
        return db.query(Task).filter(Task.id == task_id).first()

    def update_task(self, db: Session, task, title, description, status):
        task.title = title
        task.description = description
        task.status = status

        db.commit()
        db.refresh(task)
        return task

    def delete_task(self, db: Session, task):
        db.delete(task)
        db.commit()


