import webbrowser
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

# बैकग्राउंड थीम
Window.clearcolor = (0.05, 0.08, 0.15, 1)

# यहाँ अपना असली मोबाइल नंबर डालें
PHONE_NUMBER = "+91 99703 77795"


class RSSecuritiesApp(App):

    def build(self):
        main_layout = BoxLayout(
            orientation="vertical", padding=15, spacing=10
        )

        # 1. हेडर सेक्शन
        header = Label(
            text="R S SECURITIES",
            font_size="26sp",
            bold=True,
            color=(1, 0.8, 0, 1),
            size_hint=(1, 0.08),
        )

        sub_header = Label(
            text="Rajesh Meghji Maru | Market Expert",
            font_size="16sp",
            color=(0.8, 0.8, 0.8, 1),
            size_hint=(1, 0.05),
        )

        # 2. चार्ट विजेट (विजुअल डायग्राम)
        chart_box = BoxLayout(
            orientation="vertical", size_hint=(1, 0.35), padding=10
        )

        with chart_box.canvas.before:
            Color(0.1, 0.15, 0.25, 1)
            self.rect = Rectangle(size=(320, 180), pos=(40, 360))

        chart_label = Label(
            text="[color=00ff00]▲ NIFTY 50 : LIVE ANALYSIS[/color]\n\n"
            "🟢 Bullish Trend Detected\n"
            "📊 Support: 22,000 | Resistance: 22,500\n\n"
            "[color=ffff00]★ Join Advisory For Daily Live Calls[/color]",
            markup=True,
            font_size="15sp",
            halign="center",
        )
        chart_box.add_widget(chart_label)

        # 3. सर्विसेज लिस्ट
        services_text = (
            "[b][color=00ffff]Our Services:[/color][/b]\n"
            "• Equity & F&O Strategies\n"
            "• Portfolio Management\n"
            "• Risk Advisory"
        )
        info_label = Label(
            text=services_text,
            markup=True,
            font_size="15sp",
            halign="center",
            size_hint=(1, 0.2),
        )

        # 4. एक्शन बटन (कॉल एवं व्हाट्सएप)
        call_btn = Button(
            text="Call Rajesh Ji Now",
            font_size="18sp",
            bold=True,
            background_color=(0, 0.6, 1, 1),
            size_hint=(1, 0.1),
        )
        call_btn.bind(on_press=self.make_call)

        wa_btn = Button(
            text="Chat on WhatsApp",
            font_size="18sp",
            bold=True,
            background_color=(0.1, 0.8, 0.3, 1),
            size_hint=(1, 0.1),
        )
        wa_btn.bind(on_press=self.open_whatsapp)

        # स्क्रीन में जोड़ें
        main_layout.add_widget(header)
        main_layout.add_widget(sub_header)
        main_layout.add_widget(chart_box)
        main_layout.add_widget(info_label)
        main_layout.add_widget(call_btn)
        main_layout.add_widget(wa_btn)

        return main_layout

    def make_call(self, instance):
        webbrowser.open(f"tel:{PHONE_NUMBER}")

    def open_whatsapp(self, instance):
        webbrowser.open(
            f"https://wa.me/{PHONE_NUMBER}?text=Hello%20Rajesh%20Ji,%20I%20want%20stock%20market%20guidance"
        )


if __name__ == "__main__":
    RSSecuritiesApp().run()
