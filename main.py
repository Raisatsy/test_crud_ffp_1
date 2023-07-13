from fastapi import FastAPI, Depends, HTTPException

from user_schemas import User, UserUpdate
from db import connect_to_db

app = FastAPI()


@app.post('/users')
def create_user(user: User, db=Depends(connect_to_db)):
    user_data = dict(user)
    collection = db['users']
    existing_user = collection.fetchFirstExample({"user_id": user.user_id})

    if existing_user:
        raise HTTPException(status_code=400, detail="User with the same user_id already exists")
    collection.createDocument(user_data).save()
    return {"message": "User created succesfully"}


@app.get('/users/{user_id}')
def get_user(user_id: int, db=Depends(connect_to_db)):
    collection = db['users']
    result = collection.fetchFirstExample({'user_id': user_id})

    if result:
        user = result[0]
        return {"name": user['name'], "surname": user['surname'], 'email': user['email']}

    else:
        return {'message': 'User not found'}


@app.put('/users_update/{user_id}')
def update_user(user_id: int, user_data: UserUpdate, db=Depends(connect_to_db)):
    collection = db['users']
    current_user = collection.fetchFirstExample({"user_id": user_id})

    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')

    updated_data = dict(user_data)
    updated_data = {key: value for key, value in updated_data.items() if value is not None}

    if updated_data:
        for key, value in updated_data.items():
            current_user[0][key] = value
        current_user[0].save()

    updated_user = collection.fetchFirstExample({"user_id": user_id})

    user = updated_user[0]
    return {"name": user['name'], "surname": user['surname'], 'email': user['email']}


@app.delete('/users_delete/{user_id}')
def delete_user(user_id: int, db=Depends(connect_to_db)):
    collection = db['users']
    current_user = collection.fetchFirstExample({"user_id": user_id})

    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')

    current_user[0].delete()

    return {'message': 'User was deleted'}
