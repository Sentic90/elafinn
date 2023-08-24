import random
import string
from django.dispatch import receiver
from django.db.models.signals import post_save
from geopy.distance import distance as geopy_distance
from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from PIL import Image
from django.urls import reverse
from django.template.defaultfilters import slugify
from core.models import Notification

Admin = get_user_model()

NATIONALITY = (
    ("ALL", "ALL"),
    ("AF", "Afghanistan"),
    ("AL", "Albania"),
    ("DZ", "Algeria"),
    ("AS", "American Samoa"),
    ("AD", "Andorra"),
    ("AO", "Angola"),
    ("AI", "Anguilla"),
    ("AQ", "Antarctica"),
    ("AG", "Antigua and Barbuda"),
    ("AR", "Argentina"),
    ("AM", "Armenia"),
    ("AW", "Aruba"),
    ("AU", "Australia"),
    ("AT", "Austria"),
    ("AZ", "Azerbaijan"),
    ("BS", "Bahamas (the)"),
    ("BH", "Bahrain"),
    ("BD", "Bangladesh"),
    ("BB", "Barbados"),
    ("BY", "Belarus"),
    ("BE", "Belgium"),
    ("BZ", "Belize"),
    ("BJ", "Benin"),
    ("BM", "Bermuda"),
    ("BT", "Bhutan"),
    ("BO", "Bolivia (Plurinational State of)"),
    ("BQ", "Bonaire, Sint Eustatius and Saba"),
    ("BA", "Bosnia and Herzegovina"),
    ("BW", "Botswana"),
    ("BV", "Bouvet Island"),
    ("BR", "Brazil"),
    ("IO", "British Indian Ocean Territory (the)"),
    ("BN", "Brunei Darussalam"),
    ("BG", "Bulgaria"),
    ("BF", "Burkina Faso"),
    ("BI", "Burundi"),
    ("CV", "Cabo Verde"),
    ("KH", "Cambodia"),
    ("CM", "Cameroon"),
    ("CA", "Canada"),
    ("KY", "Cayman Islands (the)"),
    ("CF", "Central African Republic (the)"),
    ("TD", "Chad"),
    ("CL", "Chile"),
    ("CN", "China"),
    ("CX", "Christmas Island"),
    ("CC", "Cocos (Keeling) Islands (the)"),
    ("CO", "Colombia"),
    ("KM", "Comoros (the)"),
    ("CD", "Congo (the Democratic Republic of the)"),
    ("CG", "Congo (the)"),
    ("CK", "Cook Islands (the)"),
    ("CR", "Costa Rica"),
    ("HR", "Croatia"),
    ("CU", "Cuba"),
    ("CW", "Curaçao"),
    ("CY", "Cyprus"),
    ("CZ", "Czechia"),
    ("CI", "Côte d'Ivoire"),
    ("DK", "Denmark"),
    ("DJ", "Djibouti"),
    ("DM", "Dominica"),
    ("DO", "Dominican Republic (the)"),
    ("EC", "Ecuador"),
    ("EG", "Egypt"),
    ("SV", "El Salvador"),
    ("GQ", "Equatorial Guinea"),
    ("ER", "Eritrea"),
    ("EE", "Estonia"),
    ("SZ", "Eswatini"),
    ("ET", "Ethiopia"),
    ("FK", "Falkland Islands (the) [Malvinas]"),
    ("FO", "Faroe Islands (the)"),
    ("FJ", "Fiji"),
    ("FI", "Finland"),
    ("FR", "France"),
    ("GF", "French Guiana"),
    ("PF", "French Polynesia"),
    ("TF", "French Southern Territories (the)"),
    ("GA", "Gabon"),
    ("GM", "Gambia (the)"),
    ("GE", "Georgia"),
    ("DE", "Germany"),
    ("GH", "Ghana"),
    ("GI", "Gibraltar"),
    ("GR", "Greece"),
    ("GL", "Greenland"),
    ("GD", "Grenada"),
    ("GP", "Guadeloupe"),
    ("GU", "Guam"),
    ("GT", "Guatemala"),
    ("GG", "Guernsey"),
    ("GN", "Guinea"),
    ("GW", "Guinea-Bissau"),
    ("GY", "Guyana"),
    ("HT", "Haiti"),
    ("HM", "Heard Island and McDonald Islands"),
    ("VA", "Holy See (the)"),
    ("HN", "Honduras"),
    ("HK", "Hong Kong"),
    ("HU", "Hungary"),
    ("IS", "Iceland"),
    ("IN", "India"),
    ("ID", "Indonesia"),
    ("IR", "Iran (Islamic Republic of)"),
    ("IQ", "Iraq"),
    ("IE", "Ireland"),
    ("IM", "Isle of Man"),
    ("IL", "Israel"),
    ("IT", "Italy"),
    ("JM", "Jamaica"),
    ("JP", "Japan"),
    ("JE", "Jersey"),
    ("JO", "Jordan"),
    ("KZ", "Kazakhstan"),
    ("KE", "Kenya"),
    ("KI", "Kiribati"),
    ("KP", "Korea (the Democratic People's Republic of)"),
    ("KR", "Korea (the Republic of)"),
    ("KW", "Kuwait"),
    ("KG", "Kyrgyzstan"),
    ("LA", "Lao People's Democratic Republic (the)"),
    ("LV", "Latvia"),
    ("LB", "Lebanon"),
    ("LS", "Lesotho"),
    ("LR", "Liberia"),
    ("LY", "Libya"),
    ("LI", "Liechtenstein"),
    ("LT", "Lithuania"),
    ("LU", "Luxembourg"),
    ("MO", "Macao"),
    ("MG", "Madagascar"),
    ("MW", "Malawi"),
    ("MY", "Malaysia"),
    ("MV", "Maldives"),
    ("ML", "Mali"),
    ("MT", "Malta"),
    ("MH", "Marshall Islands (the)"),
    ("MQ", "Martinique"),
    ("MR", "Mauritania"),
    ("MU", "Mauritius"),
    ("YT", "Mayotte"),
    ("MX", "Mexico"),
    ("FM", "Micronesia (Federated States of)"),
    ("MD", "Moldova (the Republic of)"),
    ("MC", "Monaco"),
    ("MN", "Mongolia"),
    ("ME", "Montenegro"),
    ("MS", "Montserrat"),
    ("MA", "Morocco"),
    ("MZ", "Mozambique"),
    ("MM", "Myanmar"),
    ("NA", "Namibia"),
    ("NR", "Nauru"),
    ("NP", "Nepal"),
    ("NL", "Netherlands (the)"),
    ("NC", "New Caledonia"),
    ("NZ", "New Zealand"),
    ("NI", "Nicaragua"),
    ("NE", "Niger (the)"),
    ("NG", "Nigeria"),
    ("NU", "Niue"),
    ("NF", "Norfolk Island"),
    ("MP", "Northern Mariana Islands (the)"),
    ("NO", "Norway"),
    ("OM", "Oman"),
    ("PK", "Pakistan"),
    ("PW", "Palau"),
    ("PS", "Palestine, State of"),
    ("PA", "Panama"),
    ("PG", "Papua New Guinea"),
    ("PY", "Paraguay"),
    ("PE", "Peru"),
    ("PH", "Philippines (the)"),
    ("PN", "Pitcairn"),
    ("PL", "Poland"),
    ("PT", "Portugal"),
    ("PR", "Puerto Rico"),
    ("QA", "Qatar"),
    ("MK", "Republic of North Macedonia"),
    ("RO", "Romania"),
    ("RU", "Russian Federation (the)"),
    ("RW", "Rwanda"),
    ("RE", "Réunion"),
    ("BL", "Saint Barthélemy"),
    ("SH", "Saint Helena, Ascension and Tristan da Cunha"),
    ("KN", "Saint Kitts and Nevis"),
    ("LC", "Saint Lucia"),
    ("MF", "Saint Martin (French part)"),
    ("PM", "Saint Pierre and Miquelon"),
    ("VC", "Saint Vincent and the Grenadines"),
    ("WS", "Samoa"),
    ("SM", "San Marino"),
    ("ST", "Sao Tome and Principe"),
    ("SA", "Saudi Arabia"),
    ("SN", "Senegal"),
    ("RS", "Serbia"),
    ("SC", "Seychelles"),
    ("SL", "Sierra Leone"),
    ("SG", "Singapore"),
    ("SX", "Sint Maarten (Dutch part)"),
    ("SK", "Slovakia"),
    ("SI", "Slovenia"),
    ("SB", "Solomon Islands"),
    ("SO", "Somalia"),
    ("ZA", "South Africa"),
    ("GS", "South Georgia and the South Sandwich Islands"),
    ("SS", "South Sudan"),
    ("ES", "Spain"),
    ("LK", "Sri Lanka"),
    ("SD", "Sudan (the)"),
    ("SR", "Suriname"),
    ("SJ", "Svalbard and Jan Mayen"),
    ("SE", "Sweden"),
    ("CH", "Switzerland"),
    ("SY", "Syrian Arab Republic"),
    ("TW", "Taiwan"),
    ("TJ", "Tajikistan"),
    ("TZ", "Tanzania, United Republic of"),
    ("TH", "Thailand"),
    ("TL", "Timor-Leste"),
    ("TG", "Togo"),
    ("TK", "Tokelau"),
    ("TO", "Tonga"),
    ("TT", "Trinidad and Tobago"),
    ("TN", "Tunisia"),
    ("TR", "Turkey"),
    ("TM", "Turkmenistan"),
    ("TC", "Turks and Caicos Islands (the)"),
    ("TV", "Tuvalu"),
    ("UG", "Uganda"),
    ("UA", "Ukraine"),
    ("AE", "United Arab Emirates (the)"),
    ("GB", "United Kingdom of Great Britain and Northern Ireland (the)"),
    ("UM", "United States Minor Outlying Islands (the)"),
    ("US", "United States of America (the)"),
    ("UY", "Uruguay"),
    ("UZ", "Uzbekistan"),
    ("VU", "Vanuatu"),
    ("VE", "Venezuela (Bolivarian Republic of)"),
    ("VN", "Viet Nam"),
    ("VG", "Virgin Islands (British)"),
    ("VI", "Virgin Islands (U.S.)"),
    ("WF", "Wallis and Futuna"),
    ("EH", "Western Sahara"),
    ("YE", "Yemen"),
    ("ZM", "Zambia"),
    ("ZW", "Zimbabwe"),
    ("AX", "Åland Islands")
)
BANK_CHOICE = (
    (1, 'البنك الأهلي التجاري'),
    (2, 'البنك السعودي البريطاني'),
    (3, 'البنك السعودي الفرنسي'),
    (4, 'البنك الأول'),
    (5, 'البنك السعودي للاستثمار'),
    (6, 'البنك العربي الوطني'),
    (7, 'بنك البلاد'),
    (8, 'بنك الجزيرة'),
    (9, 'بنك الرياض'),
    (10, 'مجموعة سامبا المالية (سامبا)'),
    (11, 'مصرف الراجحي'),
    (12, 'مصرف الإنماء'),
)

