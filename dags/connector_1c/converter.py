from typing import List
from venv import logger
from dags.connector_1c.models import Zhufvr, Works, Pikets, Materials, TechniqueWorkers, NormWorkload
from dags.connector_1c.schemas import ZhufvrSchema

def filter_items_by_key(items: list, key):
    
    return [i for i in items if i.work_id == key]

async def zhufvr_to_sql(zfv: ZhufvrSchema) -> Zhufvr:
    """
    Convert pydantic Zhufvr model to SQLAlchemy ORM model
    """
    
    works_lst = []
    materials_lst = []
    technique_workers_lst = []
    n_workloads_lst = []
    pikets_lst = []
    
    for mat in zfv.value.materials:
        
        mat_sql = Materials(
            
            work_id = mat.work_id,
            num_row = mat.num_row,
            value = mat.value,
            comment = mat.comment
        )
        
        if mat.resource:
            mat_sql.res_value = mat.resource.value
            mat_sql.res_name = mat.resource.name
            mat_sql.res_code = mat.resource.code
        
        materials_lst.append(mat_sql)
        
    for pk in zfv.value.pikets:
        
        pk_sql = Pikets(
            work_id = pk.key_link,
            key_row = pk.key_row,
            vol = pk.vol,
            start_pk = pk.start_pk,
            fin_pk = pk.fin_pk,
            start_offset = pk.start_offset,
            fin_offset = pk.fin_offset,
            # comment = pk.comment,
        )
        
        if pk.kind_piket:
            pk_sql.kind_piket_value = pk.kind_piket.value
            pk_sql.kind_piket_name = pk.kind_piket.name
            pk_sql.kind_piket_code = pk.kind_piket.code
            
        if pk.group_spider_piket:
            pk_sql.group_spider_piket_value = pk.group_spider_piket.value
            pk_sql.group_spider_piket_name = pk.group_spider_piket.name
            pk_sql.group_spider_piket_code = pk.group_spider_piket.code
        
        if pk.type_piket:
            pk_sql.type_piket_value = pk.type_piket.value
            pk_sql.type_piket_name = pk.type_piket.name
            pk_sql.type_piket_code = pk.type_piket.code
            
            
        pikets_lst.append(pk_sql)
        
        
    for tch_wrkrs in zfv.value.technique_workers:
        
        tw_sql = TechniqueWorkers(
            work_id = tch_wrkrs.key_link,
            gos_num_not_find = tch_wrkrs.gos_num_not_find,
            num = tch_wrkrs.num,
            comment = tch_wrkrs.comment,
            hours = tch_wrkrs.hours
        )
        
        if tch_wrkrs.analytics:
            tw_sql.analytics_value = tch_wrkrs.analytics.value
            tw_sql.analytics_name = tch_wrkrs.analytics.name
            tw_sql.analytics_code = tch_wrkrs.analytics.code
        
        if tch_wrkrs.contragent:
            tw_sql.contragent_value = tch_wrkrs.contragent.value
            tw_sql.contragent_name = tch_wrkrs.contragent.name
            tw_sql.contragent_code = tch_wrkrs.contragent.code
            
        if tch_wrkrs.res:
            tw_sql.res_value = tch_wrkrs.res.value
            tw_sql.res_name = tch_wrkrs.res.name
            tw_sql.res_code = tch_wrkrs.res.code
              
        
        technique_workers_lst.append(tw_sql)
        
    
    for n_wrld in zfv.value.norm_workload:
        
        n_wrld_sql = NormWorkload(
            zhufvr_id = n_wrld.zhufvr_id,
            key_doc_res = n_wrld.key_doc_res,
            work_id = n_wrld.registrator,
            nt_res = n_wrld.nt_res,
            some_key_res = n_wrld.some_key_res,
            period = n_wrld.period,
            calc_vol = n_wrld.calc_vol,
            norm_workload = n_wrld.norm_workload,
            fact_workload = n_wrld.fact_workload
        )
        
        if n_wrld.analytics:
            n_wrld_sql.analytics_value = n_wrld.analytics.value
            n_wrld_sql.analytics_name = n_wrld.analytics.name
            n_wrld_sql.analytics_code = n_wrld.analytics.code
        
        if n_wrld.key_res:
            n_wrld_sql.key_res_value = n_wrld.key_res.value
            n_wrld_sql.key_res_name = n_wrld.key_res.name
            n_wrld_sql.key_res_code = n_wrld.key_res.code
        
        if n_wrld.res_spider:
            n_wrld_sql.res_spider_value = n_wrld.res_spider.value
            n_wrld_sql.res_spider_name = n_wrld.res_spider.name
            n_wrld_sql.res_spider_code = n_wrld.res_spider.code

        if n_wrld.structure_works:
            n_wrld_sql.structure_works_value = n_wrld.structure_works.value
            n_wrld_sql.structure_works_name = n_wrld.structure_works.name
            n_wrld_sql.structure_works_code = n_wrld.structure_works.code
        
        n_workloads_lst.append(n_wrld_sql)
        
        
    for work in zfv.value.works:
        
        work_sql = Works(
            zhufvr_id = zfv.value.link,
            work_id = work.key_link,
            vol = work.vol,
            comment = work.comment,
            num_con = work.num_con,
            structure_is_delete = work.structure_is_delete,
            structure_unique_code = work.structure_unique_code,
            structure_idnt = work.structure_idnt,
            enrp_type = work.enrp_type,
            
            #children relations
            pikets = filter_items_by_key(pikets_lst, work.key_link),
            materials = filter_items_by_key(materials_lst, work.key_link),
            norm_workload = filter_items_by_key(n_workloads_lst, work.key_link),
            technique_workers = filter_items_by_key(technique_workers_lst, work.key_link)
        )
        
        if work.type_work:
            work_sql.type_work_value = work.type_work.value
            work_sql.type_work_name = work.type_work.name
            work_sql.type_work_code = work.type_work.code
            
        if work.structure_works:
            work_sql.structure_works_value = work.structure_works.value
            work_sql.structure_works_name = work.structure_works.name
            work_sql.structure_works_code = work.structure_works.code
        
        works_lst.append(work_sql)
    
        
    zhufvr_sql = Zhufvr( 
        uuid = zfv.uuid,
        send_date = zfv.date,
        sender = zfv.sender,
        reciever = zfv.reciever,
        key = zfv.key,
        type = zfv.type,
        link = zfv.value.link,
        zhfvr_date = zfv.value.date,
        number = zfv.value.number,
        comment = zfv.value.comment,
        delete_flag = zfv.value.delete_flag,
        is_done = zfv.value.is_done,
        #children relations
        works = works_lst
    )
    
    if zfv.value.direction:
        zhufvr_sql.direction_value = zfv.value.direction.value
        zhufvr_sql.direction_name = zfv.value.direction.name
    
    if zfv.value.territory:
        zhufvr_sql.territory_value = zfv.value.territory.value
        zhufvr_sql.territory_name = zfv.value.territory.name
        zhufvr_sql.territory_code = zfv.value.territory.code
        
    if zfv.value.recorder:
        zhufvr_sql.recorder_value = zfv.value.recorder.value
        zhufvr_sql.recorder_name = zfv.value.recorder.name
        zhufvr_sql.recorder_code = zfv.value.recorder.code
        
    if zfv.value.sector:
        zhufvr_sql.sector_value = zfv.value.sector.value
        zhufvr_sql.sector_name = zfv.value.sector.name
        zhufvr_sql.sector_code = zfv.value.sector.code
        
    if zfv.value.boss_builder:
        zhufvr_sql.boss_builder_value = zfv.value.boss_builder.value
        zhufvr_sql.boss_builder_name = zfv.value.boss_builder.name
        zhufvr_sql.boss_builder_code = zfv.value.boss_builder.code
        
    if zfv.value.work_shift:
        zhufvr_sql.work_shift_value = zfv.value.work_shift.value
        zhufvr_sql.work_shift_name = zfv.value.work_shift.name
        zhufvr_sql.work_shift_code = zfv.value.work_shift.code
    
    return zhufvr_sql
    