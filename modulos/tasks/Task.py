# Sage

# kivy
import kivy
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import Screen

Builder.load_file('modulos/tasks/task.kv')

class Task(Screen):
    pass

class TaskZone(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(0, 1000):
            size = dp(100)
            self.add_widget(
                Button(
                    text=str(i+1),
                    size_hint=(None, None),
                    size=(size, size)))

# Funcion main para probar la zona
def main():
    from kivy.app import App
    class TaskApp(App):
        def build(self):
            return Task()
    TaskApp().run()

if __name__ == '__main__':
    main()
