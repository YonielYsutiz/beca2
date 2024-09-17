from .entities.User import User

class ModelUser():
    @classmethod
    def register(self, db, user):
        try:
            cursor=db.connection.cursor()
            sql= "SELECT id, username, password, number_phone, email, fullname FROM user WHERE username = '{}'".format(user.username)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3], row[4], row[5])
                return user 
            else:
                return None
        except Exception as ex : 
            raise Exception(ex)    