CATEGORY = (
    (1, 'نجمة'),
    (2, 'نجمتان'),
    (3, '3 نجوم'),
    (4, '4 نجوم'),
    (5, '5 نجوم'),
    (6, 'شقق مخدومة'),
    (7, 'غير مصنف'),
)

CITY = (
    ('Makkah', 'مكة المكرمة'),
    ('Madinah', 'المدينة المنورة'),
)

CANCELLATION = (
    (1, 'مستردة'),
    (2, 'غير مستردة'),
)

CANCELLATION_HOURS = (
    (1, '24 ساعة'),
    (2, '48 ساعة'),
    (3, '72 ساعة'),
)

RTYPE = (
    (1, 'مفردة'),
    (2, 'ثنائية'),
    (3, 'ثلاثية'),
    (4, 'رباعية'),
    (5, 'خماسية'),
    (6, 'سداسية'),
)

ELECTRIC = (
    ('1', 'تلفزيون'),
    ('2', 'فرن'),
    ('3', 'ميكرويف'),
    ('4', 'غسالة'),
    ('5', 'مكواة'),
    ('6', 'غلاية شاهي'),
    ('7', 'ثلاجة'),
)

FACILITIES = (
    ('1', 'مطبخ'),
    ('2', 'غرفة غسيل'),
    ('3', 'بانيو/ جاكوزي'),
)
SERVICES = (
    ('1', 'واي فاي'),
    ('2', 'خدمة الغسيل'),
    ('3', 'خدمة الغرف'),
)
STATUS = (
    (1, 'غير مفعلة'),
    (2, 'متاحة'),
    (3, 'انتظار'),
    (4, 'محجوزة'),
)
RENT_STATUS = (
    (1, 'ملغي'),
    (2, 'متاح لاستقبال الطلبات'),
    (3, 'قيد إجراءات التأجير'),
    (4, 'تم التأجير'),
)
VIEW = (
    (1, 'إطلالة كاملة على الحرم'),
    (2, 'إطلالة جزئية على الحرم'),
    (3, 'إطلالة على المدينة'),
    (4, 'غير مطلة'),
)



