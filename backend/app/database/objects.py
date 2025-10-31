from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    name: str
    second_name: str
    surname: str
    username: str
    email: str
    creation_date: str # add date class

class Account(BaseModel):
    id: int
    user_id: int
    name: str
    type: int
    balance: float
    creation_date: str
    currenct: str

class Transaction(BaseModel):
    id: int
    account_id: int
    from_user_id: int
    to_user_id: int
    amount: int
    currency: str
    category: str
    description: str
    transaction_at: str
    created_at: str

class Group(BaseModel):
    id: int
    name: str
    owner_user_id: int
    created_at: str

class User_Group(BaseModel):
    user_id: int
    group_id: int
    role: str
    joined_at: str

class GroupTransaction(BaseModel):
    id: int
    group_id: int
    paid_by_user_id: int
    ammount: int
    currency: str
    description: str | None = None
    created_at: str