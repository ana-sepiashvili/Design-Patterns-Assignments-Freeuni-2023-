"""database constants"""
RECEIPT_TABLE_NAME = "Receipt"
RECEIPT_TABLE_COLUMNS = "Product TEXT, Unit INTEGER, Price DOUBLE, Total Double"

PRODUCTS_TABLE_NAME = "Products"
PRODUCTS_TABLE_COLUMNS = (
    "Product TEXT, Unit INTEGER, Price DOUBLE, "
    + "Discount INTEGER, PRIMARY KEY (Product, Unit)"
)
PRODUCTS_DEFAULT_VALUES = (
    ("Bread", 1, 2.0, 0),
    ("Milk", 1, 3.5, 10),
    ("Water", 1, 1.0, 0),
    ("Water", 6, 6.0, 0),
    ("Diapers", 1, 4.5, 0),
)

X_SALES_REPORT_TABLE_NAME = "X_Sales_Report"
SALES_REPORT_TABLE_COLUMNS = "Product TEXT, Sales INTEGER"

X_REVENUE_REPORT_TABLE_NAME = "X_Revenue_Report"
REVENUE_REPORT_TABLE_COLUMNS = "Payment TEXT, Revenue DOUBLE"
REVENUE_REPORT_DEFAULT_VALUES = (("Cash", 0.0), ("Card", 0.0))

Z_SALES_REPORT_TABLE_NAME = "Z_Sales_Report"
Z_REVENUE_REPORT_TABLE_NAME = "Z_Revenue_Report"

MIN_ITEMS_AMOUNT = 1
MAX_ITEMS_AMOUNT = 4

DISCOUNT_ON_PRIME_CUSTOMER = 17
DISCOUNT_ON_PACKS = 10

NUMBER_OF_SHIFTS = 3
RANGE_FOR_X_REPORT = 20
RANGE_FOR_Z_REPORT = 200

DATABASE_NAME = "store.db"
