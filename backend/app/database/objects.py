from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    id: int
    name: str
    second_name: str
    surname: str
    username: str
    email: str
    creation_date: str # add datetime

class Account(BaseModel):
    id: int
    user_id: int
    name: str
    type: str
    balance: float
    creation_date: str
    currency: str

class Transaction(BaseModel):
    id: int
    account_id: int
    from_account_id: int
    to_account_id: int
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
    amount: float
    currency: str
    description: str | None = None
    created_at: str

class Password(BaseModel):
    user_id: int
    password: str