from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, sql
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.types import DateTime
from typing import List
from datetime import datetime
from database import BaseModel
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, BOOLEAN, NUMERIC


tabprefix = '1_c__'

class TimedBaseModel(BaseModel):
    """
    An abstract base model that adds created_at and updated_at timestamp fields to the model
    """
    __abstract__ = True
    
    is_actual: Mapped[bool] = mapped_column(BOOLEAN, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=sql.func.now())
  
    
class TechniqueWorkers(TimedBaseModel):
    __tablename__ = f'{tabprefix}technique_workers'
    __table_args__ = {"schema": "1c", 'comment': 'ТехникаРабочие'}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    
    analytics_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='Аналитика_value')
    analytics_name: Mapped[str] = mapped_column(String, nullable=True, comment='Аналитика_name')
    analytics_code: Mapped[str] = mapped_column(String, nullable=True, comment='Аналитика_code')
    contragent_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='Контрагент_value')
    contragent_name: Mapped[str] = mapped_column(String, nullable=True, comment='Контрагент_name')
    contragent_code: Mapped[str] = mapped_column(String, nullable=True, comment='Контрагент_code')
    work_id: Mapped[UUID] = mapped_column(ForeignKey(f'1c.{tabprefix}works.work_id', ondelete='CASCADE'), index=True, comment='КлючСвязи')
    gos_num_not_find: Mapped[str] = mapped_column(String, nullable=True, comment='ГосНомерТехникаНеНайдена')
    num: Mapped[int] = mapped_column(Integer, nullable=True, comment='Количество')
    comment: Mapped[str] = mapped_column(String, nullable=True, comment='Примечание')
    res_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='Ресурс_value')
    res_name: Mapped[str] = mapped_column(String, nullable=True, comment='Ресурс_name')
    res_code: Mapped[str] = mapped_column(String, nullable=True, comment='Ресурс_code')
    hours: Mapped[float] = mapped_column(NUMERIC, nullable=True, comment='Часы')
    
    works: Mapped['Works'] = relationship(back_populates="technique_workers")
    
class Materials(TimedBaseModel):
    __tablename__ = f'{tabprefix}materials'
    __table_args__ = {"schema": "1c", 'comment': 'Материалы'}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    
    work_id: Mapped[UUID] = mapped_column(ForeignKey(f'1c.{tabprefix}works.work_id', ondelete='CASCADE'), index=True, comment='КлючСвязи')
    num_row: Mapped[int] = mapped_column(Integer, nullable=True, comment='НомерСтроки')
    res_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='Ресурс_value')
    res_name: Mapped[str] = mapped_column(String, nullable=True, comment='Ресурс_name')
    res_code: Mapped[str] = mapped_column(String, nullable=True, comment='Ресурс_code')
    value: Mapped[float] = mapped_column(NUMERIC, nullable=True, comment='ОбъемМатериала')
    comment: Mapped[str] = mapped_column(String, nullable=True, comment='Примечание')
    
    works: Mapped['Works'] = relationship(back_populates="materials")
    
    
class NormWorkload(TimedBaseModel):
    __tablename__ = f'{tabprefix}norm_workload'
    __table_args__ = {"schema": "1c", 'comment': 'НормативнаяТрудоемкость'}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    
    analytics_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='Аналитика_value')
    analytics_name: Mapped[str] = mapped_column(String, nullable=True, comment='Аналитика_name')
    analytics_code: Mapped[str] = mapped_column(String, nullable=True, comment='Аналитика_code')
    zhufvr_id: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='ID ЖУФВР')
    key_doc_res: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='КлючДокументаРесурс')
    work_id: Mapped[UUID] = mapped_column(ForeignKey(f'1c.{tabprefix}works.work_id', ondelete='CASCADE'), index=True, comment='Регистратор')
    key_res_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='КлючевойРесурс_value')
    key_res_name: Mapped[str] = mapped_column(String, nullable=True, comment='КлючевойРесурс_name')
    key_res_code: Mapped[str] = mapped_column(String, nullable=True, comment='КлючевойРесурс_code')
    nt_res: Mapped[bool] = mapped_column(BOOLEAN, nullable=True, comment='НаемныйРесурс')
    some_key_res: Mapped[bool] = mapped_column(BOOLEAN, nullable=True, comment='НесколькоКлючевыхРесурсов')
    period: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True, comment='Период')
    calc_vol: Mapped[float] = mapped_column(NUMERIC, nullable=True, comment='РассчетныйОбъем')
    res_spider_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='РесурсSpider_value')
    res_spider_name: Mapped[str] = mapped_column(String, nullable=True, comment='РесурсSpider_name')
    res_spider_code: Mapped[str] = mapped_column(String, nullable=True, comment='РесурсSpider_code')
    structure_works_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='СтруктураРабот_value')
    structure_works_name: Mapped[str] = mapped_column(String, nullable=True, comment='СтруктураРабот_name')
    structure_works_code: Mapped[str] = mapped_column(String, nullable=True, comment='СтруктураРабот_code')
    norm_workload: Mapped[float] = mapped_column(NUMERIC, nullable=True, comment='ТрудоемкостьНормативная')
    fact_workload: Mapped[float] = mapped_column(NUMERIC, nullable=True, comment='ТрудоемкостьФактическая')
    
    works: Mapped['Works'] = relationship(back_populates='norm_workload')


