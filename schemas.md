# ***Schemas for Split Smart***

### **This is the schemas design I've come up with :**




-  ***User Table***
    ```python
    id : int # primary key
    name : str 
    email : EmailStr
    hash_pwd : str
    
    ```

- ***Group Table***
    ```python
    id : int # primary key
    name : str
    invite_code : str

    ```
- ***User_Group junction-table***
    ```python
    user_id : int # foreign_key users.id
    group_id : int # foreign_key groups.id
    role : str # Literal["admin" , "member"]

    # primary key -> (user_id , group_id)
    ```

- ***Expense Table***
    ```python
    id : int
    user_id : int # foreign_key users.id
    group_id : int # foreign_key groups.id
    total_amt : float
    split_type : Literal["disproportionate" , "equal"]
    # primary key -> (user_id , group_id)
    ```

- ***Expense_split Table***
    ```python 
    user_id : int # foreign_key users.id
    expense_id : int # foreign_key expenses.id
    decided_amt : float
    # primary key -> (user_id , expense_id)
    ```

- ***Payments Table***
    ```python
    id : int # primary key
    payer_id : int # foreign_key users.id
    payee_id : int # foreign_key users.id
    paid_amt : float

    ```


