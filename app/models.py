from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Literal

from pydantic import AnyHttpUrl, BaseModel, EmailStr, Field


# Metadata schemas (aligned with schema-profile.json)


class OtherLink(BaseModel):
    platform: str = Field(..., description="Nombre de la plataforma", min_length=1)
    url: AnyHttpUrl = Field(..., description="URL del perfil")
    label: Optional[str] = Field(
        None, description="Etiqueta personalizada para mostrar"
    )


class Contact(BaseModel):
    github: Optional[str] = Field(None, description="Username de GitHub")
    linkedin: Optional[str] = Field(
        None, description="URL o username de LinkedIn"
    )
    email: Optional[EmailStr] = Field(None, description="Correo electrónico")
    twitter: Optional[str] = Field(None, description="Handle de Twitter/X")
    website: Optional[AnyHttpUrl] = Field(None, description="Sitio web personal")
    other: Optional[List[OtherLink]] = Field(
        None, description="Otros enlaces de perfil adicionales"
    )


class Profile(BaseModel):
    name: str = Field(..., description="Nombre completo del usuario", min_length=1)
    avatar: Optional[AnyHttpUrl] = Field(
        None, description="URL de la imagen de avatar"
    )
    contact: Optional[Contact] = Field(None, description="Datos de contacto")


class FileList(BaseModel):
    url: AnyHttpUrl = Field(
        ..., description="URL del recurso con la lista de archivos"
    )
    format: Literal["json", "xml", "csv"] = Field(
        "json", description="Formato del archivo de lista"
    )
    lastUpdated: Optional[datetime] = Field(
        None, description="Fecha y hora de última actualización"
    )


class ProfileMetadata(BaseModel):
    version: str = Field(
        ..., description="Versión del esquema de metadata", pattern=r"^\d+\.\d+\.\d+$"
    )
    profile: Profile
    fileList: FileList


# Notes schemas


class NoteFrontMatter(BaseModel):
    title: str = Field(..., min_length=1)
    date: datetime
    tags: List[str] = Field(default_factory=list)
    summary: Optional[str] = None
    draft: bool = False


class NoteListItem(BaseModel):
    slug: str = Field(..., description="Identificador de la nota (slug)")
    title: str = Field(..., min_length=1)
    date: datetime
    tags: List[str] = Field(default_factory=list)
    summary: Optional[str] = None


class NotesListResponse(BaseModel):
    count: int
    items: List[NoteListItem]
