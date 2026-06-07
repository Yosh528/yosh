"""Novel-to-Script 数据模型"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Version(BaseModel):
    """版本控制层"""
    schema_version: str = Field(default="1.0.0")
    schema_url: Optional[str] = None
    last_modified: str = Field(default="2026-06-05")
    compatible_tools: List[str] = Field(default_factory=lambda: ["Final Draft 13", "Celtx", "WriterDuet", "Fountain"])


class Project(BaseModel):
    """项目信息层"""
    repo_url: Optional[str] = None
    commit_hash: Optional[str] = None
    pr_number: Optional[str] = None
    generated_by: Optional[str] = None
    generation_date: Optional[str] = None


class Metadata(BaseModel):
    """剧本元数据"""
    title: str
    original_title: Optional[str] = None
    author: str
    source_author: Optional[str] = None
    genre: str  # 爱情/悬疑/科幻/古装/都市/职场
    format: str  # 短剧/网剧/电影/舞台剧/广播剧
    total_scenes: int = 0
    total_pages: int = 0
    draft_version: str = "v1.0"
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    logline: str
    fountain_compatible: bool = True


class Character(BaseModel):
    """角色定义"""
    id: str  # char_xxx
    name: str
    code_name: str  # 全大写
    aliases: List[str] = Field(default_factory=list)
    age: Optional[int] = None
    gender: Optional[str] = None  # 男/女/未知
    occupation: Optional[str] = None
    traits: List[str] = Field(default_factory=list)
    arc: Optional[str] = None
    description: Optional[str] = None
    scene_count: int = 0
    total_lines: int = 0
    total_words: int = 0
    first_appearance: Optional[str] = None
    last_appearance: Optional[str] = None
    notes: Optional[str] = None


class Slugline(BaseModel):
    """场景标题"""
    int_ext: str  # INT./EXT.
    location: str
    time: str  # DAY/NIGHT/DAWN/etc


class ContentItem(BaseModel):
    """场景内容项"""
    type: str  # scene_heading/action/character/parenthetical/dialogue/transition/shot/sound
    text: Optional[str] = None
    notes: Optional[str] = None
    name: Optional[str] = None
    id: Optional[str] = None
    extension: Optional[str] = None  # V.O./O.S./O.C.
    emotion: Optional[str] = None
    delivery: Optional[str] = None
    parenthetical: Optional[str] = None
    offscreen: bool = False
    voiceover: bool = False
    shot_type: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None  # 环境音/音乐/特效/拟音


class Scene(BaseModel):
    """场景定义"""
    scene_id: str  # SCxxx
    act: Optional[str] = None
    sequence: Optional[str] = None
    slugline: Slugline
    full_slugline: str
    mood: Optional[str] = None
    characters_present: List[str] = Field(default_factory=list)
    estimated_duration: Optional[str] = None
    pages: int = 1
    content: List[ContentItem] = Field(default_factory=list)


class Note(BaseModel):
    """注释"""
    scene_id: Optional[str] = None
    type: str  # 待修改/AI提示/导演备注/编剧备忘/技术备注/审核意见/PR关联
    author: str
    text: str
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    pr_reference: Optional[str] = None


class Extensions(BaseModel):
    """扩展字段"""
    custom_fields: dict = Field(default_factory=dict)
    production_notes: dict = Field(default_factory=dict)
    scheduling_info: dict = Field(default_factory=dict)
    git_history: List[str] = Field(default_factory=list)


class Screenplay(BaseModel):
    """完整剧本模型"""
    version: Version = Field(default_factory=Version, alias="version")
    project: Optional[Project] = Field(default=None, alias="project")
    metadata: Metadata
    characters: List[Character] = Field(default_factory=list)
    scenes: List[Scene] = Field(default_factory=list)
    notes: List[Note] = Field(default_factory=list)
    extensions: Extensions = Field(default_factory=Extensions)

    class Config:
        populate_by_name = True
        populate_by_alias = True