from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
 
# Ajustamos tamaño de la ventana
Window.size = (400, 600)
 
#colores tema oscuro personalizado
backgroundColor = (1, 1, 1, 1)
textColor = [1, 1, 1, 1]
textColorDark = [0, 0, 0, 1]
MainButonColor = (60/255, 0/255, 98/255, 1)
SecondButonColor = [0.5, 0, 0.6, 1]
 
#Usuarios validos
usuarios = {
    "admin": "1234",
    "caro": "oso",
}
  
# Clase con borde para el Spinner principal
class BorderedSpinner(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)  # Fondo transparente real (dibujaremos uno blanco)
        self.color = (0, 0, 0, 0.7)             # Texto negro

        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)  # Fondo blanco
            self.bg_rect = RoundedRectangle(radius=[10])
            self.border_color = Color(0, 0, 0, 0.5)  # Borde negro con opacidad
            self.border_line = Line(width=1.2, rounded_rectangle=[0, 0, 0, 0, 10])

        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (*self.pos, *self.size, 10)
 
 
#Función para bordes en general
def aplicar_borde_redondeado(widget, borde_color=(0, 0, 0, 0.15), fondo_color=(1, 1, 1, 1), radius=10, borde_grosor=2):
    with widget.canvas.before:
        Color(*borde_color)
        widget.borde = RoundedRectangle(radius=[radius])

        Color(*fondo_color)
        widget.fondo = RoundedRectangle(radius=[radius - 2])

    def actualizar(_inst, *args):
        widget.borde.pos = widget.pos
        widget.borde.size = widget.size

        widget.fondo.pos = (widget.x + borde_grosor, widget.y + borde_grosor)
        widget.fondo.size = (widget.width - 2 * borde_grosor, widget.height - 2 * borde_grosor)

    widget.bind(pos=actualizar, size=actualizar)

#TextInput personalizado con bordes

class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super(CustomTextInput, self).__init__(**kwargs)

        self.background_normal = ''
        self.background_active = ''
        self.background_color = (0, 0, 0, 0)  # Hacemos transparente el fondo original

        self.foreground_color = (0, 0, 0, 0.7)  # Texto negro
        self.hint_text_color = (0, 0, 0, 0.7)   # Hint text negro
        self.padding = [10, 10, 10, 10]

        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)  # Fondo blanco
            self.bg_rect = RoundedRectangle(radius=[10])

            # Borde negro con opacidad del 50%
            self.border_color = Color(0, 0, 0, 0.5)  # ← Cambia aquí la opacidad
            self.border_line = Line(width=1.2, rounded_rectangle=[0, 0, 0, 0, 10])

        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.bind(focus=self.on_focus_change)  # Para cambiar opacidad dinámicamente

    def update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = (*self.pos, *self.size, 10)
    def on_focus_change(self, instance, value):
        """Opcional: Cambia opacidad del borde al enfocar/desenfocar"""
        if value:
            self.border_color.a = 0.7  # Borde completamente opaco al enfocar
        else:
            self.border_color.a = 0.5  # Borde semitransparente al desenfocar



# Clase con estilo para cada opción desplegable
class WhiteOption(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (1, 1, 1, 1)  # Blanco
        self.color = (0, 0, 0, 1)             # Negro
 
        with self.canvas.after:
            Color(0, 0, 0, 1)  # Borde negro
            self.borde = Line(rectangle=(self.x, self.y, self.width, self.height), width=1)
        self.bind(pos=self.actualizar_borde, size=self.actualizar_borde)
 
    def actualizar_borde(self, *args):
        self.borde.rectangle = (self.x, self.y, self.width, self.height)
 
 
#Boton Personalizado
class BotonPersonalizado(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 15
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = kwargs.get('color', textColor)
        with self.canvas.before:
            self.bg_color = Color(*kwargs.get('background_color', MainButonColor))
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10])
        self.bind(pos=self.update_rect, size=self.update_rect)

        
 
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
 
 
class MyLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._update_text_size)
 
    def _update_text_size(self, instance, value):
        self.text_size = value
 
