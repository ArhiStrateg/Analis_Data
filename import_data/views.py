from django.shortcuts import render, redirect
from import_data.models import EF_App, EF_Orders, EF_Link_Data, EB_App, EB_Data_App, EB_App_Ul, EB_Data_Link, EB_Place, EB_Session,\
    EB_Order, \
    New_EB_App_Ul, New_EB_Data_App, New_EB_Data_Link, New_EB_Place, New_EB_Session, New_EB_Order, New_EB_Sinhronisation, \
    Active_Hour, Active_Day, Day_of_the_week, \
    Resume_Day_Week_Win, Resume_Hour_Win, \
    Resume_Day_Week_Dont_Win, Resume_Hour_Dont_Win


import datetime as dt
from datetime import datetime, date, time
import dateutil.parser
import calendar


def main(request):
    return render(request, 'import_data/main.html', locals())


def import_data_prime(request):

    all_file_apps = EF_App.objects.filter()
    all_file_orders = EF_Orders.objects.filter()
    all_file_link_data = EF_Link_Data.objects.filter()

    form_button = request.POST
    form_file = request.FILES

    if "export_apps" in form_button:
        file = form_file["file_for_export"]
        EF_App.objects.create(file=file)

    if "export_apps_file_in_BD" in form_button:
        id_for_file = form_button["file_for_load_in_BD"]
        query_file = EF_App.objects.get(id=int(id_for_file))
        i_file = str(query_file.file)
        i_file = "media/" + i_file

        # Del all elements in BD (Apps) - Begin
        all_elem_for_del = EB_App.objects.filter()
        all_elem_for_del.delete()
        # Del all elements in BD (Apps) - End

        file = open(i_file, 'r')
        list_result = list()
        # Create list all element in file - Begin
        for fil in file:
            list_for_fil = fil.split(",")
            list_pre_result = list()
            for in_list_for_fil in list_for_fil:
                pre = in_list_for_fil.replace('"', "")
                pre = pre.replace('\n', "")
                if "AppId" not in pre and "StartTime" not in pre and "EndTime" not in pre and "Id" not in pre:
                    list_pre_result.append(pre)
                    # input()
            if list_pre_result != []:
                list_result.append(list_pre_result)
        # Create list all element in file - End

        # Del all elementsin BD (Apps) - Begin
        all_elem_for_del = EB_App.objects.filter()
        all_elem_for_del.delete()
        # Del all elementsin BD (Apps) - End

        # Save App name - Begin
        for in_list_result in list_result:
            app_name = in_list_result[0]
            all_apps = EB_App.objects.filter()
            list_all_apps = list()
            for all_app in all_apps:
                list_all_apps.append(all_app.name)
            if app_name not in list_all_apps:
                EB_App.objects.create(name=str(app_name))
        # Save App name - End

        # Del all elements in BD (Apps) - Begin
        all_elem_for_del = EB_Data_App.objects.filter()
        all_elem_for_del.delete()
        all_elem_for_del = EB_App_Ul.objects.filter()
        all_elem_for_del.delete()
        # Del all elements in BD (Apps) - End

        # Save App_Data - Begin
        for in_list_result in list_result:
            name_appic = in_list_result[0]
            start_time = in_list_result[1]
            end_time = in_list_result[2]
            app_id = in_list_result[3]
            query_set_apps = EB_App.objects.filter(name=name_appic)
            for query_set_app in query_set_apps:
                break
            start_time = dateutil.parser.parse(start_time)
            end_time = dateutil.parser.parse(end_time)
            create_unic_id_app = EB_App_Ul.objects.create(local_key=query_set_app, app_id_unic=app_id)
            result_save_data_app = EB_Data_App.objects.create(local_key=query_set_app, start_time=start_time, end_time=end_time, app_id=create_unic_id_app)
        # Save App_Data - End
        file.close()

    if "export_orders" in form_button:
        file = form_file["file_for_export"]
        EF_Orders.objects.create(file=file)

    if "export_orders_file_in_BD" in form_button:
        id_for_file = form_button["file_for_load_in_BD"]
        query_file = EF_Orders.objects.get(id=int(id_for_file))
        i_file = str(query_file.file)
        i_file = "media/" + i_file

        # Del all elements in BD (EB_Data_Link) - Begin
        all_elem_for_del = EB_Order.objects.filter()
        all_elem_for_del.delete()
        # Del all elements in BD (EB_Data_Link) - End

        str_work = 0

        all_eb_sessions = EB_Session.objects.filter()
        list_all_session = list()
        for all_eb_session in all_eb_sessions:
            list_all_session.append(str(all_eb_session.session_id))

        file = open(i_file, 'r')

        for fil in file:
            list_for_fil = fil.split(",")
            list_pre_result = list()
            for in_list_for_fil in list_for_fil:
                pre = in_list_for_fil.replace('"', "")
                pre = pre.replace('\n', "")
                if "OrderId" not in pre and "Revenue" not in pre and "SessionId" not in pre and "Time" not in pre:
                    if pre != []:
                        list_pre_result.append(pre)

            if list_pre_result != []:
                order_id_unic = list_pre_result[0]

                revenue_str = list_pre_result[1]
                index_start = int(revenue_str.index("."))
                index_end = int(len(revenue_str))
                index_end = index_end
                srez = revenue_str[index_start:index_end]
                revenue = revenue_str.replace(srez, "")
                revenue = int(revenue)

                session_key = list_pre_result[2]

                time_create_str = list_pre_result[3]
                time_create_str = time_create_str + "+00:00"
                time_create = dateutil.parser.parse(time_create_str)
                # time_create = datetime.isoformat(time_create)

                if session_key in list_all_session:
                    eb_sessions = EB_Session.objects.filter(session_id=session_key)
                    for eb_session in eb_sessions:
                        break
                    order = EB_Order.objects.create(order_id_unic=order_id_unic, revenue=revenue, session_key=eb_session,
                                            time_create=time_create)
                    app_data_searchs = EB_Data_App.objects.filter(app_id__app_id_unic=order.session_key.local_key.app_id.app_id_unic)
                    for app_data_search in app_data_searchs:
                        break
                    str_work = str_work + 1
        file.close()

    if "export_link_data" in form_button:
        file = form_file["file_for_export"]
        EF_Link_Data.objects.create(file=file)

    if "export_link_data_file_in_BD" in form_button:
        id_for_file = form_button["file_for_load_in_BD"]
        query_file = EF_Link_Data.objects.get(id=int(id_for_file))
        i_file = str(query_file.file)
        i_file = "media/" + i_file

        # Del all elements in BD (EB_Data_Link) - Begin
        all_elem_for_del = EB_Data_Link.objects.filter()
        all_elem_for_del.delete()
        # Del all elements in BD (EB_Data_Link) - End
        # Del all elements in BD (EB_Place) - Begin
        all_elem_for_del = EB_Place.objects.filter()
        all_elem_for_del.delete()
        # Del all elements in BD (EB_Place) - End
        # Del all elements in BD (EB_Session) - Begin
        all_elem_for_del = EB_Session.objects.filter()
        all_elem_for_del.delete()
        # Del all elements in BD (EB_Session) - End

        num_save_data_link = 0
        num_str = 0
        eb_app_uis = EB_App_Ul.objects.filter()
        list_eb_app_uis = list()
        for eb_app_uir in eb_app_uis:
            id_str = str(eb_app_uir.app_id_unic)
            list_eb_app_uis.append(id_str)

        file = open(i_file, 'r')
        for fil in file:
            list_for_fil = fil.split(",")
            list_pre_result = list()
            for in_list_for_fil in list_for_fil:
                pre = in_list_for_fil.replace('"', "")
                pre = pre.replace('\n', "")
                if "ApplicationID" not in pre and "SessionID" not in pre and "PlaceID" not in pre and "ApplicationName" not in pre:
                    if pre != []:
                        list_pre_result.append(pre)

            if list_pre_result != []:

                app_id_unic = list_pre_result[0]
                app_id_unic = app_id_unic.lower()
                session_id = list_pre_result[1]
                session_id = session_id.lower()
                place_id = list_pre_result[2]
                name = list_pre_result[3]

                num_str = num_str + 1

                if app_id_unic in list_eb_app_uis:
                    eb_apps = EB_App.objects.filter(name=name)
                    for eb_app in eb_apps:
                        break
                    eb_app_uis = EB_App_Ul.objects.filter(app_id_unic=app_id_unic)
                    for eb_app_ui in eb_app_uis:
                        break
                    create_eb_data_link = EB_Data_Link.objects.create(app_name=eb_app, app_id=eb_app_ui)
                    EB_Place.objects.create(local_key=create_eb_data_link, place_id=place_id)
                    EB_Session.objects.create(local_key=create_eb_data_link, session_id=session_id)
                    num_save_data_link = num_save_data_link + 1
        file.close()

    if "cleen_EB_Session" in form_button:
        all_session_key_in_eb_orders = EB_Order.objects.filter()
        list_for_save = list()
        for all_session_key_in_eb_order in all_session_key_in_eb_orders:
            id_for_save = all_session_key_in_eb_order.session_key.id
            if id_for_save not in list_for_save:
                list_for_save.append(id_for_save)
        num_del = 0
        num_save = 0
        all_elements_eb_session = EB_Session.objects.filter()
        for element_eb_session in all_elements_eb_session:
            if element_eb_session.id not in list_for_save:
                element_eb_session.delete()
                num_del = num_del + 1
            else:
                num_save = num_save + 1

    if "cleen_EB_Data_Link" in form_button:
        all_elements_in_eb_session = EB_Session.objects.filter()
        list_for_save_main = list()
        for element in all_elements_in_eb_session:
            id_for_save = element.local_key.id
            if id_for_save not in list_for_save_main:
                list_for_save_main.append(id_for_save)

        num_del = 0
        list_for_del = list()
        num_save = 0
        list_for_save = list()

        all_elements_eb_data_link = EB_Data_Link.objects.filter()
        for element in all_elements_eb_data_link:
            if element.id not in list_for_save_main:
                list_for_del.append(element.id)
                num_del = num_del + 1
            else:
                list_for_save.append(element.id)
                num_save = num_save + 1

        for element in list_for_del:
            EB_Data_Link.objects.filter(id=element).delete()

        num_del = 0
        list_for_del = list()
        num_save = 0
        list_for_save = list()

        all_elements_eb_place = EB_Place.objects.filter()
        for element in all_elements_eb_place:
            if element.local_key.id not in list_for_save_main:
                num_del = num_del + 1
                list_for_del.append(element.id)
            else:
                num_save = num_save + 1
                list_for_save.append(element.id)

        for element in list_for_del:
            EB_Place.objects.filter(id=element).delete()

    if "cleen_EB_App_Ul" in form_button:
        all_elements_in_eb_order = EB_Order.objects.filter()
        list_for_save_main = list()
        for element in all_elements_in_eb_order:
            id_for_save = element.session_key.local_key.app_id.id
            if id_for_save not in list_for_save_main:
                list_for_save_main.append(id_for_save)
        num_del = 0
        list_for_del = list()
        num_save = 0
        list_for_save = list()
        all_elements_in_eb_app_ui = EB_App_Ul.objects.filter()
        for element in all_elements_in_eb_app_ui:
            if element.id not in list_for_save_main:
                num_del = num_del + 1
                list_for_del.append(element.id)
            else:
                num_save = num_save + 1
                list_for_save.append(element.id)

        for element in list_for_del:
            EB_App_Ul.objects.filter(id=element).delete()

    if "create_new_bd_xx_00" in form_button:
        # del all elements in new DB (BEGIN)
        New_EB_App_Ul.objects.filter().delete()
        # del all elements in new DB (END)

        all_orders = EB_Order.objects.filter()
        for element in all_orders:
            id_eb_app_ui = element.session_key.local_key.app_id.id
            el_datas_app = EB_Data_App.objects.filter(app_id__id=id_eb_app_ui)
            for el in el_datas_app:
                break
            start_time = el.start_time
            end_time = el.end_time

            str_start_time = str(start_time)
            position_ss_hour = int(str_start_time.index(" "))
            position_se_hour = position_ss_hour + 3
            srez_s = str_start_time[int(position_ss_hour): int(position_se_hour)]

            str_end_time = str(end_time)
            position_es_hour = int(str_end_time.index(" "))
            position_ee_hour = position_es_hour + 3
            srez_e = str_end_time[position_es_hour: position_ee_hour]

            int_start = int(srez_s)
            int_end = int(srez_e)

            list_hours = list()

            if int_start != int_end:
                prom_hour = int_start
                list_hours.append(prom_hour)
                while prom_hour < int_end:
                    prom_hour = prom_hour + 1
                    list_hours.append(prom_hour)

                if len(list_hours) == 2:
                    hr_str = list_hours[0]
                    hr_end = list_hours[1]

                    position_hr_beg = int(str_start_time.index(" ")) + 1
                    position_hr_end = position_hr_beg + 2
                    all_len_time = len(str_start_time)
                    srez_1 = str_start_time[0:position_hr_beg]
                    srez_2 = str(hr_end)
                    srez_3 = ":00:00.000000+00:00"
                    str_start_time_end = srez_1 + srez_2 + srez_3

                    for_app_id_unic = element.session_key.local_key.app_id.app_id_unic
                    for_local_key = element.session_key.local_key.app_id.local_key
                    for_new_eb_data_app_1 = New_EB_App_Ul.objects.create(local_key=for_local_key, app_id_unic=for_app_id_unic)
                    for_new_eb_data_app_2 = New_EB_App_Ul.objects.create(local_key=for_local_key, app_id_unic=for_app_id_unic)

                    for_local_key = element.session_key.local_key.app_id.local_key
                    id_for_save_new_eb_app_ui = element.session_key.local_key.app_id.id
                    for_save = EB_Data_App.objects.filter(app_id__id=id_for_save_new_eb_app_ui)
                    for for_save_in in for_save:
                        break
                    start_time_in_1 = dateutil.parser.parse(str_start_time)
                    end_time_in_1 = dateutil.parser.parse(str_start_time_end)
                    end_end_time_in = dateutil.parser.parse(str_end_time)
                    New_EB_Data_App.objects.create(local_key=for_local_key, start_time=start_time_in_1, end_time=end_time_in_1, app_id=for_new_eb_data_app_1)
                    New_EB_Data_App.objects.create(local_key=for_local_key, start_time=end_time_in_1, end_time=end_end_time_in, app_id=for_new_eb_data_app_2)

                    for_new_eb_place_1 = New_EB_Data_Link.objects.create(app_name=for_local_key, app_id=for_new_eb_data_app_1)
                    for_new_eb_place_2 = New_EB_Data_Link.objects.create(app_name=for_local_key, app_id=for_new_eb_data_app_2)

                    id_for_place = element.session_key.local_key.id
                    places = EB_Place.objects.filter(local_key__id=id_for_place)
                    for place in places:
                        break
                    place_id = place.place_id
                    New_EB_Place.objects.create(local_key=for_new_eb_place_1, place_id=place_id)
                    New_EB_Place.objects.create(local_key=for_new_eb_place_2, place_id=place_id)

                    session_id = element.session_key.session_id
                    for_new_eb_order_1 = New_EB_Session.objects.create(local_key=for_new_eb_place_1, session_id=session_id)
                    for_new_eb_order_2 = New_EB_Session.objects.create(local_key=for_new_eb_place_2, session_id=session_id)

                    order_id_unic = element.order_id_unic
                    revenue = element.revenue
                    time_create = element.time_create

                    time_sec_1 = datetime.timestamp(start_time_in_1)
                    time_sec_2 = datetime.timestamp(end_time_in_1)
                    time_sec_3 = datetime.timestamp(end_end_time_in)
                    delta_time = time_sec_3 - time_sec_1
                    delta_time_zero = time_sec_2 - time_sec_1
                    delta_x = delta_time_zero / delta_time
                    revenue_1 = round(delta_x * int(revenue))
                    revenue_2 = int(revenue) - revenue_1

                    New_EB_Order.objects.create(order_id_unic=order_id_unic, revenue=revenue_1, time_create=time_create, session_key=for_new_eb_order_1)
                    New_EB_Order.objects.create(order_id_unic=order_id_unic, revenue=revenue_2, time_create=time_create, session_key=for_new_eb_order_2)

                if len(list_hours) > 2:
                    len_list_hours = len(list_hours)
                    all_list_for_save = list()
                    for elem in list_hours:
                        if elem == list_hours[0]:
                            hr_str = list_hours[0]
                            hr_end = list_hours[1]
                            position_hr_beg = int(str_start_time.index(" ")) + 1
                            position_hr_end = position_hr_beg + 2
                            all_len_time = len(str_start_time)
                            srez_1 = str_start_time[0:position_hr_beg]
                            srez_2 = str(hr_end)
                            srez_3 = ":00:00.000000+00:00"
                            str_start_time_end = srez_1 + srez_2 + srez_3
                            dict_for_list_hours = dict(start=str_start_time, end=str_start_time_end)

                        if elem == list_hours[len_list_hours - 1]:
                            hr_str = list_hours[len_list_hours - 2]
                            hr_end = list_hours[len_list_hours - 1]
                            position_hr_beg = int(str_start_time.index(" ")) + 1
                            position_hr_end = position_hr_beg + 2
                            all_len_time = len(str_start_time)
                            srez_1 = str_start_time[0:position_hr_beg]
                            srez_2 = str(hr_end)
                            srez_3 = ":00:00.000000+00:00"
                            str_start_time_end = srez_1 + srez_2 + srez_3
                            dict_for_list_hours = dict(start=str_start_time_end, end=str_end_time)

                        if elem != list_hours[len_list_hours - 1] and int(elem) != int(list_hours[0]):
                            hr_str = elem
                            position_elem = list_hours.index(elem)
                            hr_end = list_hours[position_elem + 1]
                            position_hr_beg = int(str_start_time.index(" ")) + 1
                            position_hr_end = position_hr_beg + 2
                            all_len_time = len(str_start_time)
                            srez_1 = str_start_time[0:position_hr_beg]
                            srez_2 = str(hr_str)
                            srez_3 = ":00:00.000000+00:00"
                            str_start_time_end = srez_1 + srez_2 + srez_3
                            srez_2 = str(hr_end)
                            str_end_time_end = srez_1 + srez_2 + srez_3
                            dict_for_list_hours = dict(start=str_start_time_end, end=str_end_time_end)

                        all_list_for_save.append(dict_for_list_hours)
                    len_list_for_save = len(all_list_for_save)
                    list_for_rev = list()
                    summ_delta = 0
                    for elm_for_save in all_list_for_save:

                        for_app_id_unic = element.session_key.local_key.app_id.app_id_unic
                        for_local_key = element.session_key.local_key.app_id.local_key
                        for_new_eb_data_app = New_EB_App_Ul.objects.create(local_key=for_local_key, app_id_unic=for_app_id_unic)

                        for_local_key = element.session_key.local_key.app_id.local_key
                        id_for_save_new_eb_app_ui = element.session_key.local_key.app_id.id
                        for_save = EB_Data_App.objects.filter(app_id__id=id_for_save_new_eb_app_ui)
                        for for_save_in in for_save:
                            break
                        start_time_in = elm_for_save["start"]
                        start_time_in = dateutil.parser.parse(start_time_in)
                        end_time_in = elm_for_save["end"]
                        end_time_in = dateutil.parser.parse(end_time_in)
                        New_EB_Data_App.objects.create(local_key=for_local_key, start_time=start_time_in, end_time=end_time_in, app_id=for_new_eb_data_app)

                        for_new_eb_place = New_EB_Data_Link.objects.create(app_name=for_local_key, app_id=for_new_eb_data_app)

                        id_for_place = element.session_key.local_key.id
                        places = EB_Place.objects.filter(local_key__id=id_for_place)
                        for place in places:
                            break
                        place_id = place.place_id
                        New_EB_Place.objects.create(local_key=for_new_eb_place, place_id=place_id)

                        session_id = element.session_key.session_id
                        for_new_eb_order = New_EB_Session.objects.create(local_key=for_new_eb_place, session_id=session_id)

                        order_id_unic = element.order_id_unic
                        revenue = element.revenue
                        time_create = element.time_create
                        query = New_EB_Order.objects.create(order_id_unic=order_id_unic, time_create=time_create, session_key=for_new_eb_order)

                        delta_1 = datetime.timestamp(start_time_in)
                        delta_2 = datetime.timestamp(end_time_in)
                        delta = delta_2 - delta_1
                        dict_for_sum = dict(query=query, delta=delta)
                        list_for_rev.append(dict_for_sum)
                        summ_delta = summ_delta + delta

                    revenue = element.revenue
                    sum_re = 0
                    num_pos = 0
                    len_list_rev = len(list_for_rev)
                    for for_rev in list_for_rev:
                        delta_r = for_rev["delta"]

                        delta_x = delta_r / summ_delta
                        revenue_for_s = round(delta_x * int(revenue))
                        sum_re = sum_re + revenue_for_s
                        num_pos = num_pos + 1
                        if num_pos == len_list_rev:
                            revenue_for_s = revenue - sum_re

                        query_for_save_in_result = for_rev["query"]
                        id_for_save = query_for_save_in_result.id
                        New_EB_Order.objects.filter(id=id_for_save).update(revenue=int(revenue_for_s))

            if list_hours == []:
                for_app_id_unic = element.session_key.local_key.app_id.app_id_unic
                for_local_key = element.session_key.local_key.app_id.local_key
                for_new_eb_data_app = New_EB_App_Ul.objects.create(local_key=for_local_key, app_id_unic=for_app_id_unic)

                for_local_key = element.session_key.local_key.app_id.local_key
                id_for_save_new_eb_app_ui = element.session_key.local_key.app_id.id
                for_save = EB_Data_App.objects.filter(app_id__id=id_for_save_new_eb_app_ui)
                for for_save_in in for_save:
                    break
                start_time_in = for_save_in.start_time
                end_time_in = for_save_in.end_time
                New_EB_Data_App.objects.create(local_key=for_local_key, start_time=start_time_in, end_time=end_time_in, app_id=for_new_eb_data_app)

                for_new_eb_place = New_EB_Data_Link.objects.create(app_name=for_local_key, app_id=for_new_eb_data_app)

                id_for_place = element.session_key.local_key.id
                places = EB_Place.objects.filter(local_key__id=id_for_place)
                for place in places:
                    break
                place_id = place.place_id
                New_EB_Place.objects.create(local_key=for_new_eb_place, place_id=place_id)

                session_id = element.session_key.session_id
                for_new_eb_order = New_EB_Session.objects.create(local_key=for_new_eb_place, session_id=session_id)

                order_id_unic = element.order_id_unic
                revenue = element.revenue
                time_create = element.time_create
                New_EB_Order.objects.create(order_id_unic=order_id_unic, revenue=revenue, time_create=time_create, session_key=for_new_eb_order)

    if "load_key" in form_button:
        all_new_orders = New_EB_Order.objects.filter()
        for order in all_new_orders:
            id_order = order.id
            id_app_id = order.session_key.local_key.app_id.id
            all = New_EB_Data_App.objects.filter(app_id__id=id_app_id)
            for one in all:
                break
            New_EB_Order.objects.filter(id=id_order).update(key_for_data=one)

    if "rep_db" in form_button:
        # del all elements in new DB (BEGIN)
        New_EB_Sinhronisation.objects.filter().delete()
        # del all elements in new DB (END)

        all_orders_old = EB_Order.objects.filter()
        all_orders_new = New_EB_Order.objects.filter()
        for order in all_orders_old:
            cont_sum_1 = order.revenue
            order_id_unic = order.order_id_unic
            new_orders_for_sin = New_EB_Order.objects.filter(order_id_unic=order_id_unic)
            cont_sum_2 = 0
            for new_order in new_orders_for_sin:
                cont_sum_2 = new_order.revenue + cont_sum_2

            if cont_sum_2 == cont_sum_1:
                New_EB_Sinhronisation.objects.create(old_order=order, sinhronis_ok=True, order_id_unic=order.order_id_unic)
            else:
                New_EB_Sinhronisation.objects.create(old_order=order, sinhronis_ok=False, order_id_unic=order.order_id_unic)

    if "sinhronisation_db" in form_button:
        all_sinh_false = New_EB_Sinhronisation.objects.filter(sinhronis_ok=False)

        for elem in all_sinh_false:
            old_order = elem.old_order
            order_id_unic = elem.order_id_unic
            revenue = old_order.revenue

            orders_false_new = New_EB_Order.objects.filter(order_id_unic=order_id_unic)
            list_for_find_new = list()
            for order_new in orders_false_new:
                id_orders_false_new = order_new.id
                start_time = order_new.key_for_data.start_time
                end_time = order_new.key_for_data.end_time
                list_for_find_new.append(dict(id=id_orders_false_new, time_start=start_time, time_end=end_time))

            if len(list_for_find_new) > 0:
                summ = 0
                num = 0
                len_list = len(list_for_find_new)
                for isprav in list_for_find_new:
                    num = num + 1
                    id = isprav["id"]
                    order = New_EB_Order.objects.get(id=id)
                    order_rev = order.revenue
                    if num != len_list:
                        summ = summ + order_rev
                end_rev = revenue - summ
                for_save = list_for_find_new[len_list-1]
                id_for_save = for_save["id"]
                save_in = New_EB_Order.objects.filter(id=id_for_save).update(revenue=end_rev)

                for_re_provs = New_EB_Order.objects.filter(order_id_unic=order_id_unic)
                itog_summ = 0
                for el in for_re_provs:
                    itog_summ = itog_summ + el.revenue
                if itog_summ == revenue:
                    New_EB_Sinhronisation.objects.filter(id=elem.id).update(sinhronis_ok=True)
            else:
                id = elem.old_order.session_key.local_key.app_id.id
                doors = EB_Data_App.objects.filter(app_id__id=id)
                for door in doors:
                    break
                sre_start_time = str(door.start_time)
                sre_end_time = str(door.end_time)

                len_for_prob = len(sre_start_time)
                index_prob = sre_start_time.index(" ") + 1
                srez = sre_start_time[index_prob:len_for_prob]
                hour_start = srez[0:2]
                hour_start = int(hour_start)
                list_hour = list()
                while hour_start < 24:
                    hour_start = hour_start + 1
                    list_hour.append(hour_start)

                len_list = len(list_hour)
                num_for_create = 0
                end_iter_create = len_list + 1
                list_ho = list()
                while num_for_create != end_iter_create:
                    num_for_create = num_for_create + 1

                    if num_for_create == 1:
                        srez_1 = sre_start_time[0:11]
                        srez_2 = str(list_hour[0])
                        if srez_2 == str(24):
                            srez_1 = sre_end_time[0:11]
                            srez_2 = "00"
                        srez_3 = ":00:00.000000+00:00"
                        srez = srez_1 + srez_2 + srez_3

                        sor_start_time_end = dateutil.parser.parse(sre_start_time)
                        sor_end_time_end = dateutil.parser.parse(srez)
                        dict_for_list_hours = dict(start=sor_start_time_end, end=sor_end_time_end)
                        list_ho.append(dict_for_list_hours)

                    if num_for_create == end_iter_create:
                        srez_1 = sre_end_time[0:11]
                        srez_2 = "00:00:00.000000+00:00"
                        srez = srez_1 + srez_2

                        sor_start_time_end = dateutil.parser.parse(srez)
                        sor_end_time_end = dateutil.parser.parse(sre_end_time)
                        dict_for_list_hours = dict(start=sor_start_time_end, end=sor_end_time_end)
                        list_ho.append(dict_for_list_hours)

                    if num_for_create != end_iter_create and num_for_create != 1:
                        position_for_in = num_for_create - 2
                        hour_st = list_hour[position_for_in]
                        hour_st = str(hour_st)
                        hour_end = list_hour[position_for_in + 1]
                        hour_end = str(hour_end)

                        srez_1 = sre_start_time[0:11]
                        srez_2_s = hour_st
                        rez_3 = ":00:00.000000+00:00"
                        srez_s = srez_1 + srez_2_s + srez_3
                        srez_2_e = hour_end
                        if hour_end == str(24):
                            srez_1 = sre_end_time[0:11]
                            hour_end = "00"
                            srez_2_e = hour_end
                        srez_3 = ":00:00.000000+00:00"
                        srez_e = srez_1 + srez_2_e + srez_3

                        sor_start_time_end = dateutil.parser.parse(srez_s)
                        sor_end_time_end = dateutil.parser.parse(srez_e)
                        dict_for_list_hours = dict(start=sor_start_time_end, end=sor_end_time_end)
                        list_ho.append(dict_for_list_hours)
                list_for_rev_rep = list()
                summ_delta = 0
                for ho in list_ho:

                    for_app_id_unic = elem.old_order.session_key.local_key.app_id.app_id_unic
                    for_local_key = elem.old_order.session_key.local_key.app_id.local_key
                    for_new_eb_data_app = New_EB_App_Ul.objects.create(local_key=for_local_key, app_id_unic=for_app_id_unic)

                    id_for_save_new_eb_app_ui = elem.old_order.session_key.local_key.app_id.id
                    for_save = EB_Data_App.objects.filter(app_id__id=id_for_save_new_eb_app_ui)
                    for for_save_in in for_save:
                        break
                    start_time_in = ho["start"]
                    end_time_in = ho["end"]
                    for_new_orders = New_EB_Data_App.objects.create(local_key=for_local_key, start_time=start_time_in, end_time=end_time_in, app_id=for_new_eb_data_app)

                    for_new_eb_place = New_EB_Data_Link.objects.create(app_name=for_local_key, app_id=for_new_eb_data_app)

                    id_for_place = elem.old_order.session_key.local_key.id
                    places = EB_Place.objects.filter(local_key__id=id_for_place)
                    for place in places:
                        break
                    place_id = place.place_id
                    New_EB_Place.objects.create(local_key=for_new_eb_place, place_id=place_id)

                    session_id = elem.old_order.session_key.session_id
                    for_new_eb_order = New_EB_Session.objects.create(local_key=for_new_eb_place, session_id=session_id)

                    order_id_unic = elem.old_order.order_id_unic
                    revenue = elem.old_order.revenue
                    time_create = elem.old_order.time_create
                    query = New_EB_Order.objects.create(order_id_unic=order_id_unic, time_create=time_create, session_key=for_new_eb_order, key_for_data=for_new_orders)

                    delta_1 = datetime.timestamp(start_time_in)
                    delta_2 = datetime.timestamp(end_time_in)
                    delta = delta_2 - delta_1
                    dict_for_sum = dict(query=query, delta=delta)
                    list_for_rev_rep.append(dict_for_sum)
                    summ_delta = summ_delta + delta

                revenue = elem.old_order.revenue
                sum_re = 0
                num_pos = 0
                len_list_rev = len(list_for_rev_rep)
                for for_rev in list_for_rev_rep:
                    delta_r = for_rev["delta"]

                    delta_x = delta_r / summ_delta
                    revenue_for_s = round(delta_x * int(revenue))
                    sum_re = sum_re + revenue_for_s
                    num_pos = num_pos + 1
                    if num_pos == len_list_rev:
                        revenue_for_s = revenue - sum_re

                    query_for_save_in_result = for_rev["query"]
                    id_for_save = query_for_save_in_result.id
                    New_EB_Order.objects.filter(id=id_for_save).update(revenue=int(revenue_for_s))

    if "cont_db" in form_button:
        all_orders_old = EB_Order.objects.filter()
        summ_old = 0
        for order in all_orders_old:
            summ_old = order.revenue + summ_old
        all_orders_new = New_EB_Order.objects.filter()
        summ_new = 0
        for order in all_orders_new:
            summ_new = order.revenue + summ_new

    if "activ_hour_db" in form_button:
        all_orders = New_EB_Order.objects.filter()
        for order in all_orders:
            time_start = order.key_for_data.start_time
            time_hour = datetime.time(time_start)
            hour_time = int(time_hour.hour)
            app_data = order.key_for_data
            app = order.key_for_data.local_key
            Active_Hour.objects.create(active=hour_time, app_data=app_data, order=order, app=app)

    if "activ_day_db" in form_button:
        # del all elements in new DB (BEGIN)
        Active_Day.objects.filter().delete()
        # del all elements in new DB (END)

        all_hours = Active_Hour.objects.filter()
        for hour in all_hours:
            data_start_time = hour.order.key_for_data.start_time
            data_data_start_time = datetime.date(data_start_time)
            one_days = Active_Day.objects.filter(day=int(data_data_start_time.day))
            if one_days.exists():
                for one_day in one_days:
                    break
                hour_id = hour.id
                Active_Hour.objects.filter(id=hour_id).update(active_day=one_day)
            else:
                active_day = Active_Day.objects.create(day=int(data_data_start_time.day))
                hour_id = hour.id
                Active_Hour.objects.filter(id=hour_id).update(active_day=active_day)

    if "day_of_the_week" in form_button:
        all_hours = Active_Hour.objects.filter()
        for hour in all_hours:
            app = hour.app
            hour_id = hour.id
            data_start = hour.order.key_for_data.start_time
            data_data_start_time = datetime.date(data_start)
            day_of_the_week_day = calendar.day_name[data_data_start_time.weekday()]
            days_of_the_week = Day_of_the_week.objects.filter(day_of_the_week=str(day_of_the_week_day), app=app)
            for day_of_the_week in days_of_the_week:
                break
            if days_of_the_week.exists() and day_of_the_week.day_of_the_week == str(day_of_the_week_day) and day_of_the_week.app == app:
                for_save = Active_Hour.objects.filter(id=hour_id, app=app).update(day_of_the_week=day_of_the_week)
            else:
                day_of_the_week_create = Day_of_the_week.objects.create(day_of_the_week=str(day_of_the_week_day), app=app)
                for_save = Active_Hour.objects.filter(id=hour_id, app=app).update(day_of_the_week=day_of_the_week_create)

    if "res_med_speed" in form_button:
        all_apps = EB_App.objects.filter()
        all_day_week_all = Day_of_the_week.objects.filter()

        list_day_week = list()
        for day_week_all in all_day_week_all:
            if day_week_all.day_of_the_week not in list_day_week:
                list_day_week.append(day_week_all.day_of_the_week)

        all_list_for_rep = list()
        for day_week in list_day_week:
            for app in all_apps:
                id_app = app.id
                all_hour_in_day = Active_Hour.objects.filter(app=app, day_of_the_week__day_of_the_week=day_week)
                list_all_hour = list()
                for hour in all_hour_in_day:
                    if hour.active_hour not in list_all_hour:
                        list_all_hour.append(hour.active_hour)
                list_all_hour = sorted(list_all_hour)
                dict_activ_hours = dict(name_app=app.name, list_activ=list_all_hour, day_week=day_week)
                all_list_for_rep.append(dict_activ_hours)
        for element in all_list_for_rep:
            name_app = element["name_app"]
            list_hour = element["list_activ"]
            len_list_hour = len(list_hour)
            day_week = element["day_week"]
            elems = Active_Hour.objects.filter(app__name=name_app, active_hour__in=list_hour, day_of_the_week__day_of_the_week=day_week)
            summ = 0
            for elem in elems:
                revenu = elem.order.revenue
                summ = summ + revenu
            speed_money = summ / len_list_hour
            Day_of_the_week.objects.filter(app__name=name_app, day_of_the_week=day_week).update(med_speed=speed_money)

    if "res_med_speed_week" in form_button:
        all_apps = EB_App.objects.filter()
        for app in all_apps:
            all_day_week = Day_of_the_week.objects.filter(app=app)
            len_all_day_week = len(all_day_week)
            summ = 0
            for day_week in all_day_week:
                summ = summ + day_week.med_speed
            koef_med = summ / len_all_day_week

    return render(request, 'import_data/import_data_prime.html', locals())


