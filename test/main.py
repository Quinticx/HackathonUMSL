from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy_garden.mapview import MapSource, MapView
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem, MDList
from kivy_garden.mapview import MapSource, MapView, MapMarker
from kivymd.theming import ThemableBehavior
from kivy.clock import mainthread
from kivy.utils import platform
from plyer import gps
from kivy.clock import Clock


class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


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
            gps.start(1000, 0)
            self.root.ids.mapview.add_marker(
                MapMarker(lat=38.718775, lon=-90.329539)
            )

            Clock.schedule_interval(self.streak_callback, 30)

    def streak_callback(self, dt):
        print("YES THE CALLBACK IS RUNNING")
        print(dt)

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
