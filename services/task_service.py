from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import status
from repositories.task_repository import TaskRepository

class TaskService:
    
    def __init__(self):
        self.repo=TaskRepository()

    def create_task(
            self, db: Session, title: str, description: str, user_id: int
            ):
        return self.repo.create_task(db, title, description, user_id)
    
    def get_tasks(self, db: Session, user_id: int):
        return self.repo.get_tasks(db, user_id)

    def get_task(
    self,
    db: Session,
    task_id: int,
    user_id: int
    ):
        task =self.repo.get_task_by_id(db, task_id)

        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task Not Found")
        
        if task.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
        return task
    
    def update_task(
    self,
    db: Session,
    task_id: int,
    title: str,
    description: str,
    status: str,
    user_id: int
   ):
        task = self.get_task(db,task_id,user_id)
        return  self.repo.update_task(db,task,title,description,status)
    

    
    def delete_task(self, db: Session, task_id: int, user_id: int):
        task = self.get_task(db,task_id,user_id)
        self.repo.delete_task(db,task)



