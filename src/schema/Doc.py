from pydantic import BaseModel

class Doc(BaseModel):
    csv_file_url: str
    school_id: str

    
class Result(BaseModel):
    query: str
    school_id: str