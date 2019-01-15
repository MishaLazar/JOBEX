from datetime import datetime


class Match:
    def __init__(self,student_id,position_id,match_level_id, is_deleted=False):
        self.match_level_id = match_level_id
        self.position_id = position_id
        self.student_id = student_id
        self.match_update_date = datetime.now()
        self.is_deleted = is_deleted