#Pantalla de bienvenida
class BienvenidaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*backgroundColor)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.actualizar_rect, pos=self.actualizar_rect)
 
        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)
        layout.add_widget(Image(source='logo.png', size_hint=(1, 1), allow_stretch=True))
        layout.add_widget(Label(
            text="Bienvenido a Devboost",
            font_size=24,
            size_hint=(1, 0.1),
            color=textColor
        ))
        self.add_widget(layout)
        
    def on_enter(self):
        # Solo se ejecuta cuando esta pantalla se muestra
        Clock.schedule_once(self.ir_a_login, 3)
 
    def actualizar_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
 
    def ir_a_login(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'seleccion'
 
#Pantalla de seleccion
class SeleccionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*backgroundColor)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.actualizar_rect, pos=self.actualizar_rect)
 
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
 
        logo_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4), spacing=5)
        logo_image = Image(source='logo.png', size_hint=(1, 0.5), allow_stretch=True)
        logo_layout.add_widget(logo_image)
        layout.add_widget(logo_layout)
 
        botones_layout = BoxLayout(orientation='vertical', spacing=15, size_hint=(1, 0.25))
        btn_login = BotonPersonalizado(text="Login", size_hint=(1, None), height=50, font_size=18, background_color=MainButonColor, color=textColor)
        btn_login.bind(on_press=self.ir_a_login)
        btn_register = BotonPersonalizado(text="Register", size_hint=(1, None), height=50, font_size=18, background_color=MainButonColor, color=textColor)
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
 
#Pantalla de register
class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.popup = None
        with self.canvas.before:
            Color(*backgroundColor)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.actualizar_rect, pos=self.actualizar_rect)

        layout = BoxLayout(orientation='vertical', padding=35, spacing=20)
        
        # Creamos el label para mensajes (inicialmente vacío)
        self.mensaje_label = Label(text="", size_hint=(1, None), height=5, color=(0, 0, 0, 1))
        layout.add_widget(self.mensaje_label)

        logo_image = Image(source='logo.png', size_hint=(0.7, None), height=120, allow_stretch=True, pos_hint={'center_x': .5})
        layout.add_widget(logo_image)
        
        # Campos del formulario con valores iniciales
        self.fullName = CustomTextInput(hint_text="Nombre completo")
        self.spinner = BorderedSpinner(
            text='Selecciona tu nivel',
            values=('Beginner', 'Junior', 'Senior'),
            size_hint=(1, None),
            size=(200, 44),
            option_cls=WhiteOption
        )
        self.email = CustomTextInput(hint_text="Correo electrónico")
        # self.email = TextInput(text="", hint_text="Correo electrónico", multiline=False, size_hint=(1, None), height=40)
        self.username = CustomTextInput(hint_text="Nombre de usuario")
        self.password = CustomTextInput(hint_text="Contraseña", password=True)

        # Botones
        btn_register = BotonPersonalizado(text="Registrar", size_hint=(1, None), height=40)
        btn_register.bind(on_press=self.registrar_usuario)

        self.in_sesion = Label(text="¿Ya tienes una cuenta")

        self.reg = BoxLayout(orientation='vertical', padding=20, spacing=15)
        aplicar_borde_redondeado(self.reg)

        # Añadir widgets al layout
        self.reg.add_widget(self.fullName)
        self.reg.add_widget(self.spinner)
        self.reg.add_widget(self.email)
        self.reg.add_widget(self.username)
        self.reg.add_widget(self.password)
        self.reg.add_widget(btn_register)
        layout.add_widget(self.reg)
        
        self.add_widget(layout)

    def on_enter(self):
        """Se ejecuta cuando se muestra la pantalla"""
        self.resetear_formulario()

    def resetear_formulario(self):
        """Restablece todos los campos a sus valores iniciales"""
        self.fullName.text = ""
        self.spinner.text = "Selecciona tu nivel"
        self.email.text = ""
        self.username.text = ""
        self.password.text = ""
        self.mensaje_label.text = ""  # Ocultamos el mensaje

    def registrar_usuario(self, instance):
        # Validación de campos
        if not all([self.fullName.text, self.email.text, self.username.text, self.password.text]):
            self.mostrar_mensaje_error("Todos los campos son obligatorios")
            return

        # Verificar si el usuario ya existe
        if self.username.text in usuarios:
            self.mostrar_mensaje_error("El nombre de usuario ya existe")
            return

        # Registro exitoso
        usuarios[self.username.text] = self.password.text
        self.mostrar_mensaje_exito("¡Registro exitoso! Redirigiendo a login...")
        
        # Programar la redirección después de 2 segundos
        Clock.schedule_once(self.redirigir_a_login, 2)

    def mostrar_mensaje_error(self, mensaje):
        """Muestra un mensaje de error temporal"""
        self.mensaje_label.text = mensaje
        self.mensaje_label.color = (1, 0, 0, 1)  # Rojo
        Clock.schedule_once(lambda dt: setattr(self.mensaje_label, 'text', ""), 3)

    def mostrar_mensaje_exito(self, mensaje):
        """Muestra un mensaje de éxito y prepara la redirección"""
        self.mensaje_label.text = mensaje
        self.mensaje_label.color = (0, 0.5, 0, 1)  # Verde

    def redirigir_a_login(self, dt):
        """Redirige a la pantalla de login y limpia el formulario"""
        self.resetear_formulario()
        self.manager.transition.direction = 'left'
        self.manager.current = 'login'

    def volver(self, instance):
        self.resetear_formulario()
        self.manager.transition.direction = 'right'
        self.manager.current = 'seleccion'

    def actualizar_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

 
