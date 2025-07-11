from django.db import models
from django.contrib.auth.models import User


AVANCE_CHOICES = [
    
    ('proceso', 'En proceso'),
    ('atendido', 'Atendido'),
    ('cancelado', 'Cancelado'),
]

DEPARTAMENTO_CHOICES = sorted([
    ('secretaria','Secretario de Ayuntamiento'),
    ('tesoreria', 'Tesoreria'),
    ('contraluria','Contraluria'),
    ('oficialia','Oficialia'),
    ('compras','Compras y Adquisiciones'),
    ('lipia', 'Direccion de Limpia'),
    ('diversidad','Diversidad Social'),
    ('desarrollo_rural','Desarrollo Rural'),
    ('mercado','Mercado Morelos'),
    ('mercado_madero','Mercado Madero'),
    ('comunicacion_social','Comunicacion Social'),
    ('estacionamiento','Estacionamiento'),
    ('relaciones_ext','Relaciones Exteriores'),
    ('ecologia','Ecología'),
    ('obras_publicas','Obras Publicas'),
    ('archivo_municipal','Archivo Municipal'),
    ('dif','DIF'),
    ('cultura','Cultura e Historia'),
    ('planeacion','Planeación'),
    ('seguridad_publica','Seguridad Publica'),
    ('alcoholes','Alcoholes y Espectaculos'),
    ('desarrollo_rural','Desarrollo Rural'),
    ('sistemas','Sistemas'),
    ('educacion','Educación'),
    ('urbanismo','Urbanismo y Vivienda'),
    ('migrante','Migrante'),
    ('recursos_humanos','Recursos Humanos'),
    ('predial','Predial'),
    ('parques_jardines','Parques y Jardines'),
    ('turismo','Turismo'),
    ('transito','Transito'),
    ('servicios_publicos','Servicios Publicos'),
    ('instituto_mujer','Institudo Municipal de la Mujer'),
    ('desarrollo_social','Desarrollo Social'),
    ('departamento_juridico','Departamento Juridico'),
    ('deportes','Deportes'),
    ('sapas','SAPAS'),
    ('salud_municipal','Salud Municipal'),
    ('rastro','Rastro Municipal'),
    ('atencion_ciudadana','Atencion Ciudadana'),
    ('comercio_publica','Comercio y Via Publica'),
    ('alumbrado_publico','Alumbrado Publico'),
    ('desarrollo_economico','Desarrollo Economico'),
    ('proteccion_civil','Protección Civil'),
    ('nodo_umsnh','Nodo UMSNH'),
    ('protocolo','Protocolo'),
], key=lambda x: x[1].lower()) #ordena alfanumericamente mi diccionario