def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


# Create your models here.
class Hotel(models.Model):
    user = models.ForeignKey(
        Admin, on_delete=models.CASCADE, verbose_name='اسم المالك')
    hotel_name = models.CharField(max_length=200, verbose_name='اسم الفندق')
    city = models.CharField(
        max_length=200, choices=CITY, verbose_name='المدينة')
    address = models.CharField(
        max_length=200, verbose_name='العنوان', blank=True, null=True)
    tel = models.CharField(
        max_length=200, verbose_name='رقم الهاتف', blank=True, null=True)
    mobile = models.CharField(
        max_length=200, verbose_name='رقم الجوال', blank=True, null=True)
    category = models.IntegerField(choices=CATEGORY, verbose_name='التصنيف')
    Cancellation_policy = models.IntegerField(
        choices=CANCELLATION, verbose_name='سياسة الإلغاء', blank=True, null=True)
    Cancellation_hours = models.IntegerField(
        choices=CANCELLATION_HOURS, verbose_name='إلغاء الحجز بعد', blank=True, null=True)
    Check_in = models.CharField(
        max_length=100, verbose_name='سياسة وقت الدخول', blank=True, null=True)
    Check_out = models.CharField(
        max_length=100, verbose_name='سياسة وقت الخروج', blank=True, null=True)
    nationality = CountryField(multiple=True, verbose_name='جنسية الضيوف')
    is_priority = models.BooleanField(default=False, verbose_name='أولوية؟')
    about_hotel = models.TextField(
        verbose_name='نبذة عن الفندق', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    logo = models.ImageField(upload_to='images/gallery/',
                             null=True, blank=True, verbose_name='صورة رمزية')
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True, unique=True)
    vat = models.FloatField(verbose_name="ضريبة القيمة المضافة", default=7)
    location = models.OneToOneField(
        to='HotelLocation', on_delete=models.CASCADE, verbose_name='الموقع', 
        blank=True, null=True, related_name='hotels')
    
    def __str__(self):
        return self.hotel_name

    def save(self,  *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + self.hotel_name)
        super().save(*args, **kwargs)
        img = Image.open(self.logo.path)
        img = img.resize((640, 480))
        img.save(self.logo.path)

    class Meta:
        ordering = ['-is_priority']

    def get_absolute_url(self):
        return reverse("hotel_dashboard", kwargs={"slug": self.slug})

    def get_hotel_page(self):
        return reverse('main:hotel_detail', kwargs={"slug": self.slug})

    @property
    def rooms(self):
        """"
            return: QuerySet (avaliable rooms)
        
        """
        return self.room_set.filter(status=2)
    @property 
    def total_room(self):
        """"
            return: Number (total avaliable rooms)
        
        """
        return self.room_set.filter(status=2).count()

    @property
    def total_capacity(self):
        """"
            return: Number (total guests capacity including booked room)
        
        """
        return self.room_set.all().aggregate(total_capacity=models.Sum('capacity'))['total_capacity']

    @property 
    def accomadate_space(self):
        """"
            return: Number (total guests capacity avaliable )
        
        """
        return self.room_set.filter(status=2).aggregate(accomadate_space=models.Sum('capacity'))['accomadate_space']


