import sqlite3
from dataclasses import dataclass
from typing import Protocol, Sequence


class SQLite(Protocol):
    def create_table(self, table_name: str, columns: str) -> None:
        pass

    def insert_data(self, table_name: str, values: str) -> None:
        pass

    def query_data(self, table_name: str) -> list[tuple]:
        pass

    def close(self) -> None:
        pass

    def contains(self, param: str) -> bool:
        pass


class SQLiteHandler:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name: str, columns: str) -> None:
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        self.connection.commit()

    def insert_data(self, table_name: str, values: tuple) -> None:
        self.cursor.execute(f"INSERT INTO {table_name} VALUES {values}")
        self.connection.commit()

    def query_data(self, table_name: str) -> list[tuple]:
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()

    def close(self) -> None:
        self.connection.close()

    def contains(self, table_name: str, param: str, column_name: str) -> bool:
        self.cursor.execute(
            f"SELECT * FROM {table_name} WHERE {column_name} = '{param}'"
        )
        return len(self.cursor.fetchall()) >= 1

    def increment_amount(
        self,
        table_name: str,
        param: str,
        column: str,
        amount: float,
        to_increment: str,
    ) -> None:
        query = f"SELECT {to_increment} FROM {table_name} WHERE {column} = '{param}'"
        self.cursor.execute(query)
        number = self.cursor.fetchone()[0]
        update = (
            f"UPDATE {table_name} SET {to_increment} = "
            + f"{number + amount} WHERE {column} = '{param}'"
        )
        self.cursor.execute(update)
        self.connection.commit()


class Repository(Protocol):
    def create(self) -> None:
        pass

    def update(self, value: tuple) -> None:
        pass

    def read(self) -> list[tuple]:
        pass

    def __str__(self) -> str:
        pass


@dataclass
class ItemRepository:
    db_handler: SQLiteHandler
    table_name: str
    columns: str
    default_values: Sequence[tuple]

    def create(self) -> None:
        self.db_handler.create_table(self.table_name, self.columns)
        for value in self.default_values:
            self.db_handler.insert_data(self.table_name, value)

    def update(self, value: tuple) -> None:
        # value = (
        #     item.get_name(),
        #     item.get_amount(),
        #     item.get_price(),
        #     item.get_discount(),
        # )
        self.db_handler.insert_data(self.table_name, value)

    def read(self) -> list[tuple]:
        return self.db_handler.query_data(self.table_name)

    def __str__(self) -> str:
        result = (
            "\nProduct        | Units | Price | Total   | Discount |\n"
            + "---------------|-------|-------|---------|----------|\n"
        )
        for item in self.read():
            result += (
                f"{item[0]}{' ' * (15 - len(str(item[0])))}|"
                + f"  {item[1]}{' ' * (5 - len(str(item[1])))}|"
                + f"  {item[2]}{' ' * (5 - len(str(item[2])))}|"
                + f"  {item[2] * item[1]}"
                + f"{' ' * (7 - len(str(item[2] * item[1])))}|"
                + f"  {item[3]}%{' '*(7 - len(str(item[3])))}|\n"
            )

        return result


@dataclass
class SalesReportRepository:
    db_handler: SQLiteHandler
    table_name: str
    columns: str

    def create(self) -> None:
        self.db_handler.create_table(self.table_name, self.columns)

    def update(self, value: tuple) -> None:
        # value = (item.get_name(), item.get_amount())
        if self.db_handler.contains(self.table_name, value[0], "Product"):
            self.db_handler.increment_amount(
                self.table_name, value[0], "Product", value[1], "Sales"
            )
        else:
            self.db_handler.insert_data(self.table_name, value)

    def read(self) -> list[tuple]:
        return self.db_handler.query_data(self.table_name)

    def __str__(self) -> str:
        sales = " Product | Sales |\n" + "---------|-------|\n"
        for sale in self.read():
            sales += (
                f" {sale[0]}{' '*(8 - len(sale[0]))}|"
                + f" {sale[1]}{' '*(6 - len(str(sale[1])))}|\n"
            )

        return sales


@dataclass
class RevenueReportRepository:
    db_handler: SQLiteHandler
    table_name: str
    columns: str
    default_values: Sequence[tuple]

    def create(self) -> None:
        self.db_handler.create_table(self.table_name, self.columns)
        for value in self.default_values:
            self.db_handler.insert_data(self.table_name, value)

    def update(self, value: tuple) -> None:
        # value = (payment, price)
        self.db_handler.increment_amount(
            self.table_name, value[0], "Payment", value[1], "Revenue"
        )

    def read(self) -> list[tuple]:
        return self.db_handler.query_data(self.table_name)

    def __str__(self) -> str:
        revenues = (
            " Payment | Revenue           |\n" + "---------|-------------------|\n"
        )
        for revenue in self.read():
            revenues += (
                f" {revenue[0]}{' '*(8 - len(revenue[0]))}|"
                + f" {revenue[1]}{' '*(18 - len(str(revenue[1])))}|\n"
            )

        return revenues