def restaurant(request):
    app = EB_App.objects.get(id=84)

    all_day_week = Day_of_the_week.objects.filter(app=app)
    len_all_day_week = len(all_day_week)
    summ = 0
    for day_week in all_day_week:
        summ = summ + day_week.med_speed
    koef_med = summ / len_all_day_week

    list_all_winer = list()
    for day_week in all_day_week:
        dict_for_day = dict()
        if day_week.med_speed >= koef_med:
            day_of_the_week = day_week.day_of_the_week
            med_speed = day_week.med_speed
            dict_for_day = dict(day_of_the_week=day_of_the_week, med_speed=med_speed)
        if dict_for_day != {}:
            list_all_winer.append(dict_for_day)
    list_day_week = list()
    for day_week in list_all_winer:
        list_day_week.append(day_week["day_of_the_week"])
    list_all_day_week_dont_winner = list()
    for day_week in all_day_week:
        if day_week.day_of_the_week not in list_day_week:
            list_all_day_week_dont_winner.append(day_week.day_of_the_week)
    list_day_mo = list()
    for winer in list_all_winer:
        activ_hours_winer = Active_Hour.objects.filter(day_of_the_week__day_of_the_week=winer["day_of_the_week"], app=app)
        for activ_hour in activ_hours_winer:
            active_day = activ_hour.active_day
            if active_day not in list_day_mo:
                list_day_mo.append(active_day)
    list_id_win = list()
    for win_id in list_day_mo:
        list_id_win.append(win_id.id)
    all_id_all_day = list()
    list_id_dont_win = list()
    all_day = Active_Day.objects.filter()
    for day_dont_win in all_day:
        if day_dont_win.id not in list_id_win:
            list_id_dont_win.append(day_dont_win.id)
    list_all_day_id = list()
    all_day = Active_Day.objects.filter()
    for day_all_for_id in all_day:
        list_all_day_id.append(day_all_for_id.id)

    all_day = Active_Day.objects.filter(id__in=list_all_day_id)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_all_day_id)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time = list()
    result_summ_1_1 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_1 = result_summ_1_1 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_1 = round(result_summ_1_1 * 1.01)
        ras_1_1 = round(result_summ_1_1 * 0.01)
        list_all_max_time.append(dict_for_save)

    all_day = Active_Day.objects.filter(id__in=list_id_win)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_id_win)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time_1_2 = list()
    result_summ_1_2 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_2 = result_summ_1_2 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_2 = round(result_summ_1_2 * 1.01)
        ras_1_2 = round(result_summ_1_2 * 0.01)
        list_all_max_time_1_2.append(dict_for_save)

    all_day = Active_Day.objects.filter(id__in=list_id_dont_win)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_id_dont_win)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time_1_3 = list()
    result_summ_1_3 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_3 = result_summ_1_3 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_3 = round(result_summ_1_3 * 1.01)
        ras_1_3 = round(result_summ_1_3 * 0.01)
        list_all_max_time_1_3.append(dict_for_save)

    app = EB_App.objects.get(id=84)

    if "save_result_win" in request.POST:
        list_for_save_day = list()
        for element in list_all_winer:
            day = element["day_of_the_week"]
            list_for_save_day.append(day)

        list_for_save_hour = list()
        for element in list_all_max_time_1_2:
            start_time = element["start_time"]
            end_time = element["end_time"]
            sum_one = element["sum_one"]
            srez_start = int(start_time[0:2])
            srez_end = int(end_time[0:2])
            dict_for_day = dict(start=srez_start, end=srez_end, sum_one=int(sum_one))
            list_for_save_hour.append(dict_for_day)

        for element in list_for_save_day:
            if element == "Monday":
                day_create = Resume_Day_Week_Win.objects.create(Monday_day=True, app=app)
            if element == "Tuesday":
                day_create = Resume_Day_Week_Win.objects.create(Tuesday_day=True, app=app)
            if element == "Wednesday":
                day_create = Resume_Day_Week_Win.objects.create(Wednesday_day=True, app=app)
            if element == "Thursday":
                day_create = Resume_Day_Week_Win.objects.create(Thursday_day=True, app=app)
            if element == "Friday":
                day_create = Resume_Day_Week_Win.objects.create(Friday_day=True, app=app)
            if element == "Saturday":
                day_create = Resume_Day_Week_Win.objects.create(Saturday_day=True, app=app)
            if element == "Sunday":
                day_create = Resume_Day_Week_Win.objects.create(Sunday_day=True, app=app)

            for elem in list_for_save_hour:
                hour_start = elem["start"]
                hour_end = elem["end"]
                sum_one = elem["sum_one"]
                Resume_Hour_Win.objects.create(app=app, day=day_create, hour_start=hour_start, hour_end=hour_end, sum=int(sum_one))

    if "save_result_dont_win" in request.POST:
        list_for_save_day = list_all_day_week_dont_winner

        list_for_save_hour = list()
        for element in list_all_max_time_1_3:
            start_time = element["start_time"]
            end_time = element["end_time"]
            sum_one = element["sum_one"]
            srez_start = int(start_time[0:2])
            srez_end = int(end_time[0:2])
            dict_for_day = dict(start=srez_start, end=srez_end, sum_one=int(sum_one))
            list_for_save_hour.append(dict_for_day)

        for element in list_for_save_day:
            if element == "Monday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Monday_day=True, app=app)
            if element == "Tuesday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Tuesday_day=True, app=app)
            if element == "Wednesday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Wednesday_day=True, app=app)
            if element == "Thursday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Thursday_day=True, app=app)
            if element == "Friday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Friday_day=True, app=app)
            if element == "Saturday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Saturday_day=True, app=app)
            if element == "Sunday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Sunday_day=True, app=app)

            for elem in list_for_save_hour:
                hour_start = elem["start"]
                hour_end = elem["end"]
                sum_one = elem["sum_one"]
                Resume_Hour_Dont_Win.objects.create(app=app, day=day_create, hour_start=hour_start, hour_end=hour_end, sum=int(sum_one))

    return render(request, 're_data/restaurant.html', locals())


