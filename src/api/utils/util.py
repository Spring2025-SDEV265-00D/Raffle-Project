from utils.app_error import PayloadError


class Util:

    @staticmethod
    def valid_nested_payload(
        payload: dict,  # json payload from front end

        # passing single header: "header" or ["header"] //Multiple: ["header1", "header2"]
        expected_headers: list[str] | str,

        # passing one or many keys for a single header: "key" or ["key"] or ["key1", "key2"]
        # passing keys for multiple headers:[ ["keys_for_header[0]", ["keys_for_header[1]" ]
        # Example:
        #       expected_headers = ['order', 'status']
        #       expected_nester = [['race_id', 'qtty'], ['code', 'message']]
        expected_nested: list[list[str]] | list[str] | str
    ) -> dict:

        # * normalize input in case 1 header with 1 key to validate (can be passed as strings for convenience)
        if isinstance(expected_headers, str):
            expected_headers = [expected_headers]
            # * same if only 1 key passed // skipped if 1 header and many keys
            if isinstance(expected_nested, str):
                expected_nested = [expected_nested]

        # *if a flat list is passed as expected_nested, theres only 1 header with nested data
        # *wrap it in a list so we can zip it properly
        if isinstance(expected_nested[0], str):
            expected_nested = [expected_nested]

        # check if headers are present in payload
        Util.valid_payload(payload, expected=expected_headers)

       # Util.p("unziped", expected_headers=expected_headers,
       #        expected_nested=expected_nested)

        # if so, loop over only the ones that actually have nested data
        headers_with_nested = list(zip(expected_headers, expected_nested))

        # Util.p("ziped", headers_with_nested=headers_with_nested)

        for header, nested in headers_with_nested:

            # Util.p("in loop", header=header, nested=nested)

            try:
                Util.valid_payload(payload=payload[header][0],
                                   expected=nested)

            except PayloadError as e:
                raise PayloadError(f"{e.message} Nested in header: {header}",
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
                f"Missing or mismatching keys. Missing: {missing or 'none'} | Unexpected: {unexpected or 'none'}",
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
