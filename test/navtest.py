from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy_garden.mapview import MapSource, MapView
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem, MDList
from kivy_garden.mapview import MapSource, MapView
from kivymd.theming import ThemableBehavior
from kivy.uix.button import Button



class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class PinButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Add Pin"

    def addpin(self):
        mapview = App.get_running_app().root.ids.mapview
        m1 = MapMarker(lat = mapview.lat, lon = mapview.lon, source = "marker.png")
        mapview.add_marker(m1)




class TestNavigationDrawer(MDApp):
    def build(self):
        return Builder.load_file('layout.kv')


TestNavigationDrawer().run()
