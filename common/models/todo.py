from dataclasses import dataclass, field
from rococo.models import VersionedModel
from typing import ClassVar, Optional


@dataclass
class Todo(VersionedModel):
    use_type_checking: ClassVar[bool] = True
    
    person_id: str = field(default=None)
    title: str = field(default=None)
    description: Optional[str] = field(default=None)
    is_completed: bool = field(default=False)
