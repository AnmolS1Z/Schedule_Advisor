import requests
from django.core.management.base import BaseCommand
from schedule_advisor.models import Course, Meeting, Instructor


def get_courses():
    url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232"
    data = []
    i = 1
    r = requests.get(url + '&page=%s' % i, headers={'Content-Type': 'application/json'})
    print('Getting Courses')
    while r.text != '[]':
        data.append(r.json())
        i += 1
        r = requests.get(url + '&page=%s' % i, headers={'Content-Type': 'application/json'})
    print(f'{i} total pages')
    return data


def clear_data():
    Course.objects.all().delete()
    Meeting.objects.all().delete()
    Instructor.objects.all().delete()


def seed_courses():
    clear_data()
    data = get_courses()
    for datum in data:
        for i in datum:
            course_data = None
            if Course.objects.filter(subject=i['subject'], class_nbr=i['class_nbr'],
                                     catalog_number=i['catalog_nbr'], term=i['strm']).exists():
                course_data = Course.objects.filter(subject=i['subject'], class_nbr=i['class_nbr'],
                                                    catalog_number=i['catalog_nbr'], term=i['strm'])[0]
            else:
                course_data = Course(
                    crse_id=i['crse_id'],
                    descr=i['descr'],
                    subject=i['subject'],
                    class_capacity=i['class_capacity'],
                    class_section=i['class_section'],
                    class_nbr=i['class_nbr'],
                    units=i['units'],
                    term=i['strm'],
                    instruction_mode=i['instruction_mode'],
                    enrollment=i['enrollment_total'],
                    catalog_number=i['catalog_nbr'],
                    section_type=i['section_type']
                )
                course_data.save()
            for instructor in i['instructors']:
                if Instructor.objects.filter(email=instructor['email']).exists():
                    course_data.instructors.add(Instructor.objects.filter(email=instructor['email'])[0])
                else:
                    ob = Instructor.objects.create(
                        name=instructor['name'],
                        email=instructor['email']
                    )
                    ob.save()
                    course_data.instructors.add(ob)
            for meet in i['meetings']:
                stime = meet['start_time'][:5]
                stime = stime[:2] + ':' + stime[3:]
                etime = meet['end_time'][:5]
                etime = etime[:2] + ':' + etime[3:]
                if Meeting.objects.filter(days=meet['days'], st_time=stime, end_time=etime,
                                          building=('N/A' if ('bldg_cd' not in meet.keys()) else meet['bldg_cd']),
                                          room=('N/A' if ('room' not in meet.keys()) else meet['room']),
                                          st_date=meet['start_dt'],
                                          end_date=meet['end_dt']).exists():
                    course_data.meeting.add(Meeting.objects.filter(days=meet['days'], st_time=stime, end_time=etime,
                                                                   building=(
                                                                       'N/A' if ('bldg_cd' not in meet.keys()) else
                                                                       meet['bldg_cd']),
                                                                   room=('N/A' if ('room' not in meet.keys()) else
                                                                         meet['room']),
                                                                   st_date=meet['start_dt'],
                                                                   end_date=meet['end_dt'])[0])
                else:
                    ob = Meeting(
                        days=meet['days'],
                        st_time=stime,
                        end_time=etime,
                        building=('N/A' if ('bldg_cd' not in meet.keys()) else meet['bldg_cd']),
                        room=('N/A' if ('room' not in meet.keys()) else meet['room']),
                        st_date=meet['start_dt'],
                        end_date=meet['end_dt']
                    )
                    ob.save()
                    course_data.meeting.add(ob)
            course_data.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('started')
        seed_courses()
        # clear_data()
        print("completed")
