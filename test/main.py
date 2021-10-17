from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy_garden.mapview import MapSource, MapView
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem, MDList
from kivy.uix.button import Button
from kivy_garden.mapview import MapSource, MapView, MapMarker
from kivymd.theming import ThemableBehavior
from kivy.clock import mainthread
from kivy.utils import platform
from plyer import gps
from kivy.clock import Clock


class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class PinButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Add Pin"

    def addpin(self):
        mapview =MDApp.get_running_app().root.ids.mapviewpin
        m1 = MapMarker(lat = mapview.lat, lon = mapview.lon, source = "marker.png")
        mapview.add_marker(m1)



class TestNavigationDrawer(MDApp):
    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission

        request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION])


    def build(self):
        try:
            gps.configure(on_location=self.location_update,
            on_status=self.status_update)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.status_update("GPS Not Implemented")

        if platform == "android":
            print("Android! Requesting Permissions")
            self.request_android_permissions()

        return Builder.load_file("layout.kv")

    def on_start(self):
        if platform == "android":
            self.streak = 0
            gps.start(1000, 0)
            self.root.ids.mapview.add_marker(
                MapMarker(lat=38.718775, lon=-90.329539)
            )

            Clock.schedule_interval(self.streak_callback, 30)

    def streak_callback(self, dt):
        self.streak += 1
        if (self.streak < 6):
            self.root.ids["day" + str(self.streak)].source = "star.png"

    @mainthread
    def location_update(self, **kwargs):
        print("GPS INFORMATION")
        print('\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()]))
        self.lat = kwargs['lat']
        self.lon = kwargs['lon']
        self.root.ids.mapview.center_on(self.lat, self.lon)


    @mainthread
    def status_update(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

TestNavigationDrawer().run()