class HotelLocation(models.Model):
    latitude = models.FloatField(blank=True, verbose_name='Latitude')
    longitude = models.FloatField(blank=True, verbose_name='Longitude')
    hrm = models.FloatField(
        verbose_name='المسافة عن الحرم', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):TODO
    #     if self.latitude and self.longitude:
    #         hrm_coordinates_makkah = (21.4230884, 39.8305041)
    #         hrm_coordinates_madinah = (24.4672018, 39.6156392)

    #         if self.hotel.city == 'Makkah':
    #             hrm_coordinates = hrm_coordinates_makkah
    #         elif self.hotel.city == 'Madinah':
    #             hrm_coordinates = hrm_coordinates_madinah

    #         hotel_coordinates = (self.latitude, self.longitude)
    #         distance_km = geopy_distance(hrm_coordinates, hotel_coordinates).kilometers
    #         self.hrm = format(distance_km, '.2f')

    #     super().save(*args, **kwargs)
    def __str__(self):
        return str(self.hrm)+ 'كم'
    @property
    def hotel(self):
        return self.hotels
    # def get_absolute_url(self):
    #     return reverse("update_hotel_location", kwargs={"slug": self.hotel.slug, "pk": self.pk})

    class Meta:
        ordering = ['-hrm']


class HotelMultipleImage(models.Model):
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, verbose_name='اسم الفندق')
    images = models.FileField(upload_to='images/hotel_images')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.date)