def news(request):
    app = EB_App.objects.get(id=85)

    all_day_week = Day_of_the_week.objects.filter(app=app)
    len_all_day_week = len(all_day_week)
    summ = 0
    for day_week in all_day_week:
        summ = summ + day_week.med_speed
    koef_med = summ / len_all_day_week

    list_all_winer = list()
    for day_week in all_day_week:
        dict_for_day = dict()
        if day_week.med_speed >= koef_med:
            day_of_the_week = day_week.day_of_the_week
            med_speed = day_week.med_speed
            dict_for_day = dict(day_of_the_week=day_of_the_week, med_speed=med_speed)
        if dict_for_day != {}:
            list_all_winer.append(dict_for_day)
    list_day_week = list()
    for day_week in list_all_winer:
        list_day_week.append(day_week["day_of_the_week"])
    list_all_day_week_dont_winner = list()
    for day_week in all_day_week:
        if day_week.day_of_the_week not in list_day_week:
            list_all_day_week_dont_winner.append(day_week.day_of_the_week)
    list_day_mo = list()
    for winer in list_all_winer:
        activ_hours_winer = Active_Hour.objects.filter(day_of_the_week__day_of_the_week=winer["day_of_the_week"], app=app)
        for activ_hour in activ_hours_winer:
            active_day = activ_hour.active_day
            if active_day not in list_day_mo:
                list_day_mo.append(active_day)
    list_id_win = list()
    for win_id in list_day_mo:
        list_id_win.append(win_id.id)
    all_id_all_day = list()
    list_id_dont_win = list()
    all_day = Active_Day.objects.filter()
    for day_dont_win in all_day:
        if day_dont_win.id not in list_id_win:
            list_id_dont_win.append(day_dont_win.id)
    list_all_day_id = list()
    all_day = Active_Day.objects.filter()
    for day_all_for_id in all_day:
        list_all_day_id.append(day_all_for_id.id)

    all_day = Active_Day.objects.filter(id__in=list_all_day_id)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_all_day_id)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time = list()
    result_summ_1_1 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_1 = result_summ_1_1 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_1 = round(result_summ_1_1 * 1.01)
        ras_1_1 = round(result_summ_1_1 * 0.01)
        list_all_max_time.append(dict_for_save)

    all_day = Active_Day.objects.filter(id__in=list_id_win)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_id_win)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time_1_2 = list()
    result_summ_1_2 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_2 = result_summ_1_2 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_2 = round(result_summ_1_2 * 1.01)
        ras_1_2 = round(result_summ_1_2 * 0.01)
        list_all_max_time_1_2.append(dict_for_save)

    all_day = Active_Day.objects.filter(id__in=list_id_dont_win)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_id_dont_win)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time_1_3 = list()
    result_summ_1_3 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_3 = result_summ_1_3 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_3 = round(result_summ_1_3 * 1.01)
        ras_1_3 = round(result_summ_1_3 * 0.01)
        list_all_max_time_1_3.append(dict_for_save)

    app = EB_App.objects.get(id=85)

    if "save_result_win" in request.POST:
        list_for_save_day = list()
        for element in list_all_winer:
            day = element["day_of_the_week"]
            list_for_save_day.append(day)

        list_for_save_hour = list()
        for element in list_all_max_time_1_2:
            start_time = element["start_time"]
            end_time = element["end_time"]
            sum_one = element["sum_one"]
            srez_start = int(start_time[0:2])
            srez_end = int(end_time[0:2])
            dict_for_day = dict(start=srez_start, end=srez_end, sum_one=int(sum_one))
            list_for_save_hour.append(dict_for_day)

        for element in list_for_save_day:
            if element == "Monday":
                day_create = Resume_Day_Week_Win.objects.create(Monday_day=True, app=app)
            if element == "Tuesday":
                day_create = Resume_Day_Week_Win.objects.create(Tuesday_day=True, app=app)
            if element == "Wednesday":
                day_create = Resume_Day_Week_Win.objects.create(Wednesday_day=True, app=app)
            if element == "Thursday":
                day_create = Resume_Day_Week_Win.objects.create(Thursday_day=True, app=app)
            if element == "Friday":
                day_create = Resume_Day_Week_Win.objects.create(Friday_day=True, app=app)
            if element == "Saturday":
                day_create = Resume_Day_Week_Win.objects.create(Saturday_day=True, app=app)
            if element == "Sunday":
                day_create = Resume_Day_Week_Win.objects.create(Sunday_day=True, app=app)

            for elem in list_for_save_hour:
                hour_start = elem["start"]
                hour_end = elem["end"]
                sum_one = elem["sum_one"]
                Resume_Hour_Win.objects.create(app=app, day=day_create, hour_start=hour_start, hour_end=hour_end, sum=int(sum_one))

    if "save_result_dont_win" in request.POST:
        list_for_save_day = list_all_day_week_dont_winner

        list_for_save_hour = list()
        for element in list_all_max_time_1_3:
            start_time = element["start_time"]
            end_time = element["end_time"]
            sum_one = element["sum_one"]
            srez_start = int(start_time[0:2])
            srez_end = int(end_time[0:2])
            dict_for_day = dict(start=srez_start, end=srez_end, sum_one=int(sum_one))
            list_for_save_hour.append(dict_for_day)

        for element in list_for_save_day:
            if element == "Monday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Monday_day=True, app=app)
            if element == "Tuesday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Tuesday_day=True, app=app)
            if element == "Wednesday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Wednesday_day=True, app=app)
            if element == "Thursday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Thursday_day=True, app=app)
            if element == "Friday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Friday_day=True, app=app)
            if element == "Saturday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Saturday_day=True, app=app)
            if element == "Sunday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Sunday_day=True, app=app)

            for elem in list_for_save_hour:
                hour_start = elem["start"]
                hour_end = elem["end"]
                sum_one = elem["sum_one"]
                Resume_Hour_Dont_Win.objects.create(app=app, day=day_create, hour_start=hour_start, hour_end=hour_end, sum=int(sum_one))

    return render(request, 're_data/news.html', locals())


