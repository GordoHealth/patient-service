from typing import Generic, Sequence, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginationParams(BaseModel):
    page_number: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")

    @property
    def offset(self) -> int:
        return (self.page_number - 1) * self.page_size

class PaginatedResponse(BaseModel, Generic[T]):
    items: Sequence[T]
    total_count: int
    page_number: int
    page_size: int
    total_pages: int