#Pantalla de login
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*backgroundColor)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.actualizar_rect, pos=self.actualizar_rect)
 
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.username = TextInput(hint_text="Username", multiline=False, size_hint=(1, None), height=45)
        self.password = TextInput(hint_text="Password", multiline=False, password=True, size_hint=(1, None), height=45)
 
        btn_login = BotonPersonalizado(text="Iniciar sesión", size_hint=(1, None), height=45)
        btn_login.bind(on_press=self.iniciar_sesion)
 
        layout.add_widget(Label(text="Iniciar Sesión", font_size=24, color=MainButonColor))
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(btn_login)
 
        volver = Button(text="Volver", size_hint=(1, None), height=40)
        volver.bind(on_press=self.volver)
        layout.add_widget(volver)
 
        self.add_widget(layout)
 
    def actualizar_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
 
    def iniciar_sesion(self, instance):
        #email = self.email.text.strip()
        user = self.username.text.strip()
        pwd = self.password.text.strip()
        if user and pwd:
            if user in usuarios and usuarios[user] == pwd:
                self.manager.get_screen('usuario').saludo_label.text = f"[b]¡Hola, {user}![/b]"
                self.manager.transition.direction = 'left'
                self.manager.current = 'level'
            else:
                Popup(title="Error", content=Label(text="Usuario o contraseña incorrectos.", color=textColor), size_hint=(0.6, 0.3)).open()
        else:
            Popup(title="Error", content=Label(text="Completa todos los campos.", color=textColor), size_hint=(0.6, 0.3)).open()
 
    def volver(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'seleccion'
 
#Pantalla de levels
class LevelScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fondo de pantalla
        with self.canvas.before:
            Color(*backgroundColor)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.actualizar_rect, pos=self.actualizar_rect)

        # ScrollView principal
        scroll = ScrollView(size_hint=(1, 1))

        # Layout principal contenido en scroll
        layout = BoxLayout(orientation='vertical', padding=20, spacing=5, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))  # Clave para el scroll

        # Contenido fijo
        logo_image = Image(source='logo.png', size_hint=(0.7, None), height=150, allow_stretch=True, pos_hint={'center_x': .5})
        layout.add_widget(logo_image)

        layout.add_widget(Label(
            text='Select the project difficulty',
            font_size=20,
            bold=True,
            color=(0, 0, 0, 0.7),
            size_hint_y=None,
            height=40
        ))

        # Begginer
        self.box = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint_y=None)
        aplicar_borde_redondeado(self.box)
        self.box.bind(minimum_height=self.box.setter('height'))

        self.box.add_widget(Image(source='begginer.png', size_hint=(1, None), height=200, allow_stretch=True))
        self.box.add_widget(Label(text='Begginer', font_size=16, bold=True, color=textColorDark, size_hint_y=None, height=30))
        self.box.add_widget(Label(text='Start with the easiest projects.', font_size=14, color=textColorDark, size_hint_y=None, height=30))
        self.btn_explore = BotonPersonalizado(text="Explore", size_hint=(0.3, None), height=30, pos_hint={'center_x': .5})
        self.btn_explore.bind(on_press=self.redirigir_a_proyectos)
        self.box.add_widget(self.btn_explore)
        
        
        # Intermediate
        self.inter = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint_y=None)
        aplicar_borde_redondeado(self.inter)

        self.inter.bind(minimum_height=self.inter.setter('height'))

        self.inter.add_widget(Image(source='intermediate.png', size_hint=(1, None), height=200, allow_stretch=True))
        self.inter.add_widget(Label(text='Intermediate', font_size=16, bold=True, color=textColorDark, size_hint_y=None, height=30))
        self.inter.add_widget(Label(text='Develop your skills with more challenging projects.', font_size=14, color=textColorDark, size_hint_y=None, height=30))
        self.btn_exp = BotonPersonalizado(text="Explore", size_hint=(0.3, None), height=30, pos_hint={'center_x': .5})
        self.inter.add_widget(self.btn_exp)
        
        # Advanced
        self.adv = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint_y=None)
        aplicar_borde_redondeado(self.adv)

        self.adv.bind(minimum_height=self.adv.setter('height'))

        self.adv.add_widget(Image(source='advanced.png', size_hint=(1, None), height=200, allow_stretch=True))
        self.adv.add_widget(Label(text='Advanced', font_size=16, bold=True, color=textColorDark, size_hint_y=None, height=30))
        self.adv.add_widget(Label(text='Tackle complex challenges to boost your knowledge', font_size=14, color=textColorDark, size_hint_y=None, height=30))
        self.btn_ex = BotonPersonalizado(text="Explore", size_hint=(0.3, None), height=30, pos_hint={'center_x': .5})
        self.adv.add_widget(self.btn_ex)

        layout.add_widget(self.box)
        layout.add_widget(Widget(size_hint_y=None, height=10))
        layout.add_widget(self.inter)
        layout.add_widget(Widget(size_hint_y=None, height=10))
        layout.add_widget(self.adv)

        # Agregar layout completo al scroll
        scroll.add_widget(layout)

        # Agregar el scrollview a la pantalla
        self.add_widget(scroll)

    def actualizar_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def redirigir_a_proyectos(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'home'

class ProjectCard(BoxLayout):
    def __init__(self, title, description, language, image_url, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, height=300, padding=10, spacing=5, **kwargs)

        # Fondo blanco para la tarjeta
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Blanco RGBA
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.add_widget(AsyncImage(source=image_url, size_hint=(1, 0.6)))

        # Título en negro
        self.add_widget(Label(
            text=f"[b]{title}[/b]", 
            markup=True, 
            size_hint_y=None, 
            height=30, 
            font_size=16,
            color=[0, 0, 0, 1]  # Negro RGBA
        ))
        
        # Descripción en gris oscuro
        self.add_widget(Label(
            text=description, 
            size_hint_y=None, 
            height=60, 
            font_size=13,
            color=[0.2, 0.2, 0.2, 1]  # Gris oscuro RGBA
        ))
        
        # Lenguaje en gris
        self.add_widget(Label(
            text=f"[color=505050]{language}[/color]", 
            markup=True, 
            size_hint_y=None, 
            height=20, 
            font_size=12,
            color=[0.3, 0.3, 0.3, 1]  # Gris RGBA (fallback)
        ))

        btn_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_box.add_widget(Button(
            text="More", 
            background_color=get_color_from_hex("#6A0DAD"), 
            color=[1, 1, 1, 1]  # Texto blanco
        ))
        btn_box.add_widget(Button(
            text="Done", 
            background_color=get_color_from_hex("#6A0DAD"), 
            color=[1, 1, 1, 1]  # Texto blanco
        ))
        self.add_widget(btn_box)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Fondo blanco RGBA
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.actualizar_rect, pos=self.actualizar_rect)

        root_layout = BoxLayout(orientation='vertical')

        # Título principal en morado
        root_layout.add_widget(Label(
            text="[b]DevBoost[/b]", 
            markup=True, 
            font_size=24, 
            size_hint_y=None, 
            height=60, 
            color=[0.4, 0.2, 0.8, 1]  # Morado RGBA
        ))
        
        # Subtítulo en gris oscuro
        root_layout.add_widget(Label(
            text="Basic projects", 
            font_size=18, 
            size_hint_y=None, 
            height=40,
            color=[0.3, 0.3, 0.3, 1]  # Gris oscuro RGBA
        ))

        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=20, padding=10)
        content.bind(minimum_height=content.setter('height'))

        # Tarjetas de proyecto
        content.add_widget(ProjectCard(
            "Calculator",
            "Create a console application that allows the user to perform basic mathematical operations",
            "Python",
            "calculator.png"
        ))

        content.add_widget(ProjectCard(
            "Name generator",
            "A simple program that generates random names based on predefined lists of first names and surnames",
            "JavaScript",
            "name.png"
        ))

        content.add_widget(ProjectCard(
            "Currency converter",
            "A simple program that converts an amount of money from one currency to another using fixed exchange rates",
            "JavaScript",
            "currency.png"
        ))

        content.add_widget(ProjectCard(
            "World clock",
            "A web application that displays the current time in different time zones around the world",
            "JavaScript",
            "World clock.png"
        ))

        scroll.add_widget(content)
        root_layout.add_widget(scroll)
        self.add_widget(root_layout)

    def actualizar_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    #intermediate proyectos
