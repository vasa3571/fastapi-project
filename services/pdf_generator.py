import os

from fpdf import FPDF

from models.product import Product


def generate_products_report(filename: str, products: list[Product]) -> str:
    pdf = FPDF()
    pdf.add_page()

    # Заголовок
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Products Catalog Report", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)

    # Шапка таблиці
    pdf.set_font("Arial", "B", 12)
    pdf.cell(40, 10, "Product ID", border=1)
    pdf.cell(100, 10, "Product Name", border=1)
    pdf.cell(50, 10, "Price ($)", border=1, new_x="LMARGIN", new_y="NEXT")

    # Вміст таблиці (дані з БД)
    pdf.set_font("Arial", "", 12)
    for product in products:
        safe_name = (
            product.name.encode("ascii", "ignore").decode("ascii")
            or f"Product #{product.id}"
        )

        pdf.cell(40, 10, str(product.id), border=1)
        pdf.cell(100, 10, safe_name, border=1)
        pdf.cell(
            50, 10, f"{product.price:.2f}", border=1, new_x="LMARGIN", new_y="NEXT"
        )

    # Створюємо папку для звітів, якщо її немає
    os.makedirs("reports", exist_ok=True)
    filepath = f"reports/{filename}"
    pdf.output(filepath)

    return filepath
