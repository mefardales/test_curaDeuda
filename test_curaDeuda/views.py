from fastapi import Depends, HTTPException
from api import app
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from models import (
    Estados,
    Estado_Pydantic,
    EstadoIn_Pydantic,
    Municipios,
    Municipio_Pydantic,
    MunicipioIn_Pydantic,
    Colonias,
    Colonia_Pydantic,
    ColoniaIn_Pydantic,
    Users,
    User_Pydantic,
    UserIn_Pydantic,
    RulesUsers,
    RulesUser_Pydantic,
    RulesUserIn_Pydantic,
)
from tortoise.query_utils import Q
from typing import List
from pydantic import BaseModel, Field, Required
import textwrap
from datetime import datetime
import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent

#importar datos
@app.post("/api/importar")
async def imp_est(filename:str=None, cant_pag:int=33, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    token = Authorize.get_raw_jwt()
    usda = await Users.filter(username=token['identity']).all()
    if filename == None:
        dato="No se ha proporcionado un archivo excel para trabajar"
    else:
        n=1
        dato="datos importados correctamente"
        while n < cant_pag:
            try:
                excel0 = pd.read_excel(f'{BASE_DIR}/dir_tabla/{filename}',sheet_name=n)
                #estados
                if int(excel0['c_estado'][0]) < 10:
                    ce = '0{0}'.format(excel0['c_estado'][0])
                else:
                    ce = '{0}'.format(excel0['c_estado'][0])
                consult = await Estados.filter(nome=excel0['d_estado'][0]).all()
                if len(consult) == 0:
                    e_obj = await Estados.create(nome=excel0['d_estado'][0], eclave=ce)
                    await e_obj.save()
                #municipios
                cons0 = await Estados.all().count()
                for n in range(1, (cons0+1)):
                    for m in range(0, len(excel0['D_mnpio'])):
                        cpms = str(excel0['d_CP'][m]).split('.')
                        if len(cpms) > 0:
                            cpmss = cpms[0]
                        else:
                            cpmss = str(excel0['d_CP'][m])
                        clvm = str(excel0['c_mnpio'][m]).split('.')
                        if len(clvm) > 0:
                            clvms = clvm[0]
                        else:
                            clvms = str(excel0['c_mnpio'][m])
                        if int(clvms) > 10:
                            clvms = f'00{clvms}'
                        else:
                            clvms = f'0{clvms}'
                        cons1 = await Municipios.filter(nomm=excel0['D_mnpio'][m], cpm=cpmss, clavem=clvms).all()
                        if len(cons1) == 0:
                            cons2 = await Estados.filter(nome=excel0['d_estado'][m]).all()
                            if len(cons2) > 0:
                                m_obj = await Municipios.create(nomm=excel0['D_mnpio'][m], cpm=cpmss, clavem=clvms, idme_id=cons2[0].ide)
                                await m_obj.save()
                #colonias
                for n in range(1, (cons0+1)):
                    for c in range(0, len(excel0['d_asenta'])):
                        sta = str(excel0['c_tipo_asenta'][c]).split('.')
                        if len(sta) > 0:
                            if int(sta[0]) < 10:
                                sta = f'0{sta[0]}'
                            else:
                                sta = str(sta[0])
                        else:
                            sta = str(excel0['c_tipo_asenta'][c])
                        sida = str(excel0['id_asenta_cpcons'][c]).split('.')
                        if len(sida) > 0:
                            if int(sida[0]) < 1000:
                                if int(sida[0]) < 100:
                                    sida = f'00{sida[0]}'
                                else:
                                    sida = f'0{sida[0]}'
                            else:
                                sida = str(sida[0])
                        else:
                            sida = str(excel0['id_asenta_cpcons'][c])
                        szc = str(excel0['d_zona'][c])
                        zc = False
                        if szc == 'Urbano':
                            zc = True
                        elif szc == 'Rural':
                            zc = False
                        cpms = str(excel0['d_CP'][c]).split('.')
                        if len(cpms) > 0:
                            cpms = str(cpms[0])
                        else:
                            cpms = str(excel0['d_CP'][c])
                        cons1 = await Municipios.filter(nomm=excel0['D_mnpio'][c], cpm=cpms).all()
                        if len(cons1) > 0:
                            cons2 = await Colonias.filter(idacp=sida,nomc=excel0['d_asenta'][c],idcm_id=cons1[0].idm).all()
                            if len(cons2) == 0:
                                c_obj = await Colonias.create(idacp=sida,nomc=excel0['d_asenta'][c],cpoficina=excel0['c_oficina'][c],ctipo=sta,\
                                tipo=excel0['d_tipo_asenta'][c],zonaubic=zc,dcp=excel0['d_codigo'][c],idcm_id=cons1[0].idm)
                                await c_obj.save()        
            except:
                dato="error"
            n+=1        
    return JSONResponse(content={'detail':dato})

#leer datos de la tabla colonias
@app.get("/colonias", status_code=200, response_model=List[Colonia_Pydantic])
async def get_data(ccp:str=None,name_col:str=None,mun:str=None,cpm:str=None,colon:str=None,limit:int=0, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    token = Authorize.get_raw_jwt()
    usda = await Users.filter(username=token['identity']).all()
    data = ["No_data"]
    if ccp != None and name_col == None:
        if limit == 0:
            cons0 = Colonias.filter(Q(dcp__icontains=ccp)).all()
        else:
            cons0 = Colonias.filter(Q(dcp__icontains=ccp)).all().limit(limit)
        if len(await Colonia_Pydantic.from_queryset(cons0)) > 0:
            return await Colonia_Pydantic.from_queryset(cons0)
    if name_col != None and ccp == None:
        if limit == 0:
            cons0 = Colonias.filter(Q(nomc__icontains=name_col)).all()
        else:
            cons0 = Colonias.filter(Q(nomc__icontains=name_col)).all().limit(limit)
        if len(await Colonia_Pydantic.from_queryset(cons0)) > 0:
            return await Colonia_Pydantic.from_queryset(cons0)
    if mun != None:
        if cpm == None:
            conm =  await Municipios.filter(Q(nomm__icontains=mun)).all()
            if len(conm) > 0:
                cons0 = Colonias.filter(Q(idcm_id=conm[0].idm)).all()
                if len(conm) == 2:
                    cons0 = Colonias.filter(Q(idcm_id=conm[1].idm) and Q(idcm_id=conm[0].idm)).all()
                if len(conm) == 3:
                    cons0 = Colonias.filter(Q(idcm_id=conm[2].idm) and Q(idcm_id=conm[1].idm) and Q(idcm_id=conm[0].idm)).all()
                if len(conm) == 4:
                    cons0 = Colonias.filter(Q(idcm_id=conm[3].idm) and Q(idcm_id=conm[2].idm) and Q(idcm_id=conm[1].idm) and \
                                            Q(idcm_id=conm[0].idm)).all()
                if len(conm) == 5:
                    cons0 = Colonias.filter(Q(idcm_id=conm[4].idm) and Q(idcm_id=conm[3].idm) and Q(idcm_id=conm[2].idm) and \
                                            Q(idcm_id=conm[1].idm) and Q(idcm_id=conm[0].idm)).all()
            else:
                cons0 = Colonias.filter(Q(idcm_id=0)).all()
        else:
            conm =  await Municipios.filter(Q(nomm=mun) and Q(cpm=cpm)).all()
            if len(conm) > 0:
                cons0 = Colonias.filter(Q(idcm_id=conm[0].idm)).all()
            else:
                cons0 = Colonias.filter(Q(idcm_id=0)).all()
        if len(await Colonia_Pydantic.from_queryset(cons0)) > 0:
            return await Colonia_Pydantic.from_queryset(cons0)
    if colon != None:
        if limit == 0:
            cons0 = Colonias.filter(Q(tipo__icontains=colon)).all()
        else:
            cons0 = Colonias.filter(Q(tipo__icontains=colon)).all().limit(limit)
        if len(await Colonia_Pydantic.from_queryset(cons0)) > 0:
            return await Colonia_Pydantic.from_queryset(cons0)
    if name_col != None and ccp != None:
        if limit == 0:
            cons0 = Colonias.filter(Q(nomc__icontains=name_col) and Q(dcp__icontains=ccp)).all()
        else:
            cons0 = Colonias.filter(Q(nomc__icontains=name_col) and Q(dcp__icontains=ccp)).all().limit(limit)
        if len(await Colonia_Pydantic.from_queryset(cons0)) > 0:
            return await Colonia_Pydantic.from_queryset(cons0)
    return JSONResponse(content={'detail':data})

#leer datos de la tabla municipios
@app.get("/municipios", status_code=200, response_model=List[Municipio_Pydantic])
async def get_datam(mun:str=None,cpm:str=None,limit:int=0, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    token = Authorize.get_raw_jwt()
    usda = await Users.filter(username=token['identity']).all()
    data = ["No_data"]
    if mun != None:
        if limit == 0:
            if cpm == None:
                cons0 = Municipios.filter(Q(nomm__icontains=mun)).all()
            else:
                cons0 = Municipios.filter(Q(nomm=mun) and Q(cpm=cpm)).all()
        else:
            if cpm == None:
                cons0 = Municipios.filter(Q(nomm__icontains=mun)).all().limit(limit)
            else:
                cons0 = Municipios.filter(Q(nomm=mun) and Q(cpm=cpm)).all().limit(limit)
        if len(await Municipio_Pydantic.from_queryset(cons0)) > 0:
            return await Municipio_Pydantic.from_queryset(cons0)
    return JSONResponse(content={'detail':data})

#leer datos de la tabla  estados
@app.get("/estado", status_code=200, response_model=List[Estado_Pydantic])
async def get_datae(est:str=None,limit:int=0, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    token = Authorize.get_raw_jwt()
    usda = await Users.filter(username=token['identity']).all()
    data = ["No_data"]
    if est != None:
        if limit == 0:
            cons0 = Estados.filter(Q(nome__icontains=est)).all()
        else:
            cons0 = Estados.filter(Q(nome__icontains=est)).all().limit(limit)
        if len(await Estado_Pydantic.from_queryset(cons0)) > 0:
            return await Estado_Pydantic.from_queryset(cons0)
    return JSONResponse(content={'detail':data})

#autentificacion login
@app.post("/auth")
async def post_login(us: UserIn_Pydantic):
    consult =  await Users.filter(username=us.username).all().limit(1)
    csu = await Users.all().count()
    if csu == 0:
        #sin usuario
        us.entry_date, passwd = dt.datetime.now(), us.passwd
        us.passwd = password=generate_password_hash(us.passwd, method='sha256')
        us_obj = await Users.create(**us.dict(exclude_unset=True))
        await us_obj.save()
        try:
            access_token = AuthJWT.create_access_token(identity=us.username).decode("utf-8")
        except:
            access_token = AuthJWT.create_access_token(identity=us.username)
        return JSONResponse(content={'access_token': str(access_token),'uroot':us.username, 'uspasswd':passwd, 'detail': "Successful login"})
    if len(consult) > 0 and check_password_hash(consult[0].passwd, us.passwd):
        #usuario autentificado auntentificado
        cactivuser = await RulesUsers.filter(idur=consult[0].idu).all().limit(1)
        if len(cactivuser) > 0:
            if cactivuser[0].is_active == True:
                try:
                    access_token = AuthJWT.create_access_token(identity=us.username).decode("utf-8")
                except:
                    access_token = AuthJWT.create_access_token(identity=us.username)
                return JSONResponse(content={'access_token': str(access_token), 'detail': "Successful login"})
            raise HTTPException(status_code=403, detail=f"The user {us.username} is not active")
        #notificacion de usuario no registrado
        raise HTTPException(status_code=403, detail=f"The user {us.username} is not registered")
    raise HTTPException(status_code=403, detail=f"The user {us.username} not found in database")

#registro
@app.post("/reg_up_user")
async def post_regupdate(us: UserIn_Pydantic, ru: RulesUserIn_Pydantic, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    token = Authorize.get_raw_jwt()
    user_auth = await Users.filter(username=token['identity']).all().limit(1)
    csru = await RulesUsers.all().count()
    if csru == 0:
        #registro 0
        cons0 =  await Users.filter(username=token['identity']).all().limit(1)
        ru.is_superuser = True
        ru_obj = await RulesUsers.create(**ru.dict(exclude_unset=True), idur_id=cons0[0].idu)
        await ru_obj.save()
        return JSONResponse(content={'admin_register': "satisfactorily", 'user_admin': token['identity']})
    if len(user_auth) > 0:
        consult =  await Users.filter(username=us.username).all().limit(1)
        if len(consult) == 0:
            #registro
            creg = await RulesUsers.filter(idur=user_auth[0].idu).all().limit(1)
            if creg[0].is_superuser == True:
                us.entry_date = dt.datetime.now()
                us.passwd = password=generate_password_hash(us.passwd, method='sha256')
                usc_obj = await Users.create(**us.dict(exclude_unset=True))
                await usc_obj.save()
                cons =  await Users.filter(username=us.username).all().limit(1) 
                ruc_obj = await RulesUsers.create(**ru.dict(exclude_unset=True), idur_id=cons[0].idu)
                await ruc_obj.save()
                return JSONResponse(content={'registered_user': "satisfactorily", "user_name": us.username})
            raise HTTPException(status_code=401, detail=f"The user {token['identity']} is not an administrator")
        if len(consult) > 0:
            #update
            us.passwd = password=generate_password_hash(us.passwd, method='sha256')
            usu_obj = await Users.filter(idu=consult[0].idu).update(**us.dict(exclude_unset=True))
            ruu_obj = await RulesUsers.filter(idur=consult[0].idu).update(**ru.dict(exclude_unset=True), idur_id=consult[0].idu)
            return JSONResponse(content={'updated_user': "satisfactorily", "user_name": us.username})
    raise HTTPException(status_code=403, detail=f"User '{us.username}' not found in database")

#delete user
@app.post("/deluser")
async def post_del(us: UserIn_Pydantic, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    token = Authorize.get_raw_jwt()
    user_auth = await Users.filter(username=token['identity']).all().limit(1)
    if len(user_auth) > 0:
        cadmin = await RulesUsers.filter(is_superuser=True).all().count()
        cusamdin = await Users.filter(username=us.username).all()
        adminu = await RulesUsers.filter(idur_id=cusamdin[0].idu, is_superuser=True).all()
        if cadmin == 1 and len(adminu) == 1:
            raise HTTPException(status_code=401, detail=f"{us.username} is unique admin user, this account cannot be deleted")
        adminuser = await RulesUsers.filter(idur_id=user_auth[0].idu, is_superuser=True).all()
        if len(adminuser) == 0:
            raise HTTPException(status_code=401, detail=f"The user {token['identity']} is not an administrator")
        delconsult = await Users.filter(username=us.username).delete()
        return JSONResponse(content={'deleted_user': "satisfactorily", "user_name": us.username})
    raise HTTPException(status_code=403, detail=f"User '{us.username}' not found in database")
