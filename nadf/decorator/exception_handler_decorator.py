from typing import Callable
from nadf.exception.business_exception import BusinessException
from fastapi import HTTPException

def exception_handler(func: Callable) -> Callable:
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BusinessException as e:
            print("error : ", e.message)
            print("status code:", e.status_code)
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as e:
            print("error : ", str(e))
            raise HTTPException(status_code=500, detail=str(e))
    return inner