class RoomType(models.Model):
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, verbose_name='اسم الفندق')
    roomType = models.IntegerField(
        default=1, choices=RTYPE, blank=True, verbose_name='نوع الغرفة')
    # Delete
    # NoOfRoom = models.IntegerField(blank=True, verbose_name='عدد الغرف من هذا النوع')
    capacity = models.IntegerField(
        blank=True, verbose_name='عدد استيعاب الغرفة للأشخاص من هذا النوع')
    Electric = MultiSelectField(choices=ELECTRIC, max_choices=7,
                                max_length=10, null=True, verbose_name='الأجهزة الكهربائية')
    Facilities = MultiSelectField(
        choices=FACILITIES, max_choices=3, max_length=10, null=True, verbose_name='المرافق')
    Services = MultiSelectField(choices=SERVICES, max_choices=3,
                                max_length=10, null=True,  verbose_name='الخدمات المجانية')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_roomType_display()

    def get_absolute_url(self):
        return reverse("room_type_detail", kwargs={"slug": self.hotel.slug, "pk": self.pk})


class Room(models.Model):
    roomType = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, verbose_name='نوع الغرفة')
    roomNo = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='رقم الغرفة')
    floor = models.CharField(max_length=250, blank=True,
                             null=True, verbose_name='رقم الطابق')
    capacity = models.IntegerField(
        blank=True, verbose_name='عدد استيعاب الغرفة للأشخاص من هذا النوع')
    Electric = MultiSelectField(choices=ELECTRIC, max_choices=7,
                                max_length=10, null=True, verbose_name='الأجهزة الكهربائية')
    Facilities = MultiSelectField(
        choices=FACILITIES, max_choices=3, max_length=10, null=True, verbose_name='المرافق')
    Services = MultiSelectField(choices=SERVICES, max_choices=3,
                                max_length=10, null=True,  verbose_name='الخدمات المجانية')
    status = models.IntegerField(
        default=2, choices=STATUS, blank=True, verbose_name='حالة الغرفة')
    is_mine = models.BooleanField(default=True, verbose_name='تحت إدارتي؟')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,
                              verbose_name='مالك الغرفة', blank=True, null=True)
    is_view  = models.IntegerField(
        choices=VIEW, blank=True, null=True, verbose_name='الإطلالة') #TODO
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    price = models.FloatField(verbose_name='سعر الغرفة')
    # Owner --> The room can be rented by someone
    def __str__(self):
        return self.roomNo

    def get_absolute_url(self):
        return reverse("room_detail", kwargs={"slug": self.roomType.hotel.slug, "pk": self.pk})

