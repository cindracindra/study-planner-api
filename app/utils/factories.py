def set_factories_session(factories: list, session) -> None:
    for factory in factories:
        factory._meta.sqlalchemy_session = session