def memory(request):
    app = EB_App.objects.get(id=86)

    all_day_week = Day_of_the_week.objects.filter(app=app)
    len_all_day_week = len(all_day_week)
    summ = 0
    for day_week in all_day_week:
        summ = summ + day_week.med_speed
    koef_med = summ / len_all_day_week

    list_all_winer = list()
    for day_week in all_day_week:
        dict_for_day = dict()
        if day_week.med_speed >= koef_med:
            day_of_the_week = day_week.day_of_the_week
            med_speed = day_week.med_speed
            dict_for_day = dict(day_of_the_week=day_of_the_week, med_speed=med_speed)
        if dict_for_day != {}:
            list_all_winer.append(dict_for_day)
    list_day_week = list()
    for day_week in list_all_winer:
        list_day_week.append(day_week["day_of_the_week"])
    list_all_day_week_dont_winner = list()
    for day_week in all_day_week:
        if day_week.day_of_the_week not in list_day_week:
            list_all_day_week_dont_winner.append(day_week.day_of_the_week)
    list_day_mo = list()
    for winer in list_all_winer:
        activ_hours_winer = Active_Hour.objects.filter(day_of_the_week__day_of_the_week=winer["day_of_the_week"], app=app)
        for activ_hour in activ_hours_winer:
            active_day = activ_hour.active_day
            if active_day not in list_day_mo:
                list_day_mo.append(active_day)
    list_id_win = list()
    for win_id in list_day_mo:
        list_id_win.append(win_id.id)
    all_id_all_day = list()
    list_id_dont_win = list()
    all_day = Active_Day.objects.filter()
    for day_dont_win in all_day:
        if day_dont_win.id not in list_id_win:
            list_id_dont_win.append(day_dont_win.id)
    list_all_day_id = list()
    all_day = Active_Day.objects.filter()
    for day_all_for_id in all_day:
        list_all_day_id.append(day_all_for_id.id)

    all_day = Active_Day.objects.filter(id__in=list_all_day_id)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_all_day_id)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time = list()
    result_summ_1_1 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_1 = result_summ_1_1 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_1 = round(result_summ_1_1 * 1.01)
        ras_1_1 = round(result_summ_1_1 * 0.01)
        list_all_max_time.append(dict_for_save)

    all_day = Active_Day.objects.filter(id__in=list_id_win)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_id_win)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time_1_2 = list()
    result_summ_1_2 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_2 = result_summ_1_2 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_2 = round(result_summ_1_2 * 1.01)
        ras_1_2 = round(result_summ_1_2 * 0.01)
        list_all_max_time_1_2.append(dict_for_save)

    all_day = Active_Day.objects.filter(id__in=list_id_dont_win)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_id_dont_win)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time_1_3 = list()
    result_summ_1_3 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_3 = result_summ_1_3 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_3 = round(result_summ_1_3 * 1.01)
        ras_1_3 = round(result_summ_1_3 * 0.01)
        list_all_max_time_1_3.append(dict_for_save)

    app = EB_App.objects.get(id=86)

    if "save_result_win" in request.POST:
        list_for_save_day = list()
        for element in list_all_winer:
            day = element["day_of_the_week"]
            list_for_save_day.append(day)

        list_for_save_hour = list()
        for element in list_all_max_time_1_2:
            start_time = element["start_time"]
            end_time = element["end_time"]
            sum_one = element["sum_one"]
            srez_start = int(start_time[0:2])
            srez_end = int(end_time[0:2])
            dict_for_day = dict(start=srez_start, end=srez_end, sum_one=int(sum_one))
            list_for_save_hour.append(dict_for_day)

        for element in list_for_save_day:
            if element == "Monday":
                day_create = Resume_Day_Week_Win.objects.create(Monday_day=True, app=app)
            if element == "Tuesday":
                day_create = Resume_Day_Week_Win.objects.create(Tuesday_day=True, app=app)
            if element == "Wednesday":
                day_create = Resume_Day_Week_Win.objects.create(Wednesday_day=True, app=app)
            if element == "Thursday":
                day_create = Resume_Day_Week_Win.objects.create(Thursday_day=True, app=app)
            if element == "Friday":
                day_create = Resume_Day_Week_Win.objects.create(Friday_day=True, app=app)
            if element == "Saturday":
                day_create = Resume_Day_Week_Win.objects.create(Saturday_day=True, app=app)
            if element == "Sunday":
                day_create = Resume_Day_Week_Win.objects.create(Sunday_day=True, app=app)

            for elem in list_for_save_hour:
                hour_start = elem["start"]
                hour_end = elem["end"]
                sum_one = elem["sum_one"]
                Resume_Hour_Win.objects.create(app=app, day=day_create, hour_start=hour_start, hour_end=hour_end, sum=int(sum_one))

    if "save_result_dont_win" in request.POST:
        list_for_save_day = list_all_day_week_dont_winner

        list_for_save_hour = list()
        for element in list_all_max_time_1_3:
            start_time = element["start_time"]
            end_time = element["end_time"]
            sum_one = element["sum_one"]
            srez_start = int(start_time[0:2])
            srez_end = int(end_time[0:2])
            dict_for_day = dict(start=srez_start, end=srez_end, sum_one=int(sum_one))
            list_for_save_hour.append(dict_for_day)

        for element in list_for_save_day:
            if element == "Monday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Monday_day=True, app=app)
            if element == "Tuesday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Tuesday_day=True, app=app)
            if element == "Wednesday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Wednesday_day=True, app=app)
            if element == "Thursday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Thursday_day=True, app=app)
            if element == "Friday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Friday_day=True, app=app)
            if element == "Saturday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Saturday_day=True, app=app)
            if element == "Sunday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Sunday_day=True, app=app)

            for elem in list_for_save_hour:
                hour_start = elem["start"]
                hour_end = elem["end"]
                sum_one = elem["sum_one"]
                Resume_Hour_Dont_Win.objects.create(app=app, day=day_create, hour_start=hour_start, hour_end=hour_end, sum=int(sum_one))

    return render(request, 're_data/memory.html', locals())


