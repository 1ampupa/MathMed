import flet

from module.core.state import StateManager
from module.core.user import User

def TEST_play():
        from module.core.session import Session, Operators
        session = Session(Operators.ADDITION)
        user = User.create()
        session.connect_user(user)
        session.start()

def main_menu(page: flet.Page) -> None:
    # Window Settings
    if StateManager.debug_mode:
        page.title = f"MathMed Dev Build ({StateManager.program_version})"
    else:
        page.title = f"MathMed {StateManager.program_version}"

    page.window.width = 800
    page.window.height = 600
    page.window.resizable = False
    page.window.maximizable = False 
    page.window.alignment = flet.Alignment.CENTER

    # Page Settings
    page.vertical_alignment = flet.MainAxisAlignment.SPACE_BETWEEN
    page.padding = 20

    # Page Elements
    game_title_text = flet.Text("MathMed",size=50, weight=flet.FontWeight.BOLD)
    game_description_text = flet.Text("A math exercise game",size=30)

    instruction_text = flet.Text("Welcome, let's get started!",size=20)
    user_name_text_field = flet.TextField(label="User name",hint_text="User",text_align=flet.TextAlign.LEFT)
    continue_button = flet.Button(content="Let's go!",disabled=True)

    continue_as_tester_button = flet.Button(content="Continue as a tester",on_click=TEST_play)
    version_text = flet.Text(f"MathMed {StateManager.program_version}",size=12,color=flet.Colors.GREY_500)
    credit_text = flet.Text("Made by 1ampupa.",size=12,color=flet.Colors.GREY_500)

    # Page Layout
    layout_header = flet.Row(
        controls=[
            game_title_text,
            game_description_text
        ],
        align=flet.Alignment.CENTER
    )

    layout_body = flet.Container(
        content=flet.Column(
            controls=[
                instruction_text,
                user_name_text_field,
                continue_button
            ],
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=flet.Alignment.CENTER
    )

    layout_footer = flet.Column(
        controls=[
            flet.Row(
                [
                    version_text,
                    credit_text
                ],
                alignment=flet.MainAxisAlignment.SPACE_BETWEEN
            )
        ],
        horizontal_alignment=flet.CrossAxisAlignment.CENTER
    )

    # Renderer
    page.add(
        layout_header,
        layout_body,
        layout_footer
    )
    if StateManager.debug_mode:
        page.add(
            flet.Column(
                controls=[continue_as_tester_button],
                align=flet.Alignment.BOTTOM_RIGHT
            )
        )
