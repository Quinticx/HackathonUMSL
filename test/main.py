from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from plyer import gps
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList
from kivy.clock import mainthread
from kivy.utils import platform
import urllib3
from kivy_garden.mapview import MapSource,MapView

KV = '''
# Menu item in the DrawerList list.
<ItemDrawer>:
    theme_text_color: "Custom"
    on_release: self.parent.set_color_item(self)
    IconLeftWidget:
        id: icon
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color
<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"
    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None
        height: avatar.height
        Image:
            id: avatar
            size_hint: None, None
            size: "56dp", "56dp"
            source: "data/logo/kivy-icon-256.png"
    MDLabel:
        text: "KivyMD library"
        font_style: "Button"
        adaptive_height: True
    MDLabel:
        text: "kivydevelopment@gmail.com"
        font_style: "Caption"
        adaptive_height: True
    ScrollView:
        DrawerList:
            id: md_list

MDScreen:
    MDNavigationLayout:
        ScreenManager:
            MDScreen:
                MDBoxLayout:
                    orientation: 'vertical'
                    size_hint: 1, .5
                    pos_hint: {'center_x': 0.5, 'center_y': 0.8}
                    MapView:
                        id: mapview
                        lat: 38.7092
                        lon: -90.3083
                        zoom: 13
                MDBoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        title: "Navigation Drawer"
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]
                    Widget:
                MDBoxLayout:
                    orientation: 'horizontal'
                    Widget:
        MDNavigationDrawer:
            id: nav_drawer
            ContentNavigationDrawer:
                id: content_drawer
'''


class ContentNavigationDrawer(MDBoxLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class TestNavigationDrawer(MDApp):

    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission
        
        request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION])

    def build(self):
        self.lat = 0 #default lat
        self.lon = 0 #default lon

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

        return Builder.load_string(KV)

    def on_start(self):
        icons_item = {
            "folder": "My files",
            "account-multiple": "Shared with me",
            "star": "Starred",
            "history": "Recent",
            "checkbox-marked": "Shared with me",
            "upload": "Upload",
        }
        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )
        gps.start(1000, 0)

    @mainthread
    def location_update(self, **kwargs):
        print("GPS INFORMATION")
        print('\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()]))
        self.lat = kwargs['lat']
        self.lon = kwargs['lon']

    @mainthread
    def status_update(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)


TestNavigationDrawer().run()