def paint(request):
    app = EB_App.objects.get(id=87)

    all_day_week = Day_of_the_week.objects.filter(app=app)
    len_all_day_week = len(all_day_week)
    summ = 0
    for day_week in all_day_week:
        summ = summ + day_week.med_speed
    koef_med = summ / len_all_day_week

    list_all_winer = list()
    for day_week in all_day_week:
        dict_for_day = dict()
        if day_week.med_speed >= koef_med:
            day_of_the_week = day_week.day_of_the_week
            med_speed = day_week.med_speed
            dict_for_day = dict(day_of_the_week=day_of_the_week, med_speed=med_speed)
        if dict_for_day != {}:
            list_all_winer.append(dict_for_day)
    list_day_week = list()
    for day_week in list_all_winer:
        list_day_week.append(day_week["day_of_the_week"])
    list_all_day_week_dont_winner = list()
    for day_week in all_day_week:
        if day_week.day_of_the_week not in list_day_week:
            list_all_day_week_dont_winner.append(day_week.day_of_the_week)
    list_day_mo = list()
    for winer in list_all_winer:
        activ_hours_winer = Active_Hour.objects.filter(day_of_the_week__day_of_the_week=winer["day_of_the_week"], app=app)
        for activ_hour in activ_hours_winer:
            active_day = activ_hour.active_day
            if active_day not in list_day_mo:
                list_day_mo.append(active_day)
    list_id_win = list()
    for win_id in list_day_mo:
        list_id_win.append(win_id.id)
    all_id_all_day = list()
    list_id_dont_win = list()
    all_day = Active_Day.objects.filter()
    for day_dont_win in all_day:
        if day_dont_win.id not in list_id_win:
            list_id_dont_win.append(day_dont_win.id)
    list_all_day_id = list()
    all_day = Active_Day.objects.filter()
    for day_all_for_id in all_day:
        list_all_day_id.append(day_all_for_id.id)

    all_day = Active_Day.objects.filter(id__in=list_all_day_id)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_all_day_id)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time = list()
    result_summ_1_1 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_1 = result_summ_1_1 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_1 = round(result_summ_1_1 * 1.01)
        ras_1_1 = round(result_summ_1_1 * 0.01)
        list_all_max_time.append(dict_for_save)

    all_day = Active_Day.objects.filter(id__in=list_id_win)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_id_win)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time_1_2 = list()
    result_summ_1_2 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_2 = result_summ_1_2 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_2 = round(result_summ_1_2 * 1.01)
        ras_1_2 = round(result_summ_1_2 * 0.01)
        list_all_max_time_1_2.append(dict_for_save)

    all_day = Active_Day.objects.filter(id__in=list_id_dont_win)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_id_dont_win)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time_1_3 = list()
    result_summ_1_3 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_3 = result_summ_1_3 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_3 = round(result_summ_1_3 * 1.01)
        ras_1_3 = round(result_summ_1_3 * 0.01)
        list_all_max_time_1_3.append(dict_for_save)

    app = EB_App.objects.get(id=87)

    if "save_result_win" in request.POST:
        list_for_save_day = list()
        for element in list_all_winer:
            day = element["day_of_the_week"]
            list_for_save_day.append(day)

        list_for_save_hour = list()
        for element in list_all_max_time_1_2:
            start_time = element["start_time"]
            end_time = element["end_time"]
            sum_one = element["sum_one"]
            srez_start = int(start_time[0:2])
            srez_end = int(end_time[0:2])
            dict_for_day = dict(start=srez_start, end=srez_end, sum_one=int(sum_one))
            list_for_save_hour.append(dict_for_day)

        for element in list_for_save_day:
            if element == "Monday":
                day_create = Resume_Day_Week_Win.objects.create(Monday_day=True, app=app)
            if element == "Tuesday":
                day_create = Resume_Day_Week_Win.objects.create(Tuesday_day=True, app=app)
            if element == "Wednesday":
                day_create = Resume_Day_Week_Win.objects.create(Wednesday_day=True, app=app)
            if element == "Thursday":
                day_create = Resume_Day_Week_Win.objects.create(Thursday_day=True, app=app)
            if element == "Friday":
                day_create = Resume_Day_Week_Win.objects.create(Friday_day=True, app=app)
            if element == "Saturday":
                day_create = Resume_Day_Week_Win.objects.create(Saturday_day=True, app=app)
            if element == "Sunday":
                day_create = Resume_Day_Week_Win.objects.create(Sunday_day=True, app=app)

            for elem in list_for_save_hour:
                hour_start = elem["start"]
                hour_end = elem["end"]
                sum_one = elem["sum_one"]
                Resume_Hour_Win.objects.create(app=app, day=day_create, hour_start=hour_start, hour_end=hour_end, sum=int(sum_one))

    if "save_result_dont_win" in request.POST:
        list_for_save_day = list_all_day_week_dont_winner

        list_for_save_hour = list()
        for element in list_all_max_time_1_3:
            start_time = element["start_time"]
            end_time = element["end_time"]
            sum_one = element["sum_one"]
            srez_start = int(start_time[0:2])
            srez_end = int(end_time[0:2])
            dict_for_day = dict(start=srez_start, end=srez_end, sum_one=int(sum_one))
            list_for_save_hour.append(dict_for_day)

        for element in list_for_save_day:
            if element == "Monday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Monday_day=True, app=app)
            if element == "Tuesday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Tuesday_day=True, app=app)
            if element == "Wednesday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Wednesday_day=True, app=app)
            if element == "Thursday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Thursday_day=True, app=app)
            if element == "Friday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Friday_day=True, app=app)
            if element == "Saturday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Saturday_day=True, app=app)
            if element == "Sunday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Sunday_day=True, app=app)

            for elem in list_for_save_hour:
                hour_start = elem["start"]
                hour_end = elem["end"]
                sum_one = elem["sum_one"]
                Resume_Hour_Dont_Win.objects.create(app=app, day=day_create, hour_start=hour_start, hour_end=hour_end, sum=int(sum_one))

    return render(request, 're_data/paint.html', locals())


