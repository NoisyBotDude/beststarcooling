from api.models.user import user_model
from uuid import uuid4
from api.schemas.user.request_schemas import user_request_schema
from api.models.user import user_model
from passlib.hash import pbkdf2_sha256
from pymongo.errors import DuplicateKeyError
from api.utils.exceptions import exceptions


class User:
    """
        Student database driver.
        Responsible for various student related
        tasks.
    """

    async def add_user(self, 
        user_details: user_request_schema.UserRegisterSchema):

        """Adds new student to the database"""

        try:
            student = user_model.UserModel(**user_details.__dict__)

            student.password = pbkdf2_sha256.hash(student.password)

            db_response = await user_model.UserModel.save(student)
            
            return True

        except DuplicateKeyError as e:
            #TODO: log to logger
            print(f"{e} dupkey err : student driver")
            raise exceptions.DuplicateStudent()

        except Exception as e:
            #TODO: log to logger
            print(f"{e} excep err : student driver")
            raise exceptions.UnexpectedError()


    async def set_refresh_token(self, user_id: str):
            user = await user_model.UserModel.find_one(
                user_model.UserModel.user_id == user_id
            )

            if user is None:
                return False

            token = str(uuid4())

            user.refresh_token = token

            # Commiting changes in db
            db_response = await user_model.UserModel.save(user)

            if db_response:
                
                return token

            return False