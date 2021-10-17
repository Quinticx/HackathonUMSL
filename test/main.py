from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy_garden.mapview import MapSource, MapView
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.button import Button
from kivy_garden.mapview import MapSource, MapView, MapMarker
from kivymd.theming import ThemableBehavior
from kivy.clock import mainthread
from kivy.utils import platform
from plyer import gps
from kivy.clock import Clock
import math


mapPins = []

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

    def update_second_map_pos(self):
        app = MDApp.get_running_app()
        app.root.ids.mapviewpin.center_on(app.root.ids.mapview.lat, app.root.ids.mapview.lon)
        app.personLocatorPin.lat = app.lat
        app.personLocatorPin.lon = app.lon


class PinButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Add Pin"

    def addpin(self):
        root = MDApp.get_running_app().root
        m1 = MapMarker(lat = root.ids.mapviewpin.lat, lon = root.ids.mapviewpin.lon, source = "marker.png")
        m2 = MapMarker(lat = root.ids.mapviewpin.lat, lon = root.ids.mapviewpin.lon, source = "marker.png")
        root.ids.mapview.add_marker(m1)
        root.ids.mapviewpin.add_marker(m2)
        mapPins.append(m1) #if we planned on removing them later we should append both of them, maybe as a tuple or something


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
        self.insideMarkerRadius = False
        self.personLocator = MapMarker(source="person.png", lat = 0, lon = 0)
        self.personLocatorPin = MapMarker(source="person.png", lat = 0, lon = 0)
        self.root.ids.mapview.add_marker(self.personLocator)
        self.root.ids.mapviewpin.add_marker(self.personLocatorPin)

        if platform == "android":
            self.streak = 0
            gps.start(1000, 0)
            Clock.schedule_interval(self.streak_callback, 10) # 10 seconds as a testing value

    def streak_callback(self, dt):
        if (not self.insideMarkerRadius):
            self.streak += 1
            if (self.streak < 6):
                self.root.ids["day" + str(self.streak)].source = "star.png"
            if (self.streak == 5):
                self.root.ids.screen_manager.current = "Change Reward"

    @mainthread
    def location_update(self, **kwargs):
        print("GPS INFORMATION")
        print('\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()]))
        self.lat = kwargs['lat']
        self.lon = kwargs['lon']
        self.root.ids.mapview.center_on(self.lat, self.lon)

        isInRadius = False
        for marker in mapPins:
            # Distance is in terms of degrees lat/long
            # Keep in mind that 1* latitutde != 1* longitude
            distanceFromPin = math.dist([marker.lat, marker.lon], [self.lat, self.lon])
            if distanceFromPin < .0003:
                if (self.insideMarkerRadius != True):
                    print("Near a pinned location\n")
                    Clock.schedule_once(self.streak_reset, 5) # 5 seconds as a testing value
                    self.show_alert_dialog()
                isInRadius = True

        self.personLocator.lat = self.lat
        self.personLocator.lon = self.lon
        self.insideMarkerRadius = isInRadius

    def streak_reset(self, dt):
        if (self.insideMarkerRadius):
            self.streak = 0
            for x in range(5):
                self.root.ids["day" + str(x + 1)].source = "empty.jpg"

    def show_alert_dialog(self):
        self.dialog = MDDialog(
            title="WARNING!",
            text="You are entering your area of use!\nYou have 5 minutes to leave this area",
            buttons=[
                MDFlatButton(text="Okay", on_release=self.close_alert_dialog), MDRaisedButton(text="Leaving!", on_release=self.close_alert_dialog)
            ]
        )
        self.dialog.open()

    def close_alert_dialog(self, something_else):
        self.dialog.dismiss(force=True)


    @mainthread
    def status_update(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

TestNavigationDrawer().run()