def wallpapers(request):
    app = EB_App.objects.get(id=88)

    all_day_week = Day_of_the_week.objects.filter(app=app)
    len_all_day_week = len(all_day_week)
    summ = 0
    for day_week in all_day_week:
        summ = summ + day_week.med_speed
    koef_med = summ / len_all_day_week

    list_all_winer = list()
    for day_week in all_day_week:
        dict_for_day = dict()
        if day_week.med_speed >= koef_med:
            day_of_the_week = day_week.day_of_the_week
            med_speed = day_week.med_speed
            dict_for_day = dict(day_of_the_week=day_of_the_week, med_speed=med_speed)
        if dict_for_day != {}:
            list_all_winer.append(dict_for_day)
    list_day_week = list()
    for day_week in list_all_winer:
        list_day_week.append(day_week["day_of_the_week"])
    list_all_day_week_dont_winner = list()
    for day_week in all_day_week:
        if day_week.day_of_the_week not in list_day_week:
            list_all_day_week_dont_winner.append(day_week.day_of_the_week)
    list_day_mo = list()
    for winer in list_all_winer:
        activ_hours_winer = Active_Hour.objects.filter(day_of_the_week__day_of_the_week=winer["day_of_the_week"], app=app)
        for activ_hour in activ_hours_winer:
            active_day = activ_hour.active_day
            if active_day not in list_day_mo:
                list_day_mo.append(active_day)
    list_id_win = list()
    for win_id in list_day_mo:
        list_id_win.append(win_id.id)
    all_id_all_day = list()
    list_id_dont_win = list()
    all_day = Active_Day.objects.filter()
    for day_dont_win in all_day:
        if day_dont_win.id not in list_id_win:
            list_id_dont_win.append(day_dont_win.id)
    list_all_day_id = list()
    all_day = Active_Day.objects.filter()
    for day_all_for_id in all_day:
        list_all_day_id.append(day_all_for_id.id)

    all_day = Active_Day.objects.filter(id__in=list_all_day_id)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_all_day_id)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time = list()
    result_summ_1_1 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_1 = result_summ_1_1 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_1 = round(result_summ_1_1 * 1.01)
        ras_1_1 = round(result_summ_1_1 * 0.01)
        list_all_max_time.append(dict_for_save)

    all_day = Active_Day.objects.filter(id__in=list_id_win)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_id_win)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time_1_2 = list()
    result_summ_1_2 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_2 = result_summ_1_2 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_2 = round(result_summ_1_2 * 1.01)
        ras_1_2 = round(result_summ_1_2 * 0.01)
        list_all_max_time_1_2.append(dict_for_save)

    all_day = Active_Day.objects.filter(id__in=list_id_dont_win)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_id_dont_win)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time_1_3 = list()
    result_summ_1_3 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_3 = result_summ_1_3 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_3 = round(result_summ_1_3 * 1.01)
        ras_1_3 = round(result_summ_1_3 * 0.01)
        list_all_max_time_1_3.append(dict_for_save)

    app = EB_App.objects.get(id=88)

    if "save_result_win" in request.POST:
        list_for_save_day = list()
        for element in list_all_winer:
            day = element["day_of_the_week"]
            list_for_save_day.append(day)

        list_for_save_hour = list()
        for element in list_all_max_time_1_2:
            start_time = element["start_time"]
            end_time = element["end_time"]
            sum_one = element["sum_one"]
            srez_start = int(start_time[0:2])
            srez_end = int(end_time[0:2])
            dict_for_day = dict(start=srez_start, end=srez_end, sum_one=int(sum_one))
            list_for_save_hour.append(dict_for_day)

        for element in list_for_save_day:
            if element == "Monday":
                day_create = Resume_Day_Week_Win.objects.create(Monday_day=True, app=app)
            if element == "Tuesday":
                day_create = Resume_Day_Week_Win.objects.create(Tuesday_day=True, app=app)
            if element == "Wednesday":
                day_create = Resume_Day_Week_Win.objects.create(Wednesday_day=True, app=app)
            if element == "Thursday":
                day_create = Resume_Day_Week_Win.objects.create(Thursday_day=True, app=app)
            if element == "Friday":
                day_create = Resume_Day_Week_Win.objects.create(Friday_day=True, app=app)
            if element == "Saturday":
                day_create = Resume_Day_Week_Win.objects.create(Saturday_day=True, app=app)
            if element == "Sunday":
                day_create = Resume_Day_Week_Win.objects.create(Sunday_day=True, app=app)

            for elem in list_for_save_hour:
                hour_start = elem["start"]
                hour_end = elem["end"]
                sum_one = elem["sum_one"]
                Resume_Hour_Win.objects.create(app=app, day=day_create, hour_start=hour_start, hour_end=hour_end, sum=int(sum_one))

    if "save_result_dont_win" in request.POST:
        list_for_save_day = list_all_day_week_dont_winner

        list_for_save_hour = list()
        for element in list_all_max_time_1_3:
            start_time = element["start_time"]
            end_time = element["end_time"]
            sum_one = element["sum_one"]
            srez_start = int(start_time[0:2])
            srez_end = int(end_time[0:2])
            dict_for_day = dict(start=srez_start, end=srez_end, sum_one=int(sum_one))
            list_for_save_hour.append(dict_for_day)

        for element in list_for_save_day:
            if element == "Monday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Monday_day=True, app=app)
            if element == "Tuesday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Tuesday_day=True, app=app)
            if element == "Wednesday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Wednesday_day=True, app=app)
            if element == "Thursday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Thursday_day=True, app=app)
            if element == "Friday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Friday_day=True, app=app)
            if element == "Saturday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Saturday_day=True, app=app)
            if element == "Sunday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Sunday_day=True, app=app)

            for elem in list_for_save_hour:
                hour_start = elem["start"]
                hour_end = elem["end"]
                sum_one = elem["sum_one"]
                Resume_Hour_Dont_Win.objects.create(app=app, day=day_create, hour_start=hour_start, hour_end=hour_end, sum=int(sum_one))

    return render(request, 're_data/wallpapers.html', locals())


def airhockey(request):
    app = EB_App.objects.get(id=89)

    all_day_week = Day_of_the_week.objects.filter(app=app)
    len_all_day_week = len(all_day_week)
    summ = 0
    for day_week in all_day_week:
        summ = summ + day_week.med_speed
    koef_med = summ / len_all_day_week

    list_all_winer = list()
    for day_week in all_day_week:
        dict_for_day = dict()
        if day_week.med_speed >= koef_med:
            day_of_the_week = day_week.day_of_the_week
            med_speed = day_week.med_speed
            dict_for_day = dict(day_of_the_week=day_of_the_week, med_speed=med_speed)
        if dict_for_day != {}:
            list_all_winer.append(dict_for_day)
    list_day_week = list()
    for day_week in list_all_winer:
        list_day_week.append(day_week["day_of_the_week"])
    list_all_day_week_dont_winner = list()
    for day_week in all_day_week:
        if day_week.day_of_the_week not in list_day_week:
            list_all_day_week_dont_winner.append(day_week.day_of_the_week)
    list_day_mo = list()
    for winer in list_all_winer:
        activ_hours_winer = Active_Hour.objects.filter(day_of_the_week__day_of_the_week=winer["day_of_the_week"], app=app)
        for activ_hour in activ_hours_winer:
            active_day = activ_hour.active_day
            if active_day not in list_day_mo:
                list_day_mo.append(active_day)
    list_id_win = list()
    for win_id in list_day_mo:
        list_id_win.append(win_id.id)
    all_id_all_day = list()
    list_id_dont_win = list()
    all_day = Active_Day.objects.filter()
    for day_dont_win in all_day:
        if day_dont_win.id not in list_id_win:
            list_id_dont_win.append(day_dont_win.id)
    list_all_day_id = list()
    all_day = Active_Day.objects.filter()
    for day_all_for_id in all_day:
        list_all_day_id.append(day_all_for_id.id)

    all_day = Active_Day.objects.filter(id__in=list_all_day_id)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_all_day_id)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time = list()
    result_summ_1_1 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_1 = result_summ_1_1 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_1 = round(result_summ_1_1 * 1.01)
        ras_1_1 = round(result_summ_1_1 * 0.01)
        list_all_max_time.append(dict_for_save)

    all_day = Active_Day.objects.filter(id__in=list_id_win)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_id_win)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time_1_2 = list()
    result_summ_1_2 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_2 = result_summ_1_2 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_2 = round(result_summ_1_2 * 1.01)
        ras_1_2 = round(result_summ_1_2 * 0.01)
        list_all_max_time_1_2.append(dict_for_save)

    all_day = Active_Day.objects.filter(id__in=list_id_dont_win)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_id_dont_win)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time_1_3 = list()
    result_summ_1_3 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_3 = result_summ_1_3 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_3 = round(result_summ_1_3 * 1.01)
        ras_1_3 = round(result_summ_1_3 * 0.01)
        list_all_max_time_1_3.append(dict_for_save)

    app = EB_App.objects.get(id=89)

    if "save_result_win" in request.POST:
        list_for_save_day = list()
        for element in list_all_winer:
            day = element["day_of_the_week"]
            list_for_save_day.append(day)

        list_for_save_hour = list()
        for element in list_all_max_time_1_2:
            start_time = element["start_time"]
            end_time = element["end_time"]
            sum_one = element["sum_one"]
            srez_start = int(start_time[0:2])
            srez_end = int(end_time[0:2])
            dict_for_day = dict(start=srez_start, end=srez_end, sum_one=int(sum_one))
            list_for_save_hour.append(dict_for_day)

        for element in list_for_save_day:
            if element == "Monday":
                day_create = Resume_Day_Week_Win.objects.create(Monday_day=True, app=app)
            if element == "Tuesday":
                day_create = Resume_Day_Week_Win.objects.create(Tuesday_day=True, app=app)
            if element == "Wednesday":
                day_create = Resume_Day_Week_Win.objects.create(Wednesday_day=True, app=app)
            if element == "Thursday":
                day_create = Resume_Day_Week_Win.objects.create(Thursday_day=True, app=app)
            if element == "Friday":
                day_create = Resume_Day_Week_Win.objects.create(Friday_day=True, app=app)
            if element == "Saturday":
                day_create = Resume_Day_Week_Win.objects.create(Saturday_day=True, app=app)
            if element == "Sunday":
                day_create = Resume_Day_Week_Win.objects.create(Sunday_day=True, app=app)

            for elem in list_for_save_hour:
                hour_start = elem["start"]
                hour_end = elem["end"]
                sum_one = elem["sum_one"]
                Resume_Hour_Win.objects.create(app=app, day=day_create, hour_start=hour_start, hour_end=hour_end, sum=int(sum_one))

    if "save_result_dont_win" in request.POST:
        list_for_save_day = list_all_day_week_dont_winner

        list_for_save_hour = list()
        for element in list_all_max_time_1_3:
            start_time = element["start_time"]
            end_time = element["end_time"]
            sum_one = element["sum_one"]
            srez_start = int(start_time[0:2])
            srez_end = int(end_time[0:2])
            dict_for_day = dict(start=srez_start, end=srez_end, sum_one=int(sum_one))
            list_for_save_hour.append(dict_for_day)

        for element in list_for_save_day:
            if element == "Monday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Monday_day=True, app=app)
            if element == "Tuesday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Tuesday_day=True, app=app)
            if element == "Wednesday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Wednesday_day=True, app=app)
            if element == "Thursday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Thursday_day=True, app=app)
            if element == "Friday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Friday_day=True, app=app)
            if element == "Saturday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Saturday_day=True, app=app)
            if element == "Sunday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Sunday_day=True, app=app)

            for elem in list_for_save_hour:
                hour_start = elem["start"]
                hour_end = elem["end"]
                sum_one = elem["sum_one"]
                Resume_Hour_Dont_Win.objects.create(app=app, day=day_create, hour_start=hour_start, hour_end=hour_end, sum=int(sum_one))

    return render(request, 're_data/airhockey.html', locals())


