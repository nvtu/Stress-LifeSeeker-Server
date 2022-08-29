from datetime import datetime
from fastapi import UploadFile
import sentry_sdk
import shutil
from typing import Dict, List
import os
from tempfile import NamedTemporaryFile
from pathlib import Path
import zipfile
from collections import defaultdict
from itertools import groupby
from constants.external_servers import DATA_STORAGE_URL
from schemas.db_schemas import MomentDetailId, MomentMetadata
from internal.db.user_annotation_crud import (
    insert_dates_to_user
)
from internal.db.moment_annotation_crud import (
    append_moments,
)
from internal.db.moment_detail_annotation_crud import (
    insert_moment_detail
)



def unzip_file(source: Path, destination: Path) -> None:
    with zipfile.ZipFile(source, 'r') as zip_ref:
        zip_ref.extractall(destination)



def get_file_structure_from_zipfile(source: Path) -> list:
    try:
        file_structure = defaultdict(list)
        with zipfile.ZipFile(source, 'r') as zip_ref:
            IMAGE_EXTENSION = ['.jpg', '.jpeg', '.png']
            names = zip_ref.namelist()

            # Filter only the images from lifelog folder
            names = sorted([name for name in zip_ref.namelist() 
                    if 'lifelog' in name and 
                        'thumb' not in name and
                        os.path.splitext(name)[-1].lower() in IMAGE_EXTENSION])
            
            # Group by date
            DATE_INDEX_IN_NAME = 0
            for k, v in groupby(names, key=lambda name: name.split('/')[DATE_INDEX_IN_NAME]):
                file_structure[k] += list(v)
    except Exception as e:
        sentry_sdk.capture_exception(e)
    return file_structure



async def insert_data_to_db(user_id: str, file_structure: Dict[str, List[str]]) -> None:
        # Insert dates to db
        dates = sorted(file_structure.keys())
        _ = await insert_dates_to_user(user_id, dates) # Append dates to user's list of dates -> Can't be False

        TIME_INDEX_IN_NAME = -1
        DATE_TIME_INDEX_IN_NAME = -2
        for _date, moment_list in file_structure.items():
            sorted_moment_list = sorted(moment_list, key=lambda m: m.split('_')[TIME_INDEX_IN_NAME])
            _id = {
                'user_id': user_id,
                'moment_date': _date
            }
            # Insert moments list by date to db
            _ = await append_moments(_id, sorted_moment_list)

            for _moment in sorted_moment_list:
                moment_name = '_'.join(_moment.split('_')[DATE_TIME_INDEX_IN_NAME:])
                date_time = moment_name[:15] # Dummt handling of date time

                date_time = datetime.strptime(date_time, '%Y%m%d_%H%M%S')
                local_time = datetime.strftime(date_time, '%H:%M:%S')
                utc_time = local_time # Dummy value for UTC time --> Work on it later
                _id = {
                    'user_id': user_id,
                    'moment_date': _date,
                    'local_time': local_time
                }

                moment_detail = {
                    'utc_time': utc_time,
                    'image_path': _moment,
                    'other_image_path': _moment, # Dummy value for other image path --> Work on it later
                    'location': '',
                    'stress_level': '',
                    'activity': '',
                    'heart_rate': {
                        'min_value': 0,
                        'max_value': 0,
                        'mean_value': 0,
                        'std_value': 0
                    },
                    'bvp': {
                        'min_value': 0,
                        'max_value': 0,
                        'mean_value': 0,
                        'std_value': 0
                    },
                    'eda': {
                        'min_value': 0,
                        'max_value': 0,
                        'mean_value': 0,
                        'std_value': 0
                    },
                    'temp': {
                        'min_value': 0,
                        'max_value': 0,
                        'mean_value': 0,
                        'std_value': 0
                    },
                }                

                # Insert moment details to db 
                moment_id = MomentDetailId(**_id)
                moment_detail = MomentMetadata(**moment_detail)

                _ = await insert_moment_detail(moment_id, moment_detail)



def save_file_internally(source: Path, destination: Path) -> None:
    shutil.copyfile(source, destination)


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    except Exception as e:
        sentry_sdk.capture_exception(e)
    finally:
        upload_file.file.close()
    return tmp_path


async def handle_upload_file(upload_file: UploadFile, user_id: str) -> None:
    tmp_path = save_upload_file_tmp(upload_file)

    # Create folder for user if it does not exist
    user_data_path = os.path.join(DATA_STORAGE_URL, user_id)
    if not os.path.exists(user_data_path):
        os.makedirs(user_data_path)

    destination = Path(f'{user_data_path}')
    try:
        unzip_file(tmp_path, destination)  # Do something with the saved temp file
        file_structure = get_file_structure_from_zipfile(tmp_path)
        await insert_data_to_db(user_id, file_structure)
    except Exception as e:
        sentry_sdk.capture_exception(e) 
    finally:
        tmp_path.unlink()  # Delete the temp file