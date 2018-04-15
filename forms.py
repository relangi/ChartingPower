from flask_wtf import Form
from wtforms.fields import StringField,IntegerField,PasswordField,SubmitField,BooleanField,SelectField
from wtforms.validators import DataRequired,Length,Regexp,EqualTo,ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import Models

class NewDevice(Form):
    name = StringField('name',validators=[DataRequired(),Regexp('^[A-Za-z0-9_\s]{3,}$',message='Device Name can contain numbers, characters and Underscore')])
    sonoff_ip = StringField('sonoff_ip', validators=[DataRequired(),Regexp('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',message='Enter a Valid IP address')])
    sonoff_mac = StringField('sonoff_mac',validators=[DataRequired(),Regexp('^([A-Fa-f0-9]{2,2}\:){5,5}[A-Fa-f0-9]{2,2}$',message='Enter a Valid MAC address')])


    def validate_sonoff_ip(self,sonoff_ip_field):
        if Models.devices.query.filter_by(sonoff_ip=sonoff_ip_field.data).first():
            raise ValidationError('There already is a device with this IP address')

    def validate_sonoff_mac(self,sonoff_mac_field):
        if Models.devices.query.filter_by(sonoff_mac=sonoff_mac_field.data).first():
            raise ValidationError('There already is a device with this MAC address')
