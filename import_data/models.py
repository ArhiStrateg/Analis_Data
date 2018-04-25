from django.db import models


class EF_App(models.Model):
    data_load = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='file_for_export_apps/', blank=True, null=True, default=None)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Файл для экспорта - Apps'
        verbose_name_plural = 'Файл для экспорта - Apps'


class EF_Orders(models.Model):
    data_load = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='file_for_export_orders/', blank=True, null=True, default=None)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Файл для экспорта - Orders'
        verbose_name_plural = 'Файл для экспорта - Orders'


class EF_Link_Data(models.Model):
    data_load = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='file_for_export_link_data/', blank=True, null=True, default=None)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Файл для экспорта - Link_Data'
        verbose_name_plural = 'Файл для экспорта - Link_Data'


class EB_App(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Экспортируемая база - App'
        verbose_name_plural = 'Экспортируемая база - App'


class EB_App_Ul(models.Model):
    local_key = models.ForeignKey(EB_App, blank=True, null=True, default=None, on_delete=models.CASCADE)
    app_id_unic = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Экспортируемая база - App_Unic_ID'
        verbose_name_plural = 'Экспортируемая база - App_Unic_ID'


class EB_Data_App(models.Model):
    local_key = models.ForeignKey(EB_App, blank=True, null=True, default=None, on_delete=models.CASCADE)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    app_id = models.ForeignKey(EB_App_Ul, blank=True, null=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Экспортируемая база - Data_App'
        verbose_name_plural = 'Экспортируемая база - Data_App'


class EB_Data_Link(models.Model):
    app_name = models.ForeignKey(EB_App, blank=True, null=True, default=None, on_delete=models.CASCADE)
    app_id = models.ForeignKey(EB_App_Ul, blank=True, null=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Экспортируемая база - Data_Link'
        verbose_name_plural = 'Экспортируемая база - Data_Link'


class EB_Place(models.Model):
    local_key = models.ForeignKey(EB_Data_Link, blank=True, null=True, default=None, on_delete=models.CASCADE)
    place_id = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Экспортируемая база - Place'
        verbose_name_plural = 'Экспортируемая база - Place'


class EB_Session(models.Model):
    local_key = models.ForeignKey(EB_Data_Link, blank=True, null=True, default=None, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Экспортируемая база - Session'
        verbose_name_plural = 'Экспортируемая база - Session'


class EB_Order(models.Model):
    order_id_unic = models.CharField(max_length=128, blank=True, null=True)
    revenue = models.IntegerField(default=0)
    session_key = models.ForeignKey(EB_Session, blank=True, null=True, default=None, on_delete=models.CASCADE)
    time_create = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Экспортируемая база - Order'
        verbose_name_plural = 'Экспортируемая база - Order'


class New_EB_App_Ul(models.Model):
    local_key = models.ForeignKey(EB_App, blank=True, null=True, default=None, on_delete=models.CASCADE)
    app_id_unic = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Обработанная база - App_Unic_ID'
        verbose_name_plural = 'Обработанная база - App_Unic_ID'


class New_EB_Data_App(models.Model):
    local_key = models.ForeignKey(EB_App, blank=True, null=True, default=None, on_delete=models.CASCADE)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    app_id = models.ForeignKey(New_EB_App_Ul, blank=True, null=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Обработанная база - Data_App'
        verbose_name_plural = 'Обработанная база - Data_App'


class New_EB_Data_Link(models.Model):
    app_name = models.ForeignKey(EB_App, blank=True, null=True, default=None, on_delete=models.CASCADE)
    app_id = models.ForeignKey(New_EB_App_Ul, blank=True, null=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Обработанная база - Data_Link'
        verbose_name_plural = 'Обработанная база - Data_Link'


class New_EB_Place(models.Model):
    local_key = models.ForeignKey(New_EB_Data_Link, blank=True, null=True, default=None, on_delete=models.CASCADE)
    place_id = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Обработанная база - Place'
        verbose_name_plural = 'Обработанная база - Place'


class New_EB_Session(models.Model):
    local_key = models.ForeignKey(New_EB_Data_Link, blank=True, null=True, default=None, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Обработанная база - Session'
        verbose_name_plural = 'Обработанная база - Session'


class New_EB_Order(models.Model):
    order_id_unic = models.CharField(max_length=128, blank=True, null=True)
    revenue = models.IntegerField(default=0)
    session_key = models.ForeignKey(New_EB_Session, blank=True, null=True, default=None, on_delete=models.CASCADE)
    time_create = models.DateTimeField(blank=True, null=True)
    key_for_data = models.ForeignKey(New_EB_Data_App, blank=True, null=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Обработанная база - Order'
        verbose_name_plural = 'Обработанная база - Order'


class New_EB_Sinhronisation(models.Model):
    order_id_unic = models.CharField(max_length=128, blank=True, null=True)
    old_order = models.ForeignKey(EB_Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    sinhronis_ok = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Обработанная база - Sinhronisation'
        verbose_name_plural = 'Обработанная база - Sinhronisation'

class Day_of_the_week(models.Model):
    day_of_the_week = models.CharField(max_length=20, blank=True, null=True)
    app = models.ForeignKey(EB_App, blank=True, null=True, default=None, on_delete=models.CASCADE)
    med_speed = models.FloatField(default=0)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Анализ - дни недели'
        verbose_name_plural = 'Анализ - дни недели'


class Active_Day(models.Model):
    day = models.IntegerField(default=0)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Анализ - активные дни'
        verbose_name_plural = 'Анализ - активные дни'


class Active_Hour(models.Model):
    app = models.ForeignKey(EB_App, blank=True, null=True, default=None, on_delete=models.CASCADE)
    order = models.ForeignKey(New_EB_Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    app_data = models.ForeignKey(New_EB_Data_App, blank=True, null=True, default=None, on_delete=models.CASCADE)
    active_hour = models.IntegerField(default=0)
    active_day = models.ForeignKey(Active_Day, blank=True, null=True, default=None, on_delete=models.CASCADE)
    day_of_the_week = models.ForeignKey(Day_of_the_week, blank=True, null=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Анализ - активные часы'
        verbose_name_plural = 'Анализ - активные часы'


class Resume_Day_Week_Win(models.Model):
    app = models.ForeignKey(EB_App, blank=True, null=True, default=None, on_delete=models.CASCADE)
    Monday_day = models.BooleanField(default=False)
    Tuesday_day = models.BooleanField(default=False)
    Wednesday_day = models.BooleanField(default=False)
    Thursday_day = models.BooleanField(default=False)
    Friday_day = models.BooleanField(default=False)
    Saturday_day = models.BooleanField(default=False)
    Sunday_day = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Резюме - дни недели (Максимальные)'
        verbose_name_plural = 'Резюме - дни недели (Максимальные)'


class Resume_Hour_Win(models.Model):
    app = models.ForeignKey(EB_App, blank=True, null=True, default=None, on_delete=models.CASCADE)
    day = models.ForeignKey(Resume_Day_Week_Win, blank=True, null=True, default=None, on_delete=models.CASCADE)
    hour_start = models.IntegerField(default=0)
    hour_end = models.IntegerField(default=0)
    sum = models.IntegerField(default=0)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Резюме - активные часы (Максимальные)'
        verbose_name_plural = 'Резюме - активные часы (Максимальные)'


class Resume_Day_Week_Dont_Win(models.Model):
    app = models.ForeignKey(EB_App, blank=True, null=True, default=None, on_delete=models.CASCADE)
    Monday_day = models.BooleanField(default=False)
    Tuesday_day = models.BooleanField(default=False)
    Tuesday_day = models.BooleanField(default=False)
    Wednesday_day = models.BooleanField(default=False)
    Thursday_day = models.BooleanField(default=False)
    Friday_day = models.BooleanField(default=False)
    Saturday_day = models.BooleanField(default=False)
    Sunday_day = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Резюме - дни недели (Не максимальные)'
        verbose_name_plural = 'Резюме - дни недели (Не максимальные)'


class Resume_Hour_Dont_Win(models.Model):
    app = models.ForeignKey(EB_App, blank=True, null=True, default=None, on_delete=models.CASCADE)
    day = models.ForeignKey(Resume_Day_Week_Dont_Win, blank=True, null=True, default=None, on_delete=models.CASCADE)
    hour_start = models.IntegerField(default=0)
    hour_end = models.IntegerField(default=0)
    sum = models.IntegerField(default=0)


    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Резюме - активные часы (Не максимальные)'
        verbose_name_plural = 'Резюме - активные часы (Не максимальные)'



