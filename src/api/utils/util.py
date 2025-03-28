class Util:

    @staticmethod
    def f(userMsg="no msg for you"):
        print("\n\n")
        print(f"************************{userMsg}************************\n")
        print("\n\n")

    @staticmethod
    def p(userMsg="no msg for you", **kwargs):
        print("\n\n")

        print(f"************************{userMsg}************************\n")
        for var_name, var_value in kwargs.items():
            print(f"{var_name} = {var_value}")
            print("\n")

        # print(message)
        print(f"***********END OF--->***{userMsg}************************\n")
        print("\n\n")

    @staticmethod
    def round_robin_pick(horses: list, tickets_sold: int, new_tickets: int) -> list[dict]:
        next_horses = []
        roster_size = len(horses)

        for unit in range(new_tickets):
            index = (tickets_sold + unit) % roster_size
            next_horses.append({"horse_id": horses[index]})

        return next_horses

    @staticmethod
    def handle_data(data, fields=None):

        if isinstance(data, list):
            return Util._handle_multiple_rows_data(data, fields)

        return Util._handle_row_data(data, fields)

    @staticmethod
    def _filter_by_field(dictionary, fields=None):

        if not fields:
            return dictionary

        # safety check in case fields is a str and not a list of str
        if isinstance(fields, str):
            fields = [fields]

        filtered_data = {}
        for colName in fields:
            if colName in dictionary:
                filtered_data[colName] = dictionary[colName]

        return filtered_data

    @staticmethod
    def _handle_row_data(row_data, fields=None):
        row_data = dict(row_data)
        row_data = Util._filter_by_field(row_data, fields)

        return row_data

    @staticmethod
    def _handle_multiple_rows_data(rows_data, fields=None):

        rows_data = [Util._handle_row_data(row, fields) for row in rows_data]
        return rows_data

    # strips id prefix of list coming from front end
    # {'race_id': 1, 'qtty': 3} -> {'id': 1, 'qtty': 3},
    @staticmethod
    def format_batch_data(data: list):

        formatted = []

        for item in data:
            formatted_item = {}
            for key, value in item.items():
                if key.endswith("_id"):
                    formatted_item["id"] = value
                else:
                    formatted_item[key] = value

            formatted.append(formatted_item)

        # Util.p("inner loop", key=formatted)
        return formatted
