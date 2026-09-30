from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.graphics import Color, Rectangle, RoundedRectangle

# Ajustamos tamaño de la ventana
Window.size = (400, 600)

# Colores personalizados
backgroundColor = (1, 1, 1, 1)  # Blanco
textColor = (1, 1, 1, 1)  # Blanco puro para texto
MainButonColor = (60/255, 0/255, 98/255, 1)  # Morado oscuro
SecondButonColor = (255, 255, 255, 0)  # Transparente

# Usuarios válidos
usuarios = {
    "admin": "1234",
    "user": "abcd"
}

# Botón personalizado con bordes redondeados
class BotonPersonalizado(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = 'Poppins-SemiBold.ttf'
        self.font_size = 15
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = kwargs.get('color', textColor)
        with self.canvas.before:
            self.bg_color = Color(*kwargs.get('background_color', MainButonColor))
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# Pantalla de bienvenida
class BienvenidaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*backgroundColor)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.actualizar_rect, pos=self.actualizar_rect)

        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)
        layout.add_widget(Image(source='logo2.png', size_hint=(1, 0.6), allow_stretch=True))
        layout.add_widget(Label(text="Bienvenido a Devboost", font_size=24, size_hint=(1, 0.1), color=textColor))

        btn_ingresar = BotonPersonalizado(
            text="Ingresar",
            size_hint=(1, 0.1),
            font_size=16,
            background_color=SecondButonColor,
            color=textColor
        )
        btn_ingresar.bind(on_press=self.ir_a_login)

        layout.add_widget(btn_ingresar)
        self.add_widget(layout)

    def actualizar_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def ir_a_login(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'seleccion'

# Pantalla de selección entre login y registro
class SeleccionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*backgroundColor)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.actualizar_rect, pos=self.actualizar_rect)

        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        logo_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4), spacing=5)
        logo_image = Image(source='rocket_icon.png', size_hint=(1, 0.6), allow_stretch=True)
        devboost_label = Label(text='Devboost', font_size=32, color=MainButonColor, bold=True, size_hint=(1, 0.2),
                               halign='center', valign='top')
        devboost_label.bind(size=lambda *x: devboost_label.setter('text_size')(devboost_label, devboost_label.size))

        logo_layout.add_widget(logo_image)
        logo_layout.add_widget(devboost_label)
        layout.add_widget(logo_layout)

        botones_layout = BoxLayout(orientation='vertical', spacing=15, size_hint=(1, 0.25))

        btn_login = BotonPersonalizado(
            text="Login",
            size_hint=(1, None),
            height=50,
            font_size=18,
            background_color=MainButonColor,
            color=textColor
        )
        btn_login.bind(on_press=self.ir_a_login)

        btn_register = BotonPersonalizado(
            text="Register",
            size_hint=(1, None),
            height=50,
            font_size=18,
            background_color=MainButonColor,
            color=textColor
        )
        btn_register.bind(on_press=self.ir_a_registro)

        botones_layout.add_widget(btn_login)
        botones_layout.add_widget(btn_register)
        layout.add_widget(botones_layout)

        layout.add_widget(Image(source='devboost_ilustracion.png', size_hint=(1, 0.35), allow_stretch=True))

        self.add_widget(layout)

    def actualizar_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def ir_a_login(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'login'

    def ir_a_registro(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'register'

# Pantalla de registro (actualizada)
class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*backgroundColor)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.actualizar_rect, pos=self.actualizar_rect)

        main_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        container = BoxLayout(orientation='vertical', padding=30, spacing=20, size_hint=(0.9, None))
        container.height = 500

        logo = Image(source='rocket_icon.png', size_hint=(None, None), size=(70, 70))
        logo_box = AnchorLayout(anchor_x='center', anchor_y='center')
        logo_box.add_widget(logo)

        title = Label(text='DevBoost', font_size=24, bold=True, color=MainButonColor, size_hint=(1, None), height=30)

        self.email = self.crear_input("Email")
        self.username = self.crear_input("Username")
        self.password = self.crear_input("Password", password=True)

        btn_registrar = BotonPersonalizado(
            text="Register",
            size_hint=(1, None),
            height=45,
            font_size=16,
            background_color=MainButonColor,
            color=textColor
        )
        btn_registrar.bind(on_press=self.registrar_usuario)

        texto_inferior = Label(
            text="¿Ya tienes una cuenta? [ref=iniciar][color=6600cc]Iniciar sesión[/color][/ref]",
            markup=True,
            size_hint=(1, None),
            height=30,
            font_size=14,
            color=(0.3, 0.3, 0.3, 1)
        )
        texto_inferior.bind(on_ref_press=self.volver)

        container.add_widget(logo_box)
        container.add_widget(title)
        container.add_widget(self.email)
        container.add_widget(self.username)
        container.add_widget(self.password)
        container.add_widget(btn_registrar)
        container.add_widget(texto_inferior)

        main_layout.add_widget(container)
        self.add_widget(main_layout)

    def crear_input(self, hint, password=False):
        input_field = TextInput(
            hint_text=hint,
            multiline=False,
            size_hint=(1, None),
            height=45,
            font_size=16,
            password=password,
            background_normal='',
            background_active='',
            background_color=(0, 0, 0, 0),
            foreground_color=(0.2, 0.2, 0.2, 1),
            hint_text_color=(0.5, 0.5, 0.6, 1),
            padding=[10, 10]
        )
        with input_field.canvas.before:
            Color(0.85, 0.75, 0.95, 1)  # Morado claro
            input_field.rect = RoundedRectangle(size=input_field.size, pos=input_field.pos, radius=[10])
        input_field.bind(pos=self.actualizar_rect_input, size=self.actualizar_rect_input)
        return input_field

    def actualizar_rect_input(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def actualizar_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def registrar_usuario(self, instance):
        email = self.email.text.strip()
        user = self.username.text.strip()
        pwd = self.password.text.strip()

        if email and user and pwd:
            if user in usuarios:
                Popup(title="Error",
                      content=Label(text="El usuario ya existe.", color=textColor),
                      size_hint=(0.6, 0.3)).open()
            else:
                usuarios[user] = pwd
                Popup(title="¡Éxito!",
                      content=Label(text="Usuario registrado correctamente.", color=textColor),
                      size_hint=(0.6, 0.3)).open()
                self.email.text = ''
                self.username.text = ''
                self.password.text = ''
        else:
            Popup(title="Error",
                  content=Label(text="Completa todos los campos.", color=textColor),
                  size_hint=(0.6, 0.3)).open()

    def volver(self, instance, value=None):
        self.manager.transition.direction = 'right'
        self.manager.current = 'seleccion'

# Pantalla de login
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*backgroundColor)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.actualizar_rect, pos=self.actualizar_rect)

        main_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        container = BoxLayout(orientation='vertical', padding=30, spacing=20, size_hint=(0.9, None))
        container.height = 500

        logo = Image(source='rocket_icon.png', size_hint=(None, None), size=(70, 70))
        logo_box = AnchorLayout(anchor_x='center', anchor_y='center')
        logo_box.add_widget(logo)

        title = Label(text='DevBoost', font_size=24, bold=True, color=MainButonColor, size_hint=(1, None), height=30)

        self.email = self.crear_input("Email")
        self.username = self.crear_input("Username")
        self.password = self.crear_input("Password", password=True)

        btn_registrar = BotonPersonalizado(
            text="Register",
            size_hint=(1, None),
            height=45,
            font_size=16,
            background_color=MainButonColor,
            color=textColor
        )
        btn_registrar.bind(on_press=self.registrar_usuario)

        texto_inferior = Label(
            text="¿Ya tienes una cuenta? [ref=iniciar][color=6600cc]Iniciar sesión[/color][/ref]",
            markup=True,
            size_hint=(1, None),
            height=30,
            font_size=14,
            color=(0.3, 0.3, 0.3, 1)
        )
        texto_inferior.bind(on_ref_press=self.volver)

        container.add_widget(logo_box)
        container.add_widget(title)
        container.add_widget(self.email)
        container.add_widget(self.username)
        container.add_widget(self.password)
        container.add_widget(btn_registrar)
        container.add_widget(texto_inferior)

        main_layout.add_widget(container)
        self.add_widget(main_layout)

    def crear_input(self, hint, password=False):
        input_field = TextInput(
            hint_text=hint,
            multiline=False,
            size_hint=(1, None),
            height=45,
            font_size=16,
            password=password,
            background_normal='',
            background_active='',
            background_color=(0, 0, 0, 0),
            foreground_color=(0.2, 0.2, 0.2, 1),
            hint_text_color=(0.5, 0.5, 0.6, 1),
            padding=[10, 10]
        )
        with input_field.canvas.before:
            Color(0.85, 0.75, 0.95, 1)  # Morado claro
            input_field.rect = RoundedRectangle(size=input_field.size, pos=input_field.pos, radius=[10])
        input_field.bind(pos=self.actualizar_rect_input, size=self.actualizar_rect_input)
        return input_field

    def actualizar_rect_input(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def actualizar_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def registrar_usuario(self, instance):
        email = self.email.text.strip()
        user = self.username.text.strip()
        pwd = self.password.text.strip()

        if email and user and pwd:
            if user in usuarios:
                Popup(title="Error",
                      content=Label(text="El usuario ya existe.", color=textColor),
                      size_hint=(0.6, 0.3)).open()
            else:
                usuarios[user] = pwd
                Popup(title="¡Éxito!",
                      content=Label(text="Usuario registrado correctamente.", color=textColor),
                      size_hint=(0.6, 0.3)).open()
                self.email.text = ''
                self.username.text = ''
                self.password.text = ''
        else:
            Popup(title="Error",
                  content=Label(text="Completa todos los campos.", color=textColor),
                  size_hint=(0.6, 0.3)).open()

    def volver(self, instance, value=None):
        self.manager.transition.direction = 'right'
        self.manager.current = 'seleccion'

# Pantalla de usuario
class UsuarioScreen(Screen):
    usuario = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*backgroundColor)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.actualizar_rect, pos=self.actualizar_rect)

        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        self.saludo = Label(text="", font_size=24, size_hint=(1, 0.2), markup=True, color=textColor)
        self.descripcion = Label(text="Aquí verás tus datos e información personal",
                                 font_size=16, size_hint=(1, 0.2), color=textColor)

        btn_salir = BotonPersonalizado(
            text="Cerrar sesión",
            size_hint=(1, 0.1),
            font_size=16,
            background_color=SecondButonColor,
            color=textColor
        )
        btn_salir.bind(on_press=self.cerrar_sesion)

        self.layout.add_widget(self.saludo)
        self.layout.add_widget(self.descripcion)
        self.layout.add_widget(btn_salir)

        self.add_widget(self.layout)

    def actualizar_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_usuario(self, instance, value):
        self.saludo.text = f"[b]Bienvenido, {value}[/b]"

    def cerrar_sesion(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'bienvenida'

# App principal
class LoginApp(App):
    def build(self):
        self.title = "App de Login"
        sm = ScreenManager(transition=FadeTransition(duration=0.3))
        sm.add_widget(BienvenidaScreen(name='bienvenida'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(UsuarioScreen(name='usuario'))
        sm.add_widget(SeleccionScreen(name='seleccion'))
        sm.add_widget(RegisterScreen(name='register'))
        return sm

if __name__ == '__main__':
    LoginApp().run()
