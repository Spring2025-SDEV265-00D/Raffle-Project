from utils.app_error import PayloadError


class Util:

    @staticmethod
    def valid_nested_payload(
        payload: dict,
        expected_headers: list[str] | str,
        expected_nested: list[list[str]] | list[str] | str
    ) -> dict:

        if isinstance(expected_headers, str):
            expected_headers = [expected_headers]

        if isinstance(expected_nested, str):
            expected_nested = [expected_nested]

        if isinstance(expected_nested[0], str):
            expected_nested = [expected_nested] * len(expected_headers)

        # check headers
        Util.valid_payload(payload, expected=expected_headers)

        for header_index, header in enumerate(expected_headers):
            nested_payload = payload[header]

           # for index, key in enumerate(nested_payload):
            for index, item in enumerate(nested_payload):

                try:
                    Util.valid_payload(
                        item, expected=expected_nested[header_index])

                except PayloadError as e:
                    raise PayloadError(f"{e.message} Nested in {header}[{index}]",
                                       context=PayloadError.get_error_context(payload=payload,
                                                                              expected_headers=expected_headers,
                                                                              expect_nested=expected_nested,
                                                                              original_context=e.context))

        return payload

    @staticmethod
    def valid_payload(payload: dict, expected: list[str] | str) -> dict:
        """Validates that all expected keys are present in the given payload.

        Args:
            payload (dict): The incoming data to validate.
            expected (list[str] | str): Keys that must be present in the payload.

        Raises:
            PayloadError: If any expected keys are missing. The error includes a message and a context dictionary with:
                - missing: list of missing keys
                - expected: list of all required keys
                - payload: the received payload

        Example:
            {
                "error": "Payload Error: Missing or mismatching keys.",
                "context": {
                    "missing": ["end_date"],
                    "expected": ["event_name", "location", "start_date", "end_date"],
                    "payload": {...}
                }
            }

        Returns:
            dict: The validated payload.
        """

        if isinstance(expected, str):
            expected = [expected]

        missing = [key for key in expected if key not in payload]
        unexpected = [key for key in payload if key not in expected]

        if missing or unexpected:
            raise PayloadError(
                f"Missing or mismatching keys: {missing or 'none'}. Unexpected: {unexpected or 'none'}",
                context=PayloadError.get_error_context(payload=payload,
                                                       missing=missing,
                                                       unexpected=unexpected,
                                                       expected=expected))
        return payload

 #       if not all(key in payload for key in expected):
  #          raise PayloadError(f"Mismatch. Expected: {expected}")
   #     return payload

        # ---------------------------------------------------------------------------------

    @staticmethod
    def pretty_print(data):
        import json

        print("\n\n")
        print(f"************************************************")
        print(json.dumps(data, indent=4))

        print(f"************************************************")
        print("\n\n")
# ---------------------------------------------------------------------------------

    @staticmethod
    def f(userMsg="no msg for you"):
        print("\n\n")
        print(f"************************{userMsg}************************\n")
        print("\n\n")
# ---------------------------------------------------------------------------------

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
# ---------------------------------------------------------------------------------

    @staticmethod
    def split_dict(data: dict) -> tuple[dict, dict]:
        id_data = {}
        qtty_data = {}

        for key, value in data.items():
            if key.endswith("_id"):
                id_data = {key: value}
            else:
                qtty_data = {key: value}

        return id_data, qtty_data

        # dict1, dict2 = [{key:value} for key, value in data.items()]

        # ---------------------------------------------------------------------------------

    @staticmethod
    def id_int_to_dict(id_value: int | str, cls=None) -> dict:
        return {'id': id_value} if not cls else {f"{cls.__name__.lower()}_id": id_value}
# ---------------------------------------------------------------------------------

    @staticmethod
    def round_robin_pick(
        horses: list,
        tickets_sold: int,
        new_tickets: int
    ) -> list[dict]:

        next_horses = []
        roster_size = len(horses)

        for unit in range(new_tickets):
            index = (tickets_sold + unit) % roster_size
            next_horses.append({"horse_id": horses[index]})

        return next_horses
# ---------------------------------------------------------------------------------

    @staticmethod
    def handle_row_data(data: list[dict] | dict, fields=None):

        if isinstance(data, list):
            return Util._handle_many(data, fields)

        return Util._handle_single(data, fields)
# ---------------------------------------------------------------------------------

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
# ---------------------------------------------------------------------------------

    @staticmethod
    def _handle_single(row_data, fields=None):
        row_data = dict(row_data)
        row_data = Util._filter_by_field(row_data, fields)

        return row_data
# ---------------------------------------------------------------------------------

    @staticmethod
    def _handle_many(rows_data, fields=None):

        rows_data = [Util._handle_single(row, fields) for row in rows_data]
        return rows_data
# ---------------------------------------------------------------------------------

    # strips id prefix of list coming from front end
    # {'race_id': 1, 'qtty': 3} -> {'id': 1, 'qtty': 3},
    @staticmethod
    def strip_id_prefix(data: list[dict] | dict):
        only_one = False

        if isinstance(data, dict):
            only_one = True
            data = [data]

        formatted = []

        for item in data:
            formatted_item = {}
            for key, value in item.items():
                if key.endswith("_id"):
                    formatted_item["id"] = value
                else:
                    formatted_item[key] = value

            formatted.append(formatted_item)

        if only_one:
            formatted = formatted[0]

        return formatted
# ---------------------------------------------------------------------------------

    @staticmethod  # debugging
    def s():
        import inspect
        return inspect.currentframe().f_back.f_code.co_name
