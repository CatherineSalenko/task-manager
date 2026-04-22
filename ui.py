import flet as ft

from database import Task, TaskDatabase


class TaskManagerUI:
    """Базовый интерфейс списка задач на Flet."""

    def __init__(self, page: ft.Page) -> None:
        # Сохраняем ссылку на окно (страницу) Flet.
        self.page = page
        # Создаем объект для работы с SQLite.
        self.database = TaskDatabase()
        # Собираем данные и строим интерфейс.
        self._configure_page()
        self._build_layout()

    def _configure_page(self) -> None:
        # Базовые настройки окна приложения.
        self.page.title = "Task Manager"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 980
        self.page.window_height = 620
        self.page.window_min_width = 760
        self.page.window_min_height = 480
        self.page.bgcolor = "#f7f7f5"
        self.page.padding = 24

    def _load_tasks(self) -> list[Task]:
        # Получаем задачи из базы.
        tasks = self.database.get_all_tasks()
        # Если база пустая, показываем 2 примера для макета.
        if not tasks:
            return [
                Task(name="Пример задачи 1", important=False, immediately=False),
                Task(name="Пример задачи 2", important=True, immediately=False),
            ]
        return tasks

    def _build_header(self) -> ft.Row:
        # Заголовок "таблицы" (визуально).
        return ft.Row(
            controls=[
                ft.Container(width=40, content=ft.Text("")),
                ft.Container(expand=3, content=ft.Text("Название", weight=ft.FontWeight.BOLD)),
                ft.Container(expand=1, content=ft.Text("Срочность", weight=ft.FontWeight.BOLD)),
                ft.Container(expand=1, content=ft.Text("Важность", weight=ft.FontWeight.BOLD)),
                ft.Container(expand=1, content=ft.Text("Статус", weight=ft.FontWeight.BOLD)),
            ]
        )

    def _build_task_row(self, task: Task) -> ft.Row:
        # Одна строка в списке задач.
        return ft.Row(
            controls=[
                ft.Container(width=40, content=ft.Checkbox(value=task.done)),
                ft.Container(expand=3, content=ft.Text(task.name)),
                ft.Container(
                    expand=1,
                    content=ft.Text("Срочно" if task.immediately else "Не срочно"),
                ),
                ft.Container(
                    expand=1,
                    content=ft.Text("Важно" if task.important else "Не важно"),
                ),
                ft.Container(
                    expand=1,
                    content=ft.Text("Выполнено" if task.done else "В работе"),
                ),
            ]
        )

    def _build_layout(self) -> None:
        # Полностью формируем экран.
        tasks = self._load_tasks()
        task_rows = [self._build_task_row(task) for task in tasks]

        # Это заготовка для будущего добавления новой задачи.
        add_task_placeholder = ft.TextButton(
            "+ New page",
            disabled=True,
        )

        content = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=16,
            content=ft.Column(
                controls=[
                    self._build_header(),
                    ft.Divider(height=16),
                    *task_rows,
                    ft.Divider(height=16),
                    add_task_placeholder,
                ],
                spacing=8,
                tight=True,
            ),
        )

        self.page.add(
            ft.Text("Work task", size=30, weight=ft.FontWeight.BOLD),
            content,
        )


def _main(page: ft.Page) -> None:
    """Внутренняя функция запуска интерфейса Flet."""
    TaskManagerUI(page)


def run_app() -> None:
    """Публичная функция запуска приложения."""
    ft.app(target=_main)
