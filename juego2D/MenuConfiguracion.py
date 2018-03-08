class PantallaConfiguracionGUI(PantallaGUI):
    def __init__(self,menu):
        PantallaGUI.__init__(self, menu, 'Menu/PantallaInicio.jpg')
        textoJugar = TextoJugar(self)
        self.elementosGUI.append(textoJugar)