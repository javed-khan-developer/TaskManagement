from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from db_dependency import get_db
from auth_dependency import get_current_user

from schemas.task_schema import(TaskCreate, TaskUpdate, TaskResponse)

from services.task_service import TaskService

router = APIRouter(
    prefix="/tasks", tags=["Tasks"]
    )
service = TaskService()

@router.post("/")
def create_task(
    task: TaskCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)
    ):

    new_task = service.create_task(db, task.title, task.description, current_user.id)
    return new_task

@router.get(
        "/",
        response_model=list[TaskResponse]
)

def get_tasks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    return service.get_tasks(db, current_user.id)

@router.get("/{task_id}",response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return service.get_task(db,task_id,current_user.id)

@router.put("/{task_id}",response_model=TaskResponse)
def update_task( task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):
    return service.update_task(
        db,
        task_id,
        task.title,
        task.description,
        task.status,
        current_user.id
    )


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    service.delete_task(
        db,
        task_id,
        current_user.id
    )

    return {
        "message": "Task deleted successfully"
    }



