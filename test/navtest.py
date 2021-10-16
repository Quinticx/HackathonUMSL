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
                    size_hint: 1, 1
                    pos_hint: {'center_x': 0.5, 'center_y': 0.4}

                    MapView:
                        size_hint: 1, 0.6
                        id: mapview
                        lat: 38.7092
                        lon: -90.3083
                        zoom: 13


                    MDGridLayout:
                        cols: 5
                        row_default_height: (self.width - self.cols*self.spacing[0]) / self.cols
                        row_force_default: True
                        pos_hint: {'center_x': 0.5, 'center_y': 0.5 }
                        size_hint_x: 0.7

                        #adaptive_height: True
                        padding: dp(10), dp(200)
                        #spacing: dp(4)

                        SmartTileWithLabel:
                            id: 'day1'
                            source: "empty.jpg"
                            text: "[size=16]Day 1[/size]"
                            halign: 'middle'

                        SmartTileWithLabel:
                            id: 'day2'
                            source: "empty.jpg"
                            text: "[size=16]Day 2[/size]"

                        SmartTileWithLabel:
                            id: 'day3'
                            source: "empty.jpg"
                            text: "[size=16]Day 3[/size]"

                        SmartTileWithLabel:
                            id: 'day4'
                            source: "empty.jpg"
                            text: "[size=16]Day 4[/size]"

                        SmartTileWithLabel:
                            id: 'day5'
                            source: "empty.jpg"
                            text: "[size=16]Day 5[/size]"






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

                    Image:
                        id: avatar
                        size_hint: 1, 0.5
                        size: '56dp', '56dp'
                        source: 'data/logo/kivy-icon-256.png'




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
