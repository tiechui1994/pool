from utils.GetConfig import GetConfig


def test_get_config():
    """
    test class GetConfig in utils/GetConfig
    """
    gg = GetConfig()
    print(gg.db_type)
    print(gg.db_name)
    print(gg.db_host)
    print(gg.db_port)
    assert isinstance(gg.proxy_getter_functions, list)
    print(gg.proxy_getter_functions)


if __name__ == '__main__':
    test_get_config()
