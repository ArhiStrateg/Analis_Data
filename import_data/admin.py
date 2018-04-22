from django.contrib import admin
from import_data.models import EB_App, EB_Data_App, EF_App, EF_Orders, EF_Link_Data, EB_App_Ul, EB_Data_Link, EB_Place, EB_Session, \
    EB_Order, \
    New_EB_App_Ul, New_EB_Data_App, New_EB_Data_Link, New_EB_Place, New_EB_Session, New_EB_Order, New_EB_Sinhronisation, \
    Active_Hour, Active_Day, Day_of_the_week


class Inlines_EB_Order (admin.TabularInline):
    model = EB_Order
    extra = 0


class Inlines_EB_Session (admin.TabularInline):
    model = EB_Session
    extra = 0


class Inlines_EB_Place (admin.TabularInline):
    model = EB_Place
    extra = 0


class Inlines_EB_Data_Link (admin.TabularInline):
    model = EB_Data_Link
    extra = 0


class Inlines_EB_Data_App (admin.TabularInline):
    model = EB_Data_App
    extra = 0


class Inlines_EB_App_Ul (admin.TabularInline):
    model = EB_App_Ul
    extra = 0


class Inlines_Active_Hour (admin.TabularInline):
    model = Active_Hour
    extra = 0


class Inlines_Day_of_the_week (admin.TabularInline):
    model = Day_of_the_week
    extra = 0


class Inlines_New_EB_Sinhronisation (admin.TabularInline):
    model = New_EB_Sinhronisation
    extra = 0


class Inlines_New_EB_Order (admin.TabularInline):
    model = New_EB_Order
    extra = 0


class Inlines_New_EB_Session (admin.TabularInline):
    model = New_EB_Session
    extra = 0


class Inlines_New_EB_Place (admin.TabularInline):
    model = New_EB_Place
    extra = 0


class Inlines_New_EB_Data_Link (admin.TabularInline):
    model = New_EB_Data_Link
    extra = 0


class Inlines_New_EB_Data_App (admin.TabularInline):
    model = New_EB_Data_App
    extra = 0


class Inlines_New_EB_App_Ul (admin.TabularInline):
    model = New_EB_App_Ul
    extra = 0


class Admin_EF_App (admin.ModelAdmin):
    list_display = [field.name for field in EF_App._meta.fields]
    inlines = []

    class Meta:
        model = EF_App

admin.site.register(EF_App, Admin_EF_App)


class Admin_EF_Orders (admin.ModelAdmin):
    list_display = [field.name for field in EF_Orders._meta.fields]
    inlines = []

    class Meta:
        model = EF_Orders

admin.site.register(EF_Orders, Admin_EF_Orders)


class Admin_EF_Link_Data (admin.ModelAdmin):
    list_display = [field.name for field in EF_Link_Data._meta.fields]
    inlines = []

    class Meta:
        model = EF_Link_Data

admin.site.register(EF_Link_Data, Admin_EF_Link_Data)


class Admin_EB_App (admin.ModelAdmin):
    list_display = [field.name for field in EB_App._meta.fields]
    inlines = [Inlines_EB_Data_App, Inlines_EB_App_Ul, Inlines_EB_Data_Link, Inlines_New_EB_Data_App, Inlines_New_EB_App_Ul,
               Inlines_New_EB_Data_Link, Inlines_Active_Hour, Inlines_Day_of_the_week]

    class Meta:
        model = EB_App

admin.site.register(EB_App, Admin_EB_App)


class Admin_EB_App_Ul (admin.ModelAdmin):
    list_display = [field.name for field in EB_App_Ul._meta.fields]
    inlines = [Inlines_EB_Data_App, Inlines_EB_Data_Link]

    class Meta:
        model = EB_App_Ul

admin.site.register(EB_App_Ul, Admin_EB_App_Ul)


class Admin_EB_Data_App (admin.ModelAdmin):
    list_display = [field.name for field in EB_Data_App._meta.fields]
    inlines = []

    class Meta:
        model = EB_Data_App

admin.site.register(EB_Data_App, Admin_EB_Data_App)