SEASON_TYPE = (
    (1, 'موسم الحج'),
    (2, 'موسم رمضان'),
    (3, 'موسم الزيارة والعمرة'),

)


class Season(models.Model):
    season = models.CharField(max_length=250, verbose_name='الموسم')
    startDate = models.DateField(verbose_name='بداية الموسم')
    endDate = models.DateField(verbose_name='نهاية الموسم')
    year = models.PositiveIntegerField(verbose_name='للعام')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.season + ' -' + str(self.year)


class SeasonPrice(models.Model):
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, verbose_name='الموسم')
    roomType = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, verbose_name='نوع الغرفة')
    price = models.CharField(max_length=250, verbose_name='السعر')

    def __str__(self):
        return self.season.season + ' - ' + self.roomType.hotel.hotel_name

    def get_absolute_url(self):
        return reverse("season_price_detail", kwargs={"slug": self.roomType.hotel.slug, "pk": self.pk})


class AnnualRent(models.Model):
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, verbose_name='اسم الفندق')
    rooms = models.ManyToManyField(
        Room, verbose_name='الغرف', related_name='rooms')
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, verbose_name='الموسم')
    price = models.CharField(max_length=250, verbose_name='السعر')
    status = models.IntegerField(
        default=2, choices=RENT_STATUS, blank=True, verbose_name='حالة الغرفة')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hotel.hotel_name + ' - ' + self.season.season

    def get_absolute_url(self):
        return reverse("update_annual_rent", kwargs={"slug": self.hotel.slug, "pk": self.pk})


BOOKING_STATUS = (
    ("pending", 'بانتظار الدفع'),
    ("processed", "تم الحجز"),
    ("rejected", "مرفوض")
)

GENDER_TYPE = (
    ('Male', 'ذكر'),
    ("Female", 'انثى')
)


class Booking(models.Model):
    customer = models.ForeignKey(to='customer.Customer', on_delete=models.CASCADE, verbose_name='العميل')
    hotel = models.ForeignKey(
        to=Hotel, on_delete=models.CASCADE, verbose_name="الفندق")
    vat = models.FloatField(verbose_name="ضريبة القيمة المضافة", default=7)
    total_price_with_vat = models.FloatField(
        verbose_name="الاجمالي مع القيمة المضافة", default=0)
    coupon = models.FloatField(verbose_name="كوبون خصم", default=1)
    room = models.ManyToManyField(to=Room,verbose_name="الغرفة")
    status = models.CharField(
        choices=BOOKING_STATUS, verbose_name="حالة الطلب", max_length=50, default="pending")
    guests = models.PositiveIntegerField(verbose_name='عدد الضيوف', default=1)
    nationality = models.CharField(choices=NATIONALITY,max_length=3,verbose_name="جنسية الضيوف", default='ALL')
    notes = models.TextField(null=True, blank=True,verbose_name='ملاحظات')
    # docuemnts
    document = models.FileField(upload_to='documents/', null=True, blank=True, verbose_name='المستندات')
    payment_receipt = models.FileField(upload_to='payments_receipts/',null=True, blank=True, verbose_name='ايصال الدفع')
    # date
    start_date = models.DateField(verbose_name='تاريخ الوصول')
    end_date = models.DateField(verbose_name='تاريخ المغادرة')

    package = models.ForeignKey(to=Season, on_delete=models.CASCADE,verbose_name='الباقة')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="تاريخ الطلب")
    updated = models.DateTimeField(auto_now=True)


CURRENCY_CODE = (
    ('SAR', 'SAR'),
    ('USD', 'USD'),
    ('EUR', 'EUR'),
)

PAYMENT_STATUS = (
    ('active', 'نشطة'),
    ('inactive','معطلة')
)
PAYMENT_TYPE=(
    (100, 'تحويل بنكي'),
    (200, 'دفع عند الوصول'),
)

