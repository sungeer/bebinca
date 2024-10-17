from bebinca.models.base_model import BaseModel


class UserModel(BaseModel):

    def get_user_by_phone(self, phone_number):
        sql_str = '''
            SELECT
                ID, Name, Phone, PasswordHash, IsAdmin, CreatedTime
            FROM
                users
            WHERE
                Phone = %s
        '''
        self.conn()
        self.execute(sql_str, (phone_number,))
        user_info = self.cursor.fetchone()
        self.close()
        return user_info