COLONIAS_COMUNIDADES_CHOICES = sorted([
    ('col_octubre','18 de Octubre'),
    ('aguacaliente','Aguacaliente'),
    ('amp_cuauhtemoc','Ampliacion Cuauhtemoc'),
    ('amp_maravillas','Ampliacion Maravillas'),
    ('anahuac','Anáhuac'),
    ('barranca_honda','Barranca Honda'),
    ('barrio_jabali','Barrio El Jabali'),
    ('benito_juarez','Benito Juarez'),
    ('buena_vista','Buena Vista'),
    ('cantabria','Cantabria'),
    ('calos_galvez','Carlos Galvez Betancourt'),
    ('caurio_guadalupe','Caurio de Guadalupe'),
    ('celanese','Celanese'),
    ('centro','Centro'),
    ('cerro_obraje','Cerro el Obraje'),
    ('clup_campreste','Clup Campestre'),
    ('coeneo','Coeneo'),
    ('cofradia','Cofradía'),
    ('col_erendira','Colonia Eréndira'),
    ('constitucion','Constitución'),
    ('coyolote','Coyolote'),
    ('cuauhtemoc','Cuauhtemoc'),
    ('cuauhtemoc_2','Cuauhtemoc 2'),
    ('ecuandureo','Ecuandureo'),
    ('ejidal_1','Ejidal 1'),
    ('ejidal_2','Ejidal 2'),
    ('el_borrego','El Borrego'),
    ('el_capulin','El Capulin'),
    ('el_chamizal','El Chamizal'),
    ('el_cuinato','El Cuinato'),
    ('el_limon','El Limon'),
    ('el_mirador','El Mirador'),
    ('el_paraiso','El Paraiso'),
    ('el_pueblito','El Pueblito'),
    ('emiliano_zapata','Emiliano Zapata'),
    ('felix_ireta','Felix Ireta'),
    ('fracc_frente_popular','Fraccionamiento Frente Popular Zacapu'),
    ('fracc_pineda','Fraccionamiento Pineda'),
    ('fracc_revolucion','Fraccionamiento Revolucion'),
    ('fracc_san_jose','Fraccionamiento San Jose'),
    ('fracc_valle_tepacuas','Fraccionamiento Valle Tepacuas'),
    ('fracc_vista_sierra','Fraccionamiento Vista de la Sierra'),
    ('francisco_mujica','Francisco J. Mújica'),
    ('franco_reyes','Franco Reyes'),
    ('fray_jacobo_daciano','Fray Jacobo Daciano'),
    ('garcia_padilla','García Padilla'),
    ('huandacuca','Huandacuca'),
    ('ignacio_zaragoza','Ignacio Zaragoza'),
    ('independencia','Independencia'),
    ('infonavit_carlos_galvez','Infonavit Carlos Galvez Betancourt'),
    ('infonavit_moral','Infonavit el Moral'),
    ('infonavit_juventud_deportiva','Infonavit Juventud Deportiva'),
    ('infonavit_tepacuas','Infonavit Las Tepacuas'),
    ('infonavit_lomas_jardin','Infonavit Lomas Jardin'),
    ('infonavit_pirules','Infonavit Los Pirules'),
    ('infonavit_san_miguel','Infonavit San Miguel'),
    ('ing_enrique_ranguel','Ing. Enrique Rangel'),
    ('iranguataro','Iranguataro'),
    ('jardines_zacapu','Jarines de Zacapu'),
    ('jauja','Jauja'),
    ('javier_mina','Javier Mina'),
    ('joaquin_cruz','Joaquin de la Cruz'),
    ('jose_maria_morelos','Jose Maria Morelos'),
    ('angostura','La Angostura'),
    ('la_arboleda','La Arboleda'),
    ('la_cofradia','La Cofradía'),
    ('la_erendira','La Erendira'),
    ('la_huerta','La Huerta'),
    ('la_joyita','La Joyita'),
    ('la_libertad','La Libertad'),
    ('la_mojonera','La Mojonera'),
    ('la_viergen','La Virgen'),
    ('la_yesca','La Yesca'),
    ('la_zarcita','La Zarcita'),
    ('adelitas','Las Adelitas'),
    ('las_cabras','Las Cabras'),
    ('las_canoas','Las Canoas'),
    ('las_colonias','Las Colonias'),
    ('las_flores','Las Flores'),
    ('las_glorias','Las Glorias'),
    ('las_maravillas','Las Maravillas'),
    ('lazaro_cardenas','Lázaro Cárdenas'),
    ('lazaro_cardenas_jauja','Lázaro Cárdenas (Jauja)'),
    ('lazaro_cardenas_huerta','Lázado Cárndenas Sur (Huerta)'),
    ('leadro_valle','Leandro Valle'),
    ('libertadores_america','Libertadores de América'),
    ('llanos_buena_vista','Llanos de Buena Vista'),
    ('loma_alta','Loma Alta'),
    ('loma_linda','Loma Linda'),
    ('lomas_de_buena_vista','Lomas de de Buena Vista'),
    ('lomas_jardin','Lomas Jardín'),
    ('lomas_pocuaro','Lomas Pocuaro'),
    ('los_aguacates','Los Aguacates'),
    ('los_ajolotes','Los Ajolotes'),
    ('los_corrales','Los Corrales'),
    ('los_llanos','Los Llanos'),
    ('luis_donaldo_colocio','Luis Donaldo Colocio'),
    ('manantiales','Manantiales'),
    ('mexico','México'),
    ('miguel_angel','Miguel Angel'),
    ('miguel_hidalgo','Miguel Hidalgo'),
    ('moderna','Moderna'),
    ('morelia','Morelia'),
    ('morelos','Morelos'),
    ('mujica','Mujica'),
    ('naranja_de_tapia','Naranja de Tapia'),
    ('nueva_san_isidro','Nueva San Isidro'),
    ('nueva_tepeyac','Nueva Tepeyac'),
    ('obrera','Obrera'),
    ('parque_industrial','Parque Industrial'),
    ('progreso_nacional','Progreso Nacional'),
    ('pueblo_viejo','Pueblo Viejo (Jacarandas)'),
    ('puerta_chica','Puerta Chica'),
    ('quiroga','Quiroga'),
    ('rancho_alegre','Rancho Alegre'),
    ('rancho_caballeria','Rancho de Caballeria'),
    ('revolucion','Revolución'),
    ('rincon_las_tepecuas','Ricón de las Tepacuas'),
    ('rincon_quieto','Rincón Quieto'),
    ('rincon_san_miguel','Rincón de San Miguel'),
    ('san_antonio_pucuaro','San Antonio Pucuaro'),
    ('san_antonio_tariacuri','San Antonio Tariacuri'),
    ('san_francisco','San Francisco'),
    ('san_isidro','San Isidro'),
    ('san_jose','San José'),
    ('santa_gertrudis','Santa Gertrudis'),
    ('tacicuaro','Tacicuaro'),
    ('tarejero','Tarejero'),
    ('tepacuas','Tepacuas'),
    ('tierra_blancas','Tierras Blancas'),
    ('Tirindaro','Tiríndaro'),
    ('tlaquepaque_jalisco','Tlaquepaque, Jalisco'),
    ('tombero','Tombero'),
    ('tombero_1','Tombero 1'),
    ('tombero_2','Tombero 2'),
    ('tonala_jal','Tonala, Jalisco'),
    ('valle_zacapu_1','Valle de Zacapu 1'),
    ('valle_zacapu_2','Vallle de Zacapu 2'),
    ('valle_dorado','Valle Dorado'),
    ('valle_escondido','Valle Escondido'),
    ('valle_verde','Valle Verde'),
    ('villa_universidad','Villa Universidad'),
    ('vista_hermosa','Vista Hermosa'),
    ('wenceslao_victoria','Wenceslao Victoria'),
    ('zamora','Zamora'),

], key=lambda x: x[1].lower())


