from pathlib import Path
from typing import List
from langchain_core.document_loaders import BaseLoader
import icalendar
from langchain.schema import Document

class ICSLoader(BaseLoader):
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load(self) -> List[Document]:
        with self.file_path.open("rb") as f:
            calendar = icalendar.Calendar.from_ical(f.read())

        documents = []
        for i, component in enumerate(calendar.walk()):
            if component.name == "VEVENT":
                summary = str(component.get("summary", ""))
                description = str(component.get("description", ""))
                start = str(component.get("dtstart").dt)
                end = str(component.get("dtend").dt)
                location = str(component.get("location", ""))
                organizer = str(component.get("organizer", ""))
                status = str(component.get("status", ""))

                text = (
                    f"Event: {summary}\n"
                    f"Start: {start}\n"
                    f"End: {end}\n"
                    f"Location: {location}\n"
                    f"Organizer: {organizer}\n"
                    f"Status: {status}\n"
                    f"Description: {description}"
                )

                metadata = {
                    "summary": summary,
                    "start": start,
                    "end": end,
                    "location": location,
                    "organizer": organizer,
                    "status": status,
                    "source": self.file_path.name,
                }

                documents.append(Document(page_content=text, metadata=metadata))

        return documents
