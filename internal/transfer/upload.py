from fastapi import UploadFile
import shutil
from tempfile import NamedTemporaryFile
from pathlib import Path
from typing import Callable



def save_file_internally(source: Path, destination: Path) -> None:
    shutil.copyfile(source, destination)


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
            print(tmp_path)
    finally:
        upload_file.file.close()
    return tmp_path


def handle_upload_file(upload_file: UploadFile, handler: Callable[[Path], None]) -> None:
    tmp_path = save_upload_file_tmp(upload_file)
    destination = Path(f'D:/PhD/ExperimentProtocol2/AnnotationTool/{upload_file.filename}')
    try:
        handler(tmp_path, destination)  # Do something with the saved temp file
    finally:
        tmp_path.unlink()  # Delete the temp file