class Pikets(TimedBaseModel):
    __tablename__ = f'{tabprefix}pikets'
    __table_args__ = {"schema": "1c", 'comment': 'РазбивкаПоПикетам'}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    
    kind_piket_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='ВидПикета_value')
    kind_piket_name: Mapped[str] = mapped_column(String, nullable=True, comment='ВидПикета_name')
    kind_piket_code: Mapped[str] = mapped_column(String, nullable=True, comment='ВидПикета_code')
    group_spider_piket_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='ГруппаПикетовSpider_value')
    group_spider_piket_name: Mapped[str] = mapped_column(String, nullable=True, comment='ГруппаПикетовSpider_name')
    group_spider_piket_code: Mapped[str] = mapped_column(String, nullable=True, comment='ГруппаПикетовSpider_code')    
    work_id: Mapped[UUID] = mapped_column(ForeignKey(f'1c.{tabprefix}works.work_id', ondelete='CASCADE'), index=True, comment='КлючСвязи')
    key_row: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='КлючСтроки')
    vol: Mapped[float] = mapped_column(NUMERIC, nullable=True, comment='Объем')
    start_pk: Mapped[float] = mapped_column(NUMERIC, nullable=True, comment='ПикетС')
    fin_pk: Mapped[float] = mapped_column(NUMERIC, nullable=True, comment='ПикетПо')
    start_offset: Mapped[float] = mapped_column(NUMERIC, nullable=True, comment='СмещениеС')
    fin_offset: Mapped[float] = mapped_column(NUMERIC, nullable=True, comment='СмещениеПо')
    # comment: Mapped[str] = mapped_column(String)
    type_piket_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='ТипПикета_value')
    type_piket_name: Mapped[str] = mapped_column(String, nullable=True, comment='ТипПикета_name')
    type_piket_code: Mapped[str] = mapped_column(String, nullable=True, comment='ТипПикета_code')
    
    works: Mapped['Works'] = relationship(back_populates='pikets')
    
    
