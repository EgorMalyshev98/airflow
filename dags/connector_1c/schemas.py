from typing import Union, Any  # Union[str, int]
from typing import Optional  # Optional[str]
from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from uuid import UUID
from typing import List



class NoneValidateModel(BaseModel):
    
    @field_validator('*', mode='before')
    @classmethod
    def empty_to_none(cls, v):
        if v == '':
            return None
        return v


class Base1CEntity(NoneValidateModel):
    type: str | None
    value: UUID | None
    code: str | None = Field(alias='codе')
    name: str | None
    IsFolder: bool | None = Field(alias='IsFolder')


class TechniqueWorkersSchema(NoneValidateModel):
    analytics: Base1CEntity | None = Field(alias='Аналитика')
    contragent: Base1CEntity | None = Field(alias='Контрагент')
    key_link: UUID = Field(alias='КлючСвязи') #КлючСвязи, id работы
    gos_num_not_find: str | None = Field(alias='ГосНомерТехникаНеНайдена')
    num: int = Field(alias='Количество')
    comment: str | None = Field(alias='Примечание')
    res: Base1CEntity = Field(alias='Ресурс')
    hours: float = Field(alias='Часы')


class MaterialsSchema(NoneValidateModel):
    work_id: UUID = Field(alias='КлючСвязи') #КлючСвязи, id работы
    num_row: int | None = Field(alias='НомерСтроки')
    resource: Base1CEntity = Field(alias='Ресурс')
    value: float = Field(alias='ОбъемМатериала')
    comment: str | None = Field(alias='Примечание')


class NormWorkloadSchema(NoneValidateModel):
    analytics: Base1CEntity | None = Field(alias='Аналитика')
    zhufvr_id: UUID = Field(alias='ЖУФВР')
    key_doc_res: UUID = Field(alias='КлючДокументаРесурс') 
    key_res: Base1CEntity | None = Field(alias='КлючевойРесурс')
    nt_res: bool = Field(alias='НаемныйРесурс')
    some_key_res: bool = Field(alias='НесколькоКлючевыхРесурсов')
    period: datetime = Field(alias='Период')
    calc_vol: float = Field(alias='РассчетныйОбъем')
    registrator: UUID = Field(alias='Регистратор') #КлючСвязи, id работы
    res_spider: Base1CEntity | None = Field(alias='РесурсSpider')
    structure_works: Base1CEntity | None = Field(alias='СтруктураРабот')
    norm_workload: float = Field(alias='ТрудоемкостьНормативная')
    fact_workload: float = Field(alias='ТрудоемкостьФактическая')


class WorksSchema(NoneValidateModel):
    key_link: UUID = Field(alias='КлючСвязи') #КлючСвязи, id работы
    num_con: str | None = Field(alias='СтруктураРаботНомерПоКонтрактнойВедомости')
    structure_is_delete: bool | None = Field(alias='СтруктураРаботПометкаУдаления')
    structure_unique_code: str | None = Field(alias='СтруктураРаботУникальныйКод')
    structure_idnt: str | None = Field(alias='СтруктураРаботИдентификатор')
    type_work: Base1CEntity = Field(alias='ВидРабот')
    enrp_type: str | None = Field(alias='ВидРаботУровеньОперации')
    vol: float = Field(alias='ОбъемРаботы')
    comment: str | None = Field(alias='Примечание')
    structure_works: Base1CEntity | None = Field(alias='СтруктураРабот')


class PiketsSchema(NoneValidateModel):
    kind_piket: Base1CEntity = Field(alias='ВидПикета')
    group_spider_piket: Base1CEntity | None = Field(alias='ГруппаПикетовSpider')
    key_link: UUID = Field(alias='КлючСвязи') #КлючСвязи, id работы
    key_row: UUID = Field(alias='КлючСтроки')
    vol: float = Field(alias='Объем')
    start_pk: float = Field(alias='ПикетС')
    fin_pk: float = Field(alias='ПикетПо')
    start_offset: float | None = Field(alias='СмещениеС')
    fin_offset: float | None = Field(alias='СмещениеПо')
    # comment: str = Field(alias='Примечание')
    type_piket: Base1CEntity = Field(alias='ТипПикета')


class Value(NoneValidateModel):
    date: datetime = Field(alias='Дата')
    number: str = Field(alias='Номер')
    territory: Base1CEntity = Field(alias='Территория')
    direction: Base1CEntity = Field(alias='НаправлениеДеятельности')
    comment: str | None = Field(alias='Комментарий')
    materials: List[MaterialsSchema] | None = Field(alias='Материалы')
    norm_workload: List[NormWorkloadSchema] | None = Field(alias='НормативнаяТрудоемкость')
    recorder: Base1CEntity | None = Field(alias='Ответственный')
    sector: Base1CEntity | None = Field(alias='Подразделение')
    delete_flag: bool = Field(alias='ПометкаУдаления')
    is_done: bool = Field(alias='Проведен')
    boss_builder: Base1CEntity | None = Field(alias='Прораб')
    technique_workers: List[TechniqueWorkersSchema] | None = Field(alias='ТехникаРабочие')
    works: List[WorksSchema] | None = Field(alias='Работы')
    pikets: List[PiketsSchema] | None = Field(alias='РазбивкаПоПикетам')
    work_shift: Base1CEntity = Field(alias='Смена')
    link: UUID | None = Field(alias='Ссылка') #zhufvr_id


class ZhufvrSchema(NoneValidateModel):
    model_config = ConfigDict(from_attributes=True)
    
    uuid: UUID
    date: datetime
    sender: str | None = None
    reciever: str | None = None
    key: str | None
    type: str | None
    value: Value