def photoshare(request):
    app = EB_App.objects.get(id=90)

    all_day_week = Day_of_the_week.objects.filter(app=app)
    len_all_day_week = len(all_day_week)
    summ = 0
    for day_week in all_day_week:
        summ = summ + day_week.med_speed
    koef_med = summ / len_all_day_week

    list_all_winer = list()
    for day_week in all_day_week:
        dict_for_day = dict()
        if day_week.med_speed >= koef_med:
            day_of_the_week = day_week.day_of_the_week
            med_speed = day_week.med_speed
            dict_for_day = dict(day_of_the_week=day_of_the_week, med_speed=med_speed)
        if dict_for_day != {}:
            list_all_winer.append(dict_for_day)
    list_day_week = list()
    for day_week in list_all_winer:
        list_day_week.append(day_week["day_of_the_week"])
    list_all_day_week_dont_winner = list()
    for day_week in all_day_week:
        if day_week.day_of_the_week not in list_day_week:
            list_all_day_week_dont_winner.append(day_week.day_of_the_week)
    list_day_mo = list()
    for winer in list_all_winer:
        activ_hours_winer = Active_Hour.objects.filter(day_of_the_week__day_of_the_week=winer["day_of_the_week"], app=app)
        for activ_hour in activ_hours_winer:
            active_day = activ_hour.active_day
            if active_day not in list_day_mo:
                list_day_mo.append(active_day)
    list_id_win = list()
    for win_id in list_day_mo:
        list_id_win.append(win_id.id)
    all_id_all_day = list()
    list_id_dont_win = list()
    all_day = Active_Day.objects.filter()
    for day_dont_win in all_day:
        if day_dont_win.id not in list_id_win:
            list_id_dont_win.append(day_dont_win.id)
    list_all_day_id = list()
    all_day = Active_Day.objects.filter()
    for day_all_for_id in all_day:
        list_all_day_id.append(day_all_for_id.id)

    all_day = Active_Day.objects.filter(id__in=list_all_day_id)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_all_day_id)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time = list()
    result_summ_1_1 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_1 = result_summ_1_1 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_1 = round(result_summ_1_1 * 1.01)
        ras_1_1 = round(result_summ_1_1 * 0.01)
        list_all_max_time.append(dict_for_save)

    all_day = Active_Day.objects.filter(id__in=list_id_win)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_id_win)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time_1_2 = list()
    result_summ_1_2 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_2 = result_summ_1_2 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_2 = round(result_summ_1_2 * 1.01)
        ras_1_2 = round(result_summ_1_2 * 0.01)
        list_all_max_time_1_2.append(dict_for_save)

    all_day = Active_Day.objects.filter(id__in=list_id_dont_win)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_id_dont_win)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time_1_3 = list()
    result_summ_1_3 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_3 = result_summ_1_3 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_3 = round(result_summ_1_3 * 1.01)
        ras_1_3 = round(result_summ_1_3 * 0.01)
        list_all_max_time_1_3.append(dict_for_save)

    app = EB_App.objects.get(id=90)

    if "save_result_win" in request.POST:
        list_for_save_day = list()
        for element in list_all_winer:
            day = element["day_of_the_week"]
            list_for_save_day.append(day)

        list_for_save_hour = list()
        for element in list_all_max_time_1_2:
            start_time = element["start_time"]
            end_time = element["end_time"]
            sum_one = element["sum_one"]
            srez_start = int(start_time[0:2])
            srez_end = int(end_time[0:2])
            dict_for_day = dict(start=srez_start, end=srez_end, sum_one=int(sum_one))
            list_for_save_hour.append(dict_for_day)

        for element in list_for_save_day:
            if element == "Monday":
                day_create = Resume_Day_Week_Win.objects.create(Monday_day=True, app=app)
            if element == "Tuesday":
                day_create = Resume_Day_Week_Win.objects.create(Tuesday_day=True, app=app)
            if element == "Wednesday":
                day_create = Resume_Day_Week_Win.objects.create(Wednesday_day=True, app=app)
            if element == "Thursday":
                day_create = Resume_Day_Week_Win.objects.create(Thursday_day=True, app=app)
            if element == "Friday":
                day_create = Resume_Day_Week_Win.objects.create(Friday_day=True, app=app)
            if element == "Saturday":
                day_create = Resume_Day_Week_Win.objects.create(Saturday_day=True, app=app)
            if element == "Sunday":
                day_create = Resume_Day_Week_Win.objects.create(Sunday_day=True, app=app)

            for elem in list_for_save_hour:
                hour_start = elem["start"]
                hour_end = elem["end"]
                sum_one = elem["sum_one"]
                Resume_Hour_Win.objects.create(app=app, day=day_create, hour_start=hour_start, hour_end=hour_end, sum=int(sum_one))

    if "save_result_dont_win" in request.POST:
        list_for_save_day = list_all_day_week_dont_winner

        list_for_save_hour = list()
        for element in list_all_max_time_1_3:
            start_time = element["start_time"]
            end_time = element["end_time"]
            sum_one = element["sum_one"]
            srez_start = int(start_time[0:2])
            srez_end = int(end_time[0:2])
            dict_for_day = dict(start=srez_start, end=srez_end, sum_one=int(sum_one))
            list_for_save_hour.append(dict_for_day)

        for element in list_for_save_day:
            if element == "Monday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Monday_day=True, app=app)
            if element == "Tuesday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Tuesday_day=True, app=app)
            if element == "Wednesday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Wednesday_day=True, app=app)
            if element == "Thursday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Thursday_day=True, app=app)
            if element == "Friday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Friday_day=True, app=app)
            if element == "Saturday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Saturday_day=True, app=app)
            if element == "Sunday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Sunday_day=True, app=app)

            for elem in list_for_save_hour:
                hour_start = elem["start"]
                hour_end = elem["end"]
                sum_one = elem["sum_one"]
                Resume_Hour_Dont_Win.objects.create(app=app, day=day_create, hour_start=hour_start, hour_end=hour_end, sum=int(sum_one))

    return render(request, 're_data/photoshare.html', locals())


def jigsawpuzzle(request):
    app = EB_App.objects.get(id=91)

    all_day_week = Day_of_the_week.objects.filter(app=app)
    len_all_day_week = len(all_day_week)
    summ = 0
    for day_week in all_day_week:
        summ = summ + day_week.med_speed
    koef_med = summ / len_all_day_week

    list_all_winer = list()
    for day_week in all_day_week:
        dict_for_day = dict()
        if day_week.med_speed >= koef_med:
            day_of_the_week = day_week.day_of_the_week
            med_speed = day_week.med_speed
            dict_for_day = dict(day_of_the_week=day_of_the_week, med_speed=med_speed)
        if dict_for_day != {}:
            list_all_winer.append(dict_for_day)
    list_day_week = list()
    for day_week in list_all_winer:
        list_day_week.append(day_week["day_of_the_week"])
    list_all_day_week_dont_winner = list()
    for day_week in all_day_week:
        if day_week.day_of_the_week not in list_day_week:
            list_all_day_week_dont_winner.append(day_week.day_of_the_week)
    list_day_mo = list()
    for winer in list_all_winer:
        activ_hours_winer = Active_Hour.objects.filter(day_of_the_week__day_of_the_week=winer["day_of_the_week"], app=app)
        for activ_hour in activ_hours_winer:
            active_day = activ_hour.active_day
            if active_day not in list_day_mo:
                list_day_mo.append(active_day)
    list_id_win = list()
    for win_id in list_day_mo:
        list_id_win.append(win_id.id)
    all_id_all_day = list()
    list_id_dont_win = list()
    all_day = Active_Day.objects.filter()
    for day_dont_win in all_day:
        if day_dont_win.id not in list_id_win:
            list_id_dont_win.append(day_dont_win.id)
    list_all_day_id = list()
    all_day = Active_Day.objects.filter()
    for day_all_for_id in all_day:
        list_all_day_id.append(day_all_for_id.id)

    all_day = Active_Day.objects.filter(id__in=list_all_day_id)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_all_day_id)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time = list()
    result_summ_1_1 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_1 = result_summ_1_1 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_1 = round(result_summ_1_1 * 1.01)
        ras_1_1 = round(result_summ_1_1 * 0.01)
        list_all_max_time.append(dict_for_save)

    all_day = Active_Day.objects.filter(id__in=list_id_win)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_id_win)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time_1_2 = list()
    result_summ_1_2 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_2 = result_summ_1_2 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_2 = round(result_summ_1_2 * 1.01)
        ras_1_2 = round(result_summ_1_2 * 0.01)
        list_all_max_time_1_2.append(dict_for_save)

    all_day = Active_Day.objects.filter(id__in=list_id_dont_win)
    list_sort_day_hour_summ = list()
    list_list_activ_hour = list()
    for day in all_day:
        all_hours_in_day = Active_Hour.objects.filter(app=app, active_day=day)
        list_hour = list()
        for hour in all_hours_in_day:
            active_hour = hour.active_hour
            if active_hour not in list_hour:
                list_hour.append(active_hour)
        list_hour = sorted(list_hour)
        if list_hour != []:
            list_list_activ_hour.append(list_hour)
        for hour in list_hour:
            hour_for_save = Active_Hour.objects.filter(app=app, active_day=day, active_hour=hour)
            summ_hour = 0
            for hour_for_save_in in hour_for_save:
                summ_hour = hour_for_save_in.order.revenue + summ_hour
            dict_for_day = dict(day=day.day, hour_for_save_in=hour_for_save_in.active_hour, summ_hour=summ_hour)
            if dict_for_day != {}:
                list_sort_day_hour_summ.append(dict_for_day)
    unic_list_hour = list()
    for list_element in list_list_activ_hour:
        for element in list_element:
            if element not in unic_list_hour:
                unic_list_hour.append(element)
    unic_list_hour = sorted(unic_list_hour)
    list_unic_list_hour = list()
    for element in unic_list_hour:
        dict_for_save = dict(hour_unic=element, summ=0)
        list_unic_list_hour.append(dict_for_save)
    all_day = Active_Day.objects.filter(id__in=list_id_dont_win)
    len_all_day = len(all_day)
    summ_for_koef = 0
    for element in list_sort_day_hour_summ:
        for elem in unic_list_hour:
            if elem == element["hour_for_save_in"]:
                for el in list_unic_list_hour:
                    if el["hour_unic"] == element["hour_for_save_in"]:
                        hour_unic = el["hour_unic"]
                        summ = el["summ"] + element["summ_hour"]
                        summ_for_koef = summ_for_koef + element["summ_hour"]
                        index_for_del = list_unic_list_hour.index(el)
                        list_unic_list_hour.pop(index_for_del)
                        dict_for_save = dict(hour_unic=hour_unic, summ=summ)
                        list_unic_list_hour.append(dict_for_save)
    koef_med_hour = summ_for_koef / len_all_day
    list_hour_max = list()
    for element in list_unic_list_hour:
        if element["summ"] > koef_med_hour:
            list_hour_max.append(element["hour_unic"])
    list_hour_max = sorted(list_hour_max)
    list_all_max_time_1_3 = list()
    result_summ_1_3 = 0
    for hour_max in list_hour_max:
        summ_for_one_hour = 0
        all_active_hours = Active_Hour.objects.filter(active_hour=hour_max, app=app, active_day__in=all_day)
        for elem in all_active_hours:
            summ_for_one_hour = elem.order.revenue + summ_for_one_hour
        result_summ_1_3 = result_summ_1_3 + summ_for_one_hour
        start_time = str(hour_max) + ":00"
        hour_max_end = hour_max + 1
        end_time = str(hour_max_end) + ":00"
        dict_for_save = dict(start_time=start_time, end_time=end_time, sum_one=summ_for_one_hour, sum_two=round(summ_for_one_hour * 1.01))
        sum_two_1_3 = round(result_summ_1_3 * 1.01)
        ras_1_3 = round(result_summ_1_3 * 0.01)
        list_all_max_time_1_3.append(dict_for_save)

    app = EB_App.objects.get(id=91)

    if "save_result_win" in request.POST:
        list_for_save_day = list()
        for element in list_all_winer:
            day = element["day_of_the_week"]
            list_for_save_day.append(day)

        list_for_save_hour = list()
        for element in list_all_max_time_1_2:
            start_time = element["start_time"]
            end_time = element["end_time"]
            sum_one = element["sum_one"]
            srez_start = int(start_time[0:2])
            srez_end = int(end_time[0:2])
            dict_for_day = dict(start=srez_start, end=srez_end, sum_one=int(sum_one))
            list_for_save_hour.append(dict_for_day)

        for element in list_for_save_day:
            if element == "Monday":
                day_create = Resume_Day_Week_Win.objects.create(Monday_day=True, app=app)
            if element == "Tuesday":
                day_create = Resume_Day_Week_Win.objects.create(Tuesday_day=True, app=app)
            if element == "Wednesday":
                day_create = Resume_Day_Week_Win.objects.create(Wednesday_day=True, app=app)
            if element == "Thursday":
                day_create = Resume_Day_Week_Win.objects.create(Thursday_day=True, app=app)
            if element == "Friday":
                day_create = Resume_Day_Week_Win.objects.create(Friday_day=True, app=app)
            if element == "Saturday":
                day_create = Resume_Day_Week_Win.objects.create(Saturday_day=True, app=app)
            if element == "Sunday":
                day_create = Resume_Day_Week_Win.objects.create(Sunday_day=True, app=app)

            for elem in list_for_save_hour:
                hour_start = elem["start"]
                hour_end = elem["end"]
                sum_one = elem["sum_one"]
                Resume_Hour_Win.objects.create(app=app, day=day_create, hour_start=hour_start, hour_end=hour_end, sum=int(sum_one))

    if "save_result_dont_win" in request.POST:
        list_for_save_day = list_all_day_week_dont_winner

        list_for_save_hour = list()
        for element in list_all_max_time_1_3:
            start_time = element["start_time"]
            end_time = element["end_time"]
            sum_one = element["sum_one"]
            srez_start = int(start_time[0:2])
            srez_end = int(end_time[0:2])
            dict_for_day = dict(start=srez_start, end=srez_end, sum_one=int(sum_one))
            list_for_save_hour.append(dict_for_day)

        for element in list_for_save_day:
            if element == "Monday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Monday_day=True, app=app)
            if element == "Tuesday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Tuesday_day=True, app=app)
            if element == "Wednesday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Wednesday_day=True, app=app)
            if element == "Thursday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Thursday_day=True, app=app)
            if element == "Friday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Friday_day=True, app=app)
            if element == "Saturday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Saturday_day=True, app=app)
            if element == "Sunday":
                day_create = Resume_Day_Week_Dont_Win.objects.create(Sunday_day=True, app=app)

            for elem in list_for_save_hour:
                hour_start = elem["start"]
                hour_end = elem["end"]
                sum_one = elem["sum_one"]
                Resume_Hour_Dont_Win.objects.create(app=app, day=day_create, hour_start=hour_start, hour_end=hour_end, sum=int(sum_one))

    return render(request, 're_data/jigsawpuzzle.html', locals())


