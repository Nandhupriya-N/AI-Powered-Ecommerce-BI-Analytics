import chronos
print("Chronos version:", getattr(chronos, '__version__', 'unknown'))
print("Chronos exports:", [attr for attr in dir(chronos) if not attr.startswith('_')])