CONCEPTOS_CHOICES = sorted([
    ('economico','Económico'),
    ('salud','Salud'),
    ('ecológico','Ecológico'),
    ('servicios','Servicios'),
    ('combustible','Combustible'),
    ('educacion','Educación'),
    ('transporte','Transporte'),
    ('materiales','Materiales'),
    ('incentivo','Incentivo'),
    ('obra_publica','Obra Pública'),
    ('tramitologia','Tramitología'),
    ('otros','Otros'),

], key=lambda x: x[1].lower())





class Registro(models.Model):
    id = models.AutoField(primary_key=True, )
    numero_folio = models.IntegerField()
    depcon = models.CharField(max_length=100, null=True, blank=True)
    calcon = models.CharField(max_length=100, null=True, blank=True)
    sercon = models.CharField(max_length=100, null=True, blank=True)
    fecha_solicitud= models.DateField(null=True, blank=True)
    fecha_recibido = models.DateField(null=True, blank=True)
    columna1 = models.CharField(max_length=100, null=True, blank=True)
    departamento_a_canalizar= models.CharField(max_length=100, choices= DEPARTAMENTO_CHOICES, default='turismo')
    solicitante = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    colonia_o_comunidad= models.CharField(max_length=100, choices= COLONIAS_COMUNIDADES_CHOICES, default='zacapu')
    domicilio = models.CharField(max_length=100, null=True, blank=True)
    tipo_solicitud = models.CharField(max_length=100, choices= CONCEPTOS_CHOICES, default='Economico')
    fecha_atentida = models.DateField(null=True, blank=True)
    
    avance = models.CharField(max_length=20, choices=AVANCE_CHOICES, default='proceso')
   

    observaciones = models.CharField(max_length=100, null=True, blank=True)
    oficios = models.CharField(max_length=100, null=True, blank=True)
    columna3 = models.CharField(max_length=100, null=True, blank=True)
    columna4 = models.CharField(max_length=100, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null= True, blank= True, related_name='registros_creados')



    
    def __str__(self):
        return f"{self.numero_folio}"

    class Meta:
        db_table = 'datos_atencion'


