from Home import db

class devices(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text,nullable=False)
    sonoff_ip = db.Column(db.Text,nullable=False)
    sonoff_mac = db.Column(db.Text,nullable=False)

    def __repr__(self):
        return self.name

class device_state(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    logtime_year=db.Column(db.Integer,nullable=False)
    logtime_month=db.Column(db.Integer,nullable=False)
    logtime_date=db.Column(db.Integer,nullable=False)
    logtime_hour=db.Column(db.Integer,nullable=False)
    logtime_minute=db.Column(db.Integer,nullable=False)
    logtime_second=db.Column(db.Integer,nullable=False)
    devices_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    devices_name = db.Column(db.Text, db.ForeignKey('devices.name'), nullable=False)
    devices_sonoff_ip = db.Column(db.Text, db.ForeignKey('devices.sonoff_ip'), nullable=False)
    devices_sonoff_mac = db.Column(db.Text, db.ForeignKey('devices.sonoff_mac'), nullable=False)
    power_status = db.Column(db.Boolean,nullable=False)
    wifi_strength = db.Column(db.Float,nullable=False)
    vcc = db.Column(db.Float)


class energy_state(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    logtime_year=db.Column(db.Integer,nullable=False)
    logtime_month=db.Column(db.Integer,nullable=False)
    logtime_date=db.Column(db.Integer,nullable=False)
    logtime_hour=db.Column(db.Integer,nullable=False)
    logtime_minute=db.Column(db.Integer,nullable=False)
    logtime_second=db.Column(db.Integer,nullable=False)
    devices_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    devices_name = db.Column(db.Text, db.ForeignKey('devices.name'), nullable=False)
    devices_sonoff_ip = db.Column(db.Text, db.ForeignKey('devices.sonoff_ip'), nullable=False)
    devices_sonoff_mac = db.Column(db.Text, db.ForeignKey('devices.sonoff_mac'), nullable=False)
    period = db.Column(db.Integer)
    power = db.Column(db.Float,nullable=False)
    factor = db.Column(db.Float)
    voltage = db.Column(db.Float)
    current = db.Column(db.Float)
    kwh_sofar_today = db.Column(db.Float,nullable=False)
    kwh_yesterday = db.Column(db.Float,nullable=False)

class daily_summary(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    logtime_year=db.Column(db.Integer,nullable=False)
    logtime_month=db.Column(db.Integer,nullable=False)
    logtime_date=db.Column(db.Integer,nullable=False)
    devices_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    devices_name = db.Column(db.Text, db.ForeignKey('devices.name'), nullable=False)
    devices_sonoff_ip = db.Column(db.Text, db.ForeignKey('devices.sonoff_ip'), nullable=False)
    devices_sonoff_mac = db.Column(db.Text, db.ForeignKey('devices.sonoff_mac'), nullable=False)
    kwh_ontheday = db.Column(db.Float,nullable=False)
