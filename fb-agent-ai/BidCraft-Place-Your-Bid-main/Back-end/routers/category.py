from fastapi import APIRouter, Depends,status,HTTPException,Response
from typing import List
from respository import category
from sqlalchemy.orm import Session
import schemas,database,models

router = APIRouter(
    prefix='/category',
    tags=['category']
)


@router.post('/create',status_code=status.HTTP_201_CREATED)
def create_user(request : schemas.Category,db: Session = Depends(database.get_db)):
    new_category =  category.list_category(request,db)
    if not new_category:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f'User not created')
    else:
        return 'created'
    
    
@router.post('/get_items', response_model=schemas.ShowCategory, status_code=status.HTTP_302_FOUND)
def get_items(request: schemas.Category, db: Session = Depends(database.get_db)):
    category = db.query(models.Category).filter(models.Category.category_name == request.name).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    items = db.query(models.Item).join(models.ItemCategory).filter(models.ItemCategory.category_id == category.category_id).all()
    
    return {"name": category.category_name, "items": items}
