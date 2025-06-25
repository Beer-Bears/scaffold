from neomodel import db

from src.database.connection import init_neo4j
from src.database.models.nodes import ClassNode, FileNode, MethodNode



def check_neo4j():
    try:
        results, _ = db.cypher_query("RETURN 1")
        print(f"Neo4j: {results[0][0] == 1}")
    except Exception as e:
        print(f"Neo4j healthcheck failed: {e}")
        return False


async def check():
    init_neo4j()
    check_neo4j()

    # Файл
    file = FileNode(
        name="service_file",
        path="services/payment_service.py",
        start_line=1,
        end_line=120,
        docstring="Файл с сервисами для обработки платежей",
    ).save()

    # Классы
    payment_service = ClassNode(
        name="PaymentService",
        path="services/payment_service.py",
        start_line=5,
        end_line=90,
        docstring="Сервис, обрабатывающий платёжные транзакции",
    ).save()

    invoice_generator = ClassNode(
        name="InvoiceGenerator",
        path="services/payment_service.py",
        start_line=92,
        end_line=119,
        docstring="Генерирует инвойсы после оплаты",
    ).save()

    # Методы
    process_payment = MethodNode(
        name="process_payment",
        path="services/payment_service.py",
        start_line=10,
        end_line=30,
        docstring="Обрабатывает платёж клиента",
    ).save()

    validate_card = MethodNode(
        name="validate_card",
        path="services/payment_service.py",
        start_line=32,
        end_line=50,
        docstring="Проверяет валидность карты",
    ).save()

    generate_invoice = MethodNode(
        name="generate_invoice",
        path="services/payment_service.py",
        start_line=93,
        end_line=110,
        docstring="Создаёт PDF-инвойс",
    ).save()

    # Создание связей
    file.defines_classes.connect(payment_service)
    file.defines_classes.connect(invoice_generator)
    file.defines_methods.connect(process_payment)
    file.defines_methods.connect(validate_card)
    file.defines_methods.connect(generate_invoice)

    payment_service.defines_methods.connect(process_payment)
    payment_service.defines_methods.connect(validate_card)
    invoice_generator.defines_methods.connect(generate_invoice)

    process_payment.uses_methods.connect(validate_card)
    process_payment.uses_classes.connect(invoice_generator)
    generate_invoice.uses_classes.connect(payment_service)