Window.clearcolor = (1, 1, 1, 1)  # Fondo blanco

class DevBoostApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Título principal
        title = Label(
            text='[b]DevBoost[/b]',
            markup=True,
            font_size=dp(24),
            color=(0, 0, 0, 1),  # Texto negro
            size_hint_y=None,
            height=dp(40),
            halign='center'
        )
        
        # Subtítulo
        subtitle = Label(
            text='[b]Intermediate projects[/b]',
            markup=True,
            font_size=dp(18),
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(30),
            halign='center'
        )
        
        # Contenido
        content = Label(
            text='''[b]- Intermediate project[/b]
A new application for advanced service work, and other types of services.

-------------------------

[b]Window API[/b]
For a particular option (up from the application to the first one) on the application as a function of service usage (as shown in Figure 1).

-------------------------

[b]Range priority[/b]
A new application has been installed on the program and the theme is available.

-------------------------

[b]Reactivity game[/b]
An interactive player can use the Reactivity Play game to create an interactive environment with specific features such as the user's name, the user's location, and the user's position.

-------------------------

[b]CLICKING OUTPUTS[/b]''',
            markup=True,
            font_size=dp(14),
            color=(0, 0, 0, 1),
            halign='left',
            valign='top',
            size_hint_y=None,
            text_size=(Window.width - dp(40), None)
        )
        content.bind(size=content.setter('text_size'))
        content.bind(width=lambda *x: content.setter('text_size')(content, (content.width, None)))
        
        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(content)

