# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Appusers(models.Model):
    cname = models.OneToOneField('Contacts', models.DO_NOTHING, db_column='cName', primary_key=True)  # Field name made lowercase. The composite primary key (cName, aName) found, that is not supported. The first column is selected.
    aname = models.ForeignKey('Applications', models.DO_NOTHING, db_column='aName')  # Field name made lowercase.
    rating = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'AppUsers'
        unique_together = (('cname', 'aname'),)


class Applications(models.Model):
    aname = models.CharField(db_column='aName', primary_key=True, max_length=25)  # Field name made lowercase.
    acategory = models.CharField(db_column='aCategory', max_length=25, blank=True, null=True)  # Field name made lowercase.
    asize = models.IntegerField(db_column='aSize', blank=True, null=True)  # Field name made lowercase.
    isinstalled = models.BooleanField(db_column='isInstalled', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Applications'


class Contacts(models.Model):
    cname = models.CharField(db_column='cName', primary_key=True, max_length=50)  # Field name made lowercase.
    phone = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Contacts'


