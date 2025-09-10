import PySimpleGUI as sg

def configure_theme():
    giftlink_theme = {
        'BACKGROUND': '#2c3e50',
        'TEXT': '#ecf0f1',
        'INPUT': '#34495e',
        'TEXT_INPUT': '#ecf0f1',
        'SCROLL': '#34495e',
        'BUTTON': ('#ecf0f1', '#3498db'),
        'PROGRESS': ('#000000', '#000000'),
        'BORDER': 1,
        'SLIDER_DEPTH': 0,
        'PROGRESS_DEPTH': 0,
    }
    
    sg.theme_add_new('GiftLinkTheme', giftlink_theme)
    sg.theme('GiftLinkTheme')

    sg.set_options(
        font=('Helvetica', 12),
        button_element_size=(20, 2),
        element_padding=(10, 10),
        auto_size_buttons=False
    )