REQUEST_STATUS = (
('pending', 'في الانتظار'),
('accepted', 'مقبول'),
('rejected', 'مرفوض'),
)
class Request(models.Model):
    customer = models.ForeignKey(to='customer.Customer', on_delete=models.CASCADE, verbose_name='العميل')
    hotel = models.ForeignKey(
        to=Hotel, on_delete=models.CASCADE, verbose_name="الفندق")
    vat = models.FloatField(verbose_name="ضريبة القيمة المضافة", default=7)
    total_price_with_vat = models.FloatField(
        verbose_name="الاجمالي مع القيمة المضافة", default=0)
    coupon = models.FloatField(verbose_name="كوبون خصم", default=1)
    room = models.ManyToManyField(to=Room,verbose_name="الغرفة")
    status = models.CharField(
        choices=REQUEST_STATUS, verbose_name="حالة الطلب", max_length=50, default="pending")
    guests = models.PositiveIntegerField(verbose_name='عدد الضيوف', default=1)
    nationality = models.CharField(choices=NATIONALITY,max_length=3,verbose_name="جنسية الضيوف", default='ALL')
    notes = models.TextField(null=True, blank=True,verbose_name='ملاحظات')
    # date
    start_date = models.DateField(verbose_name='تاريخ الوصول')
    end_date = models.DateField(verbose_name='تاريخ المغادرة')

    package = models.ForeignKey(to=Season, on_delete=models.CASCADE,verbose_name='الباقة')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="تاريخ الطلب")
    updated = models.DateTimeField(auto_now=True)


    def accept_and_create_booking(self):
        if self.status == 'accepted':
            try:
                booking = Booking.objects.create(
                customer=self.customer,
                hotel=self.hotel,
                vat=self.vat,
                total_price_with_vat=self.total_price_with_vat,
                coupon=self.coupon,
                guests = self.guests,
                nationality = self.nationality,
                notes = self.notes,
                start_date = self.start_date,
                end_date = self.end_date,
                package = self.package,

                status='pending'
            )
                booking.room.set(self.room.all())

                # notifications 
                Notification.objects.create(
                    recipient=self.customer.user,
                    message='تم قبول الطلب بنجاح في انتظار الدفع'
                )
                return booking
            except:
                return None
        return None

@receiver(post_save, sender=Request)
def create_booking_from_request(sender, instance, **kwargs):
    if instance.status == 'accepted':
        instance.accept_and_create_booking()

# class PaymentMethodQuerySet(models.query.QuerySet):
#     def active(self):
#         return self.filter(status='active')

# class PaymentMethodManager(models.Manager):

#     def get_queryset(self):
#         return PaymentMethodQuerySet(self.model, using=self._db)

#     def all(self):
#         return self.get_queryset().active()


class PaymentMethod(models.Model):
    bank_name = models.CharField(max_length=250, verbose_name='اسم البنك', null=True, blank=True)
    ipan = models.CharField(max_length=250, verbose_name='رقم ألاي بان',null=True, blank=True)
    swifit_code = models.CharField(max_length=15, verbose_name='سويفت كود',null=True, blank=True)
    currency = models.CharField(choices=CURRENCY_CODE,max_length=3, verbose_name='العملة',null=True, blank=True)
    status = models.CharField(choices=PAYMENT_STATUS,max_length=32,
        verbose_name="حالة وسيلة الدفع")
    type = models.IntegerField(choices=PAYMENT_TYPE,verbose_name='نوع وسيلة الدفع')
    hotel = models.ForeignKey(
        to=Hotel, on_delete=models.CASCADE,related_name='payment_methods', verbose_name="الفندق")
    
    # objects = PaymentMethodManager()
    def __str__(self) -> str:
        return self.hotel.hotel_name


# class Reservation(models.Model):
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     start_date = models.DateField()
#     end_date = models.DateField()
#
#     def __str__(self):
#         return f"{self.room} ({self.start_date} to {self.end_date})"
