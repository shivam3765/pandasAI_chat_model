from fastapi import APIRouter, UploadFile, File
from schema.Doc import Result, Doc
import requests
from services.chat_with_csv import csvStoreInMongo, pandasAI , get_data

router = APIRouter()

@router.get("/")
def start():
    return "hello world"

@router.post("/datastore")
async def storedata(request: Doc):
    csv_file = request.csv_file_url

    file = requests.get(csv_file)

    # here download the pdf file
    filename = csv_file.split("/")[-1]
    with open(filename, 'wb') as f:
        f.write(file.content)

    # csv_file = 'src/routers/employees.csv'
    school_id = request.school_id
    data_id = csvStoreInMongo(filename, school_id)

    return data_id


@router.post("/result")
async def getresult(request: Result):
    response = request.query
    input_school_id = request.school_id
    
    df = get_data(input_school_id)

    result = pandasAI(df, response)
    return result