#Pantalla de usuario
class UsuarioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.saludo_label = Label(text="", font_size=24, markup=True, color=[0.2, 0.2, 0.2, 1])
        layout.add_widget(self.saludo_label)
        layout.add_widget(Label(text="Aquí verás tus datos personales", font_size=16, color=[0.2, 0.2, 0.2, 1]))
 
        cerrar_btn = Button(text="Cerrar sesión", size_hint_y=0.15, font_size=18, background_color=[0.6, 0.3, 0.8, 1], color=[1, 1, 1, 1])
        cerrar_btn.bind(on_press=self.cerrar_sesion)
        layout.add_widget(cerrar_btn)
        self.add_widget(layout)
 
    def cerrar_sesion(self, instance):
        self.manager.current = 'bienvenida'

#Intermediate
class Intermediate(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fondo de pantalla
        with self.canvas.before:
            Color(*backgroundColor)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.actualizar_rect, pos=self.actualizar_rect)

        # ScrollView principal
        scroll = ScrollView(size_hint=(1, 1))

        # Layout principal contenido en scroll
        layout = BoxLayout(orientation='vertical', padding=20, spacing=5, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))  # Clave para el scroll

        # Contenido fijo
        logo_image = Image(source='logo.png', size_hint=(0.7, None), height=150, allow_stretch=True, pos_hint={'center_x': .5})
        layout.add_widget(logo_image)

        layout.add_widget(Label(
            text='Intermediate projects',
            font_size=27,
            bold=True,
            color=(0, 0, 0, 0.7),
            size_hint_y=None,
            height=40
        ))

        # P1
        self.box = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint_y=None)
        aplicar_borde_redondeado(self.box)
        self.box.bind(minimum_height=self.box.setter('height'))

        self.box.add_widget(Image(source='library.png', size_hint=(1, None), height=200, allow_stretch=True))
        self.box.add_widget(Label(text='Library managenet', font_size=16, bold=True, color=textColorDark, size_hint_y=None, height=30))
        self.box.add_widget(Label(text='Managements system for a library\nthat allows users to search for,\nreserve, amd restun books, as well\nas enables administrators to\nmanage the book collection and\nuser registrstion\nPython', font_size=16, color=textColorDark, size_hint_y=None, height=80))
        
        self.btn1 = BoxLayout(orientation='horizontal', padding=0, spacing=10, size_hint_y=None)
        self.btn_more = BotonPersonalizado(text="More", size_hint=(0.2, None), height=40, pos_hint={'center_x': .5})
        self.btn_done = BotonPersonalizado(text="Done", size_hint=(0.2, None), height=40, pos_hint={'center_x': .5})
        self.btn_more.bind(on_press=self.redirigir_a_proyectos)
        self.btn_done.bind(on_press=self.redirigir_a_proyectos)
        self.btn1.add_widget(self.btn_more)
        self.btn1.add_widget(self.btn_done)
        self.box.add_widget(self.btn1)
        
        
        # P2
        self.inter = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint_y=None)
        aplicar_borde_redondeado(self.inter)

        self.inter.bind(minimum_height=self.inter.setter('height'))

        self.inter.add_widget(Image(source='p2.png', size_hint=(1, None), height=200, allow_stretch=True))
        self.inter.add_widget(Label(text='Online learning', font_size=16, bold=True, color=textColorDark, size_hint_y=None, height=30))
        self.inter.add_widget(Label(text='A web application that\nallows users to register, take\ncourses, and take tests to\nassess their knowledge\nJavaScript', font_size=17, color=textColorDark, size_hint_y=None, height=60))
        
        self.btns = BoxLayout(orientation='horizontal', padding=0, spacing=10, size_hint_y=None)
        self.btn_mor = BotonPersonalizado(text="More", size_hint=(0.2, None), height=40, pos_hint={'center_x': .5})
        self.btn_don = BotonPersonalizado(text="Done", size_hint=(0.2, None), height=40, pos_hint={'center_x': .5})
        self.btn_mor.bind(on_press=self.redirigir_a_proyectos)
        self.btn_don.bind(on_press=self.redirigir_a_proyectos)
        self.btns.add_widget(self.btn_mor)
        self.btns.add_widget(self.btn_don)
        self.inter.add_widget(self.btns)
        
        # p3
        self.adv = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint_y=None)
        aplicar_borde_redondeado(self.adv)

        self.adv.bind(minimum_height=self.adv.setter('height'))

        self.adv.add_widget(Image(source='p3.png', size_hint=(1, None), height=200, allow_stretch=True))
        self.adv.add_widget(Label(text='Minimalist social network', font_size=16, bold=True, color=textColorDark, size_hint_y=None, height=30))
        self.adv.add_widget(Label(text='A web application that\nallows users to create\nprofiles, post updates, and\nfollow other users\nJavaScript', font_size=17, color=textColorDark, size_hint_y=None, height=60))

        self.bt = BoxLayout(orientation='horizontal', padding=0, spacing=10, size_hint_y=None)
        self.btn_mo = BotonPersonalizado(text="More", size_hint=(0.2, None), height=40, pos_hint={'center_x': .5})
        self.btn_do = BotonPersonalizado(text="Done", size_hint=(0.2, None), height=40, pos_hint={'center_x': .5})
        self.btn_mo.bind(on_press=self.redirigir_a_proyectos)
        self.btn_do.bind(on_press=self.redirigir_a_proyectos)
        self.bt.add_widget(self.btn_mo)
        self.bt.add_widget(self.btn_do)
        self.adv.add_widget(self.bt)

        # p4
        self.p4 = BoxLayout(orientation='vertical', padding=20, spacing=20, size_hint_y=None)
        aplicar_borde_redondeado(self.p4)

        self.p4.bind(minimum_height=self.p4.setter('height'))

        self.p4.add_widget(Image(source='p4.png', size_hint=(1, None), height=200, allow_stretch=True))
        self.p4.add_widget(Label(text='Real-time chat', font_size=16, bold=True, color=textColorDark, size_hint_y=None, height=30))
        self.p4.add_widget(Label(text='A web application that\nallows users to chat in real-\ntime in different chat rooms\nJavaScript', font_size=17, color=textColorDark, size_hint_y=None, height=60))

        self.b = BoxLayout(orientation='horizontal', padding=0, spacing=10, size_hint_y=None)
        self.btn_m = BotonPersonalizado(text="More", size_hint=(0.2, None), height=40, pos_hint={'center_x': .5})
        self.btn_d = BotonPersonalizado(text="Done", size_hint=(0.2, None), height=40, pos_hint={'center_x': .5})
        self.btn_m.bind(on_press=self.redirigir_a_proyectos)
        self.btn_d.bind(on_press=self.redirigir_a_proyectos)
        self.b.add_widget(self.btn_m)
        self.b.add_widget(self.btn_d)
        self.p4.add_widget(self.b)

        layout.add_widget(self.box)
        layout.add_widget(Widget(size_hint_y=None, height=10))
        layout.add_widget(self.inter)
        layout.add_widget(Widget(size_hint_y=None, height=10))
        layout.add_widget(self.p4)

        # Agregar layout completo al scroll
        scroll.add_widget(layout)

        # Agregar el scrollview a la pantalla
        self.add_widget(scroll)

    def actualizar_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def redirigir_a_proyectos(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'home'
 
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(BienvenidaScreen(name='bienvenida'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(LevelScreen(name='level'))
        sm.add_widget(SeleccionScreen(name='seleccion'))
        sm.add_widget(Intermediate(name='intermediate'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(UsuarioScreen(name='usuario'))
        return sm
 
if __name__ == '__main__':
    MyApp().run()