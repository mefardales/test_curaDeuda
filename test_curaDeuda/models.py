from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Estados(models.Model):
    ide = fields.IntField(pk=True)
    nome = fields.CharField(max_length=100)
    eclave = fields.CharField(max_length=100)

    class Meta:
        table = 'estados'
    
    class PydanticMeta:
        exclude = ["ide"]

Estado_Pydantic = pydantic_model_creator(Estados, name="Estado")
EstadoIn_Pydantic = pydantic_model_creator(Estados, name="EstadoIn", exclude_readonly=True)

class Municipios(models.Model):
    idm = fields.IntField(pk=True)
    nomm = fields.CharField(max_length=100)
    cpm = fields.CharField(max_length=100)
    clavem = fields.CharField(max_length=100)
    idme = fields.ForeignKeyField("models.Estados", related_name="items", null=False)

    class Meta:
        table = 'municipios'
    
    class PydanticMeta:
        exclude = ["idm"]

Municipio_Pydantic = pydantic_model_creator(Municipios, name="Municipio")
MunicipioIn_Pydantic = pydantic_model_creator(Municipios, name="MunicipioIn", exclude_readonly=True)

class Colonias(models.Model):
    idc = fields.IntField(pk=True)
    nomc = fields.CharField(max_length=100)
    idacp = fields.CharField(max_length=100)
    tipo = fields.CharField(max_length=100)
    ctipo = fields.CharField(max_length=100)
    zonaubic = fields.BooleanField(default=False)
    dcp = fields.CharField(max_length=100)
    cpoficina = fields.CharField(max_length=100)
    idcm = fields.ForeignKeyField("models.Municipios", related_name="items", null=False)

    def zonau(self) -> str:
        if bool(self.zonaubic) == True:
            return "Urbano"
        else:
            return "Rural"

    class Meta:
        table = 'colonias'
    
    class PydanticMeta:
        computed = ["zonau"]
        exclude = ["idc","zonaubic"]

Colonia_Pydantic = pydantic_model_creator(Colonias, name="Colonia")
ColoniaIn_Pydantic = pydantic_model_creator(Colonias, name="ColoniaIn", exclude_readonly=True)

class Users(models.Model):
    idu = fields.IntField(pk=True)
    username = fields.CharField(max_length=100, unique=True)
    passwd = fields.CharField(max_length=200)
    entry_date = fields.DatetimeField(null=True, auto_now_add=False)

    class Meta:
        table = 'users'
    
    class PydanticMeta:
        exclude = ["idu"]

User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)

class RulesUsers(models.Model):
    idru = fields.IntField(pk=True)
    idur = fields.ForeignKeyField("models.Users", related_name="items", null=True)
    is_superuser = fields.BooleanField(default=False)
    is_adviser = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = 'rulesusers'
    
RulesUser_Pydantic = pydantic_model_creator(RulesUsers, name="RulesUser")
RulesUserIn_Pydantic = pydantic_model_creator(RulesUsers, name="RulesUserIn", exclude_readonly=True)
