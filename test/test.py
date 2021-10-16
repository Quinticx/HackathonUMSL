from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy_garden.mapview import MapSource, MapView
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList
from kivy_garden.mapview import MapSource, MapView
from kivy.properties import ObjectProperty

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
        text: "Just Don't"
        font_style: "Button"
        adaptive_height: True

    MDLabel:
        text: "justdont@gmail.com"
        font_style: "Caption"
        adaptive_height: True

    ScrollView:

        MDList:

            OneLineListItem:
                text: 'Add Pin'
                on_press:
                    root.nav_drawer.set_state('close')
                    root.screen_manager.current = 'pin'

            OneLineListItem:
                text: 'Change Reward'
                on_press:
                    root.nav_drawer.set_state('close')
                    root.screen_manager.current = 'reward'
        #DrawerList:
            #id: md_list



MDScreen:

    MDNavigationLayout:

        ScreenManager:

            MDScreen:
                name: 'pin'
                MDLabel:
                    text: 'Add Pin'

                MDBoxLayout:
                    orientation: 'vertical'
                    size_hint:1, 0.5
                    pos_hint: {'center_x': 0.5, 'center_y': 1}

                    MapView:
                        id: pins
                        lat: 38.7092
                        lon: -90.3083
                        zoom: 11
            MDScreen:
                name: 'reward'
                MDLabel:
                    text: 'Change Reward'

                MDBoxLayout:
                    orientation: 'vertical'
                    size_hint:1, 0.5
                    pos_hint: {'center_x': 0.5, 'center_y': 1}

                    MapView:
                        id: pins
                        lat: 38.7092
                        lon: -90.3083
                        zoom: 11




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
                #id: content_drawer
                screen_manager: screen_manager
                nav_drawer: nav_drawer
'''


class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

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
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        icons_item = {
            "crosshairs-gps": "Add Pin",
            "account-cash": "Change Reward",
            "account-circle": "Change Profile Picture",
        }
        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )


TestNavigationDrawer().run()