class Works(TimedBaseModel):
    __tablename__ = f'{tabprefix}works'
    __table_args__ = {"schema": "1c", 'comment': 'Работы'}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    
    zhufvr_id: Mapped[UUID] = mapped_column(ForeignKey(f'1c.{tabprefix}zhufvr.link', ondelete='CASCADE'), index=True, comment='ID ЖУФВР')
    work_id: Mapped[UUID] = mapped_column(UUID, index=True, unique=True, comment='КлючСвязи')
    type_work_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='ВидРабот_value')
    type_work_name: Mapped[str] = mapped_column(String, nullable=True, comment='ВидРабот_name')
    type_work_code: Mapped[str] = mapped_column(String, nullable=True, comment='ВидРабот_code')
    vol: Mapped[float] = mapped_column(NUMERIC, nullable=True, comment='ОбъемРаботы')
    comment: Mapped[str] = mapped_column(String, nullable=True, comment='Примечание')
    num_con: Mapped[str] = mapped_column(String, nullable=True, comment='СтруктураРаботНомерПоКонтрактнойВедомости')
    structure_is_delete: Mapped[bool] = mapped_column(BOOLEAN, nullable=True, comment='СтруктураРаботПометкаУдаления')
    structure_unique_code: Mapped[str] = mapped_column(String, nullable=True, comment='СтруктураРаботУникальныйКод')
    structure_idnt: Mapped[str] = mapped_column(String, nullable=True, comment='СтруктураРаботИдентификатор')
    enrp_type: Mapped[str] = mapped_column(String, nullable=True, comment='ВидРаботУровеньОперации')
    structure_works_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='СтруктураРабот_value')
    structure_works_name: Mapped[str] = mapped_column(String, nullable=True, comment='СтруктураРабот_name')
    structure_works_code: Mapped[str] = mapped_column(String, nullable=True, comment='СтруктураРабот_code')
    
    #to parent
    zhufvr: Mapped['Zhufvr'] = relationship(back_populates='works')
    
    #to children
    pikets: Mapped[List['Pikets'] | None] = relationship(back_populates='works', 
                                                         primaryjoin='Works.work_id==Pikets.work_id', 
                                                         passive_deletes=True)
    materials: Mapped[List['Materials'] | None]  = relationship(back_populates='works', 
                                                                primaryjoin='Works.work_id==Materials.work_id', 
                                                                passive_deletes=True)
    norm_workload: Mapped[List['NormWorkload'] | None]  = relationship(back_populates='works', 
                                                                       primaryjoin='Works.work_id==NormWorkload.work_id', 
                                                                       passive_deletes=True)
    technique_workers: Mapped[List['TechniqueWorkers'] | None]  = relationship(back_populates='works', 
                                                                               primaryjoin='Works.work_id==TechniqueWorkers.work_id', 
                                                                               passive_deletes=True)
    

class Zhufvr(TimedBaseModel):
    __tablename__ = f'{tabprefix}zhufvr'
    __table_args__ = {"schema": "1c", 'comment': 'ЖУФВР'}
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    
    #from Zhufvr schema:
    uuid: Mapped[UUID] = mapped_column(UUID)
    send_date: Mapped[datetime] = mapped_column(TIMESTAMP)
    sender: Mapped[str] = mapped_column(String, nullable=True)
    reciever: Mapped[str] = mapped_column(String, nullable=True)
    key: Mapped[str] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String, nullable=True)
    
    #from Value schema:
    link: Mapped[UUID] = mapped_column(UUID, index = True, unique=True, comment='ID ЖУФВР') #zhufvr id
    zhfvr_date: Mapped[datetime] = mapped_column(TIMESTAMP, comment='Дата ЖУФВР')
    number: Mapped[str] = mapped_column(String, comment='Номер')
    territory_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='Территория_value')
    territory_name: Mapped[str] = mapped_column(String, nullable=True, comment='Территория_name')
    territory_code: Mapped[str] = mapped_column(String, nullable=True, comment='Территория_code')
    direction_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='НаправлениеДеятельности_value')
    direction_name: Mapped[str] = mapped_column(String, nullable=True, comment='НаправлениеДеятельности_name')
    recorder_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='Ответственный_value')
    recorder_name: Mapped[str] = mapped_column(String, nullable=True, comment='Ответственный_name')
    recorder_code: Mapped[str] = mapped_column(String, nullable=True, comment='Ответственный_code')
    sector_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='Подразделение_value')
    sector_name: Mapped[str] = mapped_column(String, nullable=True, comment='Подразделение_name')
    sector_code: Mapped[str] = mapped_column(String, nullable=True, comment='Подразделение_code')
    comment: Mapped[str] = mapped_column(String, nullable=True, comment='Комментарий')
    delete_flag: Mapped[bool] = mapped_column(BOOLEAN, nullable=True, comment='ПометкаУдаления')
    is_done: Mapped[bool] = mapped_column(BOOLEAN, nullable=True, comment='Проведен')
    boss_builder_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='Прораб_value')
    boss_builder_name: Mapped[str] = mapped_column(String, nullable=True, comment='Прораб_name')
    boss_builder_code: Mapped[str] = mapped_column(String, nullable=True, comment='Прораб_code')
    work_shift_value: Mapped[UUID] = mapped_column(UUID, nullable=True, comment='Смена_value')
    work_shift_name: Mapped[str] = mapped_column(String, nullable=True, comment='Смена_name')
    work_shift_code: Mapped[str] = mapped_column(String, nullable=True, comment='Смена_code')
    
    #to children
    works: Mapped[List['Works'] | None] = relationship(back_populates="zhufvr", passive_deletes=True)
    