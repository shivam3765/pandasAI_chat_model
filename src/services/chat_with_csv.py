import pymongo
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import uuid
from utils.config import ConfigManager

# Load API key from config file
config_manager = ConfigManager()
connection_str = config_manager.get_connection_str()

client = pymongo.MongoClient(f"{connection_str}")
db = client["mongo_class_ganana"]
coll = db["studentData"]

    


# This function is use for storing data in mongodb
def csvStoreInMongo(csv_file, school_id):

    readfile = pd.read_csv(csv_file)
    # readfile.reset_index(inplace=True)
   

    # Here the generate unique id
    unique_id = str(uuid.uuid4())
    for _, row in readfile.iterrows():
        

        # Convert the row to a dictionary and add the unique ID as a key
        data = {'data_id': unique_id, "file_url": csv_file, "school_id": school_id, **row.to_dict()}
        # Insert the data into the collection
        coll.insert_one(data)

    return school_id


# This function is use for get data from mongodb
def get_data(input_school_id):

    # get data from mongodb
    if coll.find({"school_id": input_school_id}, {'_id': 0}):
        receive_data = coll.find({"school_id": input_school_id}, {'_id': 0})
    
    else:
        return "Enter valid input data key...."

    df = pd.DataFrame(receive_data)

    return df


# This function is use for chat with pandasAI
def pandasAI(df, response):

    api_key = config_manager.get_api_key()
    
    llm = OpenAI(api_token=api_key)

    pandas_ai = PandasAI(llm)
    result = pandas_ai(df, response)

    return result.to_dict()