class Admin_EB_Data_Link (admin.ModelAdmin):
    list_display = [field.name for field in EB_Data_Link._meta.fields]
    inlines = [Inlines_EB_Place, Inlines_EB_Session]

    class Meta:
        model = EB_Data_Link

admin.site.register(EB_Data_Link, Admin_EB_Data_Link)


class Admin_EB_Place (admin.ModelAdmin):
    list_display = [field.name for field in EB_Place._meta.fields]
    inlines = []

    class Meta:
        model = EB_Place

admin.site.register(EB_Place, Admin_EB_Place)


class Admin_EB_Session(admin.ModelAdmin):
    list_display = [field.name for field in EB_Session._meta.fields]
    inlines = [Inlines_EB_Order]

    class Meta:
        model = EB_Session

admin.site.register(EB_Session, Admin_EB_Session)


class Admin_EB_Order(admin.ModelAdmin):
    list_display = [field.name for field in EB_Order._meta.fields]
    inlines = [Inlines_New_EB_Sinhronisation]

    class Meta:
        model = EB_Order

admin.site.register(EB_Order, Admin_EB_Order)


class Admin_New_EB_App_Ul (admin.ModelAdmin):
    list_display = [field.name for field in New_EB_App_Ul._meta.fields]
    inlines = [Inlines_New_EB_Data_App, Inlines_New_EB_Data_Link]

    class Meta:
        model = New_EB_App_Ul

admin.site.register(New_EB_App_Ul, Admin_New_EB_App_Ul)


class Admin_New_EB_Data_App (admin.ModelAdmin):
    list_display = [field.name for field in New_EB_Data_App._meta.fields]
    inlines = [Inlines_New_EB_Order, Inlines_Active_Hour]

    class Meta:
        model = New_EB_Data_App

admin.site.register(New_EB_Data_App, Admin_New_EB_Data_App)


class Admin_New_EB_Data_Link (admin.ModelAdmin):
    list_display = [field.name for field in New_EB_Data_Link._meta.fields]
    inlines = [Inlines_New_EB_Place, Inlines_New_EB_Session]

    class Meta:
        model = New_EB_Data_Link

admin.site.register(New_EB_Data_Link, Admin_New_EB_Data_Link)


class Admin_New_EB_Place (admin.ModelAdmin):
    list_display = [field.name for field in New_EB_Place._meta.fields]
    inlines = []

    class Meta:
        model = New_EB_Place

admin.site.register(New_EB_Place, Admin_New_EB_Place)


class Admin_New_EB_Session(admin.ModelAdmin):
    list_display = [field.name for field in New_EB_Session._meta.fields]
    inlines = [Inlines_New_EB_Order]

    class Meta:
        model = New_EB_Session

admin.site.register(New_EB_Session, Admin_New_EB_Session)


class Admin_New_EB_Order(admin.ModelAdmin):
    list_display = [field.name for field in New_EB_Order._meta.fields]
    inlines = [Inlines_Active_Hour]

    class Meta:
        model = New_EB_Order

admin.site.register(New_EB_Order, Admin_New_EB_Order)


class Admin_New_EB_Sinhronisation(admin.ModelAdmin):
    list_display = [field.name for field in New_EB_Sinhronisation._meta.fields]
    inlines = []

    class Meta:
        model = New_EB_Sinhronisation

admin.site.register(New_EB_Sinhronisation, Admin_New_EB_Sinhronisation)


class Admin_Day_of_the_week(admin.ModelAdmin):
    list_display = [field.name for field in Day_of_the_week._meta.fields]
    inlines = [Inlines_Active_Hour]

    class Meta:
        model = Day_of_the_week

admin.site.register(Day_of_the_week, Admin_Day_of_the_week)


class Admin_Active_Day(admin.ModelAdmin):
    list_display = [field.name for field in Active_Day._meta.fields]
    inlines = [Inlines_Active_Hour]

    class Meta:
        model = Active_Day

admin.site.register(Active_Day, Admin_Active_Day)


class Admin_Active_Hour(admin.ModelAdmin):
    list_display = [field.name for field in Active_Hour._meta.fields]
    inlines = []

    class Meta:
        model = Active_Hour

admin.site.register(Active_Hour, Admin_Active_Hour)



