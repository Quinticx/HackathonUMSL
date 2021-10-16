from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy_garden.mapview import MapSource, MapView
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem, MDList
from kivy_garden.mapview import MapSource, MapView
from kivymd.theming import ThemableBehavior


KV = '''
<ContentNavigationDrawer>:
    orientation: 'vertical'
    padding: '8dp'
    spacing: '8dp'

    AnchorLayout:
        anchor_x: 'left'
        size_hint_y: None
        height: avatar.height

    Image:
        id: avatar
        size_hint: None, None
        size: '56dp', '56dp'
        source: 'data/logo/kivy-icon-256.png'

    MDLabel:
        text: "Just Don't"
        font_style: 'Button'
        adaptive_height: True

    MDLabel:
        text: 'justdont@gmail.com'
        font_style: 'Caption'
        adaptive_height: True



    ScrollView:

        MDList:

            OneLineListItem:
                text: "Home"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "Home"

            OneLineListItem:
                text: "Add Pin"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "Add Pin"

            OneLineListItem:
                text: "Change Reward"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "Change Reward"



MDScreen:

    MDToolbar:
        id: toolbar
        pos_hint: {"top": 1}
        elevation: 10
        title: "MDNavigationDrawer"
        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

    MDNavigationLayout:
        x: toolbar.height

        ScreenManager:
            id: screen_manager

            MDScreen:
                name: "Home"

                MDBoxLayout:
                    orientation: 'vertical'
                    size_hint: 1, 0.5
                    pos_hint: {'center_x': 0.5, 'center_y': 0.6}

                    MapView:
                        id: mapview
                        lat: 38.7092
                        lon: -90.3083
                        zoom: 13

            MDScreen:
                name: "Add Pin"

                MDBoxLayout:
                    orientation: 'vertical'
                    size_hint: 1, 0.5
                    pos_hint: {'center_x': 0.5, 'center_y': 0.6}

                    MapView:
                        id: mapview
                        lat: 38.7092
                        lon: -90.3083
                        zoom: 11
            MDScreen:
                name: "Change Reward"

                MDBoxLayout:
                    orientation: 'vertical'
                    size_hint: 1, 0.5
                    pos_hint: {'center_x': 0.5, 'center_y': 0.6}

                    Widget:
                        Image:
                            id: avatar
                            size_hint: 1, 0.5
                            source: 'amazon5.jpeg'




        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                screen_manager: screen_manager
                nav_drawer: nav_drawer
'''


class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class TestNavigationDrawer(MDApp):
    def build(self):
        return Builder.load_string(KV)


TestNavigationDrawer().run()