def resume(request):
    print(request.POST)
    for_view = False

    if "find" in request.POST:
        request_for_search = request.POST
        day_week = request_for_search["day_week"]
        time_start = int(request_for_search["time_start"])
        time_end = int(request_for_search["time_end"])
        app_che = int(request_for_search["app_che"])
        app_che_for_view = app_che


        if time_start != time_end and time_start < time_end:
            time_start_re = time_start
            time_end_re = time_end
            list_hour_for_search = list()
            while time_start_re < time_end_re:
                list_hour_for_search.append(time_start_re)
                time_start_re = time_start_re + 1
            print("список часов в поиске - ", list_hour_for_search)

            all_active_hour = Active_Hour.objects.filter(active_hour__in=list_hour_for_search, day_of_the_week__day_of_the_week=day_week)

            list_app = list()
            for element in all_active_hour:
                if element.app not in list_app:
                    list_app.append(element.app)
            print("все приложения - ", list_app)

            list_app_summ = list()
            all_sum = 0
            for element in list_app:
                all_active_hour = Active_Hour.objects.filter(app=element, active_hour__in=list_hour_for_search,
                                                             day_of_the_week__day_of_the_week=day_week)
                sum = 0
                for hour in all_active_hour:
                    revenue = hour.order.revenue
                    sum = sum + revenue
                all_sum = all_sum + sum
                dict_for_save = dict(app=element, sum=sum)
                list_app_summ.append(dict_for_save)
            print("Список всех приложений - ", list_app_summ)
            print(all_sum)
            if all_sum != 0 or len(list_app) != 0:
                koef = all_sum / len(list_app)
                print(koef)

            result_win_no_sorted = list()
            list_sum_no_sorted = list()
            for element in list_app_summ:
                if element["sum"] > koef:
                    result_win_no_sorted.append(element)
                    list_sum_no_sorted.append(element["sum"])
            print("Список всх приложений привышающих коэффициент - ", result_win_no_sorted)
            print("Список сумм - ", list_sum_no_sorted)

            list_sum_sorted = sorted(list_sum_no_sorted, reverse=True)

            result_win_no_sorted_for_del = result_win_no_sorted

            list_wins = list()
            for element in list_sum_sorted:
                for elem in result_win_no_sorted:
                    if elem["sum"] == element and elem in result_win_no_sorted_for_del:
                        list_wins.append(elem)
                        index_for_del = result_win_no_sorted_for_del.index(elem)
                        result_win_no_sorted_for_del.pop(index_for_del)

            print(list_wins)

            len_list_wins = len(list_wins)
            if app_che > len_list_wins:
                app_che = len_list_wins

            index_elem = 0
            result = list()
            while index_elem < app_che:
                result.append(list_wins[index_elem])
                index_elem = index_elem + 1
            print(result)
            for_view = True













#         list_app = list()
#         for element in list_hour_for_search:
#             sum = 0
#             if day_week == "Monday":
#                 result_hours = Resume_Hour_Win.objects.filter(hour_start=element, day__Monday_day=True)
#             if day_week == "Tuesday":
#                 result_hours = Resume_Hour_Win.objects.filter(hour_start=element, day__Tuesday_day=True)
#             if day_week == "Wednesday":
#                 result_hours = Resume_Hour_Win.objects.filter(hour_start=element, day__Wednesday_day=True)
#             if day_week == "Thursday":
#                 result_hours = Resume_Hour_Win.objects.filter(hour_start=element, day__Thursday_day=True)
#             if day_week == "Friday":
#                 result_hours = Resume_Hour_Win.objects.filter(hour_start=element, day__Friday_day=True)
#             if day_week == "Saturday":
#                 result_hours = Resume_Hour_Win.objects.filter(hour_start=element, day__Saturday_day=True)
#             if day_week == "Sunday":
#                 result_hours = Resume_Hour_Win.objects.filter(hour_start=element, day__Sunday_day=True)
#
#             for elem in result_hours:
#                 if elem.app not in list_app:
#                     list_app.append(elem.app)
#         print(list_app)
#
#         all_apps_sum = list()
#         list_sum = list()
#         for element in list_app:
#             print("Приложение - ", element.name)
#             all_active_hour = Active_Hour.objects.filter(app=element, active_hour__in=list_hour_for_search, day_of_the_week__day_of_the_week=day_week)
#             sum = 0
#             for hour in all_active_hour:
#                 revenue = hour.order.revenue
#                 sum = sum + revenue
#             dict_for_save = dict(app=element, sum=sum)
#             all_apps_sum.append(dict_for_save)
#             list_sum.append(sum)
#         print("Словарь - ", all_apps_sum)
#         list_sum_sorted = sorted(list_sum, reverse=True)
#         print("Список сумм сортированный", list_sum_sorted)
#
#         list_app_result_no_del = list()
#         for element in list_sum_sorted:
#             for elem in all_apps_sum:
#                 if elem["sum"] == element:
#                     list_app_result_no_del.append(elem)
#         print("Список не сортированный - для удаления ", list_app_result_no_del)
#
#         len_list_app_result_no_del = len(list_app_result_no_del)
#         if app_che > len_list_app_result_no_del:
#             app_che = len_list_app_result_no_del
#
#         index_elem = 0
#         result = list()
#         while index_elem < app_che:
#             result.append(list_app_result_no_del[index_elem])
#             index_elem = index_elem + 1
#         print(result)
#
#
# # +++++++++++++++++++++++++++++++++++++++++++++++
#
#         list_app_low = list()
#         for element in list_hour_for_search:
#             sum = 0
#             if day_week == "Monday":
#                 result_hours_low = Resume_Hour_Dont_Win.objects.filter(hour_start=element, day__Monday_day=True)
#             if day_week == "Tuesday":
#                 result_hours_low = Resume_Hour_Dont_Win.objects.filter(hour_start=element, day__Tuesday_day=True)
#             if day_week == "Wednesday":
#                 result_hours_low = Resume_Hour_Dont_Win.objects.filter(hour_start=element, day__Wednesday_day=True)
#             if day_week == "Thursday":
#                 result_hours_low = Resume_Hour_Dont_Win.objects.filter(hour_start=element, day__Thursday_day=True)
#             if day_week == "Friday":
#                 result_hours_low = Resume_Hour_Dont_Win.objects.filter(hour_start=element, day__Friday_day=True)
#             if day_week == "Saturday":
#                 result_hours_low = Resume_Hour_Dont_Win.objects.filter(hour_start=element, day__Saturday_day=True)
#             if day_week == "Sunday":
#                 result_hours_low = Resume_Hour_Dont_Win.objects.filter(hour_start=element, day__Sunday_day=True)
#
#             for elem in result_hours_low:
#                 if elem.app not in list_app_low:
#                     list_app_low.append(elem.app)
#         print(list_app_low)
#
#         all_apps_sum_low = list()
#         list_sum_low = list()
#         for element in list_app_low:
#             all_active_hour_low = Active_Hour.objects.filter(app=element, active_hour__in=list_hour_for_search, day_of_the_week__day_of_the_week=day_week)
#             sum_low = 0
#             for hour in all_active_hour_low:
#                 revenue = hour.order.revenue
#                 sum_low = sum_low + revenue
#             dict_for_save_low = dict(app=element, sum=sum_low)
#             all_apps_sum_low.append(dict_for_save_low)
#             list_sum_low.append(sum_low)
#         print("Словарь - ", all_apps_sum_low)
#         list_sum_sorted_low = sorted(list_sum_low, reverse=True)
#         print("Список сумм сортированный", list_sum_sorted_low)
#
#         list_app_result_no_del_low = list()
#         for element in list_sum_sorted_low:
#             for elem in all_apps_sum_low:
#                 if elem["sum"] == element:
#                     list_app_result_no_del_low.append(elem)
#         print("Список не сортированный - для удаления ", list_app_result_no_del_low)
#
#         len_list_app_result_no_del_low = len(list_app_result_no_del_low)
#         if app_che > len_list_app_result_no_del_low:
#             app_che = len_list_app_result_no_del_low
#
#         index_elem = 0
#         result_low = list()
#         while index_elem < app_che:
#             result_low.append(list_app_result_no_del_low[index_elem])
#             index_elem = index_elem + 1
#         print(result_low)

    return render(request, 're_data/resume.html', locals())