from kivy.clock import Clock

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
        background_color=(1, 1, 1, 1),  # ← esto es lo que cambiamos
        foreground_color=(0.2, 0.2, 0.2, 1),
        hint_text_color=(0.5, 0.5, 0.6, 1),
        padding=[10, 10]
    )

    def agregar_fondo(*args):
        with input_field.canvas.before:
            Color(0.85, 0.75, 0.95, 1)
            input_field.rect = RoundedRectangle(size=input_field.size, pos=input_field.pos, radius=[10])
        input_field.bind(pos=self.actualizar_rect_input, size=self.actualizar_rect_input)

    Clock.schedule_once(agregar_fondo, 0)  # ← lo aplicamos con delay para que funcione bien